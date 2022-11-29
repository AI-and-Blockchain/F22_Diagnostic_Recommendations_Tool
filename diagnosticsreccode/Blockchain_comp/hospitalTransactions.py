import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

import sys
sys.path.append('../')

from code.MachineLearning_comp import run_model

# used to allow hospitals to send and update their patient data

def trainModel():
    pima_diabetes = pd.read_csv('../../data/hospital1.csv', index_col=0)
    transformedDF = run_model.transform_data(pima_diabetes)

    random_state = 30
    models = [
        ['Logistic Regression', LogisticRegression(random_state = random_state, solver='liblinear')],
        ['Decision Tree',DecisionTreeClassifier(random_state = random_state)],
        ['Random Forest', RandomForestClassifier(random_state = random_state)],
    ]

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