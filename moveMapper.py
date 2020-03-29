"""
MOVE MAPPER FUNCTION
input: roll -- a pair of integers from 0 to 9 (n-1)
       pos -- a pair of integers (a,b) representing the player's current position
       availCards -- a list of ints representing the player's current hand
       curse -- a boolean keeping track of whether the player is currently cursed
       Spots -- a list of all positions on the board

output: finalPos -- an (?,3) array of triples containing all possible *allowable* positions 
                    the player could move to in columns 0 and 1, and an encoding of which
                    cards need to be used to get there in column 2.

Note: (1) In Prime Climb, rolling doubles gives you 4 copies of the value (not 2)
      (2) This function makes use of the functions cleanPositions, applyDie, applyCard

@author: David A. Nash
"""
import numpy as np
from itertools import permutations
from BasicGameData import Player
from applyCard import applyCard
from applyDie import applyDie
from cleanPositions import cleanPositions


def moveMapper(roll, pos, availCards, curse, Spots):
    partialFlag = 0  ##a flag keeping track of whether it is possible to win on a partial turn
    ##initialize the array of positions with the current position
    intermediatePos1 = np.array(pos) 
    '''
    add the encoding of the cards which have been used.
    Note that in this encoding, digit i (1-11) corresponds to a one-hot for card i being used
    Thus, if card 4 has been used, we will add 10^(11-4)
    '''
    intermediatePos1 = np.append(intermediatePos1, 100000000000) 
    
    ##create all possible orderings for applying cards and dice
    ##first generate a scheme of all possible orders in which to apply dice and/or cards
    ##e.g. with no cards, we can either apply die1 then die2, or die2, then die1
    if roll[0] == roll[1]:   ##rolled doubles so get 4 copies
        scheme = np.array([str(roll[0]),str(roll[0]),str(roll[0]),str(roll[0])])
    else:
        scheme = np.array([str(roll[0]),str(roll[1])])
    ##Add all available action cards to the scheme generator
    for c in range(len(availCards)):
        if 0<availCards[c]<12:
            scheme = np.append(scheme, 'c'+str(availCards[c]))
    scheme = set(permutations(scheme))  ##create all permutations of the scheme list
    ##it only makes logical sense to move yourself home at the beginning of your turn, otherwise you waste dice
    ##thus, we'll remove any permutations which have card 10 or 11 played later in the turn
    if 10 in availCards or 11 in availCards:
        keepset = []
        for x in scheme:
            if x[0]=='c10' or x[0]=='c11':
                keepset.append(x)
        if 10 in availCards and 11 in availCards:
            scheme = []
            for x in keepset:
                if x[1]=='c10' or x[1]=='c11':
                    scheme.append(x)
        else:
            scheme = keepset
    finalPos = np.array([])  #initialize the array of all complete moves
    for order in scheme:
        impossible = False  ##flag used to eliminate impossible branches
        #intermediatePos2 = intermediatePos1.reshape((1,3))  ##a distinct copy of the original array
        intermediatePos2 = np.array([intermediatePos1[0],intermediatePos1[1], intermediatePos1[2]]).reshape((1,3))
        for item in order:
            #print(intermediatePos2.shape)
            if item[0] == 'c':    ##if the first character is c, apply the given card
                ##ALSO Keep track of positions without using the card!
                intermediatePos2 = np.append(intermediatePos2, applyCard(intermediatePos2, int(item[1:]), Spots), axis=0)
            else:
                intermediatePos2 = applyDie(intermediatePos2, int(item), curse, Spots)
                ##it is possible (although unlikely) to have no allowable moves
                ##if so, it should ignore these options
                if intermediatePos2.shape[0]==0:
                    impossible=True
                    break
            if 101 in intermediatePos2[:,0]: ##you can win on a partial turn
                intermediatePos2 = np.array([101,101,100000000000])
                partialFlag = 1
                break
        if impossible == False:
            finalPos = np.append(finalPos,intermediatePos2)
        else:
            continue
        if partialFlag == 1:
            break
    num = np.int(finalPos.shape[0]/3)  ##count number of possible positions (triples)
    finalPos = finalPos.reshape((num,3))  ##reshape array to (num,3)
    finalPos = cleanPositions(finalPos, Spots) #sort, delete repeats and unallowable positions
    ##take care of *self* bumping (i.e. if pos[0]==pos[1] then one pawn goes back to start)
    delRow = np.array([])  ##initialize list of rows to delete
    for i in range(finalPos.shape[0]):
        if finalPos[i,0]==finalPos[i,1] and finalPos[i,0]!=101:
            if finalPos[i,1] !=0 and [0, finalPos[i,1]] in finalPos.tolist():
                delRow = np.append(delRow, i)
            else:
                finalPos[i,0]=0
    ##RE-SORT AND REMOVE DUPLICATES##
    finalPos = np.delete(finalPos, delRow.astype('i8'), axis=0)
    ##it is possible to have no options, if so, stay put
    if finalPos.shape[0]==0:
        finalPos = np.array([pos[0], pos[1], 100000000000]).reshape((1,3))
    finalPos.view('i8,i8,i8').sort(order=['f0','f1'], axis=0)
    return finalPos.astype('i8')
