from copy import deepcopy


class Move:

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
    
    def __init__(self, board, piece_id, direction):
        self.board = deepcopy(board)
        self.piece_id = piece_id
        self.direction = direction

        self._set_piece_locations()

    def _set_piece_locations(self):
        self.piece_locations = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id == self.piece_id:
                    self.piece_locations.append((i, j,))
    
    def resulting_board(self):
        for loc_row, loc_col in self.piece_locations:
            self.board[loc_row][loc_col].id = -1

        row_sum, col_sum = self.direction_sums[self.direction]
        for loc_row, loc_col in self.piece_locations:
            self.board[loc_row+row_sum][loc_col+col_sum].id = self.piece_id
        
        return self.board
    

class BoardCell:

    def __init__(self, row, col, id):
        self.row = row
        self.col = col
        self.id = id

        self.up = None
        self.left = None
        self.down = None
        self.right = None

    def __getitem__(self, key):
        return getattr(self, key)
    
    def late_init(self, board):
        if self.row - 1 >= 0:
            self.up = board[self.row-1][self.col]
        else:
            self.up = None

        if self.row + 1 <= len(board) - 1:
            self.down = board[self.row+1][self.col]
        else:
            self.down = None

        if self.col - 1 >= 0:
            self.left = board[self.row][self.col-1]
        else:
            self.left = None

        if self.col + 1 <= len(board[0]) - 1:
            self.right = board[self.row][self.col+1]
        else:
            self.right = None
    

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

    def __init__(self, board, move_history=[]):
        self.board = deepcopy(board)
        self.max_row = len(self.board) - 1
        self.max_col = len(self.board[0]) - 1

        self.empties = self._find_empties()
        self.empty0, self.empty1 = self.empties
        self.empty0_row, self.empty0_col = self.empty0
        self.empty1_row, self.empty1_col = self.empty1
        
        self._late_init_cells()

        self.move_history = [] + move_history + [self.board]

    def _find_empties(self):
        self.empties = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id == -1:
                    self.empties.append((i, j,))
        
        assert len(self.empties) == 2
        return set(self.empties)
    
    def _late_init_cells(self):
        for row in self.board:
            for cell in row:
                cell.late_init(self.board)

    def print(self):
        for row in self.board:
            for cell in row:
                n_spaces = 3 - len(str(cell.id))
                spaces = ''.join([' ' for _ in range(n_spaces)])
                print(f'{cell.id}{spaces}', end='')
            print('\n')

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


    def children(self):
        children = []
        if self._empties_connected():
            children += self._get_double_moves()
        children += self._get_single_moves()

        return children
    
    def do_move(self, move):
        new_board = move.resulting_board()
        return KlotskiState(new_board, self.move_history)
    

def read_board(file_name):
    proto_board = []
    with open(file_name, 'r') as f:
        for l in f:
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
    
    return board


if __name__ == '__main__':
    board = read_board('assignment1/board1.txt')
    state = KlotskiState(board)
    state.print()

    print('\n')

    children = state.children()
    for child_i, c in enumerate(children):
        print('\n')

        print(f'{c.piece_id} - {c.direction}')

        new_state = state.do_move(c)
        new_state.print()