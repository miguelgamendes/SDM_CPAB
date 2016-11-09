import socket
import struct
import sys
import pickle
import pebel
import os.path
import io
import base64
import hashlib

from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import PairingGroup
from pebel.cpabe import cpabe_encrypt
from pebel.cpabe import cpabe_decrypt
from pebel.exceptions import PebelDecryptionException
from pebel.util import write_key_to_file
from pebel.util import read_key_from_file

# User class
# User does not discriminate between different types, so a doctor and a patient
# are both a user and the only differences are the set of attributes they have and
# their ID
class User:

    # hostnames for TTP and Data Server
    hostname_server = "localhost"
    port_server = 12345
    hostname_ttp = "localhost"
    port_ttp = 12346

    # Initialize new key
    # ID: contains a unique ID for this user
    # attributes: attributes for this user, which are used for encryption
    def __init__(self, ID, attributes, force = False):
        self.ID = ID
        self.filename = "user%i" % self.ID
        self.attributes = attributes
        self.get_keys(force)

    # obtains the key corresponding to the attributes and the public master key
    def get_keys(self, force):
        # path where the keys are stored
        keypath = os.path.dirname(os.path.abspath(__file__)) + "/keys/"
        self.group = PairingGroup('SS512')
        # generate keys if they do not yet exist
        if((not os.path.isfile(keypath + self.filename + ".key")) or (not keypath + "cp_" + self.filename + ".mpk") or force):
            # create a conncection to the TTP
            s = socket.create_connection((self.hostname_ttp, self.port_ttp))
            # create request object
            obj = {}
            obj['type'] = "GENERATE"
            obj['attributes'] = self.attributes
            # send message
            message = pickle.dumps(obj)
            message_send = struct.pack('!I', len(message)) + message 
            s.send(message_send)
            # obtain status code
            [status] = struct.unpack('!B', s.recv(1))
            # if the status is 1(ok) obtain keys
            if(status == 1):
                # receive key sizes
                [size_key, size_mpk] = struct.unpack('!II', s.recv(8))
                # obtain key
                self.key = bytesToObject(s.recv(size_key), self.group)
                write_key_to_file(keypath + self.filename + ".key", self.key, self.group)
                # obtain master public key
                self.mpk = bytesToObject(s.recv(size_mpk), self.group)
                write_key_to_file(keypath + "cp_" + self.filename + ".mpk", self.mpk, self.group)
            else:
                # an error message is send
                [message_size] = struct.unpack('!I', s.recv(4))
                message = pickle.loads(s.recv(message_size))
                print(message)
            # close socket
            s.close()
        else:
            self.key = read_key_from_file(keypath + self.filename + ".key", self.group)
            self.mpk = read_key_from_file(keypath + "cp_" + self.filename + ".mpk", self.group)

    # retrieves all data from server
    def retrieve(self):
        # connect to server
        s = socket.create_connection((self.hostname_server, self.port_server))
        # create request object
        obj = {}
        obj['type'] = "REQUEST"
        message = pickle.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        s.send(message_send)
        # receive first 5 bytes indicating the status and the size of the results 
        [status, size] = struct.unpack('!BI', s.recv(5))
        results = pickle.loads(s.recv(size))
        # if status is 1(ok) try to decrypt results
        if(status == 1):
            for result in results:
                try:
                    # server only sends data, so index is 0
                    Data = self.decrypt(result[0])
                    print("result: ", Data)
                except:
                    pass
        else:
            print(results)
        s.close()

    # sends an insert request to the server, data is encrypted before it is send
    # Data contains the data to be send
    # policy is the policy under which the data has to be encrypted
    # TID is the user for who the data is inserted, there are two cases
    #   * if it is a patient TID and self.ID are the same
    #   * if it is a hospital or healthclub (h(TID), h(self.ID)) has to be in the membership table
    def insert(self, Data, policy, TID):
        Data = self.encrypt(Data, policy)
        # connect to server
        s = socket.create_connection((self.hostname_server, self.port_server))
        # prepare message object to send to server
        obj = {}
        obj['type'] = "INSERT"
        # hash target and source
        obj['target'] = hashlib.sha512(str(TID).encode()).hexdigest()
        obj['source'] = hashlib.sha512(str(self.ID).encode()).hexdigest()
        obj['Data'] = Data
        # serialize and send message
        message = pickle.dumps(obj)
        message_send = struct.pack('!I', len(message)) + message 
        s.send(message_send)
        # handle response
        [status, size] = struct.unpack('!BI', s.recv(5))
        response = pickle.loads(s.recv(size))
        print("Response message: ", response)
        s.close()

    # encrypts the data using a policy
    # Data: data to encryopt in string format
    # policy: specifies the policy under which this data may be disclosed
    def encrypt(self, Data, policy):
        Data = io.StringIO(Data)
        ctxt = cpabe_encrypt(self.group, self.mpk, Data, policy)
        return bytes.decode(base64.b64encode(ctxt))

    # decrypts the ciphertext using the master public key and the user key
    def decrypt(self, Ciphertext):
        try:
            Ciphertext = base64.b64decode(Ciphertext)
            Ciphertext = io.BytesIO(Ciphertext)
            Data = cpabe_decrypt(self.group, self.mpk, self.key, Ciphertext)
            return bytes.decode(Data)
        except PebelDecryptionException as e:
            raise