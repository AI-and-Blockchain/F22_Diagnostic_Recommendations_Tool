import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

def fund_account():
    pass

# create an account (hospital/node)

def generate_hospital_node():
    pass #remove later
    private_key, address = account.generate_account() # must have min balance of 100,000 micoalgos

    testing = str(address)
    print(testing)
    # information for hospital to maintain 
    print("New Hospital Account:")
    print("address: {}".format(address))
    print("private key: {}".format(private_key))
    print("passphrase: {}".format(mnemonic.from_private_key(private_key)))
    print()

    return private_key, address
    # fund each account in the main statement 
    # add the model to each hospital node in the main statement 

# existing hospitals perform verification? or function that creates new account could have
# some sort of check for this
# NOTE for time being will be assumed that all hospital nodes that join have been verified
def validate_new_node():
    pass

def sendToCA():
    pass

