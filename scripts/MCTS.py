from tokenize import tabsize
import numpy as np
from connectx import * 

class MCTS:
     # hiperparameter to manage expliotation vs exploration

    def __init__(self):
        self.explored = set() # fen: value // eliminar??
        self.nodes_parameters = {} # fen: (N, V) N--> times visited, V-->value
        self.UCT = {} # fen: UPC (upper confidence tree)
        self.C = 1.4 # aprox sqrt(2)

    def get_value(self, result: str, player):
        if result == '1':
            return 1 if player == '1' else -1

        elif result == '2':
            return -1 if player == '1' else 1 
        else:
            return 0

    def get_value2(result):
        pass


    # TODO: tener en cuenta el numero de movimientos sin avances para que si este es elevado se considere un empate
    def search(self, s):
        result = is_game_over(s, 4)
        if result != '0':
            v = self.get_value(result, get_turn(s)) 
            if s not in self.nodes_parameters:
                # self.visited.add(s_fen)
                self.nodes_parameters[s] = np.array((1, v))
            else:
                self.nodes_parameters[s][0] += 1
            return -v, 1

        
        # if s_fen not in self.visited:
        #   self.visited.append(s_fen)
        #   v = self.simulate(s)
        #   self.node_parameters[s_fen] = (1,v)
        #   return -v
        
        childs = get_open_cols(s)

        if s in self.explored:
        # choose which node is going to be expanded
            best_uct = float('-inf')
            best_child = None
            turn = get_turn(s)
            # best_w = 0
            n_p = self.nodes_parameters[s][0] # parent's n
            for a in childs:
                s_child = make_move(s, a, turn)
                n, w = self.nodes_parameters[s_child]
                child_uct = self.get_UCT(n, w, n_p)
                if child_uct > best_uct:
                    best_uct = child_uct
                    best_child = a
                    # best_w = w
            s = make_move(s, best_child, get_turn(s))
            sum_v, sum_n = self.search(s) # cambiar signo??
            # propagate the results
            self.nodes_parameters[s][0] += sum_n
            self.nodes_parameters[s][1] += sum_v

        
        else:
            self.explored.add(s)
            sum_v = 0
            sum_n = 0
            turn = get_turn(s)
            for a in childs:
                s_child = make_move(s, a, turn)
                if s_child not in self.nodes_parameters:
                    v = self.simulate(s_child, turn, turn) # TODO es posible que haya que mirar bien lo de los turnos
                    self.nodes_parameters[s_child] = np.array((1, v))
                    sum_v += v
                    sum_n += 1
                
            self.nodes_parameters[s][0] += sum_n
            self.nodes_parameters[s][1] += sum_v

        # v = -self.search(new_s)

        return -sum_v, sum_n

    
    def search_iter(self, s, color_playing):
        
        path = self.select(s, color_playing)
        # print(path)
        leaf = path[-1]
        self.explored.add(leaf)
        # print(self.explored)
        sum_v = 0
        sum_n = 0
        # board = chess.Board(leaf)
        board = leaf
        turn = get_turn(board)
        for a in get_open_cols(board):
            board_aux = make_move(board, a, turn)
            # a_fen = board.fen()
            if board_aux not in self.nodes_parameters:
                v = self.simulate(board_aux, color_playing, turn) 
                self.nodes_parameters[board_aux] = np.array((1, v))
                sum_v += v
                sum_n += 1
        # sum_v = -sum_v
        for i, node in enumerate(path):
            # signo = -1 if i % 2 == 0 else 1
            self.nodes_parameters[node][0] += sum_n 
            self.nodes_parameters[node][1] += sum_v
            # sum_v = -sum_v
    
    def _select(self, current_s, parent_s, turn, color_playing, best_path: dict, current_path: list, best_uct: list):
        if current_s not in self.explored: # TODO: check if is game over | podas | usar self.UCT
            if parent_s is not None:
                n_p = self.nodes_parameters[parent_s][0]
                n, w = self.nodes_parameters[current_s]
                # if turn != color_playing:
                #     w = -w
                uct = self.get_UCT(n, w, n_p)
                if uct > best_uct[0]:
                    best_uct[0] = uct
                    best_path[0] = current_path[:] # current_path[:] es mas rapido

        else:
            board = current_s
            for child in get_open_cols(board):
                child_board = make_move(board, child, turn)
                # child_fen = board.fen()
                current_path.append(child_board)
                self._select(child_board, current_s, change_turn(turn), color_playing, best_path, current_path, best_uct)
                current_path.pop()
                

    def select(self, s, turn):
        best_path = {0: [s]} # it acts as a wrapper in order to pass the varable by reference
        current_path = [s]
        best_uct = [float('-inf')] # pass this parameter by reference
        self._select(s, None, turn, turn, best_path, current_path, best_uct)
        # print(best_uct)
        return best_path[0]

    def simulate(self, s, color_playing, turn):
        result = is_game_over(s, 4)
        while result == '0': #TODO usar variable inarow
            move = np.random.choice(get_open_cols(s))
            s = make_move(s, move, turn)
            result = is_game_over(s, 4)
            turn = change_turn(turn)
        return self.get_value(result, color_playing) #TODO posible cambio

    def get_UCT(self, n, w, n_p):
        # if n_p == 0 or n == 0: return 0
        # return w/n + self.C * np.sqrt(n_p) / (1 + n)
        return w/n + self.C * np.sqrt(np.log(n_p) / n)

    def iterate(self, n_iters, s, turn):
        
        color_playing = turn
        self.nodes_parameters[s] = np.array((1, 0))
        for i in range(n_iters):
            v, n = self.search(s)
            self.nodes_parameters[s][0] += n
            self.nodes_parameters[s][1] += v
            # self.search_iter(s, color_playing)
            if i % 10 == 0:
                print(f'Iteration {i+1} [{"=" * (i//5)}>{" " * ((n_iters-i-1)//5)}]')

mcts = MCTS()
c = '000000000000000102000022100001120002111200' # juega 2 buen movimiento
# c = '000000000000000122000022100021120002111201' # juega 1 para evitar perder
# c = '000000000000000122000122100021120002111201' # juega 2 para ganar
# c = '000000000000000000000000000000000000000000'
t = get_turn(c)
mcts.iterate(150, c, t)
# mcts.simulate(c, t, t)
i = 0
# mcts.simulate(fen_prueba, chess.WHITE)
print(mcts.nodes_parameters[c])
for a in get_open_cols(c):
    c_aux = make_move(c, a, t)
    print(f'N: {mcts.nodes_parameters[c_aux][0]} , V: {mcts.nodes_parameters[c_aux][1]}')
    print_board(c_aux)
    
    i+=1
print(len(mcts.nodes_parameters), len(mcts.explored))

print_board(c)