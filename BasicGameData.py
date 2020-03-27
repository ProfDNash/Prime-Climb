"""
PLAYER class, INITGAME function, ROLLGENERATOR function

@author: David A. Nash
"""

import numpy as np


class Player:
    def __init__(self, position, cards, cursed):
        self.position = position  ##An ordered int pair (a,b) with a<b unless a=b=0 or a=b=101
        self.cards = cards   ##An int list of the cards in the player's hand
        self.cursed = cursed  ##True means player can only use - or / on next turn
        
def initGame(numPlayers, Deck):
    if numPlayers<1 or numPlayers>4:
        print("Error, can only be played with 1 to 4 players")
    else:
        PlayerList = [Player([0,0],[], False), Player([0,0],[], False), Player([0,0],[], False), Player([0,0],[], False)]
        PlayerList = PlayerList[:numPlayers]
        ##Shuffle the deck of cards
        Deck = np.random.permutation(Deck)
    return PlayerList, Deck

def rollGenerator(n):
    r = np.random.randint(1,high=n+1,size=2)
    return r

