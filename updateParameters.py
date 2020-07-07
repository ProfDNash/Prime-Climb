"""
UPDATE PARAMETERS FUNCTION
input: Yt -- most recent prediction (equal to one_hot for the winner if at the end of the game)
       Yprev -- previous prediction for comparison in update formula
       turn -- current turn
       gradcache -- a dictionary containing dictionaries of gradients of prediction for dA, dW, db in each layer
       parameters -- a dictionary containing the current weights 'W1', 'b1' etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter

output: parameters -- updated based on outcome in the current time-step

@author: David A. Nash
"""
import numpy as np

def updateParameters(Yt, Yprev, turn, gradcache, parameters, lambd=0, alpha=0.1):
    
    L = len(parameters)//2  ##number of layers
    #dim = Yt.shape[0] ##size of final output layer
    #deltas = {}  ##initialize dictionary for final adjustments to weights
    scale = alpha#*(Yt - Yprev)
    
    
    ##loop through layers
    for l in range(L):
        deltaWl = np.zeros((gradcache[1]['dW'+str(l+1)].shape))
        deltabl= np.zeros((gradcache[1]['db'+str(l+1)].shape))
        ##sum over memory
        for k in range(turn):
            deltaWl += lambd**(turn-k) * gradcache[k+1]['dW'+str(l+1)]
            deltabl += lambd**(turn-k) * gradcache[k+1]['db'+str(l+1)]
        ##update parameters
        parameters['W'+str(l+1)] += scale*deltaWl
        parameters['b'+str(l+1)] += scale*deltabl
    
    return parameters