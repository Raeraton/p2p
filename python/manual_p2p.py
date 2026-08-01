import socket
import struct
import p2p
import os
import random
import time
import json

STUN_SERVER = ("stun.l.google.com", 19302)
MAGIC_COOKIE = 0x2112A442


def build_binding_request():
    # STUN Binding Request
    msg_type = 0x0001
    msg_length = 0
    transaction_id = os.urandom(12)

    packet = struct.pack(
        "!HHI12s",
        msg_type,
        msg_length,
        MAGIC_COOKIE,
        transaction_id,
    )

    return packet, transaction_id


def parse_response(data, expected_transaction_id):
    if len(data) < 20:
        raise ValueError("Response too short")

    msg_type, msg_length, magic_cookie = struct.unpack("!HHI", data[:8])
    transaction_id = data[8:20]

    if msg_type != 0x0101:
        raise ValueError(f"Unexpected message type: {hex(msg_type)}")

    if magic_cookie != MAGIC_COOKIE:
        raise ValueError("Invalid magic cookie")

    if transaction_id != expected_transaction_id:
        raise ValueError("Transaction ID mismatch")

    offset = 20

    while offset + 4 <= len(data):
        attr_type, attr_length = struct.unpack(
            "!HH", data[offset:offset + 4]
        )

        value = data[offset + 4:offset + 4 + attr_length]

        if attr_type == 0x0020:  # XOR-MAPPED-ADDRESS

            if value[1] == 1:  # IPv4

                xor_port = struct.unpack("!H", value[2:4])[0]
                port = xor_port ^ (MAGIC_COOKIE >> 16)

                xor_ip = struct.unpack("!I", value[4:8])[0]
                ip = xor_ip ^ MAGIC_COOKIE

                ip = socket.inet_ntoa(struct.pack("!I", ip))

                return ip, port

            elif value[1] == 2:  # IPv6
                raise NotImplementedError("IPv6 not implemented")

        # Attributes are padded to a multiple of 4 bytes
        offset += 4 + ((attr_length + 3) & ~3)

    raise ValueError("No XOR-MAPPED-ADDRESS attribute found")




if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 0))
    sock.settimeout(5)
    
    request, transaction_id = build_binding_request()
    
    sock.sendto(request, STUN_SERVER)
    
    response, addr = sock.recvfrom(2048)
    
    print("Received response from", addr)
    
    ip, port = parse_response(response, transaction_id)

    print( f"listening on {ip}:{port}" )
    target = input( "enter target (x.x.x.x:port) -& " ).split(':')

    connection = p2p.P2PConnection( sock, target[0], int(target[1]) )

    connection.punch_hole()


    nums = {}
    send_back = []
    while 1:
        try:
            num = random.randrange(1, 100000)
            nums[num] = time.time()
            
            data = json.dumps({
                "echo": send_back,
                "send": num
            }).encode("utf-8")
            
            connection.send(data)
            data = connection.recv()
            
            data = json.loads(data)
            send_back = []
            send_back.append(data["send"])
            
            for echoed_num in data["echo"]:
                print( f"{round((time.time() - nums[echoed_num])*1000, 3)} ms -------> {echoed_num}" )
                del nums[echoed_num]

        except socket.timeout:
            connection.punch_hole()
    
    sock.close()
    