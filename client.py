import socket
class client:
    def __init__(self, team_name,TEST):
        self.tema_name=team_name
        self.gameClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        if TEST:
            self.gameClientUDP.bind(('172.99.255.255', 13117))
        else:
            self.gameClientUDP.bind(('172.1.255.255', 13117))
        self.gameClientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(" Server started, listening onIP address 172.1.0.88”")
if __name__ == '__main__':
    client("the good fellas",False);




