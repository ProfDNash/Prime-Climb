import numpy as np


def cursePlayer(card, playerNum, PlayerList, DiscardPile):
    """
    CURSE PLAYER FUNCTION
    input: card -- an integer representing a card (can only curse if card == 12 or card == 13)
        playerNum -- an integer index of the current player
        PlayerList -- a list of player classes
        DiscardPile -- an integer list of cards that have been discarded

    output: PlayerList -- updated with a player cursed and a card removed from the current
                        player's hand
            DiscardPile -- updated with the played card added to the discard pile
    """
    if card != 12 and card != 13:
        raise ValueError(f"You cannot curse with card: {card}")  ##for debugging

    # Only curse other players if any aren't cursed
    potential_targets = [
        idx
        for idx, player in enumerate(PlayerList)
        if idx != playerNum and not player.cursed
    ]
    if not potential_targets:
        return PlayerList, DiscardPile

    # Choose a player to curse
    player_to_curse = np.random.choice(potential_targets)

    PlayerList[player_to_curse].curse()

    # Remove the card if it can actually be played
    PlayerList[playerNum].cards.remove(card)
    # Add the card to the discard pile
    DiscardPile.append(card)

    return PlayerList, DiscardPile
