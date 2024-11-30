"""
One-hot SIMPLE MOVE GENERATOR FUNCTION
Goal: Generate an array of all possible moves given a starting position and a roll
      while ignoring cards.
input: roll -- a pair of integers from 0 to 9 (n-1)
       pos -- a (1,102)-array with one-hots for the position
           -- note that it will be possible to have 2 in either position 0 or position 101

output: Q -- a (102,k)-array containing the k-possible moves

Note: (1) In Prime Climb, rolling doubles gives you 4 copies of the value (not 2)
      (2) 

@author: David A. Nash
"""

import numpy as np
from BasicGameData import Player
from OHapplyDie import OHapplyDie


def OHsimpleMove(roll, pos):
    ##create all possible orderings for applying dice
    ##e.g. with no cards, we can either apply die1 then die2, or die2, then die1
    if roll[0] == roll[1]:  ##rolled doubles so get 4 copies
        scheme = np.ones((1, 4)).astype(int) * roll[0]
    else:
        scheme = np.array([roll[0], roll[1], roll[1], roll[0]]).reshape((2, 2))

    finalPos = np.array([]).reshape(
        (0, 102)
    )  # initialize the array of all complete moves
    for order in scheme:
        iP = pos.copy()  ##hold the initial position
        for item in order:
            posList = np.array([]).reshape(
                (0, 102)
            )  ##initialize list of potential moves
            for i in range(iP.shape[0]):
                posList = np.append(
                    posList, OHapplyDie(iP[i, :].reshape((1, 102)), item), axis=0
                )
            iP = posList.copy()
        finalPos = np.append(finalPos, iP, axis=0)

    ##sort the options to remove duplicates
    sortedIdx = np.lexsort(finalPos.T)
    sortedPos = finalPos[sortedIdx, :]
    ##get a row mask of the unique rows
    rowMask = np.append([True], np.any(np.diff(sortedPos, axis=0), 1))
    finalPos = sortedPos[rowMask]

    return finalPos
