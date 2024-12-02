import numpy as np
from src.utilities.constants import CARD_PRIMES


class Player:
    """
    Class to keep track of the state of a player during the game.
    Args:
        low_position: An integer from 0 - 101
        high_position: An integer from 0 - 101
            (> than low_position unless both are 0 or both are 101)
        cards: A list of keeper cards in the players hand
        cursed: Whether the player has been cursed to only use - or / on next turn
    """

    def __init__(
        self,
        position1: int = 0,
        position2: int = 0,
        cards: list = None,
        cursed: bool = False,
    ):
        self.position = [position1, position2]
        self._validate_positions()
        self.cards = cards if cards is not None else []
        self.cursed = cursed

    def _validate_positions(self) -> None:
        self.position.sort()

    def curse(self):
        if self.cursed:
            raise Exception("Cannot curse a player that is already cursed")

        self.cursed = True

    def landed_on_prime(self, old_position: list) -> list:
        """
        Helper function to determine whether a pawn *moved* to a new prime
        Note: Given how things are currently tracked, this logic is not strictly correct
        """
        on_a_prime = [False, False]
        for idx, spot in enumerate(self.position):
            if spot not in old_position and spot in CARD_PRIMES:
                on_a_prime[idx] = True

        return on_a_prime


def rollGenerator(n):
    r = np.random.randint(1, high=n + 1, size=2)
    return r
