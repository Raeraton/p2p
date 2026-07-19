import socket
import json
import time
import random
import p2p



# get peer ip and port
IP, PORT = input("enter ip: "), 1235

time.sleep(random.randrange(1, 1001) / 1000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))

my_ip, my_port = sock.getsockname()
print(f"running on {my_ip}:{my_port}")

sock.send(b"0")
other_peer = json.loads( sock.recv(256) )

peer_ip, peer_port = other_peer["ip"], other_peer["port"]
print(f"other peer is {peer_ip}:{peer_port}")

sock.close()



# make p2p stuff
p2pConn = p2p.P2PConnection(my_port, peer_ip, peer_port)

to_send = 1
last_recvd = 0
error_count = 0
while 1:
    p2pConn.send(f'{to_send}'.encode())
    recvd = int( p2pConn.recv().decode() )
    if recvd != last_recvd + 1: error_count += 1
    last_recvd = recvd
    print(f"sent: {to_send}    recvd: {recvd}    errors: {error_count}")
    to_send += 1