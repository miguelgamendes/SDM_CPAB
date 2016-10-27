'''
TTP, trusted third party, has two functions:
1) It does the setup of the system. It generates the master key-pair.
2) TTP distributes keys for the users, based on the attributes.
'''
import socket
import sys
import os.path
import struct
import pickle

from charm.core.engine.util import objectToBytes
from charm.toolbox.pairinggroup import PairingGroup
from pebel.util import write_key_to_file
from pebel.util import read_key_from_file
from pebel.cpabe import cpabe_setup
from pebel.cpabe import cpabe_keygen
 
class TTP:
    def __init__(self, hostname, port):
        print("TTP: \n\nHostname:\n ", hostname, "\nPort:\n ", port, "\n")
        self.hostname = hostname
        self.port = port
        self.setup()
        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.hostname, self.port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        self.listen()
 
    def setup(self):
        mpk_filename = "cp.mpk"
        msk_filename = "cp.msk"
        self.group = PairingGroup('SS512')
        if(not os.path.isfile("cp.mpk") or not os.path.isfile("cp.msk")):
            (self.mpk, self.msk) = cpabe_setup(self.group)
            write_key_to_file(mpk_filename, self.mpk, self.group)
            write_key_to_file(msk_filename, self.msk, self.group)
        else:
            self.mpk = read_key_from_file(mpk_filename, self.group)
            self.msk = read_key_from_file(msk_filename, self.group)


    def listen(self):
        self.s.listen(10)
        print("TTP is listening for requests.")
        while(True):
            connection, address = self.s.accept()
            request_size = connection.recv(4)
            size = struct.unpack('!I', request_size)[0]
            request = connection.recv(size)
            request = pickle.loads(request)
            if(request['type'] == "GENERATE"):
                # message contains key
                message = objectToBytes(self.generate(request['attributes']), self.group)
            else:
                message = pickle.dumps("Command not recognized.")
            message_send = struct.pack('!I', len(message)) + message
            connection.send(message_send)
        self.s.close()

    def generate(self, attributes):
        attributes = [a.upper() for a in attributes]
        key = cpabe_keygen(self.group, self.msk, self.mpk, attributes)
        return key

def main():
    ttp = TTP("localhost", 12346)

if __name__ == "__main__":
    main()


