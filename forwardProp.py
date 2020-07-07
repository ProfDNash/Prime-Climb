"""
FORWARD PROPAGATION (i.e. prediction)
input: Xt -- input data from the t-th turn in the game
       parameters -- a dictionary containing parameters for each layer of the network

output: AL -- activations from the final layer of the network (should sum to 1)
        caches -- a cache of the parameters and linear activations (Z) in each layer for backprop

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""
import numpy as np
from forwardStep import forwardStep

def forwardProp(Xt, parameters):  
    ##apply linear + ReLU at each layer until applying linear + softmax to the final layer##
    L = len(parameters)//2  ##counts the number of layers
    caches = []  ##initialize caches list to save values as we proceed
    A = Xt
    
    for l in range(1,L):
        A_prev = A
        A, cache = forwardStep(A_prev,parameters['W'+str(l)],parameters['b'+str(l)],'relu')
        caches.append(cache)
    
    ##For layer L, compute sigmoid
    AL, cache = forwardStep(A, parameters['W'+str(L)], parameters['b'+str(L)],'sigmoid')
    caches.append(cache)

    return AL, caches
