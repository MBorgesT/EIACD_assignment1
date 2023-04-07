class BoardCell:
    """
    A class for the individual board cells, containing pointers
    to the adjascent cells.
    """

    def __init__(self, row, col, id):
        self.row = row
        self.col = col
        self.id = id

        self.up = None
        self.left = None
        self.down = None
        self.right = None

    def __getitem__(self, key):
        """
        Used alongside the auxiliary attributes in the Klotski
        and KlotskiState classes to get the adjascent cells.
        
        Args:
            key (str): Referring to one of the four directions.

        Returns:
            BoardCell: The adjascent BoardCell referring to 
            direction in the key attribute.
        """
        return getattr(self, key)
    
    def late_init(self, board):
        """
        Setup of the pointers to the adjascent BoardCells.

        Args:
            board (BoardCell matrix): The board this BoardCell
            is part of.
        """
        if self.row - 1 >= 0:
            self.up = board[self.row-1][self.col]

        if self.row + 1 <= len(board) - 1:
            self.down = board[self.row+1][self.col]

        if self.col - 1 >= 0:
            self.left = board[self.row][self.col-1]

        if self.col + 1 <= len(board[0]) - 1:
            self.right = board[self.row][self.col+1]
