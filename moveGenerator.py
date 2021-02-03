"""
SIMPLE MOVE GENERATOR FUNCTION
Goal: Generate an array of all possible moves given a starting position and a roll
      while ignoring cards.
input: roll -- a pair of integers from 0 to 9 (n-1)
       pos -- a pair of integers (a,b) representing the player's current position

output: Q -- a (k,2)-array containing the k-possible moves

Note: (1) In Prime Climb, rolling doubles gives you 4 copies of the value (not 2)
      (2) 

@author: David A. Nash
"""
import numpy as np
from applyDie import applyDie
from cleanPositions import cleanPositions


def simpleMove(roll, pos):
    #partialFlag = 0  ##a flag keeping track of whether it is possible to win on a partial turn
    ##initialize the array of positions with the current position
    iP1 = np.array(pos).reshape((1,2))
    
    ##create all possible orderings for applying dice
    ##e.g. with no cards, we can either apply die1 then die2, or die2, then die1
    if roll[0] == roll[1]:   ##rolled doubles so get 4 copies
        scheme = np.array([str(roll[0]),str(roll[0]),str(roll[0]),str(roll[0])]).reshape((1,4))
    else:
        scheme = np.array([str(roll[0]),str(roll[1]),str(roll[1]),str(roll[0])]).reshape((2,2))

    finalPos = np.array([])  #initialize the array of all complete moves
    for order in scheme:
        intermediatePos2 = iP1.copy()
        for item in order:
            posList = np.array([])
            for i in range(intermediatePos2.shape[0]):
                pos = intermediatePos2[i,:].reshape((1,iP1.shape[1]))
                posList = np.append(posList, applyDie(pos, int(item)))
            intermediatePos2 = posList.reshape((posList.shape[0]//2, 2))
            #if 101 in intermediatePos2[:,0]: ##you can win on a partial turn
            #    partialFlag = 1
        finalPos = np.append(finalPos,intermediatePos2)
    k = np.int(finalPos.shape[0]/2)  ##count number of possible positions (pairs)
    finalPos = finalPos.reshape((k,2))  ##reshape array to (k,2)
    finalPos = cleanPositions(finalPos) #sort, delete repeats and unallowable positions
    ##take care of *self* bumping (i.e. if pos[0]==pos[1] then one pawn goes back to start)
    delRow = np.array([])  ##initialize list of rows to delete
    for i in range(finalPos.shape[0]):
        if finalPos[i,0]==finalPos[i,1] and finalPos[i,0]!=101 and finalPos[i,0]!=0:
            ##delete the option if bumping creates a duplicate
            if [0, finalPos[i,1]] in finalPos.tolist():
                delRow = np.append(delRow, i)
            else:
                finalPos[i,0]=0
    ##REMOVE DUPLICATES##
    finalPos = np.delete(finalPos, delRow.astype('i8'), axis=0)
    return finalPos.astype('int')
