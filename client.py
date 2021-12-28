import socket
import struct
class client:
    def __init__(self, team_name,TEST):
        self.tema_name=team_name
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.gameClientUDP.bind(("", 13117))
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client started, listening for offer requests...")
    def looking_server(self):
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            data, addr = self.gameClientUDP.recvfrom(1024)
            magic_cookie,message_type,server_port= struct.unpack('!IbH',data)
            if(server_port == 2121):
                print(magic_cookie)
                print(message_type)
                print(pork)
                break;
            print("again")
            
            

if __name__ == '__main__':
    c=client("the good fellas",False)
    c.looking_server()






