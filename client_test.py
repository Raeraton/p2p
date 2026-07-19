import socket
import json
import time
import random

IP, PORT = "127.0.0.1", 1235

def do_test():
    time.sleep(random.randrange(1, 1001) / 1000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    sock.send(b"connect")
    other_peer = json.loads( sock.recv(256) )

    print(f"other peer is {other_peer["ip"]}:{other_peer["port"]}")

while 1:
    do_test()