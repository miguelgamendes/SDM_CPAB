from User import User

# a hospital can insert health data
class Hospital(User):

    def __init__(self, ID, insertion_key):
        attributes = {str(ID), "HOSPITAL", "TRAINING"}
        User.__init__(self, ID, attributes)
        self.insertion_key = insertion_key

    def insert(self, Data, TID):
        policy = "PATIENT and " + str(TID)
        User.insert(self, Data, policy, TID, self.insertion_key)

    def retrieve(self):
        pass