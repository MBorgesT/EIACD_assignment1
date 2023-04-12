class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}

class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")
    
    def insert(self, board):
        """Insert a board into the trie"""
        node = self.root
        
        # Loop through each cell in the board
        # Check if there is no child containing the cell, create a new child for the current node
        for row in board:
            for cell in row:
                if cell in node.children:
                    node = node.children[cell]
                else:
                    # If a cell is not found,
                    # create a new node in the trie
                    new_node = TrieNode(cell)
                    node.children[cell] = new_node
                    node = new_node
        
        # Mark the end of a board
        node.is_end = True
        
    def is_in_trie(self, x):
        """
        Checks if the x board is in the tree.
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        node = self.root
        
        # Check if the prefix is in the trie
        for row in x:
            for cell in row:
                if cell in node.children:
                    node = node.children[cell]
                else:
                    # cannot found the prefix, return empty list
                    return False
        
        return True