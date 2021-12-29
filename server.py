from scapy.all import get_if_addr #import get_if_addr
import socket
import struct
import time
from threading import Thread
#import multiprocessing
#sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Server:
    def __init__(self, test) -> None:
        
        if test:
            self.IP = get_if_addr('eth2')
            self.broadcast_addr = ''
        else:
            self.IP = get_if_addr('eth1')
            self.broadcast_addr = ''
        
        # Get port, and whether or not its a test.
        self.server_address = socket.gethostbyname(socket.gethostname())
        print(self.server_address) 

        # Start TCP socket that will listen for new teams
        self.server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_tcp.listen(8)
        self.server_tcp.bind((self.IP, 2121))
        self.found = [] 
        self.team_names = dict() # dict of {team_name: team_socket}
        self.confirmed_teams = False  # Whether we found two teams that want to play, and they both confirmed this

        
        # Currently run on test server.
        self.listen = False  # value to stop listener
        self.listen_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_port = 64455
        self.my_port = 13177
        #self.broadcast_address = '172.1.0.0' (not used?)
    
    def broadcast_UDP_setup(self):
        self.sock_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock_UDP.bind(('', self.UDP_port))  # not sure exactly what to put here
        print("sendUDPBroadcast: Bind Completed")
        self.sock_UDP.connect(('2121', self.my_port))
        print("sendUDPBroadcast: Connect Complete")

    def send_UDP_broadcast(self):
        print("Length of sent:", len(struct.pack('IbH', 0xabcddcba, 0x2, 2121)))
        sent = self.sock_UDP.sendto(struct.pack('IbH', 0xabcddcba, 0x2, 2121), ('<broadcast>', 13177))
        print("Sent length:", sent)

    def find_teams(self):
        print("Entered Find teams")
        while not self.confirmed_teams:
            try:
                print("FindTeams: Looking for messages on tcp")
                # recieved1, rec2 = self.server_tcp.recv(2048).decode()
                self.server_tcp.settimeout(10)
                new_socket, address = self.server_tcp.accept() # address - its ip
                print(new_socket)
                print(address)
                time.sleep(2)
                print(recieved)
                #print(f"FindTeams: {new_socket}, {address} were accepted")
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
                            print(f"removing socket of {team_names[socket.getsockname()]}")
                            unresponsive.append(socket)
                            
                    # removes unresponsive sockets
                    for socket in unresponsive:
                        self.found.remove(socket)
                        print(f"removed socket {team_names[socket.getsockname()]}")
                        del team_names[socket.getsockname()]
                        
                    
                    if len(self.found) == 2:
                        self.team1_name = self.team_names[self.found[0]]
                        self.team2_name = self.team_names[self.found[0]]
                        print(f"Team {self.team1_name} and Team {self.team2_name} have confirmed their connection")
                        self.confirmed_teams = True
                        self.found = self.found[:2]  # TODO: Should we check to see that if there are extra connections, and disconnect? Is that even possible?

            except Exception as e:
                print("Problem in listening:")
                print(e)
                break
    
            
        def play(self):
            self.sock_UDP.close()  # dont need udp anymore
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
                r_socks, _, __ = select.select(self.found, [], [])  # we assume first response entered first in r_socks
                for sock in r_socks:
                    answer = sock.recv(1024).decode() 
                    try:
                        answer = int(answer)
                    except:
                        print(f"{answer} cant be converted to int!")
                    
                    try:
                        if num1 + num2 == answer:
                            winner = self.team_names[sock.getsockname()]
                            game_over = True
                    except:
                        print("There was a problem in the game!")
                        pass
            
            for socket in self.found:
                socket.sendall(f"The winner is: {winner}".encode())
            
            self.server_tcp.close()
    
    def UDP_pulses(self):
        self.broadcast_UDP_setup()
        time_counter = 0
        start_time = time.time()
        while time.time() <= start_time + 10:
            time_counter += 1
            serv.send_UDP_broadcast()
            time.sleep(1)
            print(time_counter)

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server_tcp.listen(8)
ip = get_if_addr('eth2')
print(ip)
print(type(ip))
inet = "172.1.0.121"
server_tcp.bind((ip, 2121))
sock, addr = server_tcp.accept()
print(sock)
print(addr)
# serv = Server(False)
# broadcast_thread = Thread(target=serv.UDP_pulses)
# listen_thread = Thread(target=serv.find_teams)
# #play_thread = threading.Thread(target=serv.play)

# broadcast_thread.start()
# listen_thread.start()

# broadcast_thread.join()
# listen_thread.join()

# #play_thread.start()
# print("End of program")
