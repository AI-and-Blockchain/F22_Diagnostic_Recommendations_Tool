# 
# let hospital register node on blockchain --> check if already exists 
#       creates association with patient data file --> hash 
# train model 
# get patient statistics (from the hash)
# share updates with federated learning 
#   print output 
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Tfz0xEjItu9tEGD7PPCHu6dWVzkMICsE2Lbldptf"
headers = {"X-API-Key": algod_token,}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)


from Blockchain_comp import createNewHospital
from Blockchain_comp import hospitalTransactions

def get_byte_length(str):
    '''
    return byte length of string
    '''
    return len(str.encode('utf-16'))

def get_corresponding_dataset(hospital_account):
    with open("../data/active_hospitals.txt") as f:
        lines = f.readlines()
    for line in lines:
        if hospital_account in line:
            print(len(line))
            return line[148:len(line)-1]
    

def register_hospital_node():
    '''
    First line in file denotes how many active hospital nodes exist, default 0
    Each line contains the address and public key of the hospital node.
    For this example there can only be a maximum of 5 hospital nodes so any additional
    generation requests will be ignored. 
    '''

    # First update the number of active hospitals 
    node_file = open('../data/active_hospitals.txt')
    num_hospitals = int(node_file.readline())
    new_num = num_hospitals + 1

    if(new_num > 5):
        print("Data currently split amongst 5 hospital nodes. Cannot split further.")
        return

    with open("../data/active_hospitals.txt") as f:
        lines = f.readlines()
    lines[0] = str(new_num) + "\n"
    with open("../data/active_hospitals.txt", "w") as f:
        f.writelines(lines)

    # Update file with hospital address and public key 
    node_file = open('../data/active_hospitals.txt', 'a')                       #add that hospital to the active hospital nodes file
    private_key, address = createNewHospital.generate_hospital_node()           #generate blockchain node/address for hospital
    
    # Assign hospital account a section of the data set depending on which of the 5 hospital nodes it is
    data_set_part = "hospital" + str(new_num) + ".csv"

    hospital_info = str(address) + " " + str(private_key) + " " + data_set_part + "\n"
    node_file.write(hospital_info)
    
    node_file.close()

    # TO DO assign a dataset to the generated hospital
    print(get_corresponding_dataset(str(address)))

    print("Hospital account created! Remember to fund your account with: https://bank.testnet.algorand.network/")

# put file in ipfs and store the hash in hospital node (make transaction with itself)
def upload_patient_data(hospital_account, pk, data_file):
    '''
    Send a transaction from an account to itself to store the patient data it's has
    '''
    patient_stats = hospitalTransactions.printPatientStatistics(data_file)
    hospitalTransactions.sendTransaction(hospital_account, hospital_account, pk, patient_stats)

def print_patient_statistics(data_file):
    '''
    Meant to be a function that a hospital calls to check on the distribution of values of the diabetes patients
    '''
    patientStats = hospitalTransactions.printPatientStatistics(data_file)
    print('Patient statistics at hospital \n', patientStats)
    print('Byte size ', get_byte_length(patientStats))

def train_hospital_model(data_file, pick_max, pick_other_node_model):
    '''
    This function can be called by a hospital operator when they 
    want to train their local model on the diabetes patients in their hospital
    '''
    model_result_str = hospitalTransactions.trainModel(data_file, pick_max, pick_other_node_model)
    print('Model choosen and result \n', model_result_str)
    print('Byte size ', get_byte_length(model_result_str))

def share_updates():
    '''
    Intended to connect to a federated learning implementation that would take 
    the registered hospital nodes, determine the iterations lead node, and share
    all model data with that lead node. The lead node would aggregate the model data
    in some way and return model updates. Without federated learning, that implementation
    is replecated with simple blockchain transactions. 
    '''
    # Assumed that at this point, all 5 hospital nodes have been created and trained their individual models
    # Determine the lead hospital node

    # Lead node requests model data from other hospitals

    # Lead node aggregates model data 

    # Lead node sends updates to all participating hospital nodes 

    pass

if __name__ == '__main__':
    # default message printed to allow user to choose options
    user_response = input("Welcome to the diabetes diagnostic tool! Select one of the following: \n\n" +
                                "[1] Register hospital node\n" +
                                "[2] Upload patient statistics\n" +
                                "[3] Print patient statistics\n" +
                                "[4] Train hospital model\n" +
                                "[5] Get model performance\n" + 
                                "[6] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")
    while(True):
        if(user_response == "0"): 
            break

        elif(user_response == "1"):     # register a hospital
            # ask if user has a public key already, if not register and return key
            register_hospital_node()
        
        elif(user_response == "2"):
            hospital_node = input("Enter hospital node account number: ")
            private_key = input("Enter private key: ")
            data_file = get_corresponding_dataset(hospital_node)

            upload_patient_data(hospital_node, private_key, data_file)

        elif(user_response == "3"):     # print patient statistics
            hospital_node = input("Enter hospital node account number: ")
            # print statistic from the given hospital 
            data_file = get_corresponding_dataset(hospital_node)
            print_patient_statistics(data_file)

        elif(user_response == "4"):     # train model 
            hospital_node = input("Enter hospital node account number: ")
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

            # need to pick data file here of active hospital - for now choosing hospital2
            data_file = get_corresponding_dataset(hospital_node)
            train_hospital_model(data_file, max_option, int(pick_other_node_model))

        elif(user_response == "5"):     # share updates with federated leaning 
            print(5)

        else: 
            print("Not a valid selection. Plesae try again.\n\n")

        user_response = input("Select any additional options to perform: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[2] Upload patient statistics\n" +
                                "[3] Print patient statistics\n" +
                                "[4] Train hospital model\n" +
                                "[5] Get model performance\n" +
                                "[6] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")
