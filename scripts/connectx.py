import numpy as np
from IGame import IGame

class Connectx(IGame):
    def __init__(self, inarow, rows, cols):
        self.cols = cols
        self.rows = rows
        self.inarow = inarow
        

    def change_turn(self, player): 
        if player == '1':
            return '2'
        else:
            return '1'


    def get_open_cols(self, board):
        # board is serialized
        # this order is better because the ia will start the search from the most centered columns
        return [i for i in [3,4,2,5,1,6,0] if board[i] == '0']

    def make_move(self, board, col, player):

        entire_col = [board[i*self.cols + col] for i in range(self.rows)]
        for i, cell in enumerate(reversed(entire_col)):
            if cell == '0':
                board = board[:(self.rows-i-1)*self.cols + col] + player + board[(self.rows-i-1)*self.cols+col+1:]
                break
        return board

    def get_turn(self, board):
        # assuming that '1' always starts playing
        ones = board.count('1')
        twos = board.count('2')
        return '1' if ones == twos else '2'

    def is_game_over(self, board, inarow):
        '''
        return the winner or '0' if there is no winner
        '''
        board2d = self.deserialize_board(board)
        
        # rows
        for i in range(self.rows):
            previous = ''
            count = 1
            for j in range(self.cols):
                current = board[i*self.cols + j]
                if previous != '0' and previous == current:
                    count += 1
                else:
                    count = 1
                if count == inarow:
                    return current
                previous = current
        
        # columns
        for i in range(self.cols):
            previous = ''
            count = 1
            for j in range(self.rows):
                current = board[j*self.cols + i]
                if previous != '0' and previous == current:
                    count += 1
                else:
                    count = 1
                if count == inarow:
                    return current
                previous = current
        
        # positive diagonal
        for row in range(self.rows-(inarow-1)):
            for col in range(self.cols-(inarow-1)):
                window = list(board2d[range(row, row+inarow), range(col, col+inarow)])
                
                if window.count('1') == inarow:
                    return '1'
                elif window.count('2') == inarow:
                    return '2'

        # negative diagonal
        for row in range(inarow-1, self.rows):
            for col in range(self.cols-(inarow-1)):
                window = list(board2d[range(row, row-inarow, -1), range(col, col+inarow)])
                if window.count('1') == inarow:
                    return '1'
                elif window.count('2') == inarow:
                    return '2'
        return '0' if board.count('0') != 0 else 'draw'

    def print_board(self, board):
        for i in range(self.rows):
            print('|', end='')
            for j in range(self.cols):
                print(board[i*self.cols + j], end='|')
            print()
        print(board)

    def serialize_board(self, board):
        return ''.join([str(cell) for row in board for cell in row])

    def deserialize_board(self, board: str):
        arr = np.array(list(board))
        arr = arr.reshape((self.rows, self.cols))
        return arr

    def get_bitboard_representation(self, board):
        '''
        ROWS*COLS cells and 1 bit for the turn
        1 indicate that there is a checker in thar cell
        the board is serialized
        '''
        # board = serialize_board(board)
        bitboard = np.zeros(self.rows*self.cols*2+1)

        for i in range(self.rows*self.cols):
            if board[i] != '1':
                bitboard[2*i] = '1'
            elif board[i] != '2':
                bitboard[2*i+1] = '1'
        bitboard[-1] = self.get_turn(board)

# b = '0' * ROWS * COLS

# current_player = get_turn(b)
# while is_game_over(b, 4) == '0':
#     print_board(b)
#     col = int(input('Juegan ' + current_player + ': '))
#     b = make_move(b, col, current_player)
#     current_player = '2' if current_player == '1' else '1'
#     print(is_game_over(b, 4))

# print('pierde ' + current_player)
