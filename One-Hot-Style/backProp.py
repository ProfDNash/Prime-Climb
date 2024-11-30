"""
BACKPROPAGATION FUNCTION
input: AL -- an np.array of activations from the final layer in most recent prediction
       ALt -- an np.array of activations from the final layer in the previous step
       caches -- tuple containing the forward prop cache (A_prev, W, b, Z) from each layer

output: grads -- a dictionary containing gradients of prediction for dA, dW, db, in each layer

@author: David A. Nash
"""

import numpy as np
from backStep import backStep


def backProp(AL, ALt, caches):

    grads = {}  ##initialize dictionary for gradients
    L = len(caches)  ##number of layers
    current_cache = caches[L - 1]  ##cache for final layer
    A_prev, W, b, Z = current_cache

    m = AL.shape[1]
    dim = AL.shape[0]  ##size of final output layer
    ##note, we're not taking derivative of cost... just of the prediction function,
    ##so dAL=1, and we'll spit back dZ
    # dAL = np.ones(AL.shape)  ##initialize array to collect derivatives
    ALt = ALt.reshape(AL.shape)
    dAL = AL - ALt

    ##Last activation is softmax, so derivative with respect to Zi is
    ##Zi(1-Zi) in the ith slot, and -ZiZj in the other slots
    # for i in range(dim):
    #    dALi = -Z*Z[i]
    #    dALi[i] += Z[i]
    #    dAL += dALi

    grads["dA" + str(L - 1)], grads["dW" + str(L)], grads["db" + str(L)] = backStep(
        dAL, current_cache, "leaky"
    )

    ##loop through the rest of the layers
    for l in reversed(range(L - 1)):
        ##other layers are Linear + ReLU
        current_cache = caches[l]
        dA_prev, dW, db = backStep(grads["dA" + str(l + 1)], current_cache, "leaky")
        grads["dA" + str(l)] = dA_prev
        grads["dW" + str(l + 1)] = dW
        grads["db" + str(l + 1)] = db

    return grads
