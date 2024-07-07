import os
import json


def get_results(output_folder, file_name, include_scores=True, include_cards=False, include_deck=False,
                include_history=False):
    """
    Returns a dictionary with the data from the specified file.
    Only data specified in the parameters in included in the dictionary.
    If data is not included in the dictionary the value for the key is None.
    The keys are (without '):
    'decks','player_cards', 'dealer_cards', 'player_histories', 'dealer_histories', 'player_scores' and 'dealer_scores'

    :param output_folder: path (as string) to output folder, can be relative or absolute
    :param file_name: name of the log file (with extension)
    :param include_scores: whether scores are part of the return dictionary
    :param include_cards: whether cards in hand at the end of the game are part of the return dictionary
    :param include_deck: whether the decks at the start of the game are part of the return dictionary
    :param include_history: whether the attempted actions are part of the return dictionary
    :return: returns a dictionary with the results
    """
    results = {
        "player_scores": None,
        "dealer_scores": None,
        "player_cards": None,
        "dealer_cards": None,
        "player_histories": None,
        "dealer_histories": None,
        "decks": None
    }
    with open(output_folder + file_name) as data_file:
        data = json.load(data_file)

    player_scores = []
    dealer_scores = []
    player_cards = []
    dealer_cards = []
    player_histories = []
    dealer_histories = []
    decks = []

    for game in data['games']:
        if include_cards:
            player_cards.append(game['player_cards'])
            dealer_cards.append(game['dealer_cards'])
        if include_scores:
            player_scores.append(game['player_score'])
            dealer_scores.append(game['dealer_score'])
        if include_history:
            player_histories.append(game['player_history'])
            dealer_histories.append(game['dealer_history'])
        if include_deck:
            decks.append(game['deck_to_start_of_game'])

    if include_cards:
        results["player_cards"] = player_cards
        results["dealer_cards"] = dealer_cards
    if include_scores:
        results["player_scores"] = player_scores
        results["dealer_scores"] = dealer_scores
    if include_history:
        results["player_histories"] = player_histories
        results["dealer_histories"] = dealer_histories
    if include_deck:
        results["decks"] = decks

    return results


class StaggeredLogger:
    """
    This class handles the logging of game data in the form of json files.

    Each game has to added to the class separately with the add_game method.
    All games previously added are logged with the log_staggered_games method.
    After logging the games new games can be added and logged again without making a new instance of this class.
    """

    def __init__(self, output_folder, file_name):
        """
        If there is a log file with that name in the specified directory the data will be appended to the old file.
        No compatibility checks are done.

        :param output_folder: path (as string) to output folder, can be relative or absolute
        :param file_name: name of the log file (with extension)
        """
        self.index = 0
        self.file_path = output_folder + file_name
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(self.file_path):
            log_file = open(output_folder + file_name, "x")
            log_file.close()
            self.data = {"games": []}
            self.offset = 0
        else:
            with open(self.file_path) as data_file:
                self.data = json.load(data_file)
                self.offset = len(self.data['games'])

    def add_game(self, *, deck_to_start_of_game=None, player_score=None,
                 dealer_score=None, player_history=None, dealer_history=None,
                 player_cards=None, dealer_cards=None):
        """
        :param deck_to_start_of_game: the deck at the start of the game
        :param player_score: the score of the player
        :param dealer_score: the score of the dealer
        :param player_history: the action history of the player
        :param dealer_history: the action history of the dealer
        :param player_cards: the cards the player has in their hand at the end of the game
        :param dealer_cards: the cards the dealer has in their hand at the end of the game
        """
        new_data = {"id": self.index + self.offset}
        self.index += 1
        if player_score is not None:
            new_data["player_score"] = player_score
        if dealer_score is not None:
            new_data["dealer_score"] = dealer_score
        if deck_to_start_of_game is not None:
            new_data["deck_to_start_of_game"] = deck_to_start_of_game
        if player_history is not None:
            new_data["player_history"] = player_history
        if dealer_history is not None:
            new_data["dealer_history"] = dealer_history
        if player_cards is not None:
            new_data["player_cards"] = player_cards
        if dealer_cards is not None:
            new_data["dealer_cards"] = dealer_cards
        self.data['games'].append(new_data)

    def log_staggered_games(self):
        """
        Logs all staggered (previously added) games to the file specified at class instance creation.
        More games can be added with the add_game function, but they will not be logged until
        log_staggered_games is called again.
        """
        with open(self.file_path, "w+") as data_file:
            json.dump(self.data, data_file)
