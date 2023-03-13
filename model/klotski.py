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

    def bfs(self):
        queue = [self.state]
        visited = []

        while queue:
            current = queue.pop(0)
            visited.append(self.state)

            if current.is_complete():
                return current

            for child in current.children():
                if child not in visited:
                    queue.append(child)

        return None

    def a_star(self):
        states = [self.state]
        visited = []
        
        while states:
            current = heapq.heappop(states)
            visited.append(current)

            if current.is_complete():
                return current

            for child in current.children():
                if child not in visited:
                    heapq.heappush(states, child)
        
        return None


if __name__ == '__main__':
    game = Klotski()
    game.read_board('assignment1/inputs/board1.txt')

    result = game.a_star()
    print(len(result.move_history))