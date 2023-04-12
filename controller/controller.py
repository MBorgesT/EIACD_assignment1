import os
from time import time
import tracemalloc

from model.klotski import Klotski


class Controller:
    """
    Connection class between the game logic and the graphic
    user interface. It also stores the search results and
    isolates the GUI from any non-interface logic that doesn't
    fit the model classes.
    """

    inputs_folder = 'inputs/set1/'
    search_args = {
        'greedy': (12, 1, 2),
        'a_star': (12, 1, 2),
        'bfs': (),
        'dfs': (),
        'i_dfs': (),
    }

    def __init__(self, play_interval=.7):
        """
        Initiates some attributes that are used in the follow up
        methods.

        Args:
            play_interval (float, optional): The amount of time
            it takes between moves in the play animation. Defaults 
            to 0.7.
        """
        self.play_interval = play_interval

        self.game = Klotski()
        self.search_algs = {
            'greedy': self.game.greedy_search,
            'a_star': self.game.a_star,
            'bfs': self.game.bfs,
            'dfs': self.game.dfs,
            'i_dfs': self.game.iterative_deepening_search
        }

        self.currently_playing_result = False

        self.results = dict()

    def load_game(self, game_id):
        """
        Loads a certain game level by its id.

        Args:
            game_id (int): Game id to be loaded.
        """
        self.game.read_board(f'{self.inputs_folder}{game_id}.txt')
        self.goals = self.game.get_goals()

        self.currently_playing_result = False
        self.alg_move_history = dict()

        if game_id not in self.results.keys():
            self.results[game_id] = dict()

        self.game_id = game_id

    def get_current_game_id(self):
        return self.game_id

    def get_level_names(self):
        """
        Lists the level names in the input folder.

        Returns:
            list of str: Level names in the input folder.
        """
        return [x.replace('.txt', '')
                for x in
                sorted(os.listdir(self.inputs_folder), key=lambda x: int(''.join(c for c in x if c.isdigit())))]

    def get_current_board(self):
        """
        If at the initial state of the game, returns it. If
        not, does the logic behind the play animation.

        Returns:
            tuple: Current id matrix and goals.
        """
        if self.currently_playing_result:
            if self.move_i != len(self.move_history) - 1 and time() - self.move_tick >= self.play_interval:
                self.move_i += 1
                self.move_tick = time()

            return self.move_history[self.move_i], self.goals
        else:
            return self.game.get_id_matrix(), self.goals

    def _init_play_animation(self):
        """
        Initializes the attributes that signilize the
        start of the play animation.
        """
        self.currently_playing_result = True
        self.move_i = 0
        self.move_tick = time()

    def is_alg_ready(self, alg):
        """
        Checks if the search algorithm is done.

        Args:
            alg (str): The algorithm to be checked.

        Returns:
            boolean: True if done, False if not.
        """
        try:
            self.results[self.game_id][alg]
            return True
        except KeyError:
            return False

    def play(self, alg):
        """
        Starts the play animation

        Args:
            alg (str): The algorithm result to be played.
        """
        assert self.results[self.game_id][alg] is not None
        self.move_history = self.results[self.game_id][alg]['move_history']
        self._init_play_animation()

    def search_alg(self, alg):
        """
        Performs the search algorithm and extracts information
        from it.

        Args:
            alg (str): Algorithm to be run.
        """
        print('Searching...')

        args = self.search_args[alg]

        tracemalloc.start()
        start_time = time()

        result = self.search_algs[alg](*args)

        exec_time = time() - start_time
        tm = tracemalloc.get_traced_memory()
        memory_used = tm[1] - tm[0]

        self.results[self.game_id][alg] = dict()
        self.results[self.game_id][alg]['move_history'] = result.move_history
        self.results[self.game_id][alg]['n_moves'] = len(result.move_history) - 1
        self.results[self.game_id][alg]['exec_time'] = exec_time
        self.results[self.game_id][alg]['memory_used'] = memory_used
    
        print('Done')

    def get_results(self, alg):
        """
        Returns the result of a certain algorithm.

        Args:
            alg (str): Algorithm to have its result
            returned.

        Returns:
            dict: Algorithm execution results.
        """
        return self.results[self.game_id][alg]
