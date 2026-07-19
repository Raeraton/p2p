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
bytes_sent = 0
up_speed = 0
bytes_recved = 0
down_speed = 0
timepoint = time.time()
while 1:
    bytes_to_send = f'{to_send}'.encode()
    bytes_sent += len(bytes_to_send)
    p2pConn.send(bytes_to_send)

    bytes_recv = p2pConn.recv()
    bytes_recved = len(bytes_recv)

    recvd = int( bytes_recv.decode() )
    if recvd != last_recvd + 1: error_count += 1
    last_recvd = recvd

    tn = time.time()
    if tn - timepoint >= 1:
        down_speed = bytes_recved
        up_speed = bytes_sent
        bytes_recved = 0
        bytes_sent = 0

    print(f"sent: {to_send}    recvd: {recvd}    errors: {error_count}   upspeed: {up_speed*8} b/s  downspeed: {down_speed*8} b/s")
    to_send += 1