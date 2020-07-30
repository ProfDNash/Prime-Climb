"""
One-Hot CHOOSE MOVE FUNCTION
Select a move from the options available by seeing which maximizes the predicted probability of winning

input: Xt -- a (1,102)-array of the current position on the board
       roll -- [die1, die2] for the current player
       parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       Spots -- list of all locations on the board
       Rand -- a boolean determining whether the move chosen is random or predicted

output: Xnext -- new board position based on chosen move (without new rolls generated)

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""
import numpy as np
from OHmoveGen import OHsimpleMove
from forwardProp import forwardProp

##Choose the next position by selecting the maximum potential reward among all possible moves
def OHchooseMove(Xt,roll,parameters, Spots=np.arange(0,102), Rand=False):
    ##First get an array of the possible moves
    possMoves = OHsimpleMove(roll,Xt)
    
    ##choose the move that has the highest prediction value for the current player
    if Rand == False:
        best = 0 ##initialize best win probability
        bestidx = 0  ##initialize index of best move
        for i in range(possMoves.shape[0]):
            Xnext=possMoves[i,:].reshape((1,102))
            ##use forwardProp predictions to rate the options
            AL, caches = forwardProp(Xnext.T,parameters)
            score = AL[0][0]
            if score > best:
                best = score
                bestidx = i
    else: ##choose a random move -- for exploration during training
        bestidx = np.random.randint(0,possMoves.shape[0])
    
    ##return the chosen move with player turn changed
    Xnext = possMoves[bestidx,:].reshape((1,102))
    
    return Xnext