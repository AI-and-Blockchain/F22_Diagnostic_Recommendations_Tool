import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
import pandas as pd

from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation
import sys
sys.path.append('../')

from diagnosticsreccode.MachineLearning_comp import run_model

def printPatientStatistics(data_file):
	patient_data = pd.read_csv('../data/' + data_file, index_col=0)

	numeric_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
	   'BMI', 'Age', 'Pregnancies']
	mean_std = {}

	for col in numeric_columns:
		mean_std[col] = {'mean': round(patient_data[col].mean(),2), 'standard deviation': round(patient_data[col].std(), 2)}

	outcome_count = {}
	outcome_count['Diabetes'] = len(patient_data[patient_data['Outcome'] == 0])
	outcome_count['No Diabetes'] = len(patient_data[patient_data['Outcome'] == 1])

	print('Column' + ' ' + 'Mean' + ' ' + 'Standard Deviation')

	for col in mean_std.keys():
		print(col + ' ' + str(mean_std[col]['mean']) + ' ' + str(mean_std[col]['standard deviation']))

	print('Outcome ' + ' ' + 'Count')
	print('Diabetes' + ' ' + str(outcome_count['Diabetes']))
	print('No Diabetes' + ' ' + str(outcome_count['No Diabetes']))

	#need to save this to IPFS
	return (mean_std, outcome_count)


# train the model on singular hospital node
def trainModel(pick_max, pick_other_node_model):
	#pass #remove later
	#needs to be changed to calling hospital data of registered node
	pima_diabetes = pd.read_csv('../data/hospital2.csv', index_col=0)
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
	print(transact_out)
	#this will need to be replaced with saving to ipfs
	return transact_out
	

def create_asset(public_key_from, private_key_from, public_key_to, from_hospital, to_hospital):
	pass

# send training results of singular hospital node 
def uploadModelData(pick_max, default_model):
	pass

def setUpTransaction(private_key, from_hospital, to_hospital):
	pass

# send training results of singular hospital node to another node
def sendTransaction(from_hospital, from_pk, from_sk, to_hospital, to_pk, to_sk, asset_id):
	#obtains the needed parameters from the model and store in ipfs
	#save ipfs address by sending transaction to yourself with it in the notes
	pass

def setUpTransaction(private_key, from_hospital, to_hospital):
	#initial transaction of 0 eth to ensure hospital nodes can communicate to one another
	pass

# send training results of singular hospital node to another node
def sendTransaction(from_hospital, from_pk, from_sk, to_hospital, to_pk, to_sk, asset_id):
	#send the ipfs address to the requested hospital node 
	pass

# revieve updates to training model 
def recieveTransaction(data):
	pass


if __name__ == '__main__':
	trainModel(False, 2)