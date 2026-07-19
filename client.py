import socket
import json
import p2p
import random

my_port = random.randrange(17000, 60000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 1237))

sock.send(f"{my_port}".encode("utf-8"))
other_peer = json.loads( sock.recv(256) )

print(f"other peer is {other_peer["ip"]}:{other_peer["port"]}")

friend = p2p.P2PConnection(my_port, other_peer["ip"], other_peer["port"])

while 1:
    friend.send(b"hello")
    print(friend.recv())  