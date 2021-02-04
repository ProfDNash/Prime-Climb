"""
BACK STEP FUNCTION
Perform one layer of back propagation
input: A_prev -- an np.array of activations from the previous layer, shape (size of previous layer, 1)
       cache -- tuple containing A_prev, W, b, Z from current layer from forward prop
       activiation -- a string calling either 'sigmoid', 'relu', or 'softmax' activation

output: dA_prev -- gradient of the cost with respect to activation of previous layer
        dW -- gradient of cost with respect to W in current layer
        db -- gradient of cost with respect to b in current layer

@author: David A. Nash
"""
import numpy as np
from NNutils import sigmoid, relu, softmax

def backStep(dA, cache, activation):
    
    A_prev, W, b, Z = cache  ##recall values from the current layer
    m = A_prev.shape[1]
    
    ##first take derivatives of activation functions
    if activation == 'relu':
        dZ = np.array(dA, copy=True)
        dZ[Z<=0] = 0
    elif activation == 'sigmoid':
        s = sigmoid(Z)
        dZ = dA*s*(1-s)
    elif activation == 'softmax':
        dZ=dA  ##if we are in the final layer with softmax, dA input will be exactly dZ
    elif activation == 'leaky':
        dZ = np.array(dA, copy=True)
        dZ[Z<=0] *= 0.1
       
    
    ##then take linear part of the derivative
    dW = 1/m*np.dot(dZ, A_prev.T)
    db = 1/m*np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T,dZ)
    
    return dA_prev, dW, db
