"""
PLAY GAME FUNCTION
input: numPlayers -- an integer value of the number of players playing (generally 1-4)
       printData -- a boolean to determine whether to print outcomes (default is False)

output: nTurns -- the number of turns taken in the game
        winner -- the winner of the game

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function uses player classes and takeTurn (therefore, everything else)

@author: David A. Nash
"""

import numpy as np
from BasicGameData import Player
from src.utilities.constants import CARD_PRIMES
from takeTurn import takeTurn


class Game:
    def __init__(self, number_of_players: int = 1):
        self.number_of_players = number_of_players
        self.players = {idx: Player() for idx in range(self.number_of_players)}
        self.deck = np.random.permutation(np.arange(1, 25))
        self.discard_pile = []
        self.number_of_turns = 0
        self.board_spots = np.arange(102)
        self.current_player = 0
        self.card_primes = CARD_PRIMES

    def play(self, print_data: bool = False):
        """
        Method which plays the game until someone wins, will print out logging info
        if `print_data` is True
        """
        while (
            self.current_player > -1
            and self.players[self.current_player].position[0] != 101
        ):
            self.current_player, intermediate_players, self.deck, self.discard_pile = (
                takeTurn(
                    playerNum=self.current_player,
                    PlayerList=list(self.players.values()),
                    Primes=self.card_primes,
                    Deck=self.deck,
                    DiscardPile=self.discard_pile,
                    Spots=self.board_spots,
                    printData=print_data,
                )
            )
            self.players = {
                idx: player for idx, player in enumerate(intermediate_players)
            }
            self.number_of_turns += 1
            if self.number_of_turns > 1000:
                print("Something is wrong")  ##for debugging
                break
        ##currPlayer==-1 corresponds to player 0 winning, etc.
        winner = -self.current_player - 1
        return self.number_of_turns, winner


# def playGame(numPlayers, printData=False):
#     ##initialize list of Primes, the Deck, the DiscardPile, and the PlayerList
#     Spots = np.arange(102)
#     Primes = CARD_PRIMES
#     DiscardPile = []
#     PlayerList, Deck = initGame(numPlayers)

#     ##initialize the number of turns counter and the starting player
#     nTurns = 0
#     currPlayer = 0

#     ##keep taking turns until someone wins (currPlayer<0)
#     while currPlayer > -1 and PlayerList[currPlayer].position[0] != 101:
#         currPlayer, PlayerList, Deck, DiscardPile = takeTurn(
#             currPlayer, PlayerList, Primes, Deck, DiscardPile, Spots, printData
#         )
#         nTurns += 1
#         if nTurns > 1000:
#             print("Something is wrong")  ##for debugging
#             break
#     ##currPlayer==-1 corresponds to player 0 winning, etc.
#     winner = -currPlayer - 1
#     return nTurns, winner


if __name__ == "__main__":
    game = Game(2)
    game.play(True)
