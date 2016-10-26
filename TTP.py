'''
TTP, trusted third party, has two functions:
1) It does the setup of the system. It generates the master key-pair.
2) TTP distributes keys for the users, based on the attributes.
'''
import socket
import sys

from charm.toolbox.pairinggroup import PairingGroup
from pebel.util import write_key_to_file
from pebel.cpabe import cpabe_setup
 
# specify location
HOST = 'Trusted Third Party'
PORT = 1234
 
def __main__():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((HOST, PORT))
    except socket.error , msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    s.listen(10)
    print 'TTP is listening for requests.'
    conn, addr = s.accept()
 
#display client information
print 'Connected with ' + addr[0] + ':' + str(addr[1])

def setup():
    if keyfiles do not exist:
        generate master keys

def request():

