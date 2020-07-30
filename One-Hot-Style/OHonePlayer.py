"""
One-hot ONE PLAYER FUNCTION
Play a single (1-player) game using the NN to choose moves at each turn
Learn parameters as play proceeds using temporal difference model

input: parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter
       eps -- parameter controlling the level of randomness allowed in decision making
               (eps=0 corresponds to no randomness, eps=1 corr to only randomness)
       learn -- a boolean parameter determining whether the weights should be updated during play

output: Xlist -- list of all board positions throughout the game (for analysis if necessary)
        Ylist -- list of all predictions throughout the game (for analysis if necessary)
        turn -- # of turns that the game took to completion
        parameters -- updated parameters based on learning from one game

@author: David A. Nash
"""
import numpy as np
from OHchooseMove import OHchooseMove
from forwardProp import forwardProp
from backProp import backProp
from updateParameters import updateParameters

def OHonePlayerGame(parameters, lambd=0, alpha=0.1, eps=0, learn=True):
    ##initialize the beginning of the game##
    params=parameters.copy()
    Xt = np.zeros((1,102))
    Xt[0,0]=1
    Xlist = Xt.copy()
    ##initialize array to keep track of the prediction at each turn
    Y0, caches = forwardProp(Xt.T, params)
    Ylist = Y0.copy()
    gradcache = dict()
    cacheList = dict()
    cacheList[0] = caches ##save initial caches for later use in backprop
    
    turn = 0 ##initialize turn number
    
    ##loop until player wins
    while Xt[0,101]!=1 and turn<10000:
        turn += 1
        if turn%1000 == 0: print(turn)
        roll = [np.random.randint(0,10), np.random.randint(0,10)]
        ##play randomly with probability eps
        randFlag = np.random.rand(1)[0]<eps  ##true with probability eps
        Xt = OHchooseMove(Xt, roll, params, np.arange(102), randFlag)
        Xlist = np.append(Xlist, Xt, axis=0)        
        Yt, caches = forwardProp(Xt.T, params)
        cacheList[turn]=caches
        if Xt[0,101]==1: ##if player 0 wins, feed final reward instead of forward prop result
            Yt = np.array([10]).reshape((1,1))
        grads = backProp(Yt, Ylist[:,turn-1], cacheList[turn-1])
        gradcache[turn]=grads
        if learn == True:
            params = updateParameters(Yt,Ylist[:,turn-1],turn,gradcache,params,lambd,alpha)

        Ylist = np.append(Ylist,Yt, axis=1)
    
    return Xlist, Ylist, turn, params