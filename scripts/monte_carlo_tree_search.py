import numpy as np
import random


def monte_carlo_tree_search(board, iterations):
  # Initialize the root node of the search tree with the current game state
  root = Node(board)
  player = root.get_turn(board)
  print(player)
  # Iteratively expand and simulate games from the root node
  for i in range(iterations):
    # Select the best child node of the root node according to the UCB1 algorithm
    selected_node = root
    while not selected_node.is_leaf():
      selected_node = selected_node.select_best_child()
    # selected_node = root.select_best_child()

    # If the selected node is a leaf node (i.e., it has no children), expand it
    selected_node.expand()

    # Simulate a random game from the selected node
    for cild in selected_node.children:
      outcome = cild.simulate()
      # Backpropagate the outcome of the simulation to the root node
      cild.backpropagate(outcome, player)

  # Return the best child of the root node as the next move
  for node in root.children:
    print(f'Visits: {node.visits}, wins: {node.wins}, move: {node.move}')
  print(root.game_over(board))
  return root.select_best_child().move


class Node:
  def __init__(self, board, move=None, parent=None):
    self.board = board  # The current game state represented as a NumPy array
    self.move = move  # The move that led to this game state (if any)
    self.parent = parent  # The parent node in the search tree (if any)
    self.children = []  # A list of child nodes
    self.visits = 1  # The number of times this node has been visited in the search
    self.wins = 0  # The number of wins resulting from simulations starting from this node

  def is_leaf(self):
    """Returns True if this node has no children, False otherwise."""
    return len(self.children) == 0

  def select_best_child(self):
    """Selects the child node with the highest UCB1 score."""
    # Calculate the UCB1 score for each child node
    ucb1_scores = [self.calculate_ucb1(child) for child in self.children]

    # Select the child with the highest UCB1 score
    return self.children[np.argmax(ucb1_scores)]

  def calculate_ucb1(self, node):
    """Calculates the UCB1 score for a given node."""
    # Calculate the exploitation term (the average reward for this node)
    exploitation = node.wins / node.visits

    # Calculate the exploration term (a measure of the uncertainty of this node)
    exploration = np.sqrt(2 * np.log(self.visits) / node.visits)

    # Return the sum of the exploitation and exploration terms as the UCB1 score
    return exploitation + exploration

  def expand(self):
    """Expands this node by adding one child node for each legal move."""
    # Find all legal moves
    legal_moves = self.find_legal_moves()
    turn = self.get_turn(self.board)
    # Add a child node for each legal move
    for move in legal_moves:
      child_board = self.apply_move(self.board, move, turn)  # Apply the move to create a new game state
      child_node = Node(child_board, move=move, parent=self)  # Create a new node for the child game state
      self.children.append(child_node)  # Add the child node to the list of children

  def find_legal_moves(self):
    """Finds all legal moves that can be made on the current game board."""
    legal_moves = []  # Initialize an empty list of legal moves

    # Iterate over each column in the game board
    for col in range(self.board.shape[1]):
      # If the top cell in the column is empty, it's a legal move
      if self.board[0, col] == 0:
        legal_moves.append(col)

    return legal_moves

  def apply_move(self, board, move, player):
    """Applies a move to a game board and returns the resulting game board."""
    # Make a copy of the game board so we don't modify the original
    new_board = np.copy(board)

    # Find the first empty cell in the column
    for row in range(board.shape[0] - 1, -1, -1):  # Iterate over rows in reverse order
      if new_board[row, move] == 0:
        new_board[row, move] = player  # Place the move in the empty cell
        break

    return new_board

  def get_turn(self, board):
        # assuming that '1' always starts playing
        player1 = np.count_nonzero(board == 1)
        player2 = np.count_nonzero(board == -1)
        return 1 if player1 == player2 else -1

  def simulate(self):
    """Simulates a random game starting from this node and returns the outcome."""
    # Make a copy of the current game state so we don't modify the original
    board = np.copy(self.board)
    
    # Initialize the player to move (1 for the first player, -1 for the second player)
    player = self.get_turn(board)
    initial_player = player

    # Simulate the game until it's over
    while True:
      # Check if the game is over
      result = self.game_over(board)
      if result is not None:
        # print(f'Resultado: {result}')
        # imprimir_tablero(board)
        return result # Return the outcome of the game

      # Find all legal moves
      legal_moves = self.find_legal_moves()

      # If there are no legal moves, the game is a draw
      if len(legal_moves) == 0:
        # print('Resultado: empate')
        # imprimir_tablero(board)
        return 0

      # Choose a random legal move
      move = random.choice(legal_moves)

      # Apply the move to the game board
      board = self.apply_move(board, move, player)

      # Switch players
      player = -player

  def backpropagate(self, outcome, player):
    """Updates the number of visits and wins for this node and all of its ancestors based on the outcome of a simulation."""
    # Update the number of visits for this node
    self.visits += 1

    # If the outcome is 1, increment the number of wins for this node
    if outcome == player:
      self.wins += 1
    # elif outcome == -player:
    #   self.wins -= 1 # DEBERIA SER ASI????

    # If this node has a parent, backpropagate the outcome to the parent
    if self.parent is not None:
      self.parent.backpropagate(outcome, player)


  def game_over(self, board):
    cols = 7
    rows = 6

    # If the board is full, the game is a draw            
    if np.all(board != 0):
      return 0

    def _get_window_value(window):
      if window.count(1) == 4:
          return 1
      elif window.count(-1) == 4:
          return -1
      return None

    # rows
    for row in board:
      for i in range(cols-4+1):
        window = list(row[i:i+4])
        value = _get_window_value(window)
        if value is not None:
          return value
  
    # columns
    for i in range(cols):
      col = board[:, i]
      for j in range(rows-4+1):
        window = list(col[j:j+4])
        value = _get_window_value(window)
        if value is not None:
          return value

    # positive diagonal
    for row in range(rows-(4-1)):
        for col in range(cols-(4-1)):
            window = list(board[range(row, row+4), range(col, col+4)])
            value = _get_window_value(window)
            if value is not None:
              return value

    # negative diagonal
    for row in range(4-1, rows):
        for col in range(cols-(4-1)):
            window = list(board[range(row, row-4, -1), range(col, col+4)])
            value = _get_window_value(window)
            if value is not None:
              return value
    
    # If it is not gae over yet
    return None

def imprimir_tablero(board):
    for fila in board:
        print("| ", end='')
        for item in fila:
          if item == -1:
            item = 2
          print(item, "| ", end='')
        print('')
    print("_____________________________")
    print("| 0 | 1 | 2 | 3 | 4 | 5 | 6 |")

def deserialize_board(board: str):
        arr = np.array(list(board), dtype=np.int8)
        arr = arr.reshape((6, 7))
        return arr

c = '000000000000000122000122100021120002111201'
board_interface = deserialize_board(c)
board = np.where(board_interface==2, -1, board_interface)
imprimir_tablero(board_interface)

move = monte_carlo_tree_search(board, 10)

print(move)