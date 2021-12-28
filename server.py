# import scapy #import get_if_addr
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
        self.server_address = '172.1.0.121'

        # Start TCP socket that will listen for new teams
        self.tcp = socket(AF_INET, SOCK_STREAM)
        self.tcp.bind(('', GAME_PORT))
        self.tcp.listen(10)
        self.found = dict() # dict of
        self.confirmed_teams = False  # Whether we found two teams that want to play, and they both confirmed this

        
        # Currently run on test server.
        self.listen = False  # value to stop listener
        self.listen_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.hostIP = ''
        self.my_port = 13177
        # binds socket to a well known port, and a public host.
        self.listen_soc.bind((socket.gethostname(), 80))
        self.broadcast_address = '172.1.0.0'
    
    def broadcast_UDP_setup(self):
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind((self.server_address, self.my_port))
        print("sendUDPBroadcast: Bind Completed")
        self.sockUDP.connect(('2121', self.my_port))
        print("sendUDPBroadcast: Connect Complete")

    def send_UDP_broadcast(self):
        print("Length of sent:", len(struct.pack('!IbH', 0xabcddcba, 0x2, 2121)))
        sent = self.sockUDP.sendto(struct.pack('IbH', 0xabcddcba, 0x2, 2121), ('<broadcast>', 13177))
        print("Sent length:", sent)
        

    def find_teams(self):
        while not self.confirmed_teams:
            try:
                new_socket, address = self.tcp.accept()
                if not len(self.found) == 2:  # stops incoming traffic, checks if # confirmed sockets greater than 2, 
                    new_socket.setblocking(0) # socket.recv is a blocking call. Could use mutex? But then if recv fails...
                    team_name = new_socket.recv(2048).decode()
                    #print(f"Team {team_name} Connected!")
                    self.team_names[new_socket.getsockname()] = team_name
                    self.found.append(socket)
        # while self.listen is True:
        #     clientsocket, address = self.listen_soc.accept()
            # TODO: do whatever you need with the socket.
            # e.g:
    

serv = Server("IDUNNO", False)
serv.broadcast_UDP_setup()
time_counter = 0
start_time = time.time()
while time.time() <= start_time + 10:
    time_counter +=1
    serv.send_UDP_broadcast()
    time.sleep(1)
    print(time_counter)