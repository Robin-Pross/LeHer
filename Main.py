import Strategies
from LeHer import LeHer
from datetime import datetime
import numpy as np


def tournament(player_strategies, dealer_strategies, REMOVE_DRAWN_CARDS_FROM_DECK=False,
               GAMES_TO_AUTOPLAY=1000000, OUTPUT_FOLDER="output/"):
    """
    Simulates specified (1.000.000 by default) amount of games for every possible player-dealer strategy combination.
    Outputs the results of the games as well as a results summary in the specified output folder.
    The result summary has the form of 3 matrices separated by a row of -1's.
    The top matrix is win rate (as decimal) for the player.
    The middle matrix is draw rate.
    The bottom matrix is win rate (as decimal) for the dealer.
    A row uses the same player strategy but differing dealer strategies.
    A column uses the same dealer strategy but differing player strategies.
    Order of strategies is the same as order of the list given in the parameters.

    :param player_strategies: list of tuples (strategy, name)
    :param dealer_strategies: list of tuples (strategy, name)
    :param REMOVE_DRAWN_CARDS_FROM_DECK: whether drawn card should be removed from the deck
    :param GAMES_TO_AUTOPLAY: the amount of games to play for every possible player-dealer strategy combination
    :param OUTPUT_FOLDER: the folder where game data and results should be saved as
    """
    winrates = []
    drawrates = []
    dealer_winrates = []
    for i, ps in enumerate(player_strategies):
        winrates_for_current_player_strategy = []
        drawrates_for_current_player_strategy = []
        dealer_winrates_for_current_player_strategy = []
        for j, ds in enumerate(dealer_strategies):
            current_log_file = ps[1] + " (player) vs " + ds[1] + " (dealer).json"
            current_game = LeHer(PLAYER_AI=ps[0], DEALER_AI=ds[0])
            current_game_results = current_game.auto_play(GAMES_TO_AUTOPLAY, OUTPUT_FOLDER, current_log_file,
                                                          REMOVE_DRAWN_CARDS_FROM_DECK)
            player_scores = current_game_results["player_scores"]
            dealer_scores = current_game_results["dealer_scores"]
            games = len(player_scores)
            wins = 0
            draws = 0
            for p_score, d_score in zip(player_scores, dealer_scores):
                if p_score > d_score:
                    wins += 1
                elif p_score == d_score:
                    draws += 1
            winrate = wins / games
            winrates_for_current_player_strategy.append(winrate)
            drawrate = draws / games
            drawrates_for_current_player_strategy.append(drawrate)
            dealer_winrates_for_current_player_strategy.append(1 - winrate - drawrate)
        winrates.append(winrates_for_current_player_strategy)
        drawrates.append(drawrates_for_current_player_strategy)
        dealer_winrates.append(dealer_winrates_for_current_player_strategy)

    results = []
    for rate in winrates:
        results.append(rate)
    results.append([-1] * len(winrates[0]))
    for rate in drawrates:
        results.append(rate)
    results.append([-1] * len(winrates[0]))
    for rate in dealer_winrates:
        results.append(rate)
    np_results = np.array(results)
    np.set_printoptions(suppress=True)
    np.savetxt(OUTPUT_FOLDER + "results.txt", np_results, fmt="%f")
    print(np_results)


if __name__ == "__main__":
    game = LeHer()

    player_strategies_to_test = [
        (Strategies.KeepNAndAbove(n=8, is_player=True), "keep 8 and above")
    ]

    dealer_strategies_to_test = [
        (Strategies.KeepNAndAbove(n=8, is_player=False), "keep 8 and above")
    ]

    tournament(player_strategies_to_test, dealer_strategies_to_test, REMOVE_DRAWN_CARDS_FROM_DECK=True,
               OUTPUT_FOLDER="output/remove/")
    tournament(player_strategies_to_test, dealer_strategies_to_test, REMOVE_DRAWN_CARDS_FROM_DECK=False,
               OUTPUT_FOLDER="output/dupe/")
