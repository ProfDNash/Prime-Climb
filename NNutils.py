"""
NEURAL NETWORK UTILITIES

Helper functions designed to:
(1) randomly initialize (non-zero) weights (given number of incoming and outgoing connections)
(2) Apply vectorized sigmoid function
(3) Calculate softmax of a vector (thus, all output entries will be between 0 and 1 and will sum to 1)

@author: David A. Nash
"""
import numpy as np

##Randomly Initialize Weights for a given layer with L_in input connections and L_out output ones##
def randInitWeights(L_in, L_out):
    epsilon_init=0.12
    W = np.random.rand(L_out,L_in+1)*2*epsilon_init - epsilon_init
    return W

##Vectorized Sigmoid Function##
def sigmoid(z):
    return 1 / (1 + np.exp(- z))

##Softmax Function##
def softmax(X):
    '''Take vector X and return softmax'''
    denom = np.sum(np.exp(X))
    X = np.exp(X)/denom
    return X
