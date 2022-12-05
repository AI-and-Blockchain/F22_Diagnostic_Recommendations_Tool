import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

# used to determine which hospital specific data came from 
def initHospitalMap(cid):
    # use ipfs to trace cid hash to the data file and download

    # read through data file to determine which hospital data attached to 

    # return the hospital found 
    pass

def isExistsHospital(hospital_node):
    pass