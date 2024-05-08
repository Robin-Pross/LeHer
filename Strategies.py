from Scorer import standard_scorer


class Strategy:
    """
    Do not create instances of this.
    This class is supposed to be used as superclass for other strategies.
    """

    def __init__(self, is_player: bool, scorer=standard_scorer):
        """
        Makes the parameters class variables with the same name and value.

        :param is_player: whether this instance of the strategy is used by the player
        :param scorer: the scorer that is used
        """
        self.scorer = scorer
        self.is_player = is_player

    def action(self, my_cards, revealed_player_cards, revealed_dealer_cards, player_trade_history,
               dealer_redraw_history, current_turn):
        return False


class KeepNAndAbove(Strategy):
    def __init__(self, n: int, is_player: bool, scorer=standard_scorer):
        """
        Makes the parameters class variables with the same name and value.

        :param is_player: whether this instance of the strategy is used by the player
        :param n: the threshold
        :param scorer: the scorer that is used
        """
        super().__init__(is_player=is_player, scorer=scorer)
        self.threshold = n

    def action(self, my_cards, revealed_player_cards, revealed_dealer_cards, player_trade_history,
               dealer_redraw_history, current_turn: int):
        """
        Returns False if the value of the current card is at least the threshold n,
        which was set during instance creation.
        Returns True otherwise.


        :param my_cards: the list of cards
        :param current_turn: the current turn
        :param revealed_player_cards: not used.
        :param revealed_dealer_cards: not used.
        :param player_trade_history: not used.
        :param dealer_redraw_history: not used.
        """
        return self.scorer(my_cards[current_turn]) < self.threshold
