import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

'''
This file is intended to be used if IPFS is adopted into the architecture. 
The two functions are set up to recieve the cid (path to stored files) and verify
who owns the node storing it. 
'''

# create a mapping of which hospital node contains what data
def initHospitalMap(cid):
    # use ipfs to trace cid hash to the data file and download

    # read through data file to determine which hospital data attached to 

    # return the hospital found 
    pass

# used to determine if requested data exists in a hospital node
def isExistsHospital(hospital_node):
    pass