from User import User

# a health club can insert TRAINING data for a patient
# who is a member of the health club
class Healthclub(User):

    def __init__(self, ID):
        attributes = {str(ID), "HEALTHCLUB", "TRAINING"}
        User.__init__(self, ID, attributes)

    # inserts data for a given ID, ID has to be a member of the healthclub
    def insert(self, Data, TID):
    	# policy indicates that it can only be decrypted if you are a patient with ID and
    	# that it is TRAINING related data
        policy = "TRAINING and (PATIENT and " + str(TID) + ")"
        User.insert(self, Data, policy, TID)

    def retrieve(self):
        User.retrieve(self)