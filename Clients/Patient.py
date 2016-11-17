from User import User

class Patient(User):

    # insertion_key is used to insert data for the patient
    # doctor_id specifies the doctor for this patient
    # doctor_key is the shared key between user
    def __init__(self, ID, insertion_key):
        # patient can also read TRAINING data
        attributes = {str(ID), "PATIENT", "TRAINING"}
        User.__init__(self, ID, attributes)
        self.insertion_key = insertion_key

    # inserts data into the server
    def insert(self, Data, training = False, doctor_id = -1, insurance_id = -1, employer_id = -1):
        policy = ""
        # if it is training data, specify TRAINING attribute
        if(training):
            policy += "TRAINING and ("
        policy += "(PATIENT and " + str(self.ID) + ")"
        if(doctor_id != -1):
            policy += " or (DOCTOR and " + str(doctor_id) + ")"
        if(insurance_id != -1):
            policy += " or (INSURANCE and " + str(insurance_id) + ")"
        if(doctor_id != -1):
            policy += " or (EMPLOYER and " + str(employer_id) + ")"
        if training:
            policy += ")"
        User.insert(self, Data, policy, self.ID, self.insertion_key)

    def retrieve(self):
        User.retrieve(self)
