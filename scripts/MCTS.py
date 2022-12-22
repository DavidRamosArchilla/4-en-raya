import numpy as np
from IGame import IGame
from connectx import Connectx
import time
import functools

class MCTS:
     # hiperparameter to manage expliotation vs exploration

    def __init__(self, game: IGame):
        self.explored = set() # fen: value // eliminar??
        self.nodes_parameters = {} # fen: (N, V) N--> times visited, V-->value
        # self.UCT = {} # fen: UPC (upper confidence tree)
        self.C = 1.41 # aprox sqrt(2)
        self.game = game

    def get_value(self, result: str, player):
        if result == '1':
            return 1 if player == '1' else -1

        elif result == '2':
            return -1 if player == '1' else 1 
        else:
            return 0

    def search(self, s, original_turn, current_turn):
        result = self.game.is_game_over(s, self.game.inarow)
        if result != '0':
            v = self.get_value(result, original_turn) 
            n = 1
            if s not in self.nodes_parameters:
                self.nodes_parameters[s] = np.array((1, v))
            else:
                self.nodes_parameters[s][0] += 1
                n = self.nodes_parameters[s][0]
            return v, n

        childs = self.game.get_open_cols(s)

        if s in self.explored:
        # choose which node is going to be expanded
            best_uct = float('-inf')
            best_child = childs[0]
            # best_w = 0
            n_p = self.nodes_parameters[s][0] # parent's n
            for a in childs:
                s_child = self.game.make_move(s, a, current_turn)
                n, w = self.nodes_parameters[s_child]
                if current_turn != original_turn:
                    w = -w
                child_uct = self.get_UCT(n, w, n_p)
                if child_uct > best_uct:
                    best_uct = child_uct
                    best_child = a
            s = self.game.make_move(s, best_child, current_turn) # TODO: EN ESTA LLAMADA SE PRODUCEN ERRORES, best child es null
            sum_v, sum_n = self.search(s, original_turn, self.game.change_turn(current_turn))
            # propagate the results
            self.nodes_parameters[s][0] += sum_n
            self.nodes_parameters[s][1] += sum_v

        
        else:
            self.explored.add(s)
            sum_v = 0
            sum_n = 0
            for a in childs:
                s_child = self.game.make_move(s, a, current_turn)
                if s_child not in self.nodes_parameters:
                    v = self.simulate(s_child, original_turn)
                    self.nodes_parameters[s_child] = np.array((1, v)) # v no se si debe estar cambiado de signo
                    sum_v += v
                    sum_n += 1
                
            self.nodes_parameters[s][0] += sum_n
            self.nodes_parameters[s][1] += sum_v

        return sum_v, sum_n

    def simulate(self, s, color_playing):
        result = self.game.is_game_over(s, 4)
        turn = self.game.get_turn(s)
        while result == '0': # TODO usar variable inarow
            move = np.random.choice(self.game.get_open_cols(s))
            s = self.game.make_move(s, move, turn)
            result = self.game.is_game_over(s, 4)
            turn = self.game.change_turn(turn)
        return self.get_value(result, color_playing)


    def get_UCT(self, n, w, n_p):
        # return w/n + self.C * np.sqrt(n_p) / (1 + n)
        return w/n + self.C * np.sqrt(np.log(n_p) / n)

    def iterate(self, s, n_iters=None, time_limit=None):
        self.nodes_parameters[s] = np.array((1, 0))
        turn = self.game.get_turn(s)
        if time_limit is not None:
            end_time = time.time() + time_limit
            while time.time() < end_time:
                v, n = self.search(s, turn, turn)
                self.nodes_parameters[s][0] += n
                self.nodes_parameters[s][1] += v
        else:
            for _ in range(n_iters):
                v, n = self.search(s,turn, turn)
                self.nodes_parameters[s][0] += n
                self.nodes_parameters[s][1] += v
                # if i % 10 == 0:
                #     print(f'Iteration {i+1} [{"=" * (i//5)}>{" " * ((n_iters-i-1)//5)}]')

    def best_move(self, board, turn, n_iters=None, time_limit=None):
        self.iterate(board, n_iters=n_iters, time_limit=time_limit)
        max_n = 0
        moves = self.game.get_open_cols(board)
        best_move = moves[0] # por ejemplo 3
        for a in moves:
            c_aux = self.game.make_move(board, a, turn)
            # if self.game.is_game_over(c_aux, self.game.inarow) != '0':
            #     return a
            current_n = self.nodes_parameters[c_aux][0]
            if current_n > max_n:
                max_n = current_n
                best_move = a
            # print(f'N: {self.nodes_parameters[c_aux][0]} , V: {self.nodes_parameters[c_aux][1]}')
            # self.game.print_board(c_aux)
        return best_move


game = Connectx(4, 6, 7)
mcts = MCTS(game)

# c = '000000000000000102000022100001120002111200' # juega 2 buen movimiento
c = '000000000000000122000022100021120002111201' # juega 1 para evitar perder
# c = '000000000000000122000122100021120002111201' # juega 2 para ganar
# c = '000000000010000002200000210011012001221200' # juega 1 para ganar
# c = '000000000011000002200000210011012001221200' # 2 para ganar
# c = '000000000000000000000000000000000000000000'
# c = '000000000000000100020020211002022101201211'
# board = [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 1, 2, 1, 0, 0, 0, 1, 1, 2, 1, 2, 0, 2, 2, 2, 1, 2, 1, 0, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1]
# c = functools.reduce(lambda x, y: str(x) + str(y), board)
t = mcts.game.get_turn(c)
print(t)
print(game.is_game_over('000000000000000100020020211002022101201211', 4))
game.print_board(c)
print(mcts.best_move(c, t, time_limit=7))
# mcts.iterate(150, c)
print(mcts.nodes_parameters[c])
for a in mcts.game.get_open_cols(c):
    c_aux = mcts.game.make_move(c, a, t)
    print(f'N: {mcts.nodes_parameters[c_aux][0]} , V: {mcts.nodes_parameters[c_aux][1]}')
    mcts.game.print_board(c_aux)
print(len(mcts.nodes_parameters), len(mcts.explored))
mcts.game.print_board(c)
