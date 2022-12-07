import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

def fund_account():
    pass

# create an account (hospital/node)
def generate_hospital_node():
    private_key, address = account.generate_account() # must have min balance of 100,000 micoalgos
    
    # information for hospital to maintain 
    print("New Hospital Account:")
    print("address: {}".format(address))
    print("private key: {}".format(private_key))
    print("passphrase: {}".format(mnemonic.from_private_key(private_key)))
    print()

    return private_key, address

# FOR FUTURE in event we cannot assume registering hospitals are valid
def validate_new_node():
    pass

# FOR FUTURE in event we cannot assume registering hospitals are valid
def sendToCA():
    pass

