import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # for data visualization
import matplotlib.pyplot as plt # to plot charts
from collections import Counter
import os

# Modeling
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, learning_curve, train_test_split
from sklearn.metrics import classification_report


def transform_data(df):
	'''
	generate a normalized dataframe for training
	'''
	q  = QuantileTransformer()
	X = q.fit_transform(pima_diabetes)
	transformedDF = q.transform(X)
	transformedDF = pd.DataFrame(X)
	transformedDF.columns = pima_diabetes.columns
	return transformedDF

#Separate train dataset and test dataset
def generate_train_test_split(transformedDF, test_size):
	features = transformedDF.drop(["Outcome"], axis=1)
	labels = transformedDF["Outcome"]
	x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.30, random_state=7)
	return x_train, x_test, y_train, y_test


def evaluate_model(models, x_train, y_train):
	"""
	Takes a list of models and returns chart of cross validation scores using mean accuracy
	"""
	
	# Cross validate model with Kfold stratified cross val
	kfold = StratifiedKFold(n_splits = 10)
	
	result = []
	for model in models :
		model_cv = cross_val_score(estimator = model[1], X = x_train, y = y_train, scoring = "accuracy", 
									  cv = kfold, n_jobs=4)
		result.append(model_cv)

	cv_means = []
	cv_std = []
	for cv_result in result:
		#print(cv_result)
		cv_means.append(cv_result.mean())
		cv_std.append(cv_result.std())

	result_df = pd.DataFrame({
		"CrossValMeans":cv_means,
		"CrossValerrors": cv_std,
		"Models":[m[0] for m in models]
	})

	# Generate chart
	bar = sns.barplot(x = "CrossValMeans", y = "Models", data = result_df, orient = "h")
	bar.set_xlabel("Mean Accuracy")
	bar.set_title("Cross validation scores")
	return result_df


def fit_and_predict_models(model, x_train, y_train, x_test, y_test):
	'''
	Function to train a model, test it and report F1, precision and recall on the test predictions
	'''
	model[1].fit(x_train, y_train)
	y_pred_model = model[1].predict(x_test)
	print('Model : ' + model[0])
	print(classification_report(y_test, y_pred_model))


if __name__ == '__main__':
	pima_diabetes = pd.read_csv('../../data/diabetes_val_corrected.csv', index_col=0)
	transformedDF = transform_data(pima_diabetes)

	random_state = 30
	models = [
		['Logistic Regression', LogisticRegression(random_state = random_state, solver='liblinear')],
		['Decision Tree',DecisionTreeClassifier(random_state = random_state)],
		['Random Forest', RandomForestClassifier(random_state = random_state)],
	]

	x_train, x_test, y_train, y_test = generate_train_test_split(transformedDF, 0.30)
	evaluate_model(models, x_train, y_train)

	for model in models:
		fit_and_predict_models(model, x_train, y_train, x_test, y_test)


