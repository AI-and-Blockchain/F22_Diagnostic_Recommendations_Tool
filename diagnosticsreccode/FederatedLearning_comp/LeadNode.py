'''
File: LeadNode.py
Purpose: Acts as the "central server" node that aggregates the model.
'''

class LeadNode:
    def __init__(self, account_num_):
        self.account_num = account_num_
        self.models = dict()

    def storeModel(self, node, model_data):
        # Stores the model data for a specific node:
        self.models[node] = model_data
        '''
        Model data is expected to look like this:

        {'model number','model','train size','test size','test precision',
		'test recall','test f1','test sensitivity','test specificity'}
        '''

    def federatedAveraging(self):
        '''
        A federated averaging algorithm will be run on the following data from
        the dictionary of model data stored in this LeadNode:

        {overall_precision, sensitivity, specificity, overall_f1}
        '''

        # Declare variables to store model info:
        model_number = None
        model = None

        # Declare variables to store sums:
        precision_sum = 0
        sensitivity_sum = 0
        specificity_sum = 0
        f1_sum = 0
        recall_sum = 0

        # Calculate the sum of each model weight:
        total_nodes = 0
        for node in self.models:
            model_number = node['model number']
            model = node['model']
            precision_sum += node['test precision']
            sensitivity_sum += node['test sensitivity']
            specificity_sum += node['test specificity']
            f1_sum += node['test f1']
            recall_sum += node['test recall']
            total_nodes += 1

        # Average the model weights:
        precision_avg = precision_sum / total_nodes
        sensitivity_avg = sensitivity_sum / total_nodes
        specificity_avg = specificity_sum / total_nodes
        f1_avg = f1_sum / total_nodes
        recall_avg = recall_sum / total_nodes

        # Create a dictionary of the updated model weights:
        updated_model = {
            'model_number': model_number,
            'model': model,
            'precision_avg': precision_avg,
            'sensitivity_avg': sensitivity_avg,
            'specificity_avg': specificity_avg,
            'f1_avg': f1_avg,
            'recall_avg': recall_avg
        }

        return updated_model
