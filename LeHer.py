import random
import time
import math

from Decks import STANDARD_DECK
from Scorer import STANDARD_SCORER
from Strategies import KeepNAndAbove
import DataProcessing


class LeHer:
    def __init__(self, *,
                 UNSHUFFLED_DECK=None, TURNS_PER_GAME=13,
                 SCORER=STANDARD_SCORER, PLAYER_AI=KeepNAndAbove(n=8, is_player=True),
                 DEALER_AI=KeepNAndAbove(n=8, is_player=False),
                 gui_language="EN",
                 RNG_SEED=None, PRE_SHUFFLED_DECK=None,
                 HIDE_UNKNOWN_CARDS=True):
        """
        Sets parameters that stay the same for every game played.
        Does not launch the gui or play with AI against AI.
        Does not prepare the game in any way (shuffle deck, etc.)
        Call function auto_play or launch_gui on instance of the game to start.

        :param UNSHUFFLED_DECK: the deck to be used, is STANDARD_DECK by default
        :param TURNS_PER_GAME: the amount of turns per game
        :param SCORER: the scorer
        :param PLAYER_AI: the player AI
        :param DEALER_AI: the dealer AI
        :param gui_language: the language of the text in the gui
        :param RNG_SEED: the rng seed
        :param PRE_SHUFFLED_DECK: the deck to be used instead of using a shuffled version of the unshuffled deck
        :param HIDE_UNKNOWN_CARDS: whether cards that the user does not know are hidden or revealed
        """
        if RNG_SEED is not None:
            random.seed(RNG_SEED)
        if UNSHUFFLED_DECK is None:
            self.UNSHUFFLED_DECK = STANDARD_DECK
        else:
            self.UNSHUFFLED_DECK = UNSHUFFLED_DECK
        self.TURNS_PER_GAME = TURNS_PER_GAME
        self.SCORER = SCORER
        self.PLAYER_AI = PLAYER_AI
        self.DEALER_AI = DEALER_AI
        self.PRE_SHUFFLED_DECK = PRE_SHUFFLED_DECK
        self.HIDE_UNKNOWN_CARDS = HIDE_UNKNOWN_CARDS

        self.is_player = None
        self.remove_drawn_cards_from_deck = None
        self.turn_count = None
        self.player_cards = None
        self.player_shown_cards = None
        self.dealer_shown_cards = None
        self.player_card_labels = None
        self.dealer_card_labels = None
        self.player_score = None
        self.player_history = None
        self.dealer_cards = None
        self.dealer_score = None
        self.dealer_history = None
        self.revealed_player_cards_to_dealer = None
        self.revealed_dealer_cards_to_player = None
        self.shuffled_deck = None
        self.current_deck = None
        self.next_player_card = None

    def auto_play(self, GAMES_TO_AUTOPLAY, AUTO_PLAY_LOG_DIR, AUTO_PLAY_LOG_FILENAME, REMOVE_DRAWN_CARDS_FROM_DECK,
                  SILENT_MODE=False, LOG_ALL=False):
        """
        Plays a specified amount of games with the player AI against the dealer AI with no user input.
        Gives a progress update every percent of games played which includes current percent done, time since start and
        time since last percent.

        :param GAMES_TO_AUTOPLAY: the amount of games to play
        :param AUTO_PLAY_LOG_DIR: the directory of the log file (relative or absolute)
        :param AUTO_PLAY_LOG_FILENAME: the name of the log file (with .json extension)
        :param REMOVE_DRAWN_CARDS_FROM_DECK: whether cards drawn should be removed from the deck
        :param SILENT_MODE: turns off progress updates in console
        :param LOG_ALL: whether everything should be logged or only the scores
        :return: returns a dictionary with the results of the games (as well as any previous games from the same file)
                 see get_results in DataProcessing for more info
        """
        # add .json at the end if not already present
        if AUTO_PLAY_LOG_FILENAME[:-5] != ".json":
            AUTO_PLAY_LOG_FILENAME = AUTO_PLAY_LOG_FILENAME + ".json"
        current_game = 0
        logger = DataProcessing.StaggeredLogger(AUTO_PLAY_LOG_DIR, AUTO_PLAY_LOG_FILENAME)
        start_time = time.time()
        time_since_last_interval_completion = time.time()
        while GAMES_TO_AUTOPLAY > current_game:
            self.reset_state(None, REMOVE_DRAWN_CARDS_FROM_DECK)
            current_turn = 0
            while self.TURNS_PER_GAME > current_turn:
                self.draw_cards()
                if self.PLAYER_AI.action(self.player_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, current_turn):
                    self.player_action()
                else:
                    self.player_history.append("NOT_ATTEMPTED")
                if self.DEALER_AI.action(self.dealer_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, current_turn):
                    self.dealer_action()
                else:
                    self.dealer_history.append("NOT_ATTEMPTED")
                current_turn += 1
            self.score()
            if LOG_ALL:
                logger.add_game(player_score=self.player_score, dealer_score=self.dealer_score,
                                player_cards=self.player_cards, dealer_cards=self.dealer_cards,
                                player_history=self.player_history, dealer_history=self.dealer_history,
                                deck_to_start_of_game=self.shuffled_deck)
            else:
                logger.add_game(player_score=self.player_score, dealer_score=self.dealer_score)
            current_game += 1
            if not SILENT_MODE:
                for i in range(0, 100):
                    if current_game == math.floor(i * 0.01 * GAMES_TO_AUTOPLAY):
                        end_time = time.time()
                        print(str(i) + "% Done (" + str(end_time - start_time) + ") (" + str(
                            end_time - time_since_last_interval_completion) + ")")
                        time_since_last_interval_completion = time.time()
        logger.log_staggered_games()
        if LOG_ALL:
            return DataProcessing.get_results(output_folder=AUTO_PLAY_LOG_DIR, file_name=AUTO_PLAY_LOG_FILENAME,
                                              include_scores=True, include_deck=True, include_cards=True,
                                              include_history=True)
        else:
            return DataProcessing.get_results(output_folder=AUTO_PLAY_LOG_DIR, file_name=AUTO_PLAY_LOG_FILENAME,
                                              include_scores=True)

    def reset_state(self, is_player, remove_drawn_cards_from_deck):
        """
        Resets the state of all logic elements.
        Does not reset the gui.

        :param is_player: whether the user is the player
        :param remove_drawn_cards_from_deck:  whether cards drawn from the deck should be removed
        """
        self.next_player_card = None
        self.is_player = is_player
        self.remove_drawn_cards_from_deck = remove_drawn_cards_from_deck
        self.turn_count = 0
        self.player_cards = []
        self.player_shown_cards = []
        self.dealer_shown_cards = []
        self.player_card_labels = []
        self.dealer_card_labels = []
        self.player_score = 0
        self.player_history = []
        self.dealer_cards = []
        self.dealer_score = 0
        self.dealer_history = []
        self.revealed_player_cards_to_dealer = []
        self.revealed_dealer_cards_to_player = []
        for i in range(0, self.TURNS_PER_GAME):
            self.revealed_player_cards_to_dealer.append(False)
            self.revealed_dealer_cards_to_player.append(False)
        # Copy of deck is used to reset / reshuffle if the user plays more than one game.
        if self.PRE_SHUFFLED_DECK is not None:
            self.shuffled_deck = self.PRE_SHUFFLED_DECK[:]
        else:
            self.shuffled_deck = self.UNSHUFFLED_DECK[:]
            random.shuffle(self.shuffled_deck)
        # Copy of shuffled deck is used in case the state of the deck at the start of the game gets logged.
        self.current_deck = self.shuffled_deck[:]
        # Created Cards are appended to shuffled deck if drawn cards are not removed from the deck instead
        if not self.remove_drawn_cards_from_deck and self.PRE_SHUFFLED_DECK is None:
            self.shuffled_deck = []

    def draw_cards(self):
        """
        Add a card to both the player and dealer
        """
        if not self.remove_drawn_cards_from_deck and self.PRE_SHUFFLED_DECK is None:
            if self.next_player_card is None:
                self.player_cards.append(random.choice(self.current_deck))
                self.shuffled_deck.append(self.player_cards[-1])
            else:
                self.player_cards.append(self.next_player_card)
                self.next_player_card = None
            self.dealer_cards.append(random.choice(self.current_deck))
            self.shuffled_deck.append(self.dealer_cards[-1])
        else:
            self.player_cards.append(self.current_deck.pop())
            self.dealer_cards.append(self.current_deck.pop())

    def player_action(self):
        """
        Attempts to trade with the dealer.
        Fails if the dealers current card is a king.
        Changes player history and revealed status.
        """
        if self.dealer_cards[-1][0] == "K":
            self.player_history.append("ATTEMPTED_BUT_FAILED")
            return
        self.player_history.append("SUCCEEDED")
        self.revealed_dealer_cards_to_player[self.turn_count] = True
        self.revealed_player_cards_to_dealer[self.turn_count] = True
        temp = self.player_cards[-1]
        self.player_cards[-1] = self.dealer_cards[-1]
        self.dealer_cards[-1] = temp

    def dealer_action(self):
        """
        Attempts to redraw their card for the dealer.
        Fails if the next card in the deck is a king.
        Changes dealer history and revealed status.
        """
        if not self.remove_drawn_cards_from_deck and self.PRE_SHUFFLED_DECK is None:
            new_card = random.choice(self.current_deck)
            self.shuffled_deck.append(new_card)
            if new_card[0] == "K":
                self.dealer_history.append("ATTEMPTED_BUT_FAILED")
                self.next_player_card = new_card
                return
            self.next_player_card = self.dealer_cards[-1]
            self.dealer_cards[-1] = new_card
            self.revealed_dealer_cards_to_player[self.turn_count] = False
            if self.turn_count + 1 < self.TURNS_PER_GAME:
                self.revealed_player_cards_to_dealer[self.turn_count + 1] = True
            self.dealer_history.append("SUCCEEDED")
            return
        if self.current_deck[-1][0] == "K":
            self.dealer_history.append("ATTEMPTED_BUT_FAILED")
            return
        self.dealer_history.append("SUCCEEDED")
        temp = self.current_deck.pop()
        self.current_deck.append(self.dealer_cards[-1])
        self.dealer_cards[-1] = temp
        self.revealed_dealer_cards_to_player[self.turn_count] = False
        if self.turn_count + 1 < self.TURNS_PER_GAME:
            self.revealed_player_cards_to_dealer[self.turn_count + 1] = True

    def score(self):
        """
        Updates player and dealer scores for every card.
        Only call once at the end.
        """
        for card in self.player_cards:
            self.player_score += self.SCORER(card)
        for card in self.dealer_cards:
            self.dealer_score += self.SCORER(card)
