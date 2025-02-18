import random
from mcts import MCTSNode, MonteCarloTreeSearch


# base class for a player, to be extended by specific player types (human, AI).
class Player:
    def __init__(self, marker):
        self.marker = marker  # player's marker ("X" or "O")

    def make_move(self, board):
        pass  # to be implemented by subclasses


# human player
class HumanPlayer(Player):
    def make_move(self, board):
        while True:
            try:
                column_choice = int(input(f"Player {self.marker}'s turn. Choose a column (1-7): ")) - 1
                if 0 <= column_choice < 7 and board.is_valid_move(column_choice):
                    return column_choice
                else:
                    print("Invalid column. Please choose a column between 1 and 7, and ensure it's not full.")
            except ValueError:
                print("Please enter a number.")  # non-integer input


# agent that randomly selects a valid move
class RandomAIAgent(Player):
    def make_move(self, board):
        # generates a list of valid columns
        valid_columns = [col for col in range(7) if board.is_valid_move(col)]
        # randomly selects from valid columns if any are available
        if valid_columns:
            return random.choice(valid_columns)
        else:
            return -1


# an implementation of an AI agent inspired by A*
class AStarAgent(Player):
    def __init__(self, marker):
        super().__init__(marker)
        # assigns the opponent's marker based on the agent's own marker
        self.opponent_marker = 'O' if marker == 'X' else 'X'

    def heuristic_evaluation(self, game, marker):
        score = 0  # initializes the score to 0

        # adds the turn bonus
        turn_bonus = 16

        # loops through each cell on the board
        for row in range(6):
            for col in range(7):
                # horizontal segments
                if col + 3 < 7:
                    score += self.evaluate_segment(game, row, col, 0, 1, marker)
                # vertical segments
                if row + 3 < 6:
                    score += self.evaluate_segment(game, row, col, 1, 0, marker)
                # ascending diagonal
                if row - 3 >= 0 and col + 3 < 7:
                    score += self.evaluate_segment(game, row, col, -1, 1, marker)
                # descending diagonal
                if row + 3 < 6 and col + 3 < 7:
                    score += self.evaluate_segment(game, row, col, 1, 1, marker)

        # adds the turn bonus to the total score
        return score + turn_bonus

    # helper method to evaluate a segment of four cells
    def evaluate_segment(self, game, row, col, d_row, d_col, marker):
        # creates a segment of four cells based on the direction specified by d_row and d_col
        segment = [game.board[row + i * d_row][col + i * d_col] for i in range(4)]
        # assigns a score to the segment based on its composition
        return self.score_segment(segment, marker, self.opponent_marker)

    # assigns a score to the segment based on its composition
    def score_segment(self, segment, marker, opponent_marker):
        if segment.count(marker) == 4 and segment.count('-') == 0:
            return 512
        elif segment.count(marker) == 3 and segment.count('-') == 1:
            return 50
        elif segment.count(marker) == 2 and segment.count('-') == 2:
            return 10
        elif segment.count(marker) == 1 and segment.count('-') == 3:
            return 1
        elif segment.count(opponent_marker) == 4 and segment.count('-') == 0:
            return -512
        elif segment.count(opponent_marker) == 3 and segment.count('-') == 1:
            return -50
        elif segment.count(opponent_marker) == 2 and segment.count('-') == 2:
            return -10
        elif segment.count(opponent_marker) == 1 and segment.count('-') == 3:
            return -1
        return 0

    # simulates the opponent's best possible move and returns its score
    def simulate_opponent_best_move(self, game):
        best_opponent_score = float('-inf')  # initializes to the lowest possible score
        for col in game.get_valid_moves():  # iterates through all valid moves
            temp_game = game.copy()  # makes a copy of the game to simulate the move
            temp_game.make_move(col, self.opponent_marker)  # simulates the opponent's move
            score = self.heuristic_evaluation(temp_game, self.opponent_marker)  # evaluates the board after the move
            if score > best_opponent_score:  # if the move is better than the current best, updates the best score
                best_opponent_score = score
        return best_opponent_score  # returns the best score achievable by the opponent

    # chooses the best move based on the agent's heuristic evaluation
    def make_move(self, game):
        best_score = float('-inf')  # initializes the best score to the lowest possible score
        best_moves = []  # initializes a list to keep track of the best moves

        # evaluates each valid move
        for col in game.get_valid_moves():
            temp_game = game.copy()  # copy the game to simulate the move
            temp_game.make_move(col, self.marker)  # makes the simulated move
            current_score = self.heuristic_evaluation(temp_game, self.marker)  # evaluates the move's score
            opponent_best_score = self.simulate_opponent_best_move(temp_game)  # simulates the opponent's best response
            effective_score = current_score - opponent_best_score  # calculates the effective score considering the
            # opponent's best move

            # updates the list of best moves based on the effective score
            if effective_score > best_score:
                best_score = effective_score  # update the best score
                best_moves = [col]  # starts a new list with this column as the best move
            elif effective_score == best_score:
                best_moves.append(col)  # adds this column to the list of best moves if it matches the best score

        # chooses randomly among the best moves if there are multiple
        return random.choice(best_moves) if best_moves else -1


# agent that uses the MCTS strategy
class MCTSAgent(Player):
    def make_move(self, game):
        root = MCTSNode(game)
        mcts = MonteCarloTreeSearch(root)
        best_move = mcts.run_search(iterations=100)
        return best_move
