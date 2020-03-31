"""
UPDATE PARAMETERS FUNCTION
input: Yt -- most recent prediction (equal to one_hot for the winner if at the end of the game)
       Yprev -- previous prediction for comparison in update formula
       turn -- current turn
       grads -- a dictionary containing gradients of prediction for dA, dW, db in each layer
       parameters -- a dictionary containing the current weights 'W1', 'b1' etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter

output: parameters -- updated based on outcome in the current time-step

@author: David A. Nash
"""
import numpy as np

def updateParameters(Yt, Yprev, turn, grads, parameters, lambd=0, alpha=1):
    
    L = len(parameters)//2  ##number of layers
    m = Yt.shape[1]
    dim = Yt.shape[0] ##size of final output layer
    deltas = {}  ##initialize dictionary for final adjustments to weights
    scale = np.sum(alpha*(Yt - Yprev))
    
    
    ##loop through layers
    for l in range(L):
        deltaWl = np.zeros((grads['dW'+str(l)].shape))
        deltabl= np.zeros((grads['db'+str(l)].shape))
        for k in range(turn):
            deltaWl += lambd**(turn-k) * grads['dW'+str(l)]
            deltabl += lambd**(turn-k) * grads['db'+str(l)]
        ##update parameters
        parameters['W'+str(l)] += scale*deltaWl
        parameters['b'+str(l)] += scale*deltab1
    
    return parameters