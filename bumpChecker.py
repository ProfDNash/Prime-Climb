"""
BUMP CHECKER FUNCTION
input: playerNum -- an integer representing the current player
       PlayerList -- a list of player classes

output: PlayerList -- adjusted so that any pawns that have been landed on by
                      player[playerNum] get sent back to start.

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.

@author: David A. Nash
"""

import numpy as np


def bumpChecker(playerNum, PlayerList):
    curr_player = PlayerList[playerNum]

    for idx, player in enumerate(PlayerList):

        if (
            player != curr_player
        ):  ##self-bumping is taken care of in the generation of new positions

            bumped = False

            ##Players cannot be bumped back from position 101
            ##Check whether the current player's first pawn landed on one of player i's pawns
            if (
                0 < curr_player.position[0] < 101
                and curr_player.position[0] in player.position
            ):
                loc = np.where(curr_player.position[0] == player.position)[0][0]
                player.position[loc] = 0
                bumped = True

            ##Check whether the current player's second pawn landed on one of player i's pawns
            if (
                0 < curr_player.position[1] < 101
                and curr_player.position[1] in player.position
            ):
                loc = np.where(curr_player.position[1] == player.position)[0][0]
                player.position[loc] = 0
                bumped = True

            if bumped:
                ## Sort positions
                player.position = np.sort(player.position)

    return PlayerList
