import os
import sys
sys.path.append("Clients")
 
from Patient import Patient
from Doctor import Doctor
from Insurance import Insurance
from Employer import Employer
from Healthclub import Healthclub
from Hospital import Hospital

class Test:

    # setup clients, each client has a unique ID and the ID is used as an attribute
    patient1 = Patient(1, "pass1")
    patient2 = Patient(2, "pass2")
    doctor1 = Doctor(3)
    doctor2 = Doctor(4)
    insurance1 = Insurance(5)
    insurance2 = Insurance(6)
    employer1 = Employer(7)
    employer2 = Employer(8)
    healthclub1 = Healthclub(9, "pass3")
    healthclub2 = Healthclub(10, "pass4")
    hospital1 = Hospital(11, "pass5")
    hospital2 = Hospital(12, "pass6")

    def __init__(self):
        self.run()

    def retrieve_all(self):
        print("\n\npatient 1:\n")
        self.patient1.retrieve()
        print("\n\npatient 2:\n")
        self.patient2.retrieve()
        print("\n\ndoctor 1:\n")
        self.doctor1.retrieve()
        print("\n\ndoctor 2:\n")
        self.doctor2.retrieve()
        print("\n\ninsurance company 1:\n")
        self.insurance1.retrieve()
        print("\n\ninsurance company 2:\n")
        self.insurance2.retrieve()
        print("\n\nemployer 1:\n")
        self.employer1.retrieve()
        print("\n\nemployer 2:\n")
        self.employer2.retrieve()
        print("\n\nhealth club 1:\n")
        self.healthclub1.retrieve()
        print("\n\nhealth club 2:\n")
        self.healthclub2.retrieve()
        print("\n\nhospital 1:\n")
        self.hospital1.retrieve()
        print("\n\nhospital 2:\n")
        self.hospital2.retrieve()

    def run(self):
        # patient insertions
        self.patient1.insert("This message is only readable by patient 1.")
        self.patient1.insert("This message is readable by patient 1, doctor 2, insurance 1 and employer 1.", False, 4, 5, 7)
        self.patient2.insert("This message is readable by patient 2 and doctor 1.", False, 3)
        # employer1 has no TRAINING attribute so cannot read
        self.patient2.insert("This message is readable by patient 2 and doctor 1.", True, 3, -1, 7)
        # check retrieval should match messages specified above
        self.retrieve_all()
        # healthclub insertions
        # patient 1 is member of healthclub 1
        # patient 2 is a non-member
        self.healthclub1.insert("This message is only readable by patient 1", 1)
        self.healthclub1.insert("This message should not be inserted", 2)
        self.healthclub2.insert("This message should not be inserted", 1)
        self.healthclub2.insert("This message should not be inserted", 2)
        self.retrieve_all()
        # hospital insertions
        # patient 1 is a member of both hospital 1 and 2
        # patient 2 is a member of hospital 1
        self.hospital1.insert("This message is only readable by patient 1", 1)
        self.hospital1.insert("This message is only readable by patient 2", 2)
        self.hospital2.insert("This message is only readable by patient 1", 1)
        self.hospital2.insert("This message should not be inserted", 2)
        self.retrieve_all()

# clear database before executing test.py
def main():    
    test = Test()

if __name__ == "__main__":
    main()
