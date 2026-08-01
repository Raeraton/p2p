import socket


SERVER_ADDR = ("127.0.0.1", 50020)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 0))

while 1:
    msg = input("enter message: ").encode("utf-8")
    sock.sendto(msg, SERVER_ADDR)
    data, addr = sock.recvfrom(1200)
    print(f"recved: {data}")