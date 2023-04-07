from copy import deepcopy


class Move:
    """
    An auxiliary class that contains the information of a possible
    move, containing a function that returns the resulting board of
    the move.
    """

    """
    As in the KlotskiState class, the following attributes exist to
    make the class' functions easier to comprehend.
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
        """
        Self explanatory.

        Args:
            piece_id (int): The id of the piece to be moved.
            direction (str): The direction to be moved.
        """
        self.piece_id = piece_id
        self.direction = direction

    def _set_piece_locations(self, board):
        """
        Search the board for the move's piece locations.

        Args:
            board (BoardCell matrix): The current state of
            the board.

        Returns:
            piece_locations (2D tuple list): The locations
            referring to this instance's piece id.
        """
        piece_locations = []
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col].id == self.piece_id:
                    piece_locations.append((row, col))
        return piece_locations
    
    def resulting_board(self, board):
        """
        Generates a new board from the move this instance
        refers to.

        Args:
            board (BoardCell matrix): The current state of
            the board.

        Returns:
            board (BoardCell matrix): The resulting board
            after this instance's move.
        """
        board = deepcopy(board)
        piece_locations = self._set_piece_locations(board)

        for loc_row, loc_col in piece_locations:
            board[loc_row][loc_col].id = -1

        row_sum, col_sum = self.direction_sums[self.direction]
        for loc_row, loc_col in self.piece_locations:
            board[loc_row+row_sum][loc_col+col_sum].id = self.piece_id
        
        return board