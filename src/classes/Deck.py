import numpy as np


class Deck:
    """
    Class to manage the deck of cards in Prime Climb
    """

    def __init__(self):
        self.draw_pile = [int(card) for card in np.random.permutation(range(1, 25))]
        self.discard_pile = []

    def __repr__(self):
        return f"Draw Pile: {self.draw_pile}\nDiscard Pile: {self.discard_pile}"

    def _shuffle(self):
        if self.draw_pile:
            raise Exception("We shouldn't shuffle until the draw pile is empty")

        print("RESHUFFLING THE DISCARD PILE")
        self.draw_pile = [
            int(card) for card in np.random.permutation(self.discard_pile)
        ]
        self.discard_pile = []

    def draw_a_card(self) -> int:
        card = self.draw_pile.pop()
        if not self.draw_pile:
            self._shuffle()

        return card

    def discard_a_card(self, card: int):
        self.discard_pile.append(card)
