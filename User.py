import socket
import struct
import sys
import marshal

class User:

    def __init__(self, ID, hostname, port):
        self.ID = ID
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.hostname, self.port))

    # retrieves data from server
    # TODO: decryption
    def retrieve(self):
        obj = {}
        obj['type'] = "REQUEST"
        obj['ID'] = self.ID
        message = marshal.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        self.s.send(message_send)
        # receive first 4 bytes indicating the size of the result
        results_size = self.s.recv(4)
        size = struct.unpack('!I', results_size)[0]
        results_receive = self.s.recv(size)
        results = marshal.loads(results_receive)
        print(results)
        # DECRYPT DATA

    # inserts a new entry into the server if you have the permissions
    # TODO: encrypt data
    def insert(self, Data):
        # ENCRYPT DATA
        obj = {}
        obj['type'] = "INSERT"
        obj['ID'] = self.ID
        obj['CID'] = self.ID
        obj['Data'] = Data
        message = marshal.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        self.s.send(message_send)
        response_size = self.s.recv(4)
        size = struct.unpack('!I', response_size)[0]
        response_receive = self.s.recv(size)
        response = marshal.loads(response_receive)
        print("Response message: ", response)

def main():
    user = User(1, "localhost", 12345)
    #user.retrieve()
    
    while(True):
        Data = input('What is your name?\n')
        print(Data)
        user.insert(Data)
    

if __name__ == "__main__":
    main()
