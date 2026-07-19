import socket
import time
import threading
import json


class Cupple:

    class IHaveABoyfriend(Exception):
        def __init__(self, message: str):
            self.msg = message
        def __str__(self):
            return f"Sorry I have a boyfriend. {self.msg}" 

    class YouNotOnTheList(Exception):
        def __init__(self, message: str):
            self.msg = message
        def __str__(self):
            return f"Sorry you not on the list. {self.msg}" 


    ip1: str
    port1: int
    set1: bool
    popped1: bool

    ip2: str
    port2: int
    set2: bool
    popped2: bool

    lock: threading.Lock
    

    def __init__(self):
        self.set1 = False
        self.set2 = False
        self.popped1 = False
        self.popped2 = False
        self.lock = threading.Lock()
    
    def regist(self, ip:str, port:int):
        self.lock.acquire()
        if not self.set1:
            self.set1 = True
            self.ip1 = ip
            self.port1 = port
        elif not self.set2:
            self.set2 = True
            self.ip2 = ip
            self.port2 = port
        else:
            self.lock.release()
            raise self.IHaveABoyfriend("")
        self.lock.release()
    
    def unregist(self, ip:str, port:int):
        self.lock.acquire()
        if self.set1 and self.ip1==ip and self.port1==port:
            self.set1 = False
            self.ip1 = None
            self.port1 = None
        elif self.set2 and self.ip2==ip and self.port2==port:
            self.set2 = False
            self.ip2 = None
            self.port2 = None
        self.lock.release()
    
    
    def other(self, ip:str, port:int) -> tuple:
        out = None
        self.lock.acquire()
        if self.set1 and self.ip1==ip and self.port1==port:
            while not self.set2:
                self.lock.release()
                time.sleep(0.01)
                self.lock.acquire()
            out = (self.ip2, self.port2)
            self.popped2 = True
        elif self.set2 and self.ip2==ip and self.port2==port:
            while not self.set1:
                self.lock.release()
                time.sleep(0.01)
                self.lock.acquire()
            self.popped1 = True
            out = (self.ip1, self.port1)
        else:
            raise self.YouNotOnTheList("")
        self.lock.release()
        return out
    
    def clear(self):
        self.lock.acquire()
        if self.popped1 and self.popped2:
            self.set1 = False
            self.set2 = False
            self.popped1 = False
            self.popped2 = False
            self.ip1 = None
            self.ip2 = None
            self.port1 = None
            self.port2 = None
        self.lock.release()



cupple = Cupple()

def handle_client(cli: socket.socket, addr: tuple):
    global cupple
    ip, port = "", 0
    try:
        port = int(cli.recv(1024).decode("utf-8"))
        if port == 0: port = addr[1]

        ip = addr[0]

        cupple.regist(ip, port)

        other = cupple.other(ip, port)

        cupple.clear()

        to_send = json.dumps({
            "ip": other[0],
            "port": other[1]
        }).encode("utf-8")

        cli.send(to_send)
        cli.close()

    except Cupple.IHaveABoyfriend as e:
        cupple.unregist(ip, port)
        print(f"[ERROR] i have a boyfriend. {e}")
    except Cupple.YouNotOnTheList as e:
        cupple.unregist(ip, port)
        print(f"[ERROR] you not invited. {e}")
    except Exception as e:
        cupple.unregist(ip, port)
        print(f"[ERROR] other. {e}")
        

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("0.0.0.0", 1235))
sock.listen(1)

print(f"listening on {socket.gethostbyname(socket.gethostname())}:{1235}")


while 1:
    cli, addr = sock.accept()
    threading.Thread( target=handle_client, args=(cli, addr) ).start()