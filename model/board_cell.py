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
