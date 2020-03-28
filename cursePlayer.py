"""
CURSE PLAYER FUNCTION
input: card -- an integer representing a card (can only curse if card == 12 or card == 13)
       playerNum -- an integer index of the current player
       PlayerList -- a list of player classes
       DiscardPile -- an integer list of cards that have been discarded

output: PlayerList -- updated with a player cursed and a card removed from the current
                      player's hand
        DiscardPile -- updated with the played card added to the discard pile

@author: David A. Nash
"""
import numpy as np
from BasicGameData import Player

def cursePlayer(card, playerNum, PlayerList, DiscardPile):
    if card !=12 and card != 13:
        print('Error.  You cannot curse with card ', card)  ##for debugging
    else:
        if len(PlayerList)>1:  ##only curse other players if other players exist
            ##choose which player to curse (not self, and cannot already be cursed)
            pToCurse = playerNum
            while pToCurse == playerNum or PlayerList[pToCurse].cursed == True:
                pToCurse = np.random.randint(0,len(PlayerList))
            PlayerList[pToCurse].cursed = True ##apply the curse
        PlayerList[playerNum].cards.remove(card) ##remove the card from the player's hand
        DiscardPile.append(card)  ##add the card to the discard pile
    return PlayerList, DiscardPile
