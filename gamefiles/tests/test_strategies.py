import unittest

from code.Decks import STANDARD_DECK
from code.Strategies import KeepNAndAbove
from code.Scorer import standard_scorer


class TestKeepNAndAbove(unittest.TestCase):
    def test_n_equals_1(self):
        dealer_strategy = KeepNAndAbove(n=1, is_player=False, scorer=standard_scorer)
        player_strategy = KeepNAndAbove(n=1, is_player=True, scorer=standard_scorer)
        for card in STANDARD_DECK:
            self.assertFalse(player_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ))
            self.assertFalse(dealer_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ))

    def test_n_equals_14(self):
        dealer_strategy = KeepNAndAbove(n=14, is_player=False, scorer=standard_scorer)
        player_strategy = KeepNAndAbove(n=14, is_player=True, scorer=standard_scorer)
        for card in STANDARD_DECK:
            self.assertTrue(player_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ))
            self.assertTrue(dealer_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ))

    def test_n_equals_8(self):
        # returns true if strategy is to trade which is only the case if the score of the card is less than 8
        dealer_strategy = KeepNAndAbove(n=8, is_player=False, scorer=standard_scorer)
        player_strategy = KeepNAndAbove(n=8, is_player=True, scorer=standard_scorer)
        for card in STANDARD_DECK:
            self.assertEqual(player_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ), (standard_scorer(card) < 8))
            self.assertEqual(dealer_strategy.action(
                my_cards=[card], current_turn=0,
                revealed_player_cards=None, revealed_dealer_cards=None,
                dealer_redraw_history=None, player_trade_history=None
            ), (standard_scorer(card) < 8))
