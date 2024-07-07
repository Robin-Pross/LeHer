import unittest

from code.Decks import STANDARD_DECK
from code.Scorer import standard_scorer


class TestScorer(unittest.TestCase):
    def test_default_scorer(self):
        expected_values_of_standard_deck_of_52 = [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1
        ]
        for card, value in zip(STANDARD_DECK, expected_values_of_standard_deck_of_52):
            self.assertEqual(standard_scorer(card), value)
