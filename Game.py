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
from Player import Player
from src.utilities.constants import CARD_PRIMES
from cursePlayer import find_curse_target
from drawACard import drawACard
from moveMapper import moveMapper
from sendPlayerHome import find_send_home_target


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
        self.game_over = False

    def _next_player(self):
        self.current_player = (self.current_player + 1) % self.number_of_players

    def _resolve_collisions(self) -> None:
        """
        If the current player ends their turn on the same location as another player
        they bump that player's pawns back to the start
        """
        potential = set(self.players[self.current_player].position).difference({0, 101})

        # If current player is only at 0 and/or 101, there will be nothing to bump
        if not potential:
            return None

        for idx, player in self.players.items():
            # self-bumping is taken care of in the generation of new positions
            if idx == self.current_player or not set(player.position).intersection(
                potential
            ):
                continue

            new_position = [
                spot if spot not in potential else 0 for spot in player.position
            ]
            new_position.sort()
            self.players[idx].position = tuple(new_position)
            if self.verbose:
                print(f"Player {idx} was bumped!")

        return None

    def _take_turn(self, PlayerList, Primes, Deck, DiscardPile, Spots):
        ##at the start of the turn, randomly decide whether to curse another player (if the card is available)
        existing_curse_cards = set(
            self.players[self.current_player].cards
        ).intersection({12, 13})
        while existing_curse_cards and np.random.choice([True, False]):
            card = existing_curse_cards.pop()
            curse_target = find_curse_target(
                current_player=self.current_player, players=self.players
            )
            if curse_target is None:
                break

            self.players[curse_target].curse()
            # Remove the card that has been played
            self.players[self.current_player].cards.remove(card)
            self.discard_pile.append(card)

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
            self.game_over = True
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
        self._resolve_collisions()

        ##undo any curses at the end of the turn
        if self.players[self.current_player].cursed:
            self.players[self.current_player].cursed = False
            if self.verbose:
                print(f"Player {self.current_player} is no longer cursed")

        # if the player did not use the send home cards to augment their own move,
        # they can choose to send someone else back as part of their turn
        existing_home_cards = set(self.players[self.current_player].cards).intersection(
            {10, 11}
        )
        while existing_home_cards and np.random.choice([True, False]):
            card = existing_home_cards.pop()
            send_home_target, send_home_pawn = find_send_home_target(
                current_player=self.current_player, players=self.players
            )
            # bump that pawn back to start and discard the card played
            self.players[send_home_target].position[send_home_pawn] = 0
            self.players[send_home_target].position.sort()
            self.players[self.current_player].cards.remove(card)
            self.discard_pile.append(card)

        ## after all actions, check to see if they get to draw a card
        rollAgain, PlayerList, Deck, DiscardPile = drawACard(
            self.current_player, pos, Move[0:2], PlayerList, Primes, Deck, DiscardPile
        )

        # Drawing an action card could cause another collision. So re-resolve
        self._resolve_collisions()

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
        while not self.game_over:
            intermediate_players, self.deck, self.discard_pile = self._take_turn(
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

        return self.number_of_turns, self.current_player


if __name__ == "__main__":
    game = Game(2, verbose=True)
    game.play()
