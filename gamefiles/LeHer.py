import random
import time
import math

from Decks import STANDARD_DECK
from Scorer import standard_scorer
from Strategies import KeepNAndAbove
import DataProcessing


class LeHer:
    def __init__(self, *,
                 UNSHUFFLED_DECK=STANDARD_DECK, SCORER=standard_scorer, PLAYER_AI=KeepNAndAbove(n=8, is_player=True),
                 DEALER_AI=KeepNAndAbove(n=8, is_player=False),
                 RNG_SEED=None, PRE_SHUFFLED_DECK=None, TURNS_PER_GAME=13):
        """
        Sets parameters that stay the same for every game played.
        Does not launch the gui or play with AI against AI.
        Does not prepare the game in any way (shuffle deck, etc.)
        Call function auto_play or launch_gui on instance of the game to start.

        :param UNSHUFFLED_DECK: the deck to be used, standard deck of 52 by default
        :param SCORER: the scorer
        :param PLAYER_AI: the player AI
        :param DEALER_AI: the dealer AI
        :param RNG_SEED: the rng seed
        :param PRE_SHUFFLED_DECK: the deck to be used instead of using a shuffled version of the unshuffled deck
        :param TURNS_PER_GAME: the amount of turns per game, 13 by default
        """
        if RNG_SEED is not None:
            random.seed(RNG_SEED)
        self.UNSHUFFLED_DECK = UNSHUFFLED_DECK
        self.SCORER = SCORER
        self.PLAYER_AI = PLAYER_AI
        self.DEALER_AI = DEALER_AI
        self.PRE_SHUFFLED_DECK = PRE_SHUFFLED_DECK
        self.TURNS_PER_GAME = TURNS_PER_GAME

        self.is_player = None
        self.remove_drawn_cards_from_deck = None
        self.turn_count = None
        self.player_cards = None
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

    def auto_play(self, GAMES_TO_AUTOPLAY, AUTO_PLAY_LOG_DIR, auto_play_log_filename, REMOVE_DRAWN_CARDS_FROM_DECK,
                  SILENT_MODE=False, LOG_ALL=False):
        """
        Plays a specified amount of games with the player AI against the dealer AI with no user input.
        Gives a progress update every percent of games played which includes current percent done, time since start and
        time since last percent.

        :param GAMES_TO_AUTOPLAY: the amount of games to play
        :param AUTO_PLAY_LOG_DIR: the directory of the log file (relative or absolute)
        :param auto_play_log_filename: the name of the log file (with .json extension)
        :param REMOVE_DRAWN_CARDS_FROM_DECK: whether cards drawn should be removed from the deck
        :param SILENT_MODE: turns off progress updates in console
        :param LOG_ALL: whether everything should be logged or only the scores
        :return: returns a dictionary with the results of the games (as well as any previous games from the same file)
                 see get_results in DataProcessing for more info
        """
        # add .json at the end if not already present
        if len(auto_play_log_filename) <= 5:
            auto_play_log_filename = auto_play_log_filename + ".json"
        elif auto_play_log_filename[-5:] != ".json":
            auto_play_log_filename = auto_play_log_filename + ".json"
        current_game = 0
        logger = DataProcessing.StaggeredLogger(AUTO_PLAY_LOG_DIR, auto_play_log_filename)
        start_time = time.time()
        time_since_last_interval_completion = time.time()
        while GAMES_TO_AUTOPLAY > current_game:
            self.reset_state(None, REMOVE_DRAWN_CARDS_FROM_DECK)
            # turn_count starts at -1 and increases in draw_cards
            # turn_count during condition check is one less than during the loop
            # condition is offset by 1 to accommodate for that
            while self.TURNS_PER_GAME > self.turn_count + 1:
                self.draw_cards()
                if self.PLAYER_AI.action(self.player_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, self.turn_count):
                    self.player_action()
                else:
                    self.player_history.append("NOT_ATTEMPTED")
                if self.DEALER_AI.action(self.dealer_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, self.turn_count):
                    self.dealer_action()
                else:
                    self.dealer_history.append("NOT_ATTEMPTED")
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
            return DataProcessing.get_results(output_folder=AUTO_PLAY_LOG_DIR, file_name=auto_play_log_filename,
                                              include_scores=True, include_deck=True, include_cards=True,
                                              include_history=True)
        else:
            return DataProcessing.get_results(output_folder=AUTO_PLAY_LOG_DIR, file_name=auto_play_log_filename,
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
        self.turn_count = -1
        self.player_cards = []
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
        self.turn_count += 1
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
        self.revealed_dealer_cards_to_player[self.turn_count] = True
        self.revealed_player_cards_to_dealer[self.turn_count] = True
        if self.dealer_cards[-1][0] == "K":
            self.player_history.append("ATTEMPTED_BUT_FAILED")
            return False
        self.player_history.append("SUCCEEDED")
        temp = self.player_cards[-1]
        self.player_cards[-1] = self.dealer_cards[-1]
        self.dealer_cards[-1] = temp
        return True

    def dealer_action(self):
        """
        Attempts to redraw their card for the dealer.
        Fails if the next card in the deck is a king.
        Changes dealer history and revealed status.
        """
        if self.turn_count + 1 < self.TURNS_PER_GAME:
            self.revealed_player_cards_to_dealer[self.turn_count + 1] = True
        if not self.remove_drawn_cards_from_deck and self.PRE_SHUFFLED_DECK is None:
            new_card = random.choice(self.current_deck)
            self.shuffled_deck.append(new_card)
            if new_card[0] == "K":
                self.dealer_history.append("ATTEMPTED_BUT_FAILED")
                self.next_player_card = new_card
                return False
            self.next_player_card = self.dealer_cards[-1]
            self.dealer_cards[-1] = new_card
            self.revealed_dealer_cards_to_player[self.turn_count] = False
            self.dealer_history.append("SUCCEEDED")
            return True
        if self.current_deck[-1][0] == "K":
            self.dealer_history.append("ATTEMPTED_BUT_FAILED")
            return False
        self.dealer_history.append("SUCCEEDED")
        temp = self.current_deck.pop()
        self.current_deck.append(self.dealer_cards[-1])
        self.dealer_cards[-1] = temp
        self.revealed_dealer_cards_to_player[self.turn_count] = False
        return True

    def score(self):
        """
        Updates player and dealer scores for every card.
        Only call once at the end.
        """
        for card in self.player_cards:
            self.player_score += self.SCORER(card)
        for card in self.dealer_cards:
            self.dealer_score += self.SCORER(card)

    def get_card(self, from_player, index):
        """

        :param from_player: whether the card is from the player hand
        :param index: the index of the card
        :return: returns the card with specified index from the hand of the specified participant
        """
        if from_player:
            return self.player_cards[index]
        else:
            return self.dealer_cards[index]

    def is_revealed(self, from_player, index):
        """

        :param from_player: whether the card is from the player hand
        :param index: the index of the card
        :return: returns whether the card with specified index from the hand of the
                 specified participant has been revealed to the opponent
        """
        if from_player:
            return self.revealed_player_cards_to_dealer[index]
        else:
            return self.revealed_dealer_cards_to_player[index]

    def get_scores(self):
        """

        :return: returns the scores of the player and dealer as a tuple (player_score, dealer_score)
        """
        return self.player_score, self.dealer_score

    def ask_ai(self, asks_player_ai, current_turn):
        """
        :param asks_player_ai: whether the player AI is the one being asked
        :param current_turn: the current turn
        :return: returns True if the specified AI would take their action this turn
        """
        if asks_player_ai:
            return self.PLAYER_AI.action(self.player_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, current_turn)
        else:
            return self.DEALER_AI.action(self.dealer_cards, self.revealed_player_cards_to_dealer,
                                         self.revealed_dealer_cards_to_player, self.player_history,
                                         self.dealer_history, current_turn)
