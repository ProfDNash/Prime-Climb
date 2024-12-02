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
from src.classes.Deck import Deck
from src.utilities.constants import ActionCards, CARD_PRIMES, KeeperCards
from cursePlayer import find_curse_target
from moveMapper import moveMapper
from sendPlayerHome import find_send_home_target


class Game:
    def __init__(self, number_of_players: int = 1, verbose: bool = False):
        self.number_of_players = number_of_players
        self.verbose = verbose
        self.players = {idx: Player() for idx in range(self.number_of_players)}
        self.deck = Deck()
        self.number_of_turns = 0
        self.board_spots = np.arange(102)
        self.current_player = 0
        self.card_primes = CARD_PRIMES
        self.game_over = False

    def _next_player(self):
        self.current_player = (self.current_player + 1) % self.number_of_players

    def _get_active_pawns(self):
        # Ignore any pawns which have made it to 101 and left the board
        all_pawns = []
        for player in self.players.values():
            all_pawns += player.position

        return sorted([pawn for pawn in all_pawns if pawn < 101])

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
            self.players[idx].position = new_position
            if self.verbose:
                print(f"Player {idx} was bumped!")

        return None

    def _apply_action_card(self, card: int, chosen_pawn: int) -> bool:
        # Cards 14, 15, and 16 correspond to rolling again
        if card < 17:
            return True

        new_position = self.players[self.current_player].position
        if card == 17:  # 50/50 type 1 -- below 50 add 50
            if new_position[chosen_pawn] < 50:
                new_position[chosen_pawn] += 50
            else:
                new_position[chosen_pawn] -= 50

        if card == 18:  # 50/50 type 2 -- below 50, double
            if new_position[chosen_pawn] < 50:
                new_position[chosen_pawn] *= 2
            else:
                new_position[chosen_pawn] -= 10

        if card in {19, 20}:  # more forward/backward to nearest pawn
            active_pawns = self._get_active_pawns()
            # Find the chosen pawn from among the list
            idx = active_pawns.index(new_position[chosen_pawn])
            # To move forward, the chosen pawn can't be farthest forward
            if idx < len(active_pawns) - 1 and card == 19:
                new_position[chosen_pawn] = active_pawns[idx + 1]
            # To move backward, the chosen pawn can't be farthest backward
            elif idx > 0 and card == 20:
                new_position[chosen_pawn] = active_pawns[idx - 1]

        if card == 21:  # reverse digits
            new_position[chosen_pawn] = int(str(new_position[chosen_pawn])[::-1])

        # If there's only one player, swapping pawn is meaningless
        if card == 22 and self.number_of_players > 1:  # Swap any two pawns
            # Choose two distinct players
            player1, player2 = np.random.choice(
                list(self.players.keys()), size=2, replace=False
            )
            new_position1 = self.players[player1].position
            new_position2 = self.players[player2].position
            # Choose a pawn for the first player
            pawn1 = np.random.choice(
                [idx for idx, pawn in enumerate(new_position1) if pawn != 101]
            )
            # Choose a pawn for the second player
            pawn2 = np.random.choice(
                [idx for idx, pawn in enumerate(new_position2) if pawn != 101]
            )

            ##Swap the two pawns
            new_position1[pawn1], new_position2[pawn2] = (
                new_position2[pawn2],
                new_position1[pawn1],
            )
            new_position1.sort()
            new_position2.sort()
            self.players[player1].position = new_position1
            self.players[player2].position = new_position2
            return False

        if card == 23:  # Send to 64
            new_position[chosen_pawn] = 64

        if card == 24:  # Steal a card
            # First find the other players who have cards
            potential_targets = [
                idx
                for idx, player in self.players.items()
                if idx != self.current_player and player.cards
            ]

            # If at least one other player has cards, choose one randomly
            # and then choose a random card from their hand
            if potential_targets:
                chosen_target = np.random.choice(potential_targets)
                chosen_card = np.random.choice(self.players[chosen_target].cards)
                self.players[chosen_target].cards.remove(chosen_card)
                self.players[self.current_player].cards.append(chosen_card)

        # The player could have landed on themselves
        if new_position[0] == new_position[1]:
            new_position[0] = 0

        # Reset the player position in the class attribute
        self.players[self.current_player].position = new_position
        return False

    def _take_turn(self):
        roll_again = False
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
            self.deck.discard_a_card(card)

        ##Get the current player position, roll the dice, and generate the possible moves
        old_position = self.players[self.current_player].position
        roll = [np.random.randint(0, 10), np.random.randint(0, 10)]
        if self.verbose:
            print(f"Player {self.current_player} rolled: {roll}")
        possibleMoves = moveMapper(
            roll,
            old_position,
            self.players[self.current_player].cards,
            self.players[self.current_player].cursed,
            Spots=self.board_spots,
        )

        ##choose to win if you can
        if 101 in possibleMoves[:, 0]:
            Move = np.array([101, 101]).reshape((1, 2))
            print(f"Player {self.current_player} wins!!!!")
            self.game_over = True
            return None
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
                        self.players[self.current_player].cards.remove(i)
                        self.deck.discard_a_card(i)

        ##Change the current player's position to the newly chosen one (drop the card encoding)
        self.players[self.current_player].position = list(Move[0:2])
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
            print(f"{send_home_target=}, {send_home_pawn=}")
            # bump that pawn back to start and discard the card played
            self.players[send_home_target].position[send_home_pawn] = 0
            self.players[send_home_target].position.sort()
            self.players[self.current_player].cards.remove(card)
            self.deck.discard_a_card(card)

        ## after all actions, check to see if they get to draw a card
        pawn_on_prime = self.players[self.current_player].landed_on_prime(old_position)
        if any(pawn_on_prime):
            new_card = self.deck.draw_a_card()
        else:
            new_card = None

        if new_card in KeeperCards:
            self.players[self.current_player].cards.append(new_card)

        if new_card in ActionCards:
            # For many of these actions, we must apply the action to the pawn which drew
            # the card. If both are on new primes, we'll choose one randomly
            chosen_pawn = np.random.choice(
                [idx for idx, flag in enumerate(pawn_on_prime) if flag]
            )
            roll_again = self._apply_action_card(card=new_card, chosen_pawn=chosen_pawn)
            self.deck.discard_a_card(new_card)

        # Drawing an action card could cause another collision. So re-resolve
        self._resolve_collisions()

        if roll_again:
            if self.verbose:
                print(f"Player {self.current_player} gets to roll again!")

            return None
        else:  ##move to next player
            self._next_player()
            return None

    def play(self):
        """
        Method which plays the game until someone wins
        """
        while not self.game_over:
            self._take_turn()
            print(self.deck)
            self.number_of_turns += 1
            if self.number_of_turns > 1000:
                print("Something is wrong")  ##for debugging
                break

        return self.number_of_turns, self.current_player


if __name__ == "__main__":
    game = Game(2, verbose=True)
    game.play()
