"""
One-Hot APPLYDIE FUNCTION
input: iP1 -- a (1,102)-array containing a position vector
       die -- a single int value from 0 to 9 (n-1)
       curse -- a boolean keeping track of whether the player is currently cursed
       Spots -- a list of all positions on the board

output: iP2 -- (k,102)-array of possible position vectors

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function makes use of the function cleanPositions

@author: David A. Nash
"""

import numpy as np
from BasicGameData import Player
from cleanPositions import cleanPositions


def OHapplyDie(iP1, die, curse=False, Spots=np.arange(102)):
    ##first, convert position to a single integer
    pos = np.where(iP1 == 1)[1][0]
    if die == 0:  ##A roll of zero corresponds to the value 10
        die = 10

    iP2 = np.array([]).reshape((0, 102))  ##initialize new array of possible positions
    Zer = np.zeros((1, 102))  ##initialize array of zeros
    if pos == 101:  ##do not allow movement away from position 101
        iP2 = iP1
    else:
        if pos + die in Spots:
            Zer[0, pos + die] = 1
            iP2 = np.append(iP2, Zer, axis=0)
            Zer[0, pos + die] = 0
        if pos - die in Spots:
            Zer[0, pos - die] = 1
            iP2 = np.append(iP2, Zer, axis=0)
            Zer[0, pos - die] = 0
        if pos * die in Spots:
            Zer[0, pos * die] = 1
            iP2 = np.append(iP2, Zer, axis=0)
            Zer[0, pos * die] = 0
        if pos / die in Spots:
            Zer[0, int(pos / die)] = 1
            iP2 = np.append(iP2, Zer, axis=0)
            Zer[0, int(pos / die)] = 0

    return iP2
