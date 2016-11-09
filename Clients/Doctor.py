from User import User

# A doctor can only succesfully retrieve data
# if the user has given him explicit access in the access policy
# a doctor cannot insert data
class Doctor(User):

    def __init__(self, ID):
        # A doctor can also read TRAINING data
        attributes = {str(ID), "DOCTOR", "TRAINING"}
        User.__init__(self, ID, attributes)

    def insert(self, Data):
        raise

    def retrieve(self):
        User.retrieve(self)
