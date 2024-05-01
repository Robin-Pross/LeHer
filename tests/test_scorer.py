import unittest

from Decks import STANDARD_DECK
from Scorer import STANDARD_SCORER


class TestScorer(unittest.TestCase):
    def test_default_scorer(self):
        expected_values_of_standard_deck_of_52 = [
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1,
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1
        ]
        for card, value in zip(STANDARD_DECK, expected_values_of_standard_deck_of_52):
            self.assertEqual(STANDARD_SCORER(card), value)
