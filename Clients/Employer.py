from User import User

# employer can only read data if given explicit access
class Employer(User):

    def __init__(self, ID):
    	# employer cannot read TRAINING data
        attributes = {str(ID), "EMPLOYER"}
        User.__init__(self, ID, attributes)

    def insert(self, Data):
        pass

    def retrieve(self):
        User.retrieve(self)