from abc import abstractmethod


class IGame:

    @abstractmethod
    def is_game_over(board, inarow):
        pass

    @abstractmethod
    def change_turn(player):
        pass

    @abstractmethod
    def get_open_cols(board):
        pass

    @abstractmethod
    def make_move(board, col, player):
        pass

    @abstractmethod
    def get_turn(board):
        pass

    @abstractmethod
    def print_board(board):
        pass