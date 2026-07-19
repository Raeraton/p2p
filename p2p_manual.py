from requests import get
from p2p import P2PConnection
from threading import Thread


ip = get('https://api.ipify.org').content.decode('utf8')

print('My public IP address is: {}'.format(ip))
port = int(input("choose your port: "))

target_ip = input("enter target ip: ")
target_port = int(input("enter target port: "))

con = P2PConnection(port, target_ip, target_port)

def recvr_th():
    global con
    while 1:
        data = con.recv()
        try:
            print(data.decode("utf-8"))
        except Exception as e:
            print(f"err {e}")

Thread(target=recvr_th).start()


while 1:
    con.send(b"hello")
    print(con.recv())  