import socket
import struct
import time
import getch
import multiprocessing

def color(color, backgrd="black"):
    color = color.lower()
    backgrd = backgrd.lower()
    color_dict = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 
                    'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37}
    back_dict = dict()
    for color, num in color_dict.items():
        back_dict[color] = num + 10
    
    return f"\033[1;{color_dict[color]};{back_dict[backgrd]}m"

GREEN = '\033[1;32;40m'
RED = '\033[1;31;40m'
BLUE = '\033[1;34;40m'
PURPLE = '\033[1;35;40m'
CYAN = '\033[1;36;40m'
CBOLD     = '\33[1m'
CGREY     = '\33[90m'
CSELECTED = '\33[7m'
CEND      = '\33[0m'
GREEN = '\033[1;32;40m'
RED = '\033[1;31;40m'
BLUE = '\033[1;34;40m'
class client:

    def __init__(self, team_name,TEST):

        self.true_magic_cookie=0xabcddcba
        self.true_message_type=0x2
        self.team_name=team_name
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #, socket.IPPROTO_UDP
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"{BLUE}Client started, listening for offer requests...")
        self.true_magic_cookie= 0xabcddcba
        self.true_message_type= 0x2
    
    def looking_server(self):
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.gameClientUDP.bind(("", 13117))
        

        while True:
            try:
                data, addr = self.gameClientUDP.recvfrom(1024)
                # if len(data)!= struct.calcsize('IbH'):
                #     continue
                magic_cookie,message_type,server_port = struct.unpack('Ibh',data)
            #todo 
                print(server_port)

                check_magic = magic_cookie == self.true_magic_cookie
                check_message_type= message_type==self.true_message_type
                print(f"{GREEN}Received offer from {addr[0]},attempting to connect...")
                if check_message_type and check_magic :
                    self.connecting_to_TCP_server(addr[0],server_port)
            except Exception as e:
                print(e)
                pass
    
    def connecting_to_TCP_server(self,addr, gamePort):
        """
        Connecting to Game Server
        Parameters:
            addr (str): Game Server addr
            gamePort (int): Game Server Port
        """
        try:
            # self.gameClientTCP.settimeout(10)
            self.gameClientTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            self.gameClientTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            # Connecting to the TCP Game Server
            self.gameClientTCP.settimeout(10)
            self.gameClientTCP.connect((addr, gamePort))
            # Sending to the Server our Team Name
            self.gameClientTCP.sendall((self.team_name + '\n').encode())
            # Waiting for openning message
            data = None
            try:
                self.gameClientTCP.settimeout(10)
                data = self.gameClientTCP.recv(1024)
            except:
                pass
            if data is None:
                # {CBOLD}{CGREY}{CSELECTED}{CEND}
                print(f"{RED}No Welcome Message has been received. Lets find new Server.")
                raise Exception('Connected Server sucks.')
            else:
                print(data.decode())
            # Start the game !
            self.game_on()
            print(f"{CYAN}Server disconnected, listening for offer requests...")
        except Exception as e:
            print(e)
            print("connection doesn't work let's try new server")
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    
    
    def game_on(self):
        key_enter = multiprocessing.Process(target=self.PressKey)
        # Start the Thread
        key_enter.start()
        # Give the Thread 10 secs to live
        key_enter.join(10)
        if key_enter.is_alive():
            key_enter.terminate()
        self.gameClientTCP.settimeout(10)
        win_message = None
        # Getting the  win_message Message or if time pass moving on
        try:
            self.gameClientTCP.settimeout(10)
            win_message = self.gameClientTCP.recv(1024)
        except:
            pass
        if win_message is None:
            print(f"{PURPLE}No win_message Message, but it's over..")
        else:
            print(win_message.decode())
    
    
    def PressKey(self):
        # 10 secs to press, GO GO GO !
        while True:
            try:
                # Getting the pressed key
                char = getch.getch()
                # Sending it to the Server
                self.gameClientTCP.sendall(char.encode(''))
                break
            except:
                pass

if __name__ == '__main__':
    c=client("the good fellas",True)
    c.looking_server()






