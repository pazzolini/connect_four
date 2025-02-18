class ConnectFour:
    # initializes the game board, current player, and game status
    def __init__(self, player1, player2):
        self.board = self.initialize_board()
        self.players = [player1, player2]  # list of two players
        self.current_player_index = 0  # uses an index to toggle between players
        self.game_over = False  # checks if the game is ongoing/over

    # creates a 6*7 game board filled with "-" to represent empty spaces
    def initialize_board(self):
        return [["-" for _ in range(7)] for _ in range(6)]

    # prints the current state of the board along with column numbers for player reference
    def display_board(self):
        print('\nGame Board\n')
        for row in self.board:
            print(' '.join(row))
        print('\n1 2 3 4 5 6 7\n')

    # checks if a move can be made in the given column
    def is_valid_move(self, column):
        return self.board[0][column] == "-"

    # updates the board with the current player's marker if the move is valid
    def make_move(self, column, marker):
        if self.is_valid_move(column):
            for row in reversed(range(6)):
                if self.board[row][column] == "-":
                    self.board[row][column] = marker
                    return True
        return False

    # checks for a win condition in all four directions (horizontal, vertical, ascending diagonal, descending diagonal)
    def check_win(self, marker):
        # horizontal
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == marker and \
                        self.board[row][col + 1] == marker and \
                        self.board[row][col + 2] == marker and \
                        self.board[row][col + 3] == marker:
                    return True

        # vertical
        for col in range(7):
            for row in range(3):
                if self.board[row][col] == marker and \
                        self.board[row + 1][col] == marker and \
                        self.board[row + 2][col] == marker and \
                        self.board[row + 3][col] == marker:
                    return True

        # ascending diagonal (positive slope)
        for col in range(7 - 3):
            for row in range(3, 6):
                if self.board[row][col] == marker and \
                        self.board[row - 1][col + 1] == marker and \
                        self.board[row - 2][col + 2] == marker and \
                        self.board[row - 3][col + 3] == marker:
                    return True

        # descending diagonal (negative slope)
        for col in range(7 - 3):
            for row in range(3):
                if self.board[row][col] == marker and \
                        self.board[row + 1][col + 1] == marker and \
                        self.board[row + 2][col + 2] == marker and \
                        self.board[row + 3][col + 3] == marker:
                    return True

        return False

    # checks if the game is a draw
    def is_draw(self):
        return all(self.board[0][col] != "-" for col in range(7))  # if no empty cells in the top row

    # creates a deep copy of the game state
    def copy(self):
        new_game = ConnectFour(self.players[0], self.players[1])
        new_game.board = [row[:] for row in self.board]
        new_game.current_player_index = self.current_player_index
        new_game.game_over = self.game_over
        return new_game

    # returns a list of columns that can accept another marker
    def get_valid_moves(self):
        return [c for c in range(7) if self.is_valid_move(c)]

    # checks if there is a win or a draw
    def is_terminal(self):
        return self.game_over or self.is_draw()

    # determines the result of the game
    def get_result(self):
        if self.check_win(self.players[0].marker):
            return self.players[0].marker
        elif self.check_win(self.players[1].marker):
            return self.players[1].marker
        else:
            return "draw"

    # contains the game loop, handling turn taking, input validation, win/draw checking, and player switching
    def run_game(self):
        while not self.game_over:
            self.display_board()
            current_player = self.players[self.current_player_index]
            column_choice = current_player.make_move(self)

            if self.make_move(column_choice, current_player.marker):
                if self.check_win(current_player.marker):
                    self.display_board()
                    print(f"Player {current_player.marker} wins!")
                    self.game_over = True
                elif self.is_draw():
                    self.display_board()
                    print("The game is a draw!")
                    self.game_over = True
                else:
                    self.current_player_index = (self.current_player_index + 1) % 2
            else:
                print("Column is full. Try a different one.")
