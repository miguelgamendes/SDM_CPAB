# insert users
# all values are sha512 hashed so the server does not learn passwords and id's
# the server is able to authenticate though
INSERT INTO Users (UID, Pass) VALUES (SHA2('1', 512), SHA2('pass1', 512))
INSERT INTO Users (UID, Pass) VALUES (SHA2('2', 512), SHA2('pass2', 512))
INSERT INTO Users (UID, Pass) VALUES (SHA2('9', 512), SHA2('pass3', 512))
INSERT INTO Users (UID, Pass) VALUES (SHA2('10', 512), SHA2('pass4', 512))
INSERT INTO Users (UID, Pass) VALUES (SHA2('11', 512), SHA2('pass5', 512))
INSERT INTO Users (UID, Pass) VALUES (SHA2('12', 512), SHA2('pass6', 512))
# insert relations between clients and hostpitals/healthclubs
INSERT INTO Membership (UID, HID) VALUES(SHA2('1', 512), SHA2('9', 512))
INSERT INTO Membership (UID, HID) VALUES(SHA2('1', 512), SHA2('11', 512))
INSERT INTO Membership (UID, HID) VALUES(SHA2('1', 512), SHA2('12', 512))
INSERT INTO Membership (UID, HID) VALUES(SHA2('2', 512), SHA2('11', 512))