import time
import csv
from connect_four_game import ConnectFour
from player import RandomAIAgent, AStarAgent, MCTSAgent


def append_simulation_results(file_name, configuration, wins_for_X, wins_for_O, draws, average_duration):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the configuration and results
        writer.writerow([configuration, wins_for_X, wins_for_O, draws, average_duration])


# simulates a given number of games between two player types, tracking wins and draws
def simulate_games(num_games, player1_type, player2_type):
    wins_for_X = 0
    wins_for_O = 0
    draws = 0

    for _ in range(num_games):
        player1 = player1_type('X')
        player2 = player2_type('O')
        game = ConnectFour(player1, player2)

        while not game.game_over:
            current_player = game.players[game.current_player_index]
            column_choice = current_player.make_move(game)

            if game.make_move(column_choice, current_player.marker):
                if game.check_win(current_player.marker):
                    if current_player.marker == 'X':
                        wins_for_X += 1
                    else:
                        wins_for_O += 1
                    game.game_over = True
                elif game.is_draw():
                    draws += 1
                    game.game_over = True
            game.current_player_index = (game.current_player_index + 1) % 2

    return wins_for_X, wins_for_O, draws


def main():
    configurations = [
        # {"player1_type": RandomAIPlayer, "player2_type": RandomAIPlayer},
        {"player1_type": RandomAIAgent, "player2_type": MCTSAgent, "iterations": 100},
        {"player1_type": MCTSAgent, "player2_type": RandomAIAgent, "iterations": 100},
        {"player1_type": AStarAgent, "player2_type": MCTSAgent, "iterations": 100},
        {"player1_type": MCTSAgent, "player2_type": AStarAgent, "iterations": 100},

    ]
    file_name = "agents_performance_c_1_41*1000.csv"

    # checks if file exists to write the header, otherwise append
    try:
        with open(file_name, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Configuration", "Wins for X", "Wins for O", "Draws", "Average Game Duration"])
    except FileExistsError:
        pass  # file already exists, proceed with appending data

    for config in configurations:
        num_games = 1000  # or however many games you want to simulate for each configuration
        total_duration = 0

        # simulate the games first, accumulating the results
        start_time = time.time()
        wins_for_X, wins_for_O, draws = simulate_games(num_games, config["player1_type"], config["player2_type"])
        end_time = time.time()
        total_duration = end_time - start_time

        average_duration = total_duration / num_games
        # configuration_description = f"{config['player1_type'].__name__} vs {config['player2_type'].__name__}"
        configuration_description = f"{config['player1_type'].__name__} vs {config['player2_type'].__name__}, {config['iterations']} iterations"

        append_simulation_results(file_name, configuration_description, wins_for_X, wins_for_O, draws, average_duration)


if __name__ == "__main__":
    main()
