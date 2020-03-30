"""
CHOOSE MOVE FUNCTION
Select a move from the options available by seeing which maximizes the predicted probability of winning

input: Xprev -- input data from the current turn 
                [p1.pos1,p1.pos2,p2.pos1,p2.pos2,p1.turn,p2.turn,die1,die2]
       parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       Rand -- a boolean determining whether the move chosen is random or predicted

output: Xnext -- new board position based on chosen move (without new rolls generated)

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""
import numpy as np
from moveMapper import moveMapper
from forwardProp import forwardProp

##Choose the next position by selecting the maximum potential reward among all possible moves
def chooseMove(Xt,parameters, Spots, Rand=False):
    Xnext = np.zeros(8) ##initialize the next game position
    if Xt[4,0]==1:  ##it's player 0's turn
        pos1 = Xt[0:2,0]
        pos2 = Xt[2:4,0]
        Xnext[5]=1  ##we're currently ignoring cards, so turn will change
    else:  ##it's player 1's turn
        pos1 = Xt[2:4,0]
        pos2 = Xt[0:2,0]
        Xnext[4]=1
    possMoves = moveMapper(Xt[6:8,0],pos1,[],False, Spots)
    #if 101 in possMoves[:,0]:
    #    Xnext[2*Xt[5]] = 101
    #    Xnext[2*Xt[5]+1] = 101
    #    Xnext[2*Xt[4]] = pos2[0]
    #    Xnext[2*Xt[4]+1] = pos2[1]
    #else:  ##choose the move that has the best average possibility of victory (for the current player) over all possible turns for the next player
    if Rand == False:
        best = 0 ##initialize best win probability
        bestidx = 0  ##initialize index of best move
        for i in range(possMoves.shape[0]):
            Xnext[2*Xt[5]] = possMoves[i,0]
            Xnext[2*Xt[5]+1] = possMoves[i,1]
            temp = [0,0] ##initialize temp position for the next player
            ##check for bumping based on chosen move for current player##
            if pos2[0] not in possMoves[i,0:2] or pos2[0]!=101:
                temp[0]=pos2[0]
            if pos2[1] not in possMoves[i,0:2] or pos2[1]!=101:
                temp[1]=pos2[1]
            temp.sort() ##sort to ensure they are increasing
            Xnext[2*Xt[4]] = temp[0]
            Xnext[2*Xt[4]+1] = temp[1]
            total = 0  ##initialize total prediction score across all possible rolls
            for die1 in range(10):
                for die2 in range(die1,10):
                    if die1==die2:
                        multiplier = 2
                    else:
                        multiplier = 1
                    Xnext[6]=die1
                    Xnext[7]=die2
                    AL, caches = forwardProp(Xnext.reshape((8,1)), parameters)
                    ##Xt[5] == 1 if player 1 is current player, 0 if player 0 is current player##
                    total += (AL[Xt[5]][0])*multiplier
            average = total/100
            if average > best:
                best = average
                bestidx = i
    #else:
    #    bestidx = np.random.randint(0,possMoves.shape[0])
    
    ##choose best option
    Xnext[2*Xt[5]] = possMoves[bestidx,0]
    Xnext[2*Xt[5]+1] = possMoves[bestidx,1]
    ##checking for bumping##
    temp = [0,0]
    if pos2[0] not in possMoves[bestidx,0:2] or pos2[0]==101:
        temp[0]=pos2[0]
    if pos2[1] not in possMoves[bestidx,0:2] or pos2[1]==101:
        temp[1]=pos2[1]
    temp.sort()
    Xnext[2*Xt[4]] = temp[0]
    Xnext[2*Xt[4]+1] = temp[1]
    
    ##reshape Xnext to be a column vector
    Xnext = Xnext.reshape((len(Xnext),1))
    
    return Xnext