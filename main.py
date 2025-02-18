from connect_four_game import ConnectFour
from player import HumanPlayer, RandomAIAgent, AStarAgent, MCTSAgent


# displays options for player type selection
def get_player_type(player_number):
    print(f"Select Player {player_number} type:")
    print("1: Human")
    print("2: AI")

    while True:
        try:
            player_type = int(input("Enter 1 for Human, 2 for AI: "))
            if player_type == 1:
                return HumanPlayer("X" if player_number == 1 else "O")
            elif player_type == 2:
                print("Select AI type:")
                print("1. Random AI Agent")
                print("2. A* Agent")
                print("3. MCTS Agent")
                ai_type_selection = input("Enter your choice (1/2/3): ").strip()

                if ai_type_selection == "1":
                    return RandomAIAgent("X" if player_number == 1 else "O")
                elif ai_type_selection == "2":
                    return AStarAgent("X" if player_number == 1 else "O")
                elif ai_type_selection == "3":
                    return MCTSAgent("X" if player_number == 1 else "O")
                else:
                    print("Invalid selection, defaulting to Random AI Agent.")
                    return RandomAIAgent("X" if player_number == 1 else "O")  # ensures a default AI agent
            else:
                print("Invalid selection. Please enter 1 for Human or 2 for AI.")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")


# displays options for AI player type selection
def get_agent_type():
    print("Select AI type:")
    print("1. Random AI Agent")
    print("2. A* Agent")
    print("3. MCTS Agent")
    selection = input("Enter your choice (1/2/3): ").strip()

    if selection == "1":
        return RandomAIAgent
    elif selection == "2":
        return AStarAgent
    elif selection == "3":
        return MCTSAgent
    else:
        print("Invalid selection, defaulting to Random AI Player.")
        return RandomAIAgent  # ensures a default is returned


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
    print("Select mode:")
    print("1. AI vs. AI simulation (multiple games, no move display)")
    print("2. play against an AI")
    print("3. watch an AI vs. AI game")
    mode = input("Enter your choice (1/2/3): ").strip()

    if mode == "1":
        # simulation mode
        num_games = int(input("Enter the number of games to simulate: "))
        print("Configuring AI agents for simulation...")
        player1_type = get_agent_type()
        player2_type = get_agent_type()

        wins_for_X, wins_for_O, draws = simulate_games(num_games, player1_type, player2_type)

        print(f"\nSimulation Results:")
        print(f"Total games: {num_games}")
        print(f"Wins for Player 1 (X): {wins_for_X}")
        print(f"Wins for Player 2 (O): {wins_for_O}")
        print(f"Draws: {draws}")
    elif mode == "2":
        # playing against an AI
        print("You will play as 'X' against an AI agent.")
        ai_type = get_agent_type()
        game = ConnectFour(HumanPlayer("X"), ai_type("O"))
        game.run_game()
    elif mode == "3":
        # watching an AI vs. AI game
        print("AI vs. AI game. Watch the AIs play against each other.")
        player1_type = get_agent_type()
        player2_type = get_agent_type()

        game = ConnectFour(player1_type("X"), player2_type("O"))
        while not game.game_over:
            game.display_board()
            current_player = game.players[game.current_player_index]
            column_choice = current_player.make_move(game)

            if game.make_move(column_choice, current_player.marker):
                if game.check_win(current_player.marker):
                    game.display_board()
                    print(f"Player {current_player.marker} wins!")
                    game.game_over = True
                elif game.is_draw():
                    game.display_board()
                    print("The game is a draw!")
                    game.game_over = True
                else:
                    game.current_player_index = (game.current_player_index + 1) % 2
            else:
                print("Column is full. Try a different one.")
    else:
        print("Invalid mode selected.")


if __name__ == "__main__":
    main()
