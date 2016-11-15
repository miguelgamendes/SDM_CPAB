import pymysql.cursors
import socket
import sys
import pickle
import struct

# Semi-trusted server containing health data
class Server:
    
    # Server constructor
    def __init__(self, hostname, port):
        print("SERVER: \n\nHostname:\n ", hostname, "\nPort:\n ", port, "\n")
        self.hostname = hostname
        self.port = port
        # setup database
        try:
            self.db = pymysql.connect("localhost","root","","SDM")
            self.cursor = self.db.cursor()
        except Exception as e:
            print("Could not setup database connection.")
        self.create_tables()
        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.hostname, self.port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        self.listen()

    # creates tables if they do not already exist(embedded in query)
    # Table Data contains the patient health data
    # Table Membership conatins the membership relation between users
    def create_tables(self):
        create_user_table_query = """CREATE TABLE IF NOT EXISTS Users ( 
                                        ID int NOT NULL AUTO_INCREMENT,
                                        UID varchar(128) NOT NULL,
                                        Pass varchar(128) NOT NULL,
                                        PRIMARY KEY (ID),
                                        CONSTRAINT C_UID UNIQUE (UID)
                                    );"""
        create_data_table_query = """CREATE TABLE IF NOT EXISTS Data ( 
                                        ID int NOT NULL AUTO_INCREMENT,
                                        UID varchar(128),
                                        Data varchar(8192) NOT NULL,
                                        PRIMARY KEY (ID),
                                        FOREIGN KEY (UID) REFERENCES Users(UID)
                                    );"""
        create_membership_table_query = """CREATE TABLE IF NOT EXISTS Membership ( 
                                        ID int NOT NULL AUTO_INCREMENT,
                                        UID varchar(128) NOT NULL,
                                        HID varchar(128) NOT NULL,
                                        PRIMARY KEY (ID),
                                        FOREIGN KEY (UID) REFERENCES Users(UID),
                                        FOREIGN KEY (HID) REFERENCES Users(UID),
                                        CONSTRAINT UIDHID UNIQUE (UID,HID)
                                    );"""
        # create empty table containing user credentials if it does not exist
        self.cursor.execute(create_user_table_query)                            
        # create empty table containging data if it does not exist
        self.cursor.execute(create_data_table_query)
        # create empty table containging membership relations if it does not exist
        self.cursor.execute(create_membership_table_query)

    # listens to incomming requests
    def listen(self):
        self.s.listen(10)
        print("SERVER is listening for requests.")
        while(True):
            connection, address = self.s.accept()
            # first receive the size of the data the client is going to send
            size = struct.unpack('!I', connection.recv(4))[0]
            # receive the real data
            request = pickle.loads(connection.recv(size))
            try:
                # do request and prepare response
                if(request['type'] == "INSERT"):
                    return_message = pickle.dumps(self.insert(request['target'], request['source'], request['Pass'], request['Data']))
                    message = struct.pack('!BI', 1, len(return_message)) + return_message
                elif(request['type'] == "REQUEST"):
                    Data = pickle.dumps(self.request())
                    message = struct.pack('!BI', 1, len(Data)) + Data
                else:
                    error_message = pickle.dumps("Command not recognized.")
                    message = struct.pack('!BI', 0, len(error_message)) + error_message
            except:
                error_message = pickle.dumps("Error.")
                message = struct.pack('!BI', 0, len(error_message)) + error_message
            connection.send(message)
        self.s.close()

    # inserts entry into Membership table
    # NOTE: In this step the server learns the ID of the patient and the ID of the other party
    def insert(self, UID, HID, Pass, Data):
        authenticate_query = "SELECT * FROM Users WHERE UID = '%s' AND Pass = '%s'" % (HID, Pass)
        get_membership_query = "SELECT * FROM Membership WHERE UID = '%s' AND HID = '%s'" % (UID, HID)
        try:
            insert_data_query = "INSERT INTO Data (UID, Data) VALUES ('%s', '%s')" % (UID, Data)
            # authenticate user
            self.cursor.execute(authenticate_query)
            if(self.cursor.fetchone() != None):
                # if the UID and HID do not match UID has to be member of HID
                if(UID != HID):
                    self.cursor.execute(get_membership_query)
                    if(self.cursor.fetchone() == None):
                        return "NOT IN MEMBERSHIP TABLE"
                self.cursor.execute(insert_data_query)
                self.db.commit()
            else:
                return "INSERT FAILED"
        except:
            print("Person is not a member or SQL error")
            raise
        return "INSERT SUCCES"

    # obtains all health data from the database
    def request(self):
        get_data_query = "SELECT Data FROM Data"
        try:
            self.cursor.execute(get_data_query)
            results = self.cursor.fetchall()
        except:
            print("Could not fetch results")
            raise
        return results

# executes server locally on port 12345
def main():
    server = Server("localhost", 12345)

if __name__ == "__main__":
    main()
