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

def updateParameters(Yt, Yprev, turn, grads, parameters, lambd=0, alpha=10):
    
    L = len(parameters)//2  ##number of layers
    dim = Yt.shape[0] ##size of final output layer
    #deltas = {}  ##initialize dictionary for final adjustments to weights
    scale = Yt[0] - Yprev[0]#np.sum(alpha*(Yt - Yprev))
    
    
    ##loop through layers
    for l in range(L):
        deltaWl = np.zeros((grads['dW'+str(l+1)].shape))
        deltabl= np.zeros((grads['db'+str(l+1)].shape))
        ##sum over memory
        for k in range(turn):
            deltaWl += lambd**(turn-k) * grads['dW'+str(l+1)]
            deltabl += lambd**(turn-k) * grads['db'+str(l+1)]
        ##update parameters
        parameters['W'+str(l+1)] += scale*deltaWl
        parameters['b'+str(l+1)] += scale*deltabl
    
    return parameters