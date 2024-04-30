def STANDARD_SCORER(card):
    """
    Returns an int with the rank of the card.
    Aces have a score of 1.
    Numbered cards have their number as score.
    Jack, Queen and King score as 11, 12 and 13 respectively.
    The suite of the card does not affect the score.

    Card parameter has to be in the format XY where X is either an integer, 'A', 'J', 'Q' or 'K' and Y has to be
    a single Character (suites would be 'C', 'D', 'H' and 'S' but as they are not used any Character is accepted)

    :param card: the card to score
    :return: returns the integer score of the card
    """
    # suite = card[-1]
    rank = card[:-1]
    match rank:
        case "A":
            return 1
        case "J":
            return 11
        case "Q":
            return 12
        case "K":
            return 13
        case _:
            return int(rank)