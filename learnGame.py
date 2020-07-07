"""
LEARN GAME FUNCTION
Play a single (2-player) game using the NN to choose moves at each turn
Learn parameters as play proceeds using temporal difference model

input: parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter
       eps -- parameter controlling the level of randomness allowed in decision making
               (eps=0 corresponds to no randomness, eps=1 corr to only randomness)

output: Xlist -- list of all board positions throughout the game (for analysis if necessary)
        Ylist -- list of all predictions throughout the game (for analysis if necessary)
        turn -- # of turns that the game took to completion
        parameters -- updated parameters based on learning from one game
        winner -- the winner of the game simulated


@author: David A. Nash
"""
import numpy as np
from chooseMove import chooseMove
from forwardProp import forwardProp
from backProp import backProp
from updateParameters import updateParameters

def learnGame(parameters, lambd=0, alpha=0.1, eps=0):
    ##initialize the beginning of the game##
    params=parameters.copy()
    Xt = np.array([0,0,0,0,1,0]).reshape((6,1))
    Xlist = np.array(Xt, copy=True).reshape((6,1))
    ##initialize array to keep track of the prediction at each turn
    Y0, caches = forwardProp(Xt, params)
    Ylist = np.array(Y0, copy=True).reshape((2,1))
    gradcache = dict()
    cacheList = dict()
    cacheList[0] = caches ##save initial caches for later use in backprop
    
    turn = 0 ##initialize turn number
    winner = 0 ##index of winner
    
    ##loop until someone wins
    while Xt[0,-1]!=101 and Xt[2,-1]!=101 and turn<10000:
        turn += 1
        if turn%2000 == 0: print(turn)
        roll = [np.random.randint(0,10), np.random.randint(0,10)]
        if np.random.rand(1)[0]<eps:
            Xt = chooseMove(Xt, roll, params, np.arange(102), True)
        else:
            Xt = chooseMove(Xt, roll, params, np.arange(102), False)
        Xlist = np.append(Xlist, Xt, axis=1)        
        Yt, caches = forwardProp(Xt, params)
        cacheList[turn]=caches
        if Xt[0,-1]==101: ##if player 0 wins, feed final reward instead of forward prop result
            Yt = np.array([1,0]).reshape((2,1))
        elif Xt[2,-1]==101: ##player 1 wins
            Yt = np.array([0,1]).reshape((2,1))
            winner = 1 ##change index if player 1 wins
        grads = backProp(Yt, Ylist[:,turn-1], cacheList[turn-1])
        gradcache[turn]=grads
        params = updateParameters(Yt,Ylist[:,turn-1],turn,gradcache,params,lambd,alpha)
        
        Yt = np.array(Yt).reshape((2,1))
        Ylist = np.append(Ylist,Yt, axis=1)
    
    return Xlist, Ylist, turn, params, winner