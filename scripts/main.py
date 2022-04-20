from MCTS import MCTS
import functools
from connectx import Connectx

def my_agent(observation, configuration):
    board = functools.reduce(lambda x, y: str(x) + str(y), observation.board)
    game = Connectx(configuration.inarow, configuration.rows, configuration.columns)
    mcts = MCTS(game)
    turn = game.get_turn(board)
#     print(turn, configuration.rows, configuration.columns)
#     print(board)
    game.print_board(board)
    move = mcts.best_move(board, turn, time_limit=7.1)
#     print(move)
    return move

if __name__ == '__main__':
    my_agent()

