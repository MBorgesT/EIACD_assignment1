from copy import deepcopy


class Move:
    """
    

    Returns:
        _type_: _description_
    """

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
    
    def __init__(self, piece_id, direction):
        self.piece_id = piece_id
        self.direction = direction

    def _set_piece_locations(self, board):
        self.piece_locations = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].id == self.piece_id:
                    self.piece_locations.append((i, j,))
    
    def resulting_board(self, board):
        board = deepcopy(board)
        self._set_piece_locations(board)

        for loc_row, loc_col in self.piece_locations:
            board[loc_row][loc_col].id = -1

        row_sum, col_sum = self.direction_sums[self.direction]
        for loc_row, loc_col in self.piece_locations:
            board[loc_row+row_sum][loc_col+col_sum].id = self.piece_id
        
        return board