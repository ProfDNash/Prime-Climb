"""
LEARN GAME FUNCTION
Play a single (2-player) game using the NN to choose moves at each turn
Learn parameters as play proceeds using temporal difference model

input: Xprev -- input data from the current turn 
                [p1.pos1,p1.pos2,p2.pos1,p2.pos2,p1.turn,p2.turn]
       roll -- [die1, die2] for the current player
       parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       Rand -- a boolean determining whether the move chosen is random or predicted

output: Xnext -- new board position based on chosen move (without new rolls generated)


@author: David A. Nash
"""
import numpy as np
from chooseMove import chooseMove
from forwardProp import forwardProp
from backProp import backProp

def learnGame(parameters, lambd):
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
        
        Yt = np.array(Yt).reshape((2,1))
        Ylist = np.append(Ylist,Yt, axis=1)
        #print('Turn: ', turn,'Roll: ', roll, 'Move: ',Xt.T)
    
    if Xt[2,-1]==101: winner = 1  ##change index if player 1 wins
    
    return Xlist, Ylist, turn