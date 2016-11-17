install guide:

The code is written in python 3 and is dependend on the following dependencies:
- CharmCrypto
- PyCrypto
- PyPebel
- PyMySQL

These dependencies have to be installed before running the code.
The code has three programs:
- The server program in the Server directory, which stores the user data. Upon execution the server runs locally on port 12345.
- The TTP program in the TTP directory, which does key generation and distribution. Upon execution the TTP generates master keys and runs locally on port 12346.
- The client test program (test.py) which creates several users and shows a demonstration of the program. Each client communicates with the TTP to get the personal keys.

The server can be run with the command "python3 Server.py", the TTP can be run with the command "python3 TTP.py" and the test can be run with the command "python3 test.py".

To run the test properly the server database has to be initialized. There is a sql file in the Server directory called "setup.sql", this sql file does not create tables but imports data into the tables. It can be executed by the command "mysql -u root -p SDM < setup.sql", note that the credentials have to be setup properly (I used root without password).

This should be enough to run the program, if there are any problems please contact f.heikamp@student.utwente.nl

