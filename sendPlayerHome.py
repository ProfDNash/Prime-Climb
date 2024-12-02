"""
SEND PLAYER HOME FUNCTION
input: card -- an integer representing the card (can only send home if card==10 or card==11)
       playerNum -- the index of the current player
       PlayerList -- a list of player classes
       DiscardPile -- a list of the cards which have been discarded

output: PlayerList -- updated with any new positions and hands
        DiscardPile -- updated with added card played (if any)

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.

@author: David A. Nash
"""

import numpy as np


def find_send_home_target(current_player: int, players: dict) -> tuple:
    """
    Helper function to find all pawns (identified by player and index) which
    are not on the start (0) or the end (101) and which can be bumped back to start
    Args:
        current_player (int): the index of the current player
        players (dict): A dictionary of Player classes

    output:
        player_to_send_home: A tuple of the chosen player index and pawn index
    """
    potential_targets = [
        (idx, pos)
        for idx, player in players.items()
        for pos, spot in enumerate(player.position)
        if idx != current_player and spot not in {0, 101}
    ]

    if not potential_targets:
        print("No one to bump")  # For debugging
        return None

    ##choose a random player and pawn from the list of options
    choice = np.random.choice(range(len(potential_targets)))
    player_pawn_to_send_home = potential_targets[choice]

    return player_pawn_to_send_home
