from copy import deepcopy

from model.move import Move


class KlotskiState:

    possible_directions = ('up', 'left', 'down', 'right')
    direction_sums = {
        'up': (-1, 0),
        'left': (0, -1),
        'down': (1, 0),
        'right': (0, 1)
    }
    direction_opposites = {
        'up': 'down',
        'left': 'right',
        'down': 'up',
        'right': 'left'
    }
    direction_adjascents = {
        'up': ('left', 'right'),
        'left': ('up', 'down'),
        'down': ('left', 'right'),
        'right': ('up', 'down')
    }

    def __init__(self, board, objectives, move_history=[]):
        self.board = deepcopy(board)
        self.max_row = len(self.board) - 1
        self.max_col = len(self.board[0]) - 1

        self.objectives = objectives

        self.empties = self._find_empties()
        self.empty0, self.empty1 = self.empties
        self.empty0_row, self.empty0_col = self.empty0
        self.empty1_row, self.empty1_col = self.empty1

        self.move_history = [] + move_history + [self.board]

    def __eq__(self, other):
        # assumes that the boards are of same size
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id != other.board[i][j].id:
                    return False
        return True
    
    '''
    def __lt__(self, other):
        return self.heuristic() < other.heuristic()
    '''

    def _find_empties(self):
        self.empties = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id == -1:
                    self.empties.append((i, j,))
        
        assert len(self.empties) == 2
        return set(self.empties)

    def print(self):
        for row in self.board:
            for cell in row:
                n_spaces = 3 - len(str(cell.id))
                spaces = ''.join([' ' for _ in range(n_spaces)])
                print(f'{cell.id}{spaces}', end='')
            print('\n')

    def get_id_matrix(self):
        return [[cell.id for cell in row] for row in self.board]
    
    def get_objectives(self):
        return self.objectives

    def _empties_connected(self):
        return abs(self.empty0_row - self.empty1_row) + abs(self.empty0_col - self.empty1_col) == 1

    def _get_double_moves(self):
        doubles = []
        if self.empty0_row == self.empty1_row:
            if self.empty0_row >= 1 \
                and self.board[self.empty0_row][self.empty0_col].up.id == self.board[self.empty1_row][self.empty1_col].up.id:
                doubles.append(Move(self.board, self.board[self.empty0_row][self.empty0_col].up.id, 'down'))
            
            if self.empty0_row <= self.max_row - 1 \
                and self.board[self.empty0_row][self.empty0_col].down.id == self.board[self.empty1_row][self.empty1_col].down.id:
                doubles.append(Move(self.board, self.board[self.empty0_row][self.empty0_col].down.id, 'up'))
        
        elif self.empty0_col == self.empty1_col:
            if self.empty0_col >= 1 \
                and self.board[self.empty0_row][self.empty0_col].left.id == self.board[self.empty1_row][self.empty1_col].left.id:
                doubles.append(Move(self.board, self.board[self.empty0_row][self.empty0_col].left.id, 'right'))

            if self.empty0_col <= self.max_col - 1 \
                and self.board[self.empty0_row][self.empty0_col].right.id == self.board[self.empty1_row][self.empty1_col].right.id:
                doubles.append(Move(self.board, self.board[self.empty0_row][self.empty0_col].right.id, 'left'))
            
        else:
            raise Exception('''this shouldn't happen; check the connection func''')
        
        return doubles
    
    def _get_single_moves(self):
        # this assumes that every piece is rectangular
        singles = []
        
        for empty_row, empty_col in self.empties:
            for dir in self.possible_directions:
                row_sum, col_sum = self.direction_sums[dir]
                test_row, test_col = empty_row + row_sum, empty_col + col_sum

                if test_row >= 0 and test_row <= self.max_row \
                    and test_col >= 0 and test_col <= self.max_col:

                    test_cell = self.board[test_row][test_col]
                    if test_cell.id == -1:
                        continue

                    adj0, adj1 = self.direction_adjascents[dir]

                    if (test_cell[adj0] is None or test_cell.id != test_cell[adj0].id) \
                        and (test_cell[adj1] is None or test_cell.id != test_cell[adj1].id):

                        singles.append(Move(self.board, test_cell.id, self.direction_opposites[dir]))

        return singles
    
    def _get_top_left_most_red_square(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id == 0:
                    return (i, j)
        raise Exception('''this shouldn't happen''')
    
    def manhattan(self):
        # checks the manhattan distance of the top-left most square
        # of the red piece to the top-left most destination
        origin = self._get_top_left_most_red_square()
        destination = self.objectives[0]

        return abs(origin[0] - destination[0]) \
            + abs(origin[1] - destination[1])

    def children(self):
        moves = []
        if self._empties_connected():
            moves += self._get_double_moves()
        moves += self._get_single_moves()

        return [self.do_move(m) for m in moves]
    
    def do_move(self, move):
        new_board = move.resulting_board()
        return KlotskiState(new_board, self.objectives, self.move_history)
    
    def is_complete(self):
        for i, j in self.objectives:
            if self.board[i][j].id != 0:
                return False
        return True
