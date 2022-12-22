import random
import numpy as np

def monte_carlo_tree_search(game, iterations):
    root = Node(game)

    for _ in range(iterations):
        # Selection
        node = root
        while not node.is_leaf():
            node = node.select_child()

        # Expansion
        if not game.is_game_over():
            node = node.expand()

        # Simulation
        result = node.simulate()

        # Backpropagation
        node.backpropagate(result)

    return root.get_best_child()

class Node:
    def __init__(self, game):
        self.game = game
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_leaf(self):
        return len(self.children) == 0

    def select_child(self):
        # Select child with highest value
        return max(self.children, key=lambda c: c.wins / c.visits)

    def expand(self):
        # Add child nodes for all possible actions
        for action in self.game.get_available_actions():
            child = Node(self.game.get_next_state(action))
            self.children.append(child)
        return random.choice(self.children)

    def simulate(self):
        # Randomly simulate the remainder of the game
        game = self.game.copy()
        while not game.is_game_over():
            game.make_random_move()
        return game.get_result()

    def backpropagate(self, result):
        # Update node values with result of simulation
        self.visits += 1
        if result == self.game.current_player:
            self.wins += 1

    def get_best_child(self):
        # Choose child with highest win rate
        return max(self.children, key=lambda c: c.wins / c.visits)

def imprimir_tablero(board):
    for fila in board:
        print("| ", end='')
        for item in fila:
            print(item, "| ", end='')
        print('')
    print("_____________________________")
    print("| 0 | 1 | 2 | 3 | 4 | 5 | 6 |")

def deserialize_board(board: str):
        arr = np.array(list(board), dtype=np.int8)
        arr = arr.reshape((6, 7))
        return arr

c = '000000000010000002200000210011012001221200'
board = deserialize_board(c)
imprimir_tablero(board)

move = monte_carlo_tree_search(board, 15)
print(move)

  # def game_over(self, board):
  #   """Returns True if the game is over, False otherwise."""
  #   # Comprobamos si hay algún hueco en el tablero
  #   if np.any(board == 0):
  #     return None

  #   # Comprobamos si hay alguna combinación de 4 fichas del mismo color en horizontal, vertical o diagonal
  #   for i in range(board.shape[0]):
  #     for j in range(board.shape[1]):
  #       if (j+3 < board.shape[1] and 
  #           all(board[i,j+k] == board[i,j] for k in range(4))):
  #         return board[i,j]

  #       if (i+3 < board.shape[0] and
  #           all(board[i+k,j] == board[i,j] for k in range(4))):
  #         return board[i,j]

  #       if (i+3 < board.shape[0] and j+3 < board.shape[1] and
  #           all(board[i+k,j+k] == board[i,j] for k in range(4))):
  #         return board[i,j]

  #       if (i+3 < board.shape[0] and j-3 >= 0 and
  #           all(board[i+k,j-k] == board[i,j] for k in range(4))):
  #         return board[i,j]
    
  #   # If the board is full, the game is a draw
  #   if np.all(board != 0):
  #     return 0
def calculate_outcome(self, board):
    """Calculates the outcome of the game based on the current game board."""
    # Check if the first player has won
    if np.any(np.abs(np.sum(board, axis=0)) == 4) or np.any(np.abs(np.sum(board, axis=1)) == 4) or np.abs(np.trace(board)) == 4 or np.abs(np.trace(np.fliplr(board))) == 4:
        return 1

    # Check if the second player has won
    if np.any(np.abs(np.sum(board, axis=0)) == -4) or np.any(np.abs(np.sum(board, axis=1)) == -4) or np.abs(np.trace(board)) == -4 or np.abs(np.trace(np.fliplr(board))) == -4:
        return -1

    # If the board is full, the game is a draw
    if np.all(board != 0):
        return 0
