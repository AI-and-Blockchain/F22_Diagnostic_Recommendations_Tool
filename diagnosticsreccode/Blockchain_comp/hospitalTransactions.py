import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction
import pandas as pd

from diagnosticsreccode.MachineLearning_comp import run_model

# used to allow hospitals to send and update their patient data

def trainModel():
    pima_diabetes = pd.read_csv('data/hospital1.csv', index_col=0)
    transformedDF = run_model.transform_data(pima_diabetes)

    random_state = 30
    models = run_model.get_models()

    x_train, x_test, y_train, y_test = run_model.generate_train_test_split(transformedDF, 0.30)
    run_model.evaluate_model(models, x_train, y_train)

    for model in models:
        run_model.fit_and_predict_models(model, x_train, y_train, x_test, y_test)
    

def uploadPatientData():
    pass

# send patient data to model
def sendTransaction():
    pass

# revieve updates to patient data from model
def recieveTransaction():
    pass