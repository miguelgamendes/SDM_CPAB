import socket
import struct
import sys
import pickle
import pebel
import os.path
import io
import base64

from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import PairingGroup
from pebel.cpabe import cpabe_encrypt
from pebel.cpabe import cpabe_decrypt
from pebel.exceptions import PebelDecryptionException
from pebel.util import write_key_to_file
from pebel.util import read_key_from_file

class User:

    # force forces to get a new key
    def __init__(self, ID, hostname_server, port_server, hostname_ttp, port_ttp, attributes, force = False):
        self.ID = ID
        self.filename = "user%i.key" % self.ID
        self.hostname_server = hostname_server
        self.port_server = port_server
        self.hostname_ttp = hostname_ttp
        self.port_ttp = port_ttp
        self.attributes = attributes
        self.get_keys(force)


    def get_keys(self, force):
        self.group = PairingGroup('SS512')
        # TODO: make nice because this is aquick fix for master key
        self.mpk = read_key_from_file("../TTP/cp.mpk", self.group)
        # do the rest
        if(not os.path.isfile(self.filename) or force):
            s = socket.create_connection((self.hostname_ttp, self.port_ttp))
            obj = {}
            obj['type'] = "GENERATE"
            obj['attributes'] = self.attributes
            message = pickle.dumps(obj)
            message_send = struct.pack('!I', len(message)) + message 
            s.send(message_send)
            results_size = s.recv(4)
            size = struct.unpack('!I', results_size)[0]
            results_receive = s.recv(size)
            self.key = bytesToObject(results_receive, self.group)
            write_key_to_file(self.filename, self.key, self.group)
            print(self.key)
            s.close()
        else:
            self.key = read_key_from_file(self.filename, self.group)

    # retrieves data from server
    # TODO: decryption
    def retrieve(self):
        # connect to server
        s = socket.create_connection((self.hostname_server, self.port_server))
        obj = {}
        obj['type'] = "REQUEST"
        obj['ID'] = self.ID
        message = pickle.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        s.send(message_send)
        # receive first 4 bytes indicating the size of the result
        results_size = s.recv(4)
        size = struct.unpack('!I', results_size)[0]
        results_receive = s.recv(size)
        results = pickle.loads(results_receive)
        for result in results:
            # server only sends data, so index is 0
            Data = self.decrypt(result[0])
            print("result: ", Data)
        s.close()

    # inserts a new entry into the server if you have the permissions
    # TODO: encrypt data
    def insert(self, Data, policy):
        Data = self.encrypt(Data, policy)
        # connect to server
        s = socket.create_connection((self.hostname_server, self.port_server))
        obj = {}
        obj['type'] = "INSERT"
        obj['ID'] = self.ID
        obj['CID'] = self.ID
        obj['Data'] = Data
        message = pickle.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        s.send(message_send)
        response_size = s.recv(4)
        size = struct.unpack('!I', response_size)[0]
        response_received = s.recv(size)
        response = pickle.loads(response_received)
        print("Response message: ", response)
        s.close()

    # encrypts the data using a policy
    # @param Data, data to encryopt in string format
    # @param policy, specifies the policy under which this data may be disclosed
    def encrypt(self, Data, policy):
        # conversion
        Data = io.StringIO(Data)
        ctxt = cpabe_encrypt(self.group, self.mpk, Data, policy)
        return bytes.decode(base64.b64encode(ctxt))

    def decrypt(self, Ciphertext):
        try:
            # conversion
            Ciphertext = base64.b64decode(Ciphertext)
            Ciphertext = io.BytesIO(Ciphertext)
            Data = cpabe_decrypt(self.group, self.mpk, self.key, Ciphertext)
        except PebelDecryptionException as e:
            print("Unable to decrypt ciphertext: {}".format(e))
        return bytes.decode(Data)

def main():
    '''
    # test encryption
    policy = 'a'
    data_string = "test123"
    c = user.encrypt(data_string, policy)
    print("Ciphertext:\n\n", c, "\n\n")
    m = user.decrypt(c)
    print("Plaintext:\n\n", m, "\n")
    '''
    # USER 1
    #user = User(1, "localhost", 12345, 'localhost', 12346, {"a", "b", "c", "d"})
    #user.retrieve()
    
    #while(True):
    #   Data = input('What is your name?\n')
    #    print(Data)
    #    user.insert(Data, policy)

    # -------------------------------------------------
    # USER 2
    user2 = User(2, "localhost", 12345, 'localhost', 12346, {"d"})
    user2.retrieve()

if __name__ == "__main__":
    main()
