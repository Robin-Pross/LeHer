import os
import unittest

from code.LeHer import LeHer
from code.Decks import STANDARD_DECK


class TestAutoPlay(unittest.TestCase):
    TEST_OUTPUT_DIRECTORY = "test_outputs/"

    def delete_old_test_file(self, file_name):
        if file_name[:-5] != ".json":
            file_name = file_name + ".json"
        if os.path.isfile(self.TEST_OUTPUT_DIRECTORY + file_name):
            os.remove(self.TEST_OUTPUT_DIRECTORY + file_name)

    def test_only_seven_of_spades_redraw(self):
        file_name = "only Kings redraw"
        self.delete_old_test_file(file_name)
        game = LeHer(UNSHUFFLED_DECK=["7S"])
        results = game.auto_play(AUTO_PLAY_LOG_DIR=self.TEST_OUTPUT_DIRECTORY, auto_play_log_filename=file_name,
                                 GAMES_TO_AUTOPLAY=1, REMOVE_DRAWN_CARDS_FROM_DECK=False, SILENT_MODE=True,
                                 LOG_ALL=True)
        self.assertEqual(results["player_scores"], [91])
        self.assertEqual(results["dealer_scores"], [91])
        self.assertEqual(results["player_histories"], [["SUCCEEDED"] * 13])
        self.assertEqual(results["dealer_histories"], [["SUCCEEDED"] * 13])
        self.assertEqual(results["player_cards"], [["7S"] * 13])
        self.assertEqual(results["dealer_cards"], [["7S"] * 13])
        self.assertEqual(results["decks"], [["7S"] * 27])

    def test_only_seven_of_spades_no_redraw(self):
        file_name = "only Kings no redraw"
        self.delete_old_test_file(file_name)
        game = LeHer(UNSHUFFLED_DECK=["7S"] * 27)
        results = game.auto_play(AUTO_PLAY_LOG_DIR=self.TEST_OUTPUT_DIRECTORY, auto_play_log_filename=file_name,
                                 GAMES_TO_AUTOPLAY=1, REMOVE_DRAWN_CARDS_FROM_DECK=True, SILENT_MODE=True,
                                 LOG_ALL=True)
        self.assertEqual(results["player_scores"], [91])
        self.assertEqual(results["dealer_scores"], [91])
        self.assertEqual(results["player_histories"], [["SUCCEEDED"] * 13])
        self.assertEqual(results["dealer_histories"], [["SUCCEEDED"] * 13])
        self.assertEqual(results["player_cards"], [["7S"] * 13])
        self.assertEqual(results["dealer_cards"], [["7S"] * 13])
        self.assertEqual(results["decks"], [["7S"] * 27])

    def test_deck_in_order_no_redraw(self):
        file_name = "deck in order no redraw"
        self.delete_old_test_file(file_name)
        game = LeHer(PRE_SHUFFLED_DECK=STANDARD_DECK)
        results = game.auto_play(AUTO_PLAY_LOG_DIR=self.TEST_OUTPUT_DIRECTORY, auto_play_log_filename=file_name,
                                 GAMES_TO_AUTOPLAY=1, REMOVE_DRAWN_CARDS_FROM_DECK=True, SILENT_MODE=True,
                                 LOG_ALL=True)
        self.assertEqual(results["player_scores"], [85])
        self.assertEqual(results["dealer_scores"], [91])
        self.assertEqual(results["player_histories"], [
            ["ATTEMPTED_BUT_FAILED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED",
             "SUCCEEDED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED", "SUCCEEDED"]
        ])
        self.assertEqual(results["dealer_histories"], [
            ["NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED", "SUCCEEDED",
             "ATTEMPTED_BUT_FAILED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED",
             "SUCCEEDED"]
        ])
        self.assertEqual(results["player_cards"],
                         [['AS', 'QS', '10S', '8S', '5S', '3S', 'AH', 'KH', 'JH', '9H', '6H', '4H', '2H']])
        self.assertEqual(results["dealer_cards"],
                         [['KS', 'JS', '9S', '6S', '4S', '2S', '7S', 'QH', '10H', '8H', '5H', '3H', 'AD']])
        self.assertEqual(results["decks"], [STANDARD_DECK])

    def test_deck_in_order_redraw(self):
        file_name = "deck in order redraw"
        self.delete_old_test_file(file_name)
        game = LeHer(PRE_SHUFFLED_DECK=STANDARD_DECK)
        # setting rng is not necessary as it is only used when generating new cards from the deck
        # when using a pre_shuffled_deck no new cards are generated
        results = game.auto_play(AUTO_PLAY_LOG_DIR=self.TEST_OUTPUT_DIRECTORY, auto_play_log_filename=file_name,
                                 GAMES_TO_AUTOPLAY=1, REMOVE_DRAWN_CARDS_FROM_DECK=False, SILENT_MODE=True,
                                 LOG_ALL=True)
        self.assertEqual(results["player_scores"], [85])
        self.assertEqual(results["dealer_scores"], [91])
        self.assertEqual(results["player_histories"], [
            ["ATTEMPTED_BUT_FAILED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED",
             "SUCCEEDED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED", "SUCCEEDED"]
        ])
        self.assertEqual(results["dealer_histories"], [
            ["NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED", "SUCCEEDED",
             "ATTEMPTED_BUT_FAILED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "NOT_ATTEMPTED", "SUCCEEDED", "SUCCEEDED",
             "SUCCEEDED"]
        ])
        self.assertEqual(results["player_cards"],
                         [['AS', 'QS', '10S', '8S', '5S', '3S', 'AH', 'KH', 'JH', '9H', '6H', '4H', '2H']])
        self.assertEqual(results["dealer_cards"],
                         [['KS', 'JS', '9S', '6S', '4S', '2S', '7S', 'QH', '10H', '8H', '5H', '3H', 'AD']])
        self.assertEqual(results["decks"], [STANDARD_DECK])
