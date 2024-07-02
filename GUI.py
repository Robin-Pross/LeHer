from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import lang
from LeHer import LeHer
from Scorer import standard_scorer
from Strategies import KeepNAndAbove
from Decks import STANDARD_DECK


class GUI:
    """
    The graphical user interface for an instance of the game le her.
    """

    def __init__(self, path_to_main, *,
                 unshuffled_deck=STANDARD_DECK, SCORER=standard_scorer, PLAYER_AI=KeepNAndAbove(n=8, is_player=True),
                 DEALER_AI=KeepNAndAbove(n=8, is_player=False),
                 gui_language="EN",
                 RNG_SEED=None, PRE_SHUFFLED_DECK=None,
                 HIDE_UNKNOWN_CARDS=True):
        """
        Opens a new window with the game Le Her.

        :param path_to_main: the path to the main file
        :param unshuffled_deck: the deck to be used, standard deck of 52 by default
        :param SCORER: the scorer
        :param PLAYER_AI: the player AI
        :param DEALER_AI: the dealer AI
        :param RNG_SEED: the rng seed
        :param PRE_SHUFFLED_DECK: the deck to be used instead of using a shuffled version of the unshuffled deck
        :param gui_language: the language of the gui, english by default
        :param HIDE_UNKNOWN_CARDS: whether unknown cards are revealed to the user
        """
        app = QApplication(sys.argv)
        main_window = QtWidgets.QMainWindow()
        main_window.setWindowTitle("Le Her")
        GUIWindow(path_to_main=path_to_main, main_window=main_window, unshuffled_deck=unshuffled_deck, SCORER=SCORER,
                  PLAYER_AI=PLAYER_AI,
                  DEALER_AI=DEALER_AI,
                  gui_language=gui_language,
                  RNG_SEED=RNG_SEED, PRE_SHUFFLED_DECK=PRE_SHUFFLED_DECK,
                  HIDE_UNKNOWN_CARDS=HIDE_UNKNOWN_CARDS)
        main_window.show()
        sys.exit(app.exec_())


class GUIWindow(QMainWindow):
    def __init__(self, path_to_main, main_window,
                 unshuffled_deck=STANDARD_DECK, SCORER=standard_scorer, PLAYER_AI=KeepNAndAbove(8, True),
                 DEALER_AI=KeepNAndAbove(8, False),
                 gui_language="EN",
                 RNG_SEED=None, PRE_SHUFFLED_DECK=None,
                 HIDE_UNKNOWN_CARDS=True):
        """

        :param path_to_main: the path to the main file
        :param unshuffled_deck: the deck to be used, standard deck of 52 by default
        :param SCORER: the scorer
        :param PLAYER_AI: the player AI
        :param DEALER_AI: the dealer AI
        :param RNG_SEED: the rng seed
        :param PRE_SHUFFLED_DECK: the deck to be used instead of using a shuffled version of the unshuffled deck
        :param gui_language: the language of the gui, english by default
        :param HIDE_UNKNOWN_CARDS: whether unknown cards are revealed to the user
        :param main_window: the main window this window is placed in
        """
        super().__init__()
        self.TURNS_PER_GAME = 13
        self.HIDE_UNKNOWN_CARDS = HIDE_UNKNOWN_CARDS
        self.CARDS = set(unshuffled_deck)
        self.game = LeHer(TURNS_PER_GAME=self.TURNS_PER_GAME, RNG_SEED=RNG_SEED, PLAYER_AI=PLAYER_AI,
                          DEALER_AI=DEALER_AI,
                          SCORER=SCORER, PRE_SHUFFLED_DECK=PRE_SHUFFLED_DECK, UNSHUFFLED_DECK=unshuffled_deck)
        if gui_language == "GER":
            self.dict = lang.GER
        else:
            self.dict = lang.EN
        self.dealer_knows_next_drawn_card = False
        self.is_player = None
        self.current_turn = None

        main_window.setObjectName("Main Window")
        main_window.resize(1091, 631)

        # Create all layout managers
        self.Container = QtWidgets.QWidget(main_window)
        self.Container.setObjectName("Container")
        self.LayoutContainer = QtWidgets.QVBoxLayout(self.Container)
        self.LayoutContainer.setContentsMargins(0, 0, 0, 0)
        self.LayoutContainer.setGeometry(QtCore.QRect(0, 0, 1091, 601))
        self.LayoutContainer.setSpacing(20)
        self.LayoutContainer.setObjectName("LayoutContainer")
        self.DealerCardLabelContainer = QtWidgets.QHBoxLayout()
        self.DealerCardLabelContainer.setSpacing(22)
        self.DealerCardLabelContainer.setObjectName("DealerCardLabelContainer")
        self.InteractionContainer = QtWidgets.QHBoxLayout()
        self.InteractionContainer.setSpacing(22)
        self.InteractionContainer.setObjectName("InteractionContainer")
        self.ActionLog = QtWidgets.QLabel()
        self.ActionContainer = QtWidgets.QVBoxLayout()
        self.ActionContainer.setSpacing(22)
        self.ActionContainer.setObjectName("ActionContainer")
        self.NoActionContainer = QtWidgets.QVBoxLayout()
        self.NoActionContainer.setSpacing(22)
        self.NoActionContainer.setObjectName("ActionContainer")
        self.PlayerCardLabelContainer = QtWidgets.QHBoxLayout()
        self.PlayerCardLabelContainer.setSpacing(22)
        self.PlayerCardLabelContainer.setObjectName("PlayerCardLabelContainer")

        # Declare Container and Widgets to populate the layouts
        self.playerCardLabels = []
        self.logLabel = None
        self.dealerActionButton = None
        self.dealerNoActionButton = None
        self.playerActionButton = None
        self.playerNoActionButton = None
        self.dealerCardLabels = []

        # Create Content
        self.cardArtDictionary = {
            "unknown": (QtGui.QPixmap(path_to_main + "res/unknown.png")
                        .scaled(QtCore.QSize(80, 140),
                                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)),
            "empty": (QtGui.QPixmap(path_to_main + "res/empty.png")
                      .scaled(QtCore.QSize(80, 140),
                              aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        }
        for card in self.CARDS:
            self.cardArtDictionary[card] = (QtGui.QPixmap(path_to_main + "res/" + card + ".png")
                                            .scaled(QtCore.QSize(80, 140),
                                                    aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        for i in range(0, self.TURNS_PER_GAME):
            self.playerCardLabels.append(QtWidgets.QLabel())
            self.playerCardLabels[i].setText("")
            self.playerCardLabels[i].setPixmap(self.cardArtDictionary["empty"])
            self.playerCardLabels[i].setObjectName("PlayerCard" + str(i))
            self.PlayerCardLabelContainer.addWidget(self.playerCardLabels[i])
            self.dealerCardLabels.append(QtWidgets.QLabel())
            self.dealerCardLabels[i].setText("")
            self.dealerCardLabels[i].setPixmap(self.cardArtDictionary["empty"])
            self.dealerCardLabels[i].setObjectName("PlayerCard" + str(i))
            self.DealerCardLabelContainer.addWidget(self.dealerCardLabels[i])

        button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        button_size_policy.setHorizontalStretch(0)
        button_size_policy.setVerticalStretch(0)

        self.ActionLog.setScaledContents(False)
        self.ActionLog.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.ActionLog.setWordWrap(True)
        self.ActionLog.setObjectName("ActionLog")
        self.InteractionContainer.addWidget(self.ActionLog)

        self.DealerAction = QtWidgets.QPushButton()
        self.DealerAction.setSizePolicy(button_size_policy)
        self.DealerAction.setObjectName("DealerAction")
        self.ActionContainer.addWidget(self.DealerAction)
        self.PlayerAction = QtWidgets.QPushButton()
        self.PlayerAction.setSizePolicy(button_size_policy)
        self.PlayerAction.setObjectName("PlayerAction")
        self.ActionContainer.addWidget(self.PlayerAction)
        self.InteractionContainer.addLayout(self.ActionContainer)

        self.DealerNoAction = QtWidgets.QPushButton()
        self.DealerNoAction.setSizePolicy(button_size_policy)
        self.DealerNoAction.setObjectName("DealerNoAction")
        self.NoActionContainer.addWidget(self.DealerNoAction)
        self.PlayerNoAction = QtWidgets.QPushButton()
        self.PlayerNoAction.setSizePolicy(button_size_policy)
        self.PlayerNoAction.setObjectName("PlayerNoAction")
        self.NoActionContainer.addWidget(self.PlayerNoAction)
        self.InteractionContainer.addLayout(self.NoActionContainer)
        self.change_buttons_to_game_selection()

        self.LayoutContainer.addLayout(self.DealerCardLabelContainer)
        self.LayoutContainer.addLayout(self.InteractionContainer)
        self.LayoutContainer.addLayout(self.PlayerCardLabelContainer)

        main_window.setCentralWidget(self.Container)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def change_buttons_to_game_selection(self):
        """
        Changes the 4 Action buttons to allow for new game selection.
        """
        self.PlayerNoAction.setText(self.dict["start_player_no_redraw"])
        try:
            self.PlayerNoAction.clicked.disconnect()
            self.DealerNoAction.clicked.disconnect()
            self.PlayerAction.clicked.disconnect()
            self.DealerAction.clicked.disconnect()
        except TypeError:
            # "TypeError: disconnect() failed between 'clicked' and all its connections"
            # Error above happens if nothing is connected, can be ignored
            pass
        self.PlayerNoAction.clicked.connect(lambda: self.initialize_game(True, True))
        self.DealerNoAction.setText(self.dict["start_dealer_no_redraw"])
        self.DealerNoAction.clicked.connect(lambda: self.initialize_game(False, True))
        self.PlayerAction.setText(self.dict["start_player_redraw"])
        self.PlayerAction.clicked.connect(lambda: self.initialize_game(True, False))
        self.DealerAction.setText(self.dict["start_dealer_redraw"])
        self.DealerAction.clicked.connect(lambda: self.initialize_game(False, False))

    def initialize_game(self, is_player, remove_drawn_cards_from_deck):
        """
        Start a new game in the GUI.

        :param is_player: whether the user is the player
        :param remove_drawn_cards_from_deck: whether cards drawn should be removed from the deck
        """
        self.disable_all()
        self.reset_gui()
        self.is_player = is_player
        self.current_turn = 0
        self.game.reset_state(self.is_player, remove_drawn_cards_from_deck)
        self.game.draw_cards()
        self.update_card(True, 0)
        self.update_card(False, 0)
        if self.is_player:
            self.enable_player()
        else:
            if self.game.ask_ai(True, self.current_turn):
                self.player_action()
            else:
                self.player_no_action()
            self.enable_dealer()

    def enable_dealer(self):
        """
        Disable player action buttons.
        Enable dealer action buttons.
        """
        self.DealerAction.setEnabled(True)
        self.DealerNoAction.setEnabled(True)
        self.PlayerAction.setEnabled(False)
        self.PlayerNoAction.setEnabled(False)

    def enable_player(self):
        """
        Enable player action buttons.
        Disable dealer action buttons.
        """
        self.DealerAction.setEnabled(False)
        self.DealerNoAction.setEnabled(False)
        self.PlayerAction.setEnabled(True)
        self.PlayerNoAction.setEnabled(True)

    def disable_all(self):
        """
        Disable player action buttons.
        Disable dealer action buttons.
        """
        self.DealerAction.setEnabled(False)
        self.DealerNoAction.setEnabled(False)
        self.PlayerAction.setEnabled(False)
        self.PlayerNoAction.setEnabled(False)

    def enable_all(self):
        """
        Enable player action buttons.
        Enable dealer action buttons.
        """
        self.DealerAction.setEnabled(True)
        self.DealerNoAction.setEnabled(True)
        self.PlayerAction.setEnabled(True)
        self.PlayerNoAction.setEnabled(True)

    def update_card(self, change_for_player, index, card=None):
        """
        Updates the art for the specified card.
        Sets card art to unknown if the user does not know the card.
        Unknown kings will also be set to unknown.
        To force cards be visible use change_card_art instead.

        :param change_for_player: whether the card is changed for the player
        :param index: the index of the card to be changed
        :param card: the card the art should be changed to, by default the card selected is the card t
        """
        if card is None:
            card = self.game.get_card(change_for_player, index)
        if change_for_player:
            if self.is_player or not self.HIDE_UNKNOWN_CARDS or self.game.is_revealed(True, index):
                self.change_card_art(True, card, index)
            else:
                self.change_card_art(True, "unknown", index)
        else:
            if not self.is_player or not self.HIDE_UNKNOWN_CARDS or self.game.is_revealed(False, index):
                self.change_card_art(False, card, index)
            else:
                self.change_card_art(False, "unknown", index)

    def change_card_art(self, change_for_player, card, index):
        """
        Changes the art for the specified card.

        :param change_for_player: whether the card is changed for the player
        :param index: the index of the card to be changed
        :param card: the card the art should be changed to
        """
        if change_for_player:
            self.playerCardLabels[index].setPixmap(self.cardArtDictionary[card])
        else:
            self.dealerCardLabels[index].setPixmap(self.cardArtDictionary[card])

    def reset_gui(self):
        """
        Resets the gui for a new game of le her to be played.
        """
        for i in range(0, self.TURNS_PER_GAME):
            self.change_card_art(True, "empty", i)
            self.change_card_art(False, "empty", i)
        self.ActionLog.setText("")
        self.DealerAction.setText(self.dict["dealer_action"])
        self.DealerAction.clicked.disconnect()
        self.DealerAction.clicked.connect(lambda: self.dealer_action())
        self.PlayerAction.setText(self.dict["player_action"])
        self.PlayerAction.clicked.disconnect()
        self.PlayerAction.clicked.connect(lambda: self.player_action())
        self.PlayerNoAction.setText(self.dict["no_action"])
        self.PlayerNoAction.clicked.disconnect()
        self.PlayerNoAction.clicked.connect(lambda: self.dealer_no_action())
        self.DealerNoAction.setText(self.dict["no_action"])
        self.DealerNoAction.clicked.disconnect()
        self.DealerNoAction.clicked.connect(lambda: self.dealer_no_action())

    def dealer_action(self):
        """
        Attempts to use the action of the dealer.
        Then asks the player for their action.
        """
        self.disable_all()
        if self.game.dealer_action():
            self.ActionLog.setText(self.dict["dealer_action_success"])
            self.update_card(False, self.current_turn)
        else:
            self.ActionLog.setText(self.dict["dealer_action_failure"])
        self.ask_player()

    def player_action(self):
        """
        Attempts to use the action of the player.
        Then asks the dealer for their action.
        """
        self.disable_all()
        if self.game.player_action():
            self.ActionLog.setText(self.dict["player_action_success"])
            self.update_card(True, self.current_turn)
            self.update_card(False, self.current_turn)
        else:
            self.ActionLog.setText(self.dict["player_action_failure"])
        self.ask_dealer()

    def dealer_no_action(self):
        """
        Updates the log and asks the player for their action.
        """
        self.disable_all()
        self.ActionLog.setText(self.dict["dealer_no_action"])
        self.ask_player()

    def player_no_action(self):
        """
        Updates the log and asks the dealer for their action.
        """
        self.disable_all()
        self.ActionLog.setText(self.dict["player_no_action"])
        self.ask_dealer()

    def ask_dealer(self):
        """
        Waits for the user to click a button if they play as the dealer and lets the dealer AI decide if
        the user plays as player.
        """
        if self.is_player:
            if self.game.ask_ai(False, self.current_turn):
                self.dealer_action()
            else:
                self.dealer_no_action()
        else:
            self.enable_dealer()

    def ask_player(self):
        """
        Increments turn count and checks if the game is over.
        Waits for the user to click a button if they play as the player and lets the player AI decide if
        the user plays as dealer.
        """
        self.current_turn += 1
        if self.current_turn >= self.TURNS_PER_GAME:
            self.end_game()
        else:
            self.game.draw_cards()
            self.update_card(True, self.current_turn)
            self.update_card(False, self.current_turn)
            if not self.is_player:
                if self.game.ask_ai(True, self.current_turn):
                    self.player_action()
                else:
                    self.player_no_action()
            else:
                self.enable_player()

    def reveal_all(self):
        """
        Change to art of all cards to be visible.
        """
        for index in range(0, self.TURNS_PER_GAME):
            player_card = self.game.get_card(True, index)
            self.change_card_art(True, player_card, index)
            dealer_card = self.game.get_card(False, index)
            self.change_card_art(False, dealer_card, index)

    def end_game(self):
        """
        Changes the buttons to new game selection buttons and outputs result of the game in the log.
        """
        self.disable_all()
        self.reveal_all()
        self.change_buttons_to_game_selection()
        self.game.score()
        player_score, dealer_score = self.game.get_scores()
        if player_score < dealer_score:
            result_message = self.dict["dealer_win"]
        elif player_score == dealer_score:
            result_message = self.dict["draw"]
        else:
            result_message = self.dict["player_win"]
        result_message += self.dict["player_score"] + str(player_score) + ".\n"
        result_message += self.dict["dealer_score"] + str(dealer_score) + ".\n"
        self.ActionLog.setText(result_message)
        self.enable_all()
