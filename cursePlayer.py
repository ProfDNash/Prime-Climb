import numpy as np


def find_curse_target(current_player: int, players: dict) -> int:
    """
    Helper function to choose a target to curse if any options exist
    input:
        current_player -- an integer index of the current player
        players -- a dictionary of player classes

    output:
        player_to_curse: An integer index of the player to target or None
    """
    potential_targets = [
        idx
        for idx, player in players.items()
        if idx != current_player and not player.cursed
    ]
    if not potential_targets:
        return None

    # Choose a player to curse
    player_to_curse = np.random.choice(potential_targets)

    return player_to_curse
