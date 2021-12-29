import socket
import struct
import time
import getch
import multiprocessing

class client:
    def __init__(self, team_name,TEST):
        self.true_magic_cookie=0xabcddcba
        self.true_message_type=0x2
        self.team_name=team_name
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#, socket.IPPROTO_UDP
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client started, listening for offer requests...")
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
                magic_cookie,message_type,server_port = struct.unpack('Ibh',data[:7])
            #todo 

                check_magic = magic_cookie == self.true_magic_cookie
                check_message_type= message_type==self.true_message_type
                if check_message_type and check_magic and int(server_port) > 0  :
                    print(f"Received offer from {addr[0]},attempting to connect...")
                    self.connecting_to_TCP_server(addr[0],server_port)
            except Exception as e:
                # print(e)
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
                print(f'No Welcome Message has been received. Lets find new Server.')
                raise Exception('Connected Server sucks.')
            else:
                print(data.decode())
            # Start the game !
            self.game_on()
            print('Server disconnected, listening for offer requests...')
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
            print(f"No win_message Message, but it's over..")
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
    c=client("the good fellas",False)
    c.looking_server()






