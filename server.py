import socket
import time
import json

TIMEOUT_TIME = 10 # sec
SERVER_ADDR = ('0.0.0.0', 1234)

class Peer:
    def __init__(self, ip:str, port:int):
        self.ip = ip
        self.port = port
        self.last_updated = time.time()

    def __init__(self, addr: tuple[str, int]):
        self.ip = addr[0]
        self.port = addr[1]
        self.last_updated = time.time()

    def is_out_dated(self):
        return time.time() - self.last_updated > TIMEOUT_TIME

    def update(self):
        self.last_updated = time.time()

    def addr(self):
        return (self.ip, self.port)

    def __eq__(self, value):
        if value == None: return False
        return self.ip==value.ip and self.port==value.port

    def __hash__(self):
        return hash(self.ip) + hash(self.port)

    def __str__(self):
        return f"{self.ip}:{self.port}"


# socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(SERVER_ADDR)


# main loop
other_peer: Peer = None

while True:
    print( "---\t", end="" )
    try:

        data, addr = sock.recvfrom(1200)

        # update
        if other_peer != None:
                if other_peer.is_out_dated():
                    print(f"peer timeout {other_peer}")
                    other_peer = None

        current_peer = Peer(addr)

        if other_peer == None:
            print(f"new peer online: {current_peer}")
            other_peer = current_peer
        elif other_peer == current_peer:
            print(f"peer updated {other_peer}")
            other_peer.update()
        else:
            print(f"peers cuppled {current_peer} <---> {other_peer}")
            sock.sendto(json.dumps({
                "ip": other_peer.ip,
                "port": other_peer.port
            }).encode("utf-8"), current_peer.addr())
            sock.sendto(json.dumps({
                "ip": current_peer.ip,
                "port": current_peer.port
            }).encode("utf-8"), other_peer.addr())
            other_peer = None
            continue

        sock.sendto(b'OK', current_peer.addr())


        
    except Exception as e:
        print(f"[ERROR] {e}")