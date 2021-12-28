from scapy import get_if_addr
import socket
import struct
import time
#import threading
#import multiprocessing
print("Starting")
sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Server:
    def __init__(self, port, test) -> None:
        # Get port, and whether or not its a test.
        self.port = port
        if test:
            self.IP = get_if_addr('eth2')
            self.broadcastAddr = '172.99.255.255'
        else:
            self.IP = get_if_addr('eth1')
            self.broadcastAddr = '172.1.255.255'
        

        # Currently run on test server.
        self.listen = False  # value to stop listener
        self.listen_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.hostIP = ''
        self.my_port = 13177
        # binds socket to a well known port, and a public host.
        self.listen_soc.bind((socket.gethostname(), 80))
        self.broadcast_address = '172.99.255.255'
    
    def sendUDPBroadcast(self):
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind((self.hostIP, self.my_port))
        print("sendUDPBroadcast: Bind Completed")
        self.sockUDP.connect(('2121', self.my_port))
        print("sendUDPBroadcast: Connect Complete")
        msg = "Can you hear me???"
        print(len(struct.pack('!IbH', 0xabcddcba, 0x2, 2121)))
        sent = self.sockUDP.sendto(struct.pack('IbH', 0xabcddcba, 0x2, 2121), ('<broadcast>', 13177))
        print(sent)
        

    def listen(self):
        self.listen_soc.listen(2)  # max num of connect requests before refusing connections
        while self.listen is True:
            clientsocket, address = self.listen_soc.accept()
            # TODO: do whatever you need with the socket.
            # e.g:
    

serv = Server()
serv.sendUDPBroadcast()
time_counter = 0
start_time = time.time()
while time.time() <= start_time + 10:
    time_counter +=1
    serv.sendUDPBroadcast()
    sleep(1)
    print(time_counter)