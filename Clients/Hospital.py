from User import User

# a hospital can insert health data
class Hospital(User):

    def __init__(self, ID):
        attributes = {str(ID), "HOSPITAL", "TRAINING"}
        User.__init__(self, ID, attributes)

    def insert(self, Data, TID):
        policy = "PATIENT and " + str(TID)
        User.insert(self, Data, policy, TID)

    def retrieve(self):
        User.retrieve(self)