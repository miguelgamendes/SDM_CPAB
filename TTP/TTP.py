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
 

#TTP, trusted third party, has two functions:
#1) It does the setup of the system. It generates the master key-pair.
#2) TTP distributes keys for the users, based on the attributes.
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
 
    # initializes the master keys, if they were not already generated
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

    # listens to incoming requests
    # sends back the key corresponding to the attributes and the master public key
    def listen(self):
        self.s.listen(10)
        print("TTP is listening for requests.")
        while(True):
            connection, address = self.s.accept()
            # get the message size
            request_size = connection.recv(4)
            size = struct.unpack('!I', request_size)[0]
            request = pickle.loads(connection.recv(size))
            try:
                if(request['type'] == "GENERATE"):
                    # obtain key and send back the key and the master public key
                    # together with the sizes and a status code
                    key = objectToBytes(self.generate(request['attributes']), self.group)
                    mpk_bytes = objectToBytes(self.mpk, self.group)
                    message = struct.pack('!BII', 1, len(key), len(mpk_bytes)) + key + mpk_bytes
                else:
                    # send back an error message together with a status code and the size of the message
                    error_message = pickle.dumps("Command not recognized.")
                    message = struct.pack('!BI', 0, len(error_message)) + error_message
            except:
                error_message = pickle.dumps("Error.")
                message = struct.pack('!BI', 0, len(error_message)) + error_message
            connection.send(message)
        self.s.close()

    # generates they key corresponding to the attributes
    def generate(self, attributes):
        attributes = [a.upper() for a in attributes]
        key = cpabe_keygen(self.group, self.msk, self.mpk, attributes)
        return key

# creates a TTP listening on localhost:12346
def main():
    ttp = TTP("localhost", 12346)

if __name__ == "__main__":
    main()


