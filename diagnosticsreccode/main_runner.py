# 
# let hospital register node on blockchain --> check if already exists 
#       creates association with patient data file --> hash 
# train model 
# get patient statistics (from the hash)
# share updates with federated learning 
#   print output 

from Blockchain_comp import createNewHospital


def register_hospital_node():
    node_file = open("active_hospitals.txt")                            #add that hospital to the active hospital nodes file
    private_key, address = createNewHospital.generate_hospital_node()   #generate blockchain node/address for hospital
    node_file.write(address + '\n')
    node_file.close()

def print_patient_statistics():
    pass

def train_hospital_model():
    createNewHospital.trainModel()

def share_updates():
    pass

if __name__ == '__main__':
    # default message printed to allow user to choose options
    user_response = input("Welcome to the diabetes diagnostic tool! Select one of the following: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[2] Print patient statistics\n" +
                                "[3] Train hospital model\n" +
                                "[4] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")
    while(True):
        if(user_response == "0"): break
        elif(user_response == "1"):     # register a hospital
            # ask if user has a public key already, if not register and return key
            register_hospital_node()
        elif(user_response == "2"):     # print patient statistics
            print(2)
        elif(user_response == "3"):     # train model 
            print(3)
        elif(user_response == "4"):     # share updates with federated leaning 
            print(4)
        else: print("Not a valid selection. Plesae try again.\n\n")

        user_response = input("Select any additional options to perform: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[2] Print patient statistics\n" +
                                "[3] Train hospital model\n" +
                                "[4] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")