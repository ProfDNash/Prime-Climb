"""
APPLYCARD FUNCTION
input: iP1 -- a list of positions (a,b,c) where c encodes any cards which have already been applied
       card -- an int value representing a single action card
       curse -- a boolean keeping track of whether the player is currently cursed
       Spots -- a list of all positions on the board

output: iP2 -- a list of positions generated by applying the card to the positions in
               iP1 in all possible ways

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function makes use of the function cleanPositions

@author: David A. Nash
"""

import numpy as np
from cleanPositions import cleanPositions


def applyCard(iP1, card, curse, Spots):
    iP2 = np.array([])  ##initialize list of generated positions
    ##cannot apply a card if both pawns are already at the end
    if iP1[0, 0] == 101:
        print("No need to apply cards... you already won!")  ##for debugging
        iP2 = iP1
    else:
        if 0 < card < 10:
            ##make sure you only apply cards which haven't already been used
            for i in range(iP1.shape[0]):
                if str(iP1[i, 2])[card] == "1":  ##then card has already been used
                    continue
                ##otherwise, apply the card and mark in the encoder that the card has been used
                iP2 = np.append(iP2, iP1[i, :] - (card, 0, -(10 ** (11 - card))))
                ## Can only subtract or divide when cursed
                if not curse:
                    iP2 = np.append(
                        iP2, iP1[i, :] + (card, 0, 10 ** (11 - card))
                    )  ##so card corresponds to digit number card
                ##again, do not apply a card to a pawn already at 101
                if iP1[i, 1] != 101:
                    iP2 = np.append(iP2, iP1[i, :] - (0, card, -(10 ** (11 - card))))
                    ## Can only subtract or divide when cursed
                    if not curse:
                        iP2 = np.append(iP2, iP1[i, :] + (0, card, 10 ** (11 - card)))
        elif (
            9 < card < 12
        ):  ##these cards bump a pawn back to start (the player could do this to themself)
            for i in range(iP1.shape[0]):
                iP2 = np.append(
                    iP2, np.array([0, iP1[i, 1], 100000000000 + 10 ** (11 - card)])
                )  ##move lower pawn
                if iP1[i, 1] != 101:  ##can't move higher pawn if it is at 101
                    iP2 = np.append(
                        iP2, np.array([0, iP1[i, 0], 100000000000 + 10 ** (11 - card)])
                    )  ##move higher pawn
        num = np.int(iP2.shape[0] / 3)  ##count number of positions in the list
        iP2 = iP2.reshape((num, 3))  ##reshape to a list of triples
        iP2 = cleanPositions(
            iP2, Spots
        )  ##sort, remove unallowable positions and duplicates
    return iP2
