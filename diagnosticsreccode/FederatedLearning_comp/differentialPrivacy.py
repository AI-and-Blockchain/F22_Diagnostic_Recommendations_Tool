'''
File: differentialPrivacy.py
Purpose: Adds Laplacian noise to each datapoint to ensure privacy.
'''

import torch
import numpy as np

# Function to add Laplacian noise:
def laplacian_mechanism(dataset, sensitivity, epsilon):
    # Calculate the scale parameter (beta):
    beta = sensitivity / epsilon

    # Calculate the noise to be added:
    noise = torch.tensor(np.random.laplace(0, beta, 1))
    
    # Add the noise to the dataset:
    updated_dataset = torch.tensor(dataset) + noise

    # Return the new dataset:
    return updated_dataset
