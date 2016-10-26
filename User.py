import socket
import sys

class User:

    def __init__(self, ID, hostname, port):
        self.ID = ID
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.hostname, self.port))

    def retrieve(self):
        obj = {}
        obj.type = "REQUEST"
        obj.ID = self.ID
        self.s.send(obj)
        while(True):
            results = self.s.recv(16)

    def insert(self, Data):
        # encrypt data
        obj = {}
        obj.type = "INSERT"
        obj.ID = self.ID
        obj.CID = self.CID
        obj.Data = Data
        self.s.send(obj)
        while(True):
            response = self.s.recv(16)
            print("Response message: ", response)

def main():
    user = User(1, "localhost", 12345)
    while(True):
        Data = input('What is your name?')
        print(Data)
        user.insert(Data)

if __name__ == "__main__":
    main()
