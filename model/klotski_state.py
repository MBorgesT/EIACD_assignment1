from copy import deepcopy

from model.move import Move


class KlotskiState:
    """
    Individual game state representation, with functions related
    to the generation of new states reachable from this one and
    its evaluation through heuristics.
    """

    """
    The following variables are used to make the  functions that
    search for new moves easier to read.
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
    direction_adjascents = {
        'up': ('left', 'right'),
        'left': ('up', 'down'),
        'down': ('left', 'right'),
        'right': ('up', 'down')
    }

    def __init__(self, board, goals, move_history=[]):
        """
        Args:
            board (Cell matrix): Matrix that represents a state of the 
            game. Cells of id 0 represent the game's red square and 
            cells of id -1 represent empty squares.

            goals (array of 2D tuples): List made out of (row, col) 
            tuples with the red square's end goal.

            move_history (list, optional): List made of out id (int)
            matrices, these being the past board states that led to
            this one. The matrices are made out of integers instead of
            Cell instances for it being a simpler data structure, and
            the pointers to adjascent cells not being necessary for
            what this is used.
        """
        self.board = deepcopy(board)
        self.max_row = len(self.board) - 1
        self.max_col = len(self.board[0]) - 1

        self.goals = goals

        self.empties = self._find_empties()
        self.empty0, self.empty1 = self.empties

        self.zeros = self._find_zeros()

        self.id_matrix = self._get_id_matrix()
        self.move_history = [] + move_history + [self.id_matrix]

    def __eq__(self, other):
        """
        Checks if both states have the same board configuration.

        Args:
            other (KlotskiState): The state to compare self to.

        Raises:
            Exception: If the boards are of different sizes.

        Returns:
            boolean: True if they're equal, False if not.
        """
        assert type(other) is KlotskiState
        if len(self.board) != len(other.board) or len(self.board[0]) != len(other.board[0]):
            raise Exception('Boards of different size being compared')
        
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].id != other.board[i][j].id:
                    return False
        return True
    
    def __str__(self):
        """
        Conversion of the state to string.

        Returns:
            str: String representation of the current state.
        """
        values = []
        for row in self.board:
            line = []
            for cell in row:
                n_spaces = 3 - len(str(cell.id))
                spaces = ''.join([' ' for _ in range(n_spaces)])
                line.append(f'{cell.id}{spaces}')
                
            values.append(''.join(line))
        
        return '\n'.join(values)

    def _find_empties(self):
        """
        Search for the empty Cells (id == -1)

        Returns:
            Tuple of 2D tuples: List of tuples made out of rows 
            and cols.
        """
        empties = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].is_empty():
                    empties.append(self.board[row][col])

        if len(empties) != 2:
            print(empties)
            raise Exception("This shouldn't happen")
        return set(empties)

    def _find_zeros(self):
        """
        Search for the red square Cells (id == 0)

        Returns:
            Tuple of 2D tuples: List of tuples made out of rows 
            and cols.
        """
        zeros = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].is_red_piece():
                    zeros.append(self.board[row][col])

        return set(zeros)

    def _get_id_matrix(self):
        """
        Creates a matrix made out of the board Cells ids

        Returns:
            int matrix: Cell id matrix
        """
        return [[cell.id for cell in row] for row in self.board]

    def _empties_connected(self):
        """
        Checks if the empty squares are connecting by calculating
        their manhattan distance, and returning True of this 
        distance equals 1.

        Returns:
            boolean: True if connected, False if not.
        """
        return abs(self.empty0.row - self.empty1.row) + abs(self.empty0.col - self.empty1.col) == 1

    def _get_double_moves(self):
        """
        Checks for the orientation of the connected empty squares 
        and looks for pieces that could be moved into their places.

        Returns:
            list of Move: Possible double moves that can be done.
        """
        doubles = []
        if self.empty0.row == self.empty1.row:
            if self.empty0.row >= 1 and self.empty0.up.id == self.empty1.up.id:
                doubles.append(
                    Move(self.empty0.up.id, 'down'))

            if self.empty0.row <= self.max_row - 1 \
                    and self.empty0.down.id == self.empty1.down.id:
                doubles.append(
                    Move(self.empty0.down.id, 'up'))

        elif self.empty0.col == self.empty1.col:
            if self.empty0.col >= 1 and self.empty0.left.id == self.empty1.left.id:
                doubles.append(
                    Move(self.empty0.left.id, 'right'))

            if self.empty0.col <= self.max_col - 1 and self.empty0.right.id == self.empty1.right.id:
                doubles.append(
                    Move(self.empty0.right.id, 'left'))

        else:
            raise Exception(
                '''this shouldn't happen; check the empties connection func''')

        return doubles

    def _get_single_moves(self):
        """

        Returns:
            _type_: _description_
        """
        # this assumes that every piece is rectangular
        singles = []

        for e in self.empties:
            for dir in self.possible_directions:
                row_sum, col_sum = self.direction_sums[dir]
                # gets the adjascent indexes to be tested
                test_row, test_col = e.row + row_sum, e.col + col_sum

                if test_row >= 0 and test_row <= self.max_row \
                        and test_col >= 0 and test_col <= self.max_col:

                    test_cell = self.board[test_row][test_col]
                    if test_cell.is_empty():
                        continue

                    adj0, adj1 = self.direction_adjascents[dir]
                    # checks if the piece is skinny enough to fit into the single
                    # empty spot
                    if (test_cell[adj0] is None or test_cell.id != test_cell[adj0].id) \
                            and (test_cell[adj1] is None or test_cell.id != test_cell[adj1].id):

                        singles.append(
                            Move(test_cell.id, self.direction_opposites[dir]))

        return singles

    def _get_top_left_most_red_square(self):
        """
        Iterates through the Cell matrix and returns the first 
        red square it finds. Used to calculate the manhattan distance.

        Returns:
            int tuple: 2D int tuple of (row, col)
        """

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col].is_red_piece():
                    return (row, col)
        raise Exception('''this shouldn't happen''')

    def _do_move(self, move):
        """
        Creates a new KlotskiState from a possible move.

        Args:
            move (Move): The move to be done.

        Returns:
            KlotskiState: State reachable by the move.
        """
        new_board = move.resulting_board(self.board)
        return KlotskiState(new_board, self.goals, self.move_history)

    def _manhattan(self):
        """
        Calculates the manhattan distance of the top-left most square
        of the red piece to the top-left most goal.

        Returns:
            int: Manhattan distance.
        """
        origin = self._get_top_left_most_red_square()
        goal = self.goals[0]

        return abs(origin[0] - goal[0]) \
            + abs(origin[1] - goal[1])

    def _zeros_empties_distance(self):
        """
        Calculates the distance between the empty squares and the red
        piece.

        Returns:
            int: Manhattan distance.
        """
        dist_func = lambda x, y: abs(x.row - y.row) + abs(x.col - y.col)

        dist0 = min([dist_func(z, self.empty0) for z in self.zeros]) - 1
        dist1 = min([dist_func(z, self.empty1) for z in self.zeros]) - 1

        return dist0 + dist1

    def _empties_inbetween_zeros_goals(self):
        """
        Checks if the the empty squares are between the red piece and 
        the goals. Each value is related to each empty square.

        Returns:
            int: Sum of the values.
        """
        v0 = int(any([self.empty0.row == z.row == o[0] \
                    or self.empty0.col == z.col == o[1] \
                    for z in self.zeros for o in self.goals]))
        
        v1 = int(any([self.empty1.row == z.row == o[0] \
                    or self.empty1.col == z.col == o[1] \
                    for z in self.zeros for o in self.goals]))
        
        return v0 + v1

    def heuristic(self, manhattan_multi, zeros_empty_multi, inbet_multi):
        """
        Weighted sum of each evaluation heuristic we have in the class.

        Args:
            manhattan_multi (float): Weight for the manhattan distance.

            zeros_empty_multi (float): Weight for the distance between
            the red piece and the empty squares.

            inbet_multi (float): Weight for the check if the the empty 
            squares are between the red piece and the goals.
        goals

        Returns:
            float: Heuristic value.
        """
        return manhattan_multi * self._manhattan() \
            + zeros_empty_multi * self._zeros_empties_distance() \
            + inbet_multi * self._empties_inbetween_zeros_goals()

    def children(self):
        """
        Generates the reachable statles from the current one.

        Returns:
            List of KlotskiState: Reachable states.
        """
        moves = []
        if self._empties_connected():
            moves += self._get_double_moves()
        moves += self._get_single_moves()

        return [self._do_move(m) for m in moves]
    
    def is_complete(self):
        """
        Checks if the state is a final one. It is when all the
        goal squares are filled with Cells of id 0.

        Returns:
            boolean: True if complete, False if not.
        """
        for row, col in self.goals:
            if not self.board[row][col].is_red_piece():
                return False
        return True
