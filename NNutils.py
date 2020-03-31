"""
NEURAL NETWORK UTILITIES

Helper functions designed to:
(1) randomly initialize (non-zero) weights (given number of incoming and outgoing connections)
(2) Apply vectorized sigmoid function
(3) Apply vectorized ReLU function
(4) Calculate softmax of a vector (thus, all output entries will be between 0 and 1 and will sum to 1)

@author: David A. Nash
"""
import numpy as np

##Randomly Initialize Weights for a given layer with L_in input connections and L_out output ones##
def randInitWeights(layer_dims):
    ''' 
    input: layer_dims -- a numpy array (list) containing the dimensions of the layers in our NN
    
    output: parameters -- a dictionary containing the randomized weights for each layer 'W1', 'b1', etc.
    '''
    parameters = {} ##initialize empty dictionary
    L = len(layer_dims)  ##number of layers (including the input layer)
    epsilon_init=0.12
    
    for l in range(1,L):
        parameters['W'+str(l)] = np.random.randn(layer_dims[l],layer_dims[l-1])*2*epsilon_init# - epsilon_init
        parameters['b'+str(l)] = np.zeros((layer_dims[l],1))
    
    return parameters

##Vectorized Sigmoid Function##
def sigmoid(z):
    return 1 / (1 + np.exp(- z))

##Vectorized ReLU Function##
def relu(z):
    return np.maximum(0,z)

##Softmax Function##
def softmax(X):
    '''Take vector X and return softmax'''
    denom = np.sum(np.exp(X))
    X = np.exp(X)/denom
    return X
