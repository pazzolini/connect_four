import math
import random


# represents a node in the Monte Carlo Tree Search (MCTS) algorithm
class MCTSNode:
    def __init__(self, game_state, parent=None, move=None, exploration_constant=1.41):
        self.game_state = game_state.copy()  # duplicate of the game state to avoid altering the original game state
        self.parent = parent  # the parent node of the current node, None if root
        self.move = move  # the move that led to the creation of this node from the parent
        self.children = []  # child nodes of this node
        self.wins = 0  # number of wins recorded from this node
        self.visits = 0  # number of times this node has been visited during search
        self.unexplored_moves = game_state.get_valid_moves()  # moves not yet explored from this node
        self.exploration_constant = exploration_constant  # balances exploration/exploitation

    def uct_score(self, total_simulations, exploration_constant=None):
        # calculates the Upper Confidence Bound 1 applied to trees (UCT) score
        if exploration_constant is None:
            exploration_constant = self.exploration_constant
        if self.visits == 0:
            return float('inf')  # infinite score for unvisited nodes to ensure they are visited
        return self.wins / self.visits + exploration_constant * (math.log(total_simulations) / self.visits) ** 0.5

    def is_fully_expanded(self):
        # checks if all possible moves have been explored from this node
        return len(self.unexplored_moves) == 0

    def is_terminal(self):
        # checks if this node represents a terminal state of the game
        return self.game_state.is_terminal()

    def best_child(self, exploration_constant=None):
        # selects the best child node based on the UCT score
        if exploration_constant is None:
            exploration_constant = self.exploration_constant
        total_simulations = sum(child.visits for child in self.children)
        return max(
            self.children,
            key=lambda child: child.uct_score(total_simulations, exploration_constant)
        )


# MCTS algorithm implementation
class MonteCarloTreeSearch:
    def __init__(self, root):
        self.root = root  # initializes the root of the Monte Carlo Tree Search

    def select_node(self):
        # selects the node to explore based on the current state of the MCTS tree
        current_node = self.root
        while not current_node.is_terminal():  # continues until a terminal node is reached
            if not current_node.is_fully_expanded():
                # expands the current node if it has unexplored children
                return self.expand_node(current_node)
            else:
                # otherwise, selects the best child based on UCT score
                current_node = current_node.best_child()
        return current_node  # returns the terminal or fully expanded node

    def expand_node(self, node):
        # expands a node by creating a new child node from an unexplored move
        move = node.unexplored_moves.pop()  # removes and retrieves the last unexplored move
        new_state = node.game_state.copy()  # creates a copy of the current game state
        # attempts to apply the move to the new game state
        success = new_state.make_move(move, new_state.players[new_state.current_player_index].marker)

        if success:
            # updates the player index and checks for a win or draw if the move is successful
            new_state.current_player_index = (new_state.current_player_index + 1) % 2
            new_state.game_over = new_state.check_win(new_state.players[0].marker) or new_state.check_win(
                new_state.players[1].marker) or new_state.is_draw()
            child_node = MCTSNode(new_state, parent=node, move=move)  # creates a new child node
            node.children.append(child_node)  # adds the new child node to the current node's children
            return child_node
        else:
            return None  # returns None if the move was not successful

    def simulate(self, node):
        # simulates a game from the current node to a terminal state
        simulation_state = node.game_state.copy()  # copies the game state for the simulation
        while not simulation_state.is_terminal():
            # continues simulation until a terminal state is reached
            possible_moves = simulation_state.get_valid_moves()  # gets all valid moves for the current state
            move = random.choice(possible_moves)  # randomly selects one of the valid moves
            simulation_state.make_move(move, simulation_state.players[simulation_state.current_player_index].marker)
            simulation_state.current_player_index = (simulation_state.current_player_index + 1) % 2  # switches players
        return simulation_state.get_result()  # returns the result of the simulation

    def backpropagate(self, node, result):
        # backpropagates the simulation result through the tree, updating node statistics
        while node is not None:  # continues until the root node is reached
            node.visits += 1  # increments the visit count for the node
            if node.move is not None:  # checks if the node is not the root (the root node does not have a move)
                last_move_player_marker = node.game_state.players[
                    (node.game_state.current_player_index + 1) % 2].marker
                if result == last_move_player_marker:  # increments the win count if the result matches the last move marker
                    node.wins += 1
            node = node.parent  # moves to the parent node

    def run_search(self, iterations):
        # runs the MCTS algorithm for a specified number of iterations
        for _ in range(iterations):
            selected_node = self.select_node()  # selects a node for exploration
            result = self.simulate(selected_node)  # simulates a playthrough from the selected node
            self.backpropagate(selected_node, result)  # backpropagates the result through the tree

        # selects the best move to make from the root node, using an exploration constant of 0 for exploitation
        best_move = self.root.best_child(exploration_constant=0).move
        return best_move  # returns the best move found
