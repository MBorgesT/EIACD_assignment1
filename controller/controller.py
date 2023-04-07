from time import time
from model.klotski import Klotski

class Controller:

    search_args = {
        'greedy': (50, 50, 15),
        'a_star': (50, 50, 15)
    }

    def __init__(self, play_interval=.67):
        self.play_interval = play_interval

        self.game = Klotski()
        self.search_algs = {
            'greedy': self.game.greedy_search,
            'a_star': self.game.a_star
        }

        self.searching = False

        self.playing_result = False
        self.alg_move_history = dict()

    def load_game(self, game_id):
        self.game.read_board(f'inputs/set1/{game_id}.txt')
        self.objectives = self.game.get_objectives()

        self.playing_result = False
        self.alg_move_history = dict()
    
    def get_current_board(self):
        if self.playing_result:
            if self.move_i != len(self.move_history) - 1 and time() - self.move_tick >= self.play_interval:
                self.move_i += 1
                self.move_tick = time()

            return self.move_history[self.move_i], self.objectives
        else:
            return self.game.get_id_matrix(), self.objectives
        
    def _init_play_animation(self):
        self.playing_result = True
        self.move_i = 0
        self.move_tick = time()

    def is_alg_ready(self, alg):
        try:
            self.alg_move_history[alg]
            return True
        except KeyError:
            return False

    def play(self, alg):
        assert self.alg_move_history[alg] is not None
        self.move_history = self.alg_move_history[alg]
        self._init_play_animation()
    
    def search_alg(self, alg):
        try:
            print('Searching...')
            self.searching = True
        finally:
            args = self.search_args[alg]
            self.alg_move_history[alg] = self.search_algs[alg](*args).move_history
            self.searching = False
            print('Done')