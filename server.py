import socket
import time
import threading
import json

peers = []

def handle_client( cli: socket.socket, addr: tuple ):
    global peers
    try:
        
        port = int(cli.recv(64).decode("utf-8"))

        print(f"[LOG] client ({addr[0]}:{addr[1]}) and waiting for a friend at port {port}")
        
        other_idx = (len(peers) + 1) % 2
        peers.append({
            "ip": addr[0],
            "port": port
        })
        while len(peers) < 2: time.sleep(0.01)

        cli.send( json.dumps( peers[other_idx] ).encode("utf-8") )
        cli.close()

        

    except Exception as e:
        print( f"[ERROR] {e}" )




IP = '127.0.0.1'
PORT = 1237

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.bind((IP, PORT))
sock.listen(1)

while 1:
    cli, addr = sock.accept()
    threading.Thread( target=handle_client, args=(cli, addr) ).start()
