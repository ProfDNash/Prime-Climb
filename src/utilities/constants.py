from enum import Enum


# Primes on the board which result in drawing a prime card
CARD_PRIMES = [
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
]


class KeeperCards(Enum):
    PLUS_MINUS_1 = 1
    PLUS_MINUS_2 = 2
    PLUS_MINUS_3 = 3
    PLUS_MINUS_4 = 4
    PLUS_MINUS_5 = 5
    PLUS_MINUS_6 = 6
    PLUS_MINUS_7 = 7
    PLUS_MINUS_8 = 8
    PLUS_MINUS_9 = 9
    BUMP_BACK_TO_START_1 = 10
    BUMP_BACK_TO_START_2 = 11
    CURSE_1 = 12
    CURSE_2 = 13


class ActionCards(Enum):
    ROLL_AGAIN_1 = 14
    ROLL_AGAIN_2 = 15
    ROLL_AGAIN_3 = 16
    BELOW_50_ADD_50 = 17
    BELOW_50_DOUBLE = 18
    FORWARD_TO_NEAREST = 19
    BACKWARD_TO_NEAREST = 20
    REVERSE_DIGITS = 21
    SWAP_TWO_PAWNS = 22
    SEND_TO_64 = 23
    STEAL_A_CARD = 24
