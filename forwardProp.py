"""
FORWARD PROPAGATION (i.e. prediction)
input: Xt -- input data from the t-th turn in the game
       parameters -- a dictionary containing parameters for each layer of the network

output: nTurns -- the number of turns taken in the game
        winner -- the winner of the game

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""
import numpy as np
from NNutils import relu, softmax, sigmoid

def forwardProp(Xt, parameters):  
    ##apply linear + ReLU at each layer until applying linear + softmax to the final layer##
    L = len(parameters)/2  ##counts the number of layers
    cache = {}  ##initialize cache to save values as we proceed
    
    for l in range(L-1):
        cache['Z'+str(l+1)] = forward prop step

    return cache
