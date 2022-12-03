import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation

## custom asset will the the training model with updates being sent to and from hospitals 

# general algorand transaction info 
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)
params = algod_client.suggested_params()
params.fee = 1000
params.flat_fee = True

# Creating model asset
txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    total=100,
    default_frozen=False,
    unit_name="",
    asset_name="",
    manager=accounts[1]['pk'],
    reserve=accounts[1]['pk'],
    freeze=accounts[1]['pk'],
    clawback=accounts[1]['pk'],
    url="https://testnet.algoexplorer.io/asset/aiblockasset", 
    decimals=3)
# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print(txid)

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client, txid)

try:
    # Pull account info for the creator
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
except Exception as e:
    print(e)