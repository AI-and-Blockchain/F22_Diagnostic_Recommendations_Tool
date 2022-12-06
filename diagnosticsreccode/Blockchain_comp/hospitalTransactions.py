import json
import base64
import pandas as pd
import sys
sys.path.append('../')
from algosdk.v2client import algod
from algosdk import mnemonic, constants, account
from algosdk.future import transaction

algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "Tfz0xEjItu9tEGD7PPCHu6dWVzkMICsE2Lbldptf"
headers = {
   "X-API-Key": algod_token,
}

algod_client = algod.AlgodClient(algod_token, algod_address, headers)


from diagnosticsreccode.MachineLearning_comp import run_model

def printPatientStatistics(data_file):
	patient_data = pd.read_csv('../data/' + data_file, index_col=0)

	numeric_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
	   'BMI', 'Age', 'Pregnancies']
	mean_std = {}

	for col in numeric_columns:
		mean_std[col] = {'mean': round(patient_data[col].mean(),2), 'standard deviation': round(patient_data[col].std(), 2)}

	outcome_count = {}
	outcome_count['Diabetes'] = {'count': len(patient_data[patient_data['Outcome'] == 0])}
	outcome_count['No Diabetes'] = {'count': len(patient_data[patient_data['Outcome'] == 1])}

	#commenting below for printing

	# print('Column' + ' ' + 'Mean' + ' ' + 'Standard Deviation')

	# for col in mean_std.keys():
	# 	print(col + ' ' + str(mean_std[col]['mean']) + ' ' + str(mean_std[col]['standard deviation']))

	# print('Outcome ' + ' ' + 'Count')
	# print('Diabetes' + ' ' + str(outcome_count['Diabetes']))
	# print('No Diabetes' + ' ' + str(outcome_count['No Diabetes']))

	#passing a string 
	return json.dumps(mean_std) +  '\n' + json.dumps(outcome_count)


# train the model on singular hospital node
def trainModel(data_file, pick_max, pick_other_node_model):
	#pass #remove later
	#needs to be changed to calling hospital data of registered node
	pima_diabetes = pd.read_csv('../data/' + data_file, index_col=0)
	transformedDF = run_model.transform_data(pima_diabetes)

	random_state = 30

	if pick_max:
		#if pick max then run all models and store the one with the best accuracy
		models = run_model.get_model(0)
	if pick_other_node_model >= 1 and pick_other_node_model <= 3:
		models = run_model.get_model(pick_other_node_model)

	x_train, x_test, y_train, y_test = run_model.generate_train_test_split(transformedDF, 0.30)
	#run_model.evaluate_model(models, x_train, y_train)

	model_output = {}

	for mod_num in models.keys():
		model = models[mod_num]

		mod_classification_report = run_model.fit_and_predict_model(mod_num, model, x_train, y_train, x_test, y_test)
		model_output[mod_num] = mod_classification_report

	#print(model_output)
	transact_out = run_model.get_model_output(model_output, pick_max, pick_other_node_model)
	#print(transact_out)
	#passing string
	return json.dumps(transact_out)
	
# upload the model date of current hospital to ipfs
def uploadModelData(from_hospital, model_data):
    # need ipfs working 
	pass

def fund_account(hospital_node, private_key):
    pass

# initial transaction of 0 eth to ensure hospital nodes can communicate to one another
def setUpTransaction(from_hospital, to_hospital, from_pk):

    print("My address: {}".format(from_hospital))
    account_info = algod_client.account_info(from_hospital)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    receiver = str(from_hospital)
    amount = 0
    note = "transaction setup".encode()
    unsigned_txn = transaction.PaymentTxn(from_hospital, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(from_pk)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 


    account_info = algod_client.account_info(from_hospital)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# send training results of singular hospital node to another node
def sendTransaction(from_hospital, to_hospital, from_pk, cid):
    #TO DO: obtain the ipfs cid 

    print("My address: {}".format(from_hospital))
    account_info = algod_client.account_info(from_hospital)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    receiver = str(to_hospital)
    amount = 0
    note = str(cid).encode()
    unsigned_txn = transaction.PaymentTxn(from_hospital, params, receiver, amount, None, note)

    # sign transaction
    signed_txn = unsigned_txn.sign(from_pk)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
    print("Amount transfered: {} microAlgos".format(amount) )    
    print("Fee: {} microAlgos".format(params.fee) ) 

    account_info = algod_client.account_info(from_hospital)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

# revieve updates to training model 
def recieveTransaction(data):
	pass


if __name__ == '__main__':
	trainModel(False, 2)
    