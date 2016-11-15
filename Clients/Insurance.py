from User import User

# an insurance company, like the doctor, can only read data 
# when he has been granted explicit access by the user
# insurance companies cannot insert data
class Insurance(User):

    def __init__(self, ID):
    	# insurance companies cannot read TRAINING data
        attributes = {str(ID), "INSURANCE"}
        User.__init__(self, ID, attributes)

    def insert(self, Data):
        pass

    def retrieve(self):
        User.retrieve(self)
