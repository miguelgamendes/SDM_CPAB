# Patient: [id], [type] :
# Encypt: id = patient_id [\/ (type = Doctor /\ id = doctor_id) 
#                          \/ (type = Insurance /\ id = insurance_id) 
#                          \/ (type = Employer /\ id = employer_id) 
#]
# --------------------------
# Doctor: [id], [type]
# Insurance: [id], [type]
# Health Club: [id], [type]
# Employer: [id], [type]
# Hospital: [id], [type] 

from User import User

class Patient(User):

    def __init__(self, ID):
        # patient can also read TRAINING data
        attributes = {str(ID), "PATIENT", "TRAINING"}
        User.__init__(self, ID, attributes)

    # inserts data into the server
    def insert(self, Data, training = False, doctor_id = -1, insurance_id = -1, employer_id = -1):
        policy = ""
        # if it is training data, specify TRAINING attribute
        if training:
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
        User.insert(self, Data, policy, self.ID)

    def retrieve(self):
        User.retrieve(self)
