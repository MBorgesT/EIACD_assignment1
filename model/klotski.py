from copy import deepcopy
import heapq
from concurrent.futures import wait, FIRST_COMPLETED
from pebble import ProcessPool
import multiprocessing

from model.board_cell import BoardCell
from model.klotski_state import KlotskiState
from model.trie import Trie
    

class Klotski:

    def __init__(self):
        pass   

    def read_board(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.readlines()

        proto_board = []
        objectives = []

        first_line = lines[0].replace('\n', '').replace(' ', '').split(';')
        for o in first_line:
            o = o.split(',')
            objectives.append((int(o[0]), int(o[1])))
        # for later usage; it helps to assure that the top-left most objective
        # is first
        objectives = sorted(objectives, key=lambda x: (x[0], x[1]))

        for l in lines[1:]:
            l = l.replace('\n', '')
            l = l.replace('  ', ' ')
            l = l.split(' ')
            proto_board.append([int(cell) for cell in l])
        
        board = []
        for i in range(len(proto_board)):
            row = []
            for j in range(len(proto_board[0])):
                row.append(BoardCell(i, j, proto_board[i][j]))
            board.append(row)
        
        for row in board:
            for cell in row:
                cell.late_init(board)
        
        self.objectives = objectives
        self.state = KlotskiState(board, objectives)

    def get_id_matrix(self):
        assert self.state is not None
        return self.state.get_id_matrix()
    
    def get_objectives(self):
        assert self.objectives is not None
        return self.objectives

    def bfs(self):
        queue = [self.state]
        visited = []

        while queue:
            current = queue.pop(0)
            visited.append(self.state.get_id_matrix())

            if current.is_complete():
                return current

            for child in current.children():
                if child.get_id_matrix() not in visited:
                    queue.append(child)

        return None
    
    def a_star(self, manhattan_multi, zeros_empty_multi, inbet_multi, len_multi=1):
        heuristic = lambda self, other: \
            self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + (len(self.move_history) - 1) * len_multi \
            < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + (len(other.move_history) - 1) * len_multi
        return self.greedy_search(heuristic=heuristic)
    
    def greedy_search(self, manhattan_multi=12, zeros_empty_multi=1, inbet_multi=2, heuristic=None):
        if heuristic is None:
            heuristic = lambda self, other: \
                self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) \
                < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi)
        setattr(KlotskiState, "__lt__", heuristic)
        
        states = [self.state]
        visited = Trie()
        
        while states:
            current = heapq.heappop(states)
            visited.insert(current.get_id_matrix())

            if current.is_complete():
                return current

            for child in current.children():
                if not visited.is_in_trie(child.get_id_matrix()):
                    heapq.heappush(states, child)
        
        return None
    
    def parallel_a_star(self, manhattan_multi, zeros_empty_multi, inbet_multi, len_multi=1):
        heuristic = lambda self, other: \
            self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + (len(self.move_history) - 1) * len_multi \
            < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + (len(other.move_history) - 1) * len_multi
        return self.parallel_greedy_search(heuristic=heuristic)
    
    def parallel_greedy_search(self, manhattan_multi=12, zeros_empty_multi=1, inbet_multi=2, heuristic=None):
        global loop
        
        if heuristic is None:
            heuristic = lambda self, other: \
                self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) \
                < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi)
        setattr(KlotskiState, "__lt__", heuristic)
        
        states = [self.state]
        visited = Trie()

        def loop():
            while True:
                current = heapq.heappop(states)
                visited.insert(current.get_id_matrix())

                if current.is_complete():
                    return current

                for child in current.children():
                    if not visited.is_in_trie(child.get_id_matrix()):
                        heapq.heappush(states, child)
        
        workers = multiprocessing.cpu_count()
        with ProcessPool(max_workers=workers) as pool:
            funcs = set()
            for _ in range(workers):
                funcs.add(pool.schedule(loop))
            done, not_done = wait(funcs, return_when=FIRST_COMPLETED)
            for f in not_done:
                f.cancel()
            return list(done)[0].result()
