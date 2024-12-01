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
from bumpChecker import bumpChecker
from cursePlayer import cursePlayer
from drawACard import drawACard
from moveMapper import moveMapper
from sendPlayerHome import sendPlayerHome


class Game:
    def __init__(self, number_of_players: int = 1, verbose: bool = False):
        self.number_of_players = number_of_players
        self.verbose = verbose
        self.players = {idx: Player() for idx in range(self.number_of_players)}
        self.deck = np.random.permutation(np.arange(1, 25))
        self.discard_pile = []
        self.number_of_turns = 0
        self.board_spots = np.arange(102)
        self.current_player = 0
        self.card_primes = CARD_PRIMES

    def _next_player(self):
        self.current_player = (self.current_player + 1) % self.number_of_players

    def _take_turn(self, PlayerList, Primes, Deck, DiscardPile, Spots):
        ##at the start of the turn, randomly decide whether to curse another player (if the card is available)
        curseFlag = 0
        if 12 in PlayerList[self.current_player].cards:
            curseFlag = np.random.randint(
                0, 2
            )  ##randomly choose whether to use the card or not
            card = 12
        elif 13 in PlayerList[self.current_player].cards:
            curseFlag = np.random.randint(0, 2)
            card = 13
        if curseFlag == 1:
            cursePlayer(card, self.current_player, PlayerList, DiscardPile)

        ##Get the current player position, roll the dice, and generate the possible moves
        pos = PlayerList[self.current_player].position
        roll = [np.random.randint(0, 10), np.random.randint(0, 10)]
        if self.verbose:
            print(f"Player {self.current_player} rolled: {roll}")
        possibleMoves = moveMapper(
            roll,
            pos,
            PlayerList[self.current_player].cards,
            PlayerList[self.current_player].cursed,
            Spots,
        )

        ##choose to win if you can
        if 101 in possibleMoves[:, 0]:
            Move = np.array([101, 101]).reshape((1, 2))
            print(f"Player {self.current_player} wins!!!!")
            self.current_player = -1 * (self.current_player + 1)
            return PlayerList, Deck, DiscardPile
        ##if 101 is an option for pawn2, don't consider other options
        elif 101 in possibleMoves:
            ##find indices of moves with 101 as one of the positions
            TryToWin = np.where(possibleMoves[:, 1] == 101)[0]
            possibleMoves = possibleMoves[TryToWin]
            ##choose a random move
            Move = possibleMoves[np.random.randint(0, possibleMoves.shape[0])]
        else:
            ##choose a random move
            Move = possibleMoves[np.random.randint(0, possibleMoves.shape[0])]

        ##ADD CHECK TO AVOID USING CARDS IF IT IS POSSIBLE TO GET TO THE CHOSEN LOCATION WITH FEWER OF THEM
        if Move.shape[0] > 2 and Move[2] != 100000000000:
            x = np.where(possibleMoves[:, 0] == Move[0])[0]
            y = np.where(possibleMoves[:, 1] == Move[1])[0]
            matches = np.intersect1d(
                x, y
            )  ##finds indices of all locations matching chosen Move
            ##first in the list should have the lowest third entry (saving lower number cards)
            bestMove = possibleMoves[matches[0], :]
            ##It may be possible to use fewer cards though, so check
            for j in range(len(matches)):
                if sum(
                    int(digit) for digit in str(possibleMoves[matches[j], 2])[1:]
                ) < sum(int(digit) for digit in str(bestMove[2])[1:]):
                    bestMove = possibleMoves[matches[j], :]
            Move = bestMove

            ##Check if any cards were used and discard them
            if Move[2] != 100000000000:
                for i in range(1, len(str(Move[2]))):
                    if str(Move[2])[i] == "1":
                        PlayerList[self.current_player].cards.remove(i)
                        DiscardPile.append(i)

        ##Change the current player's position to the newly chosen one (drop the card encoding)
        PlayerList[self.current_player].position = Move[0:2]
        if self.verbose:
            print(f"Player {self.current_player} moves to: {Move[0:2]}")

        ##Check for bumping, note: self bumping is already achieved in moveMapper
        bumpChecker(self.current_player, PlayerList)

        ##undo any curses at the end of the turn
        if PlayerList[self.current_player].cursed == True:
            PlayerList[self.current_player].cursed = False
            if self.verbose:
                print(f"Player {self.current_player} is no longer cursed")

        ##if the player did not use the send home cards to augment their own move,
        ##they can choose to send someone else back as part of their turn
        if 10 in PlayerList[self.current_player].cards:
            if np.random.randint(0, 2) == 1:
                sendPlayerHome(10, self.current_player, PlayerList, DiscardPile)
        if 11 in PlayerList[self.current_player].cards:
            if np.random.randint(0, 2) == 1:
                sendPlayerHome(11, self.current_player, PlayerList, DiscardPile)

        ## after all actions, check to see if they get to draw a card
        rollAgain, PlayerList, Deck, DiscardPile = drawACard(
            self.current_player, pos, Move[0:2], PlayerList, Primes, Deck, DiscardPile
        )

        if rollAgain:  ##take another turn!
            if self.verbose:
                print(f"Player {self.current_player} gets to roll again!")

            return PlayerList, Deck, DiscardPile
        else:  ##move to next player
            self._next_player()
            return PlayerList, Deck, DiscardPile

    def play(self):
        """
        Method which plays the game until someone wins
        """
        while (
            self.current_player > -1
            and self.players[self.current_player].position[0] != 101
        ):
            (
                intermediate_players,
                self.deck,
                self.discard_pile,
            ) = self._take_turn(
                PlayerList=list(self.players.values()),
                Primes=self.card_primes,
                Deck=self.deck,
                DiscardPile=self.discard_pile,
                Spots=self.board_spots,
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
    game = Game(2, verbose=True)
    game.play()
