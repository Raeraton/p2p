import socket
import json
import time
import p2p


MY_ADDR = ("0.0.0.0", 0)
SERVER_ADDR = ("127.0.0.1", 1234)

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

while 1:
    connection.send(f"{time.time()}".encode())
    data = connection.recv()
    print(f"diff {time.time() - float(data.decode())}")