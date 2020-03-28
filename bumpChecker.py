"""
BUMP CHECKER FUNCTION
input: playerNum -- an integer representing the current player
       PlayerList -- a list of player classes

output: PlayerList -- adjusted so that any pawns that have been landed on by
                      player[playerNum] get sent back to start.

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function makes use of the function cleanPositions

@author: David A. Nash
"""
import numpy as np
from BasicGameData import Player
from cleanPositions import cleanPositions


def bumpChecker(playerNum, PlayerList):
    for i in range(len(PlayerList)):
        if i == playerNum: ##self-bumping is taken care of in the generation of new positions
            continue
        ##Players cannot be bumped back from position 101
        ##Check whether the current player's first pawn landed on one of player i's pawns
        if 0<PlayerList[playerNum].position[0] <101 and PlayerList[playerNum].position[0] in PlayerList[i].position:
            loc = np.where(PlayerList[playerNum].position[0] in PlayerList[i].position)[0][0]
            PlayerList[i].position[loc] = 0
        ##Check whether the current player's second pawn landed on one of player i's pawns
        if 0<PlayerList[playerNum].position[1] <101 and PlayerList[playerNum].position[1] in PlayerList[i].position:
            loc = np.where(PlayerList[playerNum].position[1] in PlayerList[i].position)[0][0]
            PlayerList[i].position[loc] = 0
    return PlayerList
