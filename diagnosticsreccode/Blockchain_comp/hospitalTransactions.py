import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
import pandas as pd

<<<<<<< HEAD
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation
=======
import sys
sys.path.append('../')
>>>>>>> 12c9510dc6b7e715d31da4d7ee3b37c969f1aca1

from diagnosticsreccode.MachineLearning_comp import run_model


# train the model on singular hospital node
def trainModel():
    pima_diabetes = pd.read_csv('../data/hospital1.csv', index_col=0)
    transformedDF = run_model.transform_data(pima_diabetes)

    random_state = 30
    models = run_model.get_models()

    x_train, x_test, y_train, y_test = run_model.generate_train_test_split(transformedDF, 0.30)
    run_model.evaluate_model(models, x_train, y_train)

    for model in models:
        run_model.fit_and_predict_models(model, x_train, y_train, x_test, y_test)
    

def create_asset(public_key_from, private_key_from, public_key_to, from_hospital, to_hospital):
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
        sender=public_key_from,
        sp=params,
        total=100,
        default_frozen=False,
        unit_name="training_model",
        asset_name="hospital training model",
        manager=public_key_from,
        reserve=public_key_from,
        freeze=public_key_from,
        clawback=public_key_from,
        url="https://testnet.algoexplorer.io/asset/hospitalModel", 
        decimals=3)
    # Sign with secret key of creator
    stxn = txn.sign(private_key_from)

    # Send the transaction to the network and retrieve the txid.
    txid = algod_client.send_transaction(stxn)
    print(txid)

    # Wait for the transaction to be confirmed
    wait_for_confirmation(algod_client, txid)

    try:
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
    except Exception as e:
        print(e)

# send training results of singular hospital node 
def uploadModelData():
    pass

def setUpTransaction(private_key, from_hospital, to_hospital):
    pass

# send training results of singular hospital node to another node
def sendTransaction(from_hospital, from_pk, from_sk, to_hospital, to_pk, to_sk, asset_id):
    # make sure all hospitals have done a basic initial transaction to set up a connection 

    # take the custom asset of the hospital and send it to the requested hospital
    try:
        params = algod_client.suggested_params()
        params.flat_fee = True
        params.fee = 1000

        # first have account B do an asset opt-in so it can revieve asset from A
        opt_in()

        # transaction B sends 10 algos to A
        txn_1 = transaction.PaymentTxn(from_hospital, params, to_hospital, 1000000) #amount is in microalgos 
        # transaction A sends 1 asset to B
        txn_2 = AssetTransferTxn(
                sender=from_pk,
                sp=params,
                receiver=to_pk,
                amt=1,
                index=asset_id)

        # get group id and assign it to transactions
        gid = transaction.calculate_group_id([txn_1, txn_2])
        txn_1.group = gid
        txn_2.group = gid

        # sign transactions
        stxn_1 = txn_1.sign(from_sk)    
        stxn_2 = txn_2.sign(to_sk)

        # assemble transaction group
        signed_group =  [stxn_1, stxn_2]
        tx_id = algod_client.send_transactions(signed_group)
        # wait for confirmation
        confirmed_txn = wait_for_confirmation(algod_client, tx_id, 4)
        print("txID: {}".format(tx_id), " confirmed in round: {}".format(
        confirmed_txn.get("confirmed-round", 0)))  

    except Exception as e:
        print(e)

    pass

# revieve updates to training model 
def recieveTransaction(data):
    pass