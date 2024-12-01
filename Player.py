import numpy as np


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
        low_position: int = 0,
        high_position: int = 0,
        cards: list = None,
        cursed: bool = False,
    ):
        self.position = (
            low_position,
            high_position,
        )  # Maintain for backwards compatibility for now
        self.low_position = low_position
        self.high_position = high_position
        self.cards = cards if cards is not None else []
        self.cursed = cursed

    def _validate_positions(self) -> None:
        """
        Helper method to ensure low_position < high_position
        """
        if (
            self.low_position < self.high_position
            or self.low_position == 0
            or self.high_position == 101
        ):
            return None

        self.low_position, self.high_position = self.high_position, self.low_position
        # Keep general position for now -- remove later
        self.position = (self.low_position, self.high_position)

    def curse(self):
        if self.cursed:
            raise Exception("Cannot curse a player that is already cursed")

        self.cursed = True


def rollGenerator(n):
    r = np.random.randint(1, high=n + 1, size=2)
    return r
