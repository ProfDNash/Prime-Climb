"""
PLAY GAME FUNCTION
input: numPlayers -- an integer value of the number of players playing (generally 1-4)

output: nTurns -- the number of turns taken in the game
        winner -- the winner of the game

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""
import numpy as np
from BasicGameData import Player, initGame, rollGenerator
from takeTurn import takeTurn


def playGame(numPlayers):
    ##initialize list of Primes, the Deck, the DiscardPile, and the PlayerList
    Spots = np.arange(102)
    Primes = [11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    DiscardPile = []
    Deck = np.arange(1,25)
    PlayerList, Deck = initGame(numPlayers, Deck)
    
    ##initialize the number of turns counter and the starting player
    nTurns = 0
    currPlayer = 0
    
    ##keep taking turns until someone wins (currPlayer<0)
    while currPlayer>-1 and PlayerList[currPlayer].position[0] != 101:
        currPlayer, PlayerList, Deck, DiscardPile = takeTurn(currPlayer,
                                                             PlayerList, 
                                                             Primes, Deck,
                                                             DiscardPile, Spots)
        nTurns += 1
        if nTurns>1000:
            print("Something is wrong")  ##for debugging
            break
    ##currPlayer==-1 corresponds to player 0 winning, etc.
    winner = -currPlayer-1  
    return nTurns, winner
