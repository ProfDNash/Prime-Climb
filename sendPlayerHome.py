"""
SEND PLAYER HOME FUNCTION
input: card -- an integer representing the card (can only send home if card==10 or card==11)
       playerNum -- the index of the current player
       PlayerList -- a list of player classes
       DiscardPile -- a list of the cards which have been discarded

output: PlayerList -- updated with any new positions and hands
        DiscardPile -- updated with added card played (if any)

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.

@author: David A. Nash
"""
import numpy as np

def sendPlayerHome(card, playerNum, PlayerList, DiscardPile):
    if card !=10 and card != 11:
        print('Error.  You cannot bump with card ', card)  ##for debugging
    else:
        ##check whether any other players are away from the start (position 0)
        offStart = [] ##initialize a list of tuples of the form (player_index,pawn_index)
        for idx, player in enumerate(PlayerList):
            if idx == playerNum:
                #sending self home is take care of during moveMapper
                continue
            else:
                ##cannot bump pawns on 0 or 101
                if player.position[1] !=0 and player.position[1]!=101:
                    offStart.append([idx,1])
                    if player.position[0] !=0:  ##if pos[0]==101, then the game should be over
                        offStart.append([idx,0])
        if len(offStart)>0:  ##then there are pawns to bump which aren't at the start
            ##choose a random player and pawn from the list of options
            playerChosen, pawnChosen = offStart[np.random.randint(0,len(offStart))]
            ##bump that pawn back to start and discard the card played
            PlayerList[playerChosen].position[pawnChosen]=0
            PlayerList[playerChosen].position.sort() ##re-sort the position into increasing order
            PlayerList[playerNum].cards.remove(card)
            DiscardPile.append(card)
        else:
            print("No one to bump.")  ##for debugging
    return PlayerList, DiscardPile
