"""
BACKPROPAGATION FUNCTION
input: A_prev -- an np.array of activations from the previous layer, shape (size of previous layer, 1)
       cache -- tuple containing A_prev, W, b, Z from current layer from forward prop
       activiation -- a string calling either 'sigmoid', 'relu', or 'softmax' activation

output: dA_prev -- gradient of the cost with respect to activation of previous layer
        dW -- gradient of cost with respect to W in current layer
        db -- gradient of cost with respect to b in current layer

@author: David A. Nash
"""
import numpy as np
from backProp import backStep

def backProp(AL, Y, caches):
    
    grads = {} ##initialize dictionary for gradients
    L = len(caches)  ##number of layers
    m = AL.shape[1]
    
   
    
    return 