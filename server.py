#from scapy.all import *
import socket
#import threading
#import multiprocessing

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('2121', '13177'))
msg = "Can you hear me???"
totalsent = 0
print("Entering")
while totalsent < 13*8:
    sent = self.sock.send(msg[totalsent:])
    print(sent)
    if sent == 0:
        raise RuntimeError("socket connection broken")
    totalsent = totalsent + sent
print("nkds")

class server:
    def __init__(self) -> None:
        # Currently run on test server.
        self.listen = False  # value to stop listener
        self.listen_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # binds socket to a well known port, and a public host.
        self.listen_soc.bind((socket.gethostname(), 80))
        self.broadcast_address = '172.99.255.255'
    
    def listen(self):
        self.listen_soc.listen(2)  # max num of connect requests before refusing connections
        while self.listen is True:
            clientsocket, address = self.listen_soc.accept()
            # TODO: do whatever you need with the socket.
            # e.g:
