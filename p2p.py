import socket



class P2PConnection:

    def __init__(self, source_port:int, target_ip: str, target_port: int):
        self.target_ip = target_ip
        self.target_port = target_port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", source_port))
        self.socket.sendto(b"0", (self.target_ip, self.target_port))

    def send(self, data:bytes):
        self.socket.sendto( data, (self.target_ip, self.target_port) )
    
    def recv(self, buff_size=1200) -> bytes:
        data = b""
        while 1:
            data, addr = self.socket.recvfrom(buff_size)
            if addr[0]==self.target_ip and addr[1]==self.target_port:
                break
            else:
                print("wtf", addr)
        return data
        

