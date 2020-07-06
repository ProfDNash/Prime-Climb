"""
CHOOSE MOVE FUNCTION
Select a move from the options available by seeing which maximizes the predicted probability of winning

input: Xprev -- input data from the current turn 
                [p1.pos1,p1.pos2,p2.pos1,p2.pos2,p1.turn,p2.turn]
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
from moveMapper import moveMapper
from forwardProp import forwardProp
from bump import bump

##Choose the next position by selecting the maximum potential reward among all possible moves
def chooseMove(Xt,roll,parameters, Spots=np.arange(0,102), Rand=False):
    n = Xt.shape[0]//3 ##number of players
    order = Xt[-n:,0] ##array of one-hots for current player
    idx = np.where(order==1)[0][0] ##index of current player
    pos1 = Xt[2*idx:2*idx+2,0] ##position of current player
    possMoves = moveMapper(roll,pos1,[],False, Spots)
    
    ##choose the move that has the highest prediction value for the current player
    if Rand == False:
        best = 0 ##initialize best win probability
        bestidx = 0  ##initialize index of best move
        for i in range(possMoves.shape[0]):
            Xnext=Xt.copy()
            Xnext[2*idx:2*idx+2,0] = possMoves[i,0:2]
            Xnext = bump(Xnext) ##check for bumping
            ##use forwardProp predictions to rate the options
            AL, caches = forwardProp(Xnext,parameters)
            score = AL[idx][0]
            if score > best:
                best = score
                bestidx = i
    else:
        bestidx = np.random.randint(0,possMoves.shape[0])
    
    ##choose best option
    Xnext = Xt.copy()
    Xnext[2*idx:2*idx+2,0] = possMoves[bestidx,0:2]
    Xnext = bump(Xnext) ##check for bumping
    
    return Xnext