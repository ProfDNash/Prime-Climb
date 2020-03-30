"""
FORWARD STEP FUNCTION
Perform one layer of forward propagation
input: A_prev -- an np.array of activations from the previous layer, shape (size of previous layer, 1)
       W -- weight matrix for the current layer, shape (size of current layer, size of previous layer)
       b -- bias vector, shape (size of current layer, 1)
       activiation -- a string calling either 'sigmoid', 'relu', or 'softmax' activation

output: A -- activations for the current layer
        cache -- a cache of (Z, W, and b) for the current layer to make backpropagation easier later

@author: David A. Nash
"""
import numpy as np
from NNutils import sigmoid, relu, softmax

def forwardStep(A_prev, W, b, activation):
    Z = np.dot(W,A_prev)+b
    cache = (Z, W, b)
    
    if activation == 'sigmoid':
        A = sigmoid(Z)
    elif activation == 'relu':
        A = relu(Z)
    elif activation == 'softmax':
        A = softmax(A)
    
    return A, cache
