import socket
import json
import time
import p2p
import random


MY_ADDR = ("0.0.0.0", 0)
SERVER_ADDR = ("127.0.0.1", 50020)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(MY_ADDR)

target_addr: tuple = None
while True:
    time.sleep(1)
    try:

        sock.sendto(b'\x00', SERVER_ADDR)
        data, addr = sock.recvfrom(1200)

        if data == b'OK':
            continue

        data = json.loads(data)
        target_addr = ( data["ip"], data["port"] )
        break

    except Exception as e:
        print(f"[ERROR] {e}")


print(f"other peer is: {target_addr[0]}:{target_addr[1]}")

connection = p2p.P2PConnection(sock, target_addr[0], target_addr[1])

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


    except Exception as e:
        print(f"[ERROR] {e}")