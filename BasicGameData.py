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


def initGame(numPlayers):
    if numPlayers < 1 or numPlayers > 4:
        print("Error, can only be played with 1 to 4 players")
    else:
        PlayerList = [Player() for _ in range(numPlayers)]
        PlayerList = PlayerList[:numPlayers]
        ##Shuffle the deck of cards
        Deck = np.arange(1, 25)
        Deck = np.random.permutation(Deck)
    return PlayerList, Deck


def rollGenerator(n):
    r = np.random.randint(1, high=n + 1, size=2)
    return r
