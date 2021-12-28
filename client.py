import socket
import struct
class client:
    def __init__(self, team_name,TEST):
        self.tema_name=team_name
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.gameClientUDP.bind(("", 13117))
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client started, listening for offer requests...")
        self.true_magic_cookie= 0xabcddcba
        self.true_message_type= 0x2
    def looking_server(self):
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.gameClientUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            try:
                data, addr = self.gameClientUDP.recvfrom(1024)
            except:
                pass
            print(f"data: {len(data)}.")
            magic_cookie,message_type,server_port = struct.unpack('IbH',data)
            if server_port==2121:
                print(magic_cookie)
                print(message_type)
                print(server_port)

            # self.gameClientTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            # self.gameClientTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            # self.gameClientTCP.connect((addr[0],server_port))
            # print(f"Connected to server {addr[0]}.") 
            # self.gameClientTCP.sendall(str.encode("troling\n"))
            
            
            

if __name__ == '__main__':
    c=client("the good fellas",False)
    c.looking_server()






