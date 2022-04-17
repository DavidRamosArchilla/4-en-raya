import numpy as np


ROWS = 6
COLS = 7
playing_board = np.zeros((ROWS, COLS))

current_player = '1' # 2 is the other player and 0 is empty cell

def change_turn(player): 
    if player == '1':
        return '2'
    else:
        return '1'


def serialize_board(board):
    return ''.join([str(cell) for row in board for cell in row])

def deserialize_board(board: str):
    arr = np.array(list(board))
    arr = arr.reshape((ROWS, COLS))
    return arr

def get_bitboard_representation(board):
    '''
    ROWS*COLS cells and 1 bit for the turn
    1 indicate that there is a checker in thar cell
    the board is serialized
    '''
    # board = serialize_board(board)
    bitboard = np.zeros(ROWS*COLS*2+1)

    for i in range(ROWS*COLS):
        if board[i] != '1':
            bitboard[2*i] = '1'
        elif board[i] != '2':
            bitboard[2*i+1] = '1'
    bitboard[-1] = current_player

def get_open_cols(board):
    # board is serialized
    # this order is better because the ia will start the search from the most centered columns
    return [i for i in [3,4,2,5,1,6,0] if board[i] == '0']

def make_move(board, col, player):
    # entire_col = ''
    # for i in range(ROWS):
    #     entire_col += board[i*ROWS + col]
    entire_col = [board[i*COLS + col] for i in range(ROWS)]
    for i, cell in enumerate(reversed(entire_col)):
        if cell == '0':
            board = board[:(ROWS-i-1)*COLS + col] + player + board[(ROWS-i-1)*COLS+col+1:]
            # aux = list(board)
            # aux[(ROWS-i-1)*COLS + col] = player
            break
    return board

def get_turn(board):
    # assuming that '1' always starts playing
    ones = board.count('1')
    twos = board.count('2')
    return '1' if ones == twos else '2'

def is_game_over(board, inarow):
    '''
    return the winner or '0' if there is no winner
    '''
    board2d = deserialize_board(board)
    # print(board2d)
    # rows
    for i in range(ROWS):
        previous = ''
        count = 1
        for j in range(COLS):
            current = board[i*COLS + j]
            if previous != '0' and previous == current:
                count += 1
            else:
                count = 1
            if count == inarow:
                return current
            previous = current
    
    # columns
    for i in range(COLS):
        previous = ''
        count = 1
        for j in range(ROWS):
            current = board[j*COLS + i]
            if previous != '0' and previous == current:
                count += 1
            else:
                count = 1
            if count == inarow:
                return current
            previous = current
    
    # positive diagonal
    for row in range(ROWS-(inarow-1)):
        for col in range(COLS-(inarow-1)):
            window = list(board2d[range(row, row+inarow), range(col, col+inarow)])
            
            if window.count('1') == inarow:
                return '1'
            elif window.count('2') == inarow:
                return '2'

    # negative diagonal
    for row in range(inarow-1, ROWS):
        for col in range(COLS-(inarow-1)):
            window = list(board2d[range(row, row-inarow, -1), range(col, col+inarow)])
            if window.count('1') == inarow:
                return '1'
            elif window.count('2') == inarow:
                return '2'
    return '0' if board.count('0') != 0 else 'draw'

def print_board(board):
    for i in range(ROWS):
        print('|', end='')
        for j in range(COLS):
            print(board[i*COLS + j], end='|')
        print()
    print(board)

# b = '0' * ROWS * COLS

# current_player = get_turn(b)
# while is_game_over(b, 4) == '0':
#     print_board(b)
#     col = int(input('Juegan ' + current_player + ': '))
#     b = make_move(b, col, current_player)
#     current_player = '2' if current_player == '1' else '1'
#     print(is_game_over(b, 4))

# print('pierde ' + current_player)
