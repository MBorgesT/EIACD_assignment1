from copy import deepcopy
import heapq

from model.board_cell import BoardCell
from model.klotski_state import KlotskiState
    

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
        
        self.state = KlotskiState(board, objectives)

    def get_id_matrix(self):
        assert self.state is not None
        return self.state.get_id_matrix()
    
    def get_objectives(self):
        assert self.state is not None
        return self.state.get_objectives()

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
    
    def greedy_search(self, heuristic=None, manhattan_multi=20, zeros_empty_multi=20, inbet_multi=0):
        if heuristic is None:
            heuristic = lambda self, other: \
                self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) \
                < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi)
        setattr(KlotskiState, "__lt__", heuristic)
        
        states = [self.state]
        visited = []
        
        while states:
            current = heapq.heappop(states)
            visited.append(current.get_id_matrix())

            if current.is_complete():
                return current

            for child in current.children():
                if child.get_id_matrix() not in visited:
                    heapq.heappush(states, child)
        
        return None

    def a_star(self, manhattan_multi, zeros_empty_multi, inbet_multi):
        heuristic = lambda self, other: \
            self.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + len(self.move_history) - 1 \
            < other.heuristic(manhattan_multi, zeros_empty_multi, inbet_multi) + len(other.move_history) - 1
        return self.greedy_search(heuristic)
