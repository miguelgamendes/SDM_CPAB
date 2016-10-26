import pymysql.cursors
import socket
import sys

class Server:
    
    def __init__(self, hostname, port):
        print("Hostname:\n ", hostname, "\nPort:\n ", port, "\n")
        # setup database
        self.hostname = hostname
        self.port = port
        try:
            self.db = pymysql.connect("localhost","root","","SDM")
            self.cursor = self.db.cursor()
        except Exception as e:
            raise e
        self.create_tables()
        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.hostname, self.port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
        self.listen()

    def create_tables(self):
        create_data_table_query = """CREATE TABLE IF NOT EXISTS Data ( 
                                        ID int NOT NULL AUTO_INCREMENT,
                                        PID int NOT NULL,
                                        Data varchar(4096) NOT NULL,
                                        PRIMARY KEY (ID)
                                    );"""
        create_membership_table_query = """CREATE TABLE IF NOT EXISTS Membership ( 
                                        ID int NOT NULL AUTO_INCREMENT,
                                        PID int NOT NULL,
                                        CID int NOT NULL,
                                        PRIMARY KEY (ID),
                                        CONSTRAINT PIDCID UNIQUE (PID,CID)
                                    );"""
        # create empty table containging data if it does not exist
        self.cursor.execute(create_data_table_query)
        # create empty table containging data if it does not exist
        self.cursor.execute(create_membership_table_query)

    def listen(self):
        self.s.listen(10)
        print("TTP is listening for requests.")
        while(True):
            connection, address = self.s.accept()
            request = connection.recv()
            if(request.type == "INSERT"):
                self.insert(request.ID, request.CID, request.Data)
                connection.send("INSERT SUCCES")
            elif(request.type == "REQUEST"):
                results = self.request(request.ID)
                connection.send(results)
            else:
                connection.send("Command not recognized.")

    def insert(self, ID, CID, Data):
        get_membership_query = "SELECT * FROM Membership WHERE PID = '%i' AND CID = '%i'" % (ID, CID)
        try:
            insert_data_query = "INSERT INTO Data (PID, Data) VALUES ('%i', '%s')" % (ID, Data)
            # person inserts own data
            if(ID == CID):
                self.cursor.execute(insert_data_query)
            # person has to be a member of company
            else:
                self.cursor.execute(get_membership_query)
                result = cursor.fetchone()
                if(result[1] == ID and result[2] == CID):
                    self.cursor.execute(insert_data_query)
        except:
           print("Person is not a member or SQL error")

    def request(self, ID):
        get_data_query = "SELECT * FROM Data WHERE PID = '%i'" % ID
        try:
            self.cursor.execute(get_data_query)
            results = cursor.fetchall()
        except:
            print("Could not fetch or send results")
        return results


def main():
    server = Server("localhost", 12345)

if __name__ == "__main__":
    main()
