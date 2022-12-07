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
import random
import requests
import json
import base64
from Blockchain_comp import createNewHospital, hospitalTransactions

# Purestake key setup to allow use of Algorand blockchain 
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Tfz0xEjItu9tEGD7PPCHu6dWVzkMICsE2Lbldptf"
headers = {"X-API-Key": algod_token,}
algod_client = algod.AlgodClient(algod_token, algod_address, headers)

# Connnect to AlgoExplorer API so that transaction information can be accessed locally
base_url = "https://algoindexer.testnet.algoexplorerapi.io/"


def get_byte_length(str):
    '''
    Return byte length of string
    '''
    return len(str.encode('utf-16'))

def get_corresponding_dataset(hospital_account):
    '''
    Return the split dataset partition that's accociated with the provided hospital account
    '''
    with open("../data/active_hospitals.txt") as f:
        lines = f.readlines()
    for line in lines:
        if hospital_account in line:
            #print(len(line))
            return line[148:len(line)-1]
    
def get_transaction_note(hospital_node):
    api_url = base_url + "/v2/accounts/" + hospital_node + "/transactions"
    print(api_url)
    response = requests.get(api_url)

    # single out the 'note' fields from the entire json string
    txn_note = response.json()['transactions'][0]['note']  
    
    # decode txn_note
    note = base64.b64decode(txn_note).decode()
    return note

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

    # assign a dataset to the generated hospital
    print("Data partition assigned: " + get_corresponding_dataset(str(address)))

    print("Hospital account created! Remember to fund your account with: https://bank.testnet.algorand.network/\n\n")

# put file in ipfs and store the hash in hospital node (make transaction with itself)
def send_patient_data(hospital_account, hospital_to, pk, data_file):
    '''
    Send a transaction with the patient statistics. Can be used as a way to store
    data on the blockchain (the to and from hospital accounts are the same) or as 
    a way to send another hospital information. 
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

def train_hospital_model(hospital_node, pk, data_file, pick_max, pick_other_node_model):
    '''
    This function can be called by a hospital operator when they 
    want to train their local model on the diabetes patients in their hospital
    '''
    model_result_str = hospitalTransactions.trainModel(data_file, pick_max, pick_other_node_model)
    print('Model choosen and result \n', model_result_str)
    print('Byte size ', get_byte_length(model_result_str))

    # need to store the results of the trained model --> send transaction from account to itself
    hospitalTransactions.sendTransaction(hospital_node, hospital_node, pk, model_result_str)


def send_model_performance(from_hospital, to_hospital, private_key):
    '''
    Function accesses the from_hospital account transactions, finding the most recent
    model updata data. That data is then sent via another transaction to the to_hospital 
    account node. 

    Assumptions: train_model has been run on from_hospital data at least once
    '''
    # get most recent transaction (train_model results)
    model_results = get_transaction_note(from_hospital)
    # forward those model results to another hospital account
    hospitalTransactions.sendTransaction(from_hospital, to_hospital, private_key, model_results)

def vote_hospital_leader():
    '''
    Function used in conjunction with share_update(). Used to vote in the
    lead hospital node that the remaining nodes will send model updates to. 
    '''
    hospital_lead_node_num = random.randint(1,5)
    with open("../data/active_hospitals.txt") as f:
        hospitals_info = f.readlines()
    
    # assign account node the lead value
    hospital_lead_node = (hospitals_info[hospital_lead_node_num])[:58]
    return hospital_lead_node

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
    lead_node = vote_hospital_leader()

    # Lead node requests model data from other hospitals
    with open("../data/active_hospitals.txt") as f:
        hospitals_info = f.readlines()
    
    for hospital_line in hospitals_info:
        hospital_node = hospital_line[:58]
        hospital_pk = hospital_line[58:146]    #length: 88
        if(hospital_node != lead_node):
            send_model_performance(hospital_node, lead_node, hospital_pk)

    # Lead node aggregates model data and does something with it

    # Lead node sends updates to all participating hospital nodes 
    for hospital_line in hospitals_info:
        hospital_node = hospital_line[:58]
        # send that data aggrregate to each node (including lead node)
    return

def reset_active_hospitals():
    file = open('../data/active_hospitals.txt', 'w')
    file.write('0\n')
    file.close()

if __name__ == '__main__':
    #get_transaction_note("6BTW2JU3WCFYMXHP7UECGXLMNVPKBYGRKBZFKBGPUZFEKI5ZTT3UDHBO6M")
    
    # default message printed to allow user to choose options
    user_response = input("Welcome to the diabetes diagnostic tool! Select one of the following: \n\n" +
                                "[1] Register hospital node\n" +
                                "[2] Send patient statistics\n" +
                                "[3] Print patient statistics\n" +
                                "[4] Train hospital model\n" +
                                "[5] Send model performance\n" + 
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
            hospital_to = input("Enter hospital node account to send data to: ")
            private_key = input("Enter private key: ")
            data_file = get_corresponding_dataset(hospital_node)

            send_patient_data(hospital_node, hospital_to, private_key, data_file)

        elif(user_response == "3"):     # print patient statistics
            hospital_node = input("Enter hospital node account number: ")
            # print statistic from the given hospital 
            data_file = get_corresponding_dataset(hospital_node)
            print_patient_statistics(data_file)

        elif(user_response == "4"):     # train model 
            hospital_node = input("Enter hospital node account number: ")
            pk = input("Enter private key: ")
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
            train_hospital_model(hospital_node, pk, data_file, max_option, int(pick_other_node_model))
        
        elif(user_response == "5"):
            hospital_node = input("Enter hospital node account number: ")
            hospital_to = input("Ender hospital node account to send model update to: ")
            private_key = input("Enter private key: ")
            send_model_performance(hospital_node, hospital_to, private_key)

        elif(user_response == "6"):     # share updates with federated leaning 
            print(6)

        else: 
            print("Not a valid selection. Plesae try again.\n\n")

        user_response = input("Select any additional options to perform: \n\n" +
                                "[1] Register hospital node\n" + 
                                "[2] Send patient statistics\n" +
                                "[3] Print patient statistics\n" +
                                "[4] Train hospital model\n" +
                                "[5] Send model performance\n" +
                                "[6] Share model updates\n" +
                                "[0] exit\n" +
                                "\nselect: ")
