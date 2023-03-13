from model.klotski import Klotski

class Controller:

    def __init__(self):
        self.game = Klotski()

    def load_game(self, game_id):
        self.game.read_board(f'/home/matheus/UP/2023-1/ElemIADS/assignment1/inputs/{game_id}.txt')
    
    def get_current_board(self):
        return self.game.get_id_matrix(), self.game.get_objectives()