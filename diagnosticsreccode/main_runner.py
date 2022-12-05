# 
# let hospital register node on blockchain --> check if already exists 
#       creates association with patient data file --> hash 
# train model 
# get patient statistics (from the hash)
# share updates with federated learning 
#   print output 

from Blockchain_comp import createNewHospital
from Blockchain_comp import hospitalTransactions

def register_hospital_node():
    node_file = open('active_hospitals.txt', 'w')                       #add that hospital to the active hospital nodes file
    private_key, address = createNewHospital.generate_hospital_node()   #generate blockchain node/address for hospital
    node_file.write(str(address))
    node_file.write('\n')
    node_file.close()

# put file in ipfs and store the hash in hospital node (make transaction with itself)
def upload_patient_data(file, hospital_account):
    pass

def print_patient_statistics(data_file):
    hospitalTransactions.printPatientStatistics(data_file)

def train_hospital_model(pick_max, pick_other_node_model):
    hospitalTransactions.trainModel(pick_max, pick_other_node_model)

def share_updates():
    pass

if __name__ == '__main__':
    # default message printed to allow user to choose options
    user_response = input("Welcome to the diabetes diagnostic tool! Select one of the following: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[ ] Upload patient statistics\n" +
                                "[2] Print patient statistics\n" +
                                "[3] Train hospital model\n" +
                                "[4] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")
    while(True):
        if(user_response == "0"): 
            break

        elif(user_response == "1"):     # register a hospital
            # ask if user has a public key already, if not register and return key
            register_hospital_node()

        elif(user_response == "2"):     # print patient statistics
            print_patient_statistics('hospital2.csv')

        elif(user_response == "3"):     # train model 
            pick_max = input("pick max, enter True to choose max model and False to explicitly choose a model ")
            max_option = eval(pick_max)
            print(max_option)

            #if user said they want to choose a model, allow them to do so
            if not max_option:
                pick_other_node_model = input("pick other node model: \n   " +
                "1. Logistic Regression \n" +
                "2. Decision Tree \n" +
                "3. Random Forest \n")
            else:
                pick_other_node_model = 0

            train_hospital_model(max_option, int(pick_other_node_model))

        elif(user_response == "4"):     # share updates with federated leaning 
            print(4)

        else: 
            print("Not a valid selection. Plesae try again.\n\n")

        user_response = input("Select any additional options to perform: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[2] Print patient statistics\n" +
                                "[3] Train hospital model\n" +
                                "[4] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")