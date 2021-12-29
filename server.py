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
        self.server_tcp = socket(AF_INET, SOCK_STREAM)
        self.server_tcp.bind(('', GAME_PORT))
        self.server_tcp.listen(8)
        self.found = dict() # dict of
        self.confirmed_teams = False  # Whether we found two teams that want to play, and they both confirmed this

        
        # Currently run on test server.
        self.listen = False  # value to stop listener
        self.listen_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.UDP_port = 65339
        self.hostIP = ''
        self.my_port = 13177
        self.broadcast_address = '172.1.0.0'
    
    def broadcast_UDP_setup(self):
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind((self.server_address, self.UDP_port))  # not sure exactly what to put here
        print("sendUDPBroadcast: Bind Completed")
        self.sockUDP.connect(('2121', self.my_port))
        print("sendUDPBroadcast: Connect Complete")

    def send_UDP_broadcast(self):
        print("Length of sent:", len(struct.pack('!IbH', 0xabcddcba, 0x2, 2121)))
        sent = self.sockUDP.sendto(struct.pack('IbH', 0xabcddcba, 0x2, 2121), ('<broadcast>', 13177))
        print("Sent length:", sent)
        
    def game(self):
        return
    def find_teams(self):
        while not self.confirmed_teams:
            try:
                new_socket, address = self.server_tcp.accept()
                if len(self.found) < 2:  # stops incoming traffic, checks if # confirmed sockets greater than 2, 
                    # socket.recv is a blocking call. Could use mutex? But then if recv fails...
                    # new_socket.setblocking(0) # actually, why not make it block?
                    team_name = new_socket.recv(1024).decode()
                    print(f"We found {team_name}'s connection")
                    self.team_names[new_socket.getsockname()] = team_name
                    self.found.append(socket)
                else:
                    # Tries to send message to each team.
                    unresponsive = []
                    for socket in self.found:
                        try:
                            socket.send("Marco!".encode()) 
                        except:
                            # if they don't respond, remove them from the list. 
                            # Cant do it right here as we cant remove from a list while iterating over it
                            unresponsive.append(socket)
                    
                    # removes unresponsive sockets
                    for socket in unresponsive:
                        self.found.remove(socket)
                    
                    if len(self.found) == 2:
                        self.team1_name = self.team_names[self.found[0]]
                        self.team2_name = self.team_names[self.found[0]]
                        print(f"Team {self.team1_name} and Team {self.team2_name} have confirmed their connection")
                        self.confirmed_teams = True
                        self.found = self.found[:2]  # TODO: Should we check to see that if there are extra connections, and disconnect? Is that even possible?
                        
                # for socket in to_remove:
                #     print(f"Team {self.get_team_name(socket)} Disconnected") # PRINT TEAM NAME
                #     del self.team_names[socket.getsockname()]
                #     self.team_sockets.remove(socket)
            except:
                pass
    
            
        def __play(self):
            num1 = random.randint(0, 4)
            num2 = random.randint(0, 4)
            s = "Hello and welcome to the award winning quick maths game!!\n"
            s += f"Team 1: {self.team1_name} vs Team2: {self.team2_name}\n"
            s += f"The question for you is: What is {num1}+{num2}?"
            
            print(s)
            s = s.encode()
            self.found[0].sendall(s)
            self.found[1].sendall(s)

            game_over = False
            while not game_over:
                # TODO: implement actual game
                pass
                


serv = Server("IDUNNO", False)
serv.broadcast_UDP_setup()
time_counter = 0
start_time = time.time()
while time.time() <= start_time + 10:
    time_counter +=1
    serv.send_UDP_broadcast()
    time.sleep(1)
    print(time_counter)