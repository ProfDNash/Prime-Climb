"""
LEARN GAME FUNCTION
Play a single (2-player) game using the NN to choose moves at each turn
Learn parameters as play proceeds using temporal difference model

input: parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter

output: Xlist -- list of all board positions throughout the game (for analysis if necessary)
        Ylist -- list of all predictions throughout the game (for analysis if necessary)
        turn -- # of turns that the game took to completion
        parameters -- updated parameters based on learning from one game


@author: David A. Nash
"""
import numpy as np
from chooseMove import chooseMove
from forwardProp import forwardProp
from backProp import backProp
from updateParameters import updateParameters

def learnGame(parameters, lambd, alpha):
    ##initialize the beginning of the game##
    Xt = np.array([0,0,0,0,1,0]).reshape((6,1))
    Xlist = np.array(Xt, copy=True).reshape((6,1))
    ##initialize array to keep track of the prediction at each turn
    Y0, caches = forwardProp(Xt, parameters)
    Ylist = np.array(Y0, copy=True).reshape((2,1))
    
    turn = 0 ##initialize turn number
    winner = 0 ##index of winner
    
    ##loop until someone wins
    while Xt[0,-1]!=101 and Xt[2,-1]!=101 and turn<5000:
        turn += 1
        roll = [np.random.randint(0,10), np.random.randint(0,10)]
        Xt = chooseMove(Xt, roll, parameters, np.arange(102), False)
        Xlist = np.append(Xlist, Xt, axis=1)
        Yt, caches = forwardProp(Xt,parameters)
        grads = backProp(Yt, caches)
        parameters = updateParameters(Yt,Ylist[:,turn-1],turn,grads,parameters,lambd,alpha)
        
        Yt = np.array(Yt).reshape((2,1))
        Ylist = np.append(Ylist,Yt, axis=1)
        #print('Turn: ', turn,'Roll: ', roll, 'Move: ',Xt.T)
    
    if Xt[2,-1]==101: winner = 1  ##change index if player 1 wins
    
    return Xlist, Ylist, turn, parameters