import pygame
from decimal import Decimal

from controller.controller import Controller


class GUI:
    """
    The graphic user interface implemented in pygame.
    """

    search_algs = ('greedy', 'a_star', 'dfs', 'i_dfs', 'bfs')

    def __init__(self):
        self.screen_width, self.screen_height = 800, 650
        self.board_width = 680
        self.divider_width = 5
        self.level_selector_width = self.screen_width - \
            self.board_width - self.divider_width

        self.level_id = 'board1'

        self.controller = Controller()

    def run(self):
        pygame.init()

        self.font14 = pygame.font.SysFont('Arial', 14)
        self.font11 = pygame.font.SysFont('Arial', 11)

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        self.controller.load_game(self.level_id)

        self.solution = None

        while True:
            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click_action()

            # Do logical updates here.
            # ...

            self.screen.fill('black')  # Fill the display with a solid color

            # Render the graphics here.
            # ...
            self.draw()

            pygame.display.flip()  # Refresh on-screen display
            self.clock.tick(60)

    def click_action(self):
        mouse_pos = pygame.mouse.get_pos()

        for b, l in self.level_selection_buttons:
            if b.collidepoint(mouse_pos):
                self.controller.load_game(l)
                return

        for b, alg_name in self.search_buttons:
            if b.collidepoint(mouse_pos):
                self.controller.search_alg(alg_name)
                return
            
        for b, alg_name in self.play_buttons:
            if b.collidepoint(mouse_pos):
                self.controller.play(alg_name)
                return

    def draw(self):
        # board
        self.draw_board(*self.controller.get_current_board())

        # divider
        self.draw_divider()

        # selectors
        self.draw_level_selector()

        # search algs
        self.draw_search_buttons()

    def draw_board(self, board, goals, square_size=80, square_border=2, goal_size=16):
        margin = (self.board_width - (square_size * len(board[0]))) / 2

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == -1:
                    color = (220, 220, 220)
                elif cell == 0:
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 0)

                height_pos = margin + (i * square_size) + square_border + 50
                width_pos = margin + (j * square_size) + square_border

                pygame.draw.rect(
                    self.screen, color,
                    pygame.Rect(width_pos, height_pos,
                                square_size-(square_border*2),
                                square_size-(square_border*2))
                )

                # erasing margins
                if i >= 1 and board[i-1][j] == cell:
                    pygame.draw.rect(
                        self.screen, color,
                        pygame.Rect(width_pos, height_pos-(2*square_border),
                                    square_size-(2*square_border), 2*square_border)
                    )
                if j >= 1 and board[i][j-1] == cell:
                    pygame.draw.rect(
                        self.screen, color,
                        pygame.Rect(width_pos-(2*square_border), height_pos,
                                    2*square_border, square_size-(2*square_border))
                    )
                if i >= 1 and j >= 1 and board[i-1][j-1] == cell:
                    pygame.draw.rect(
                        self.screen, color,
                        pygame.Rect(width_pos-(2*square_border), height_pos-(2*square_border),
                                    2*square_border, 2*square_border)
                    )

        # goals
        for goal_row, goal_col in goals:
            height_pos = margin + (goal_row * square_size) + \
                ((square_size - goal_size) / 2) + 50
            width_pos = margin + (goal_col * square_size) + \
                ((square_size - goal_size) / 2)

            pygame.draw.rect(
                self.screen, (255, 50, 50),
                pygame.Rect(width_pos, height_pos,
                            goal_size, goal_size),
                border_radius=2
            )

    def draw_divider(self):
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            pygame.Rect(self.board_width, 0,
                        self.divider_width, self.screen_height)
        )

    def draw_level_selector(self, margin_size=2, rectangle_height=30):
        levels = self.controller.get_level_names()
        base_width = self.board_width + self.divider_width

        self.level_selection_buttons = []
        for i, l in enumerate(levels):
            base_height = i*rectangle_height

            pygame.draw.rect(
                self.screen, (255, 255, 255),
                pygame.Rect(base_width, base_height,
                            self.level_selector_width, rectangle_height)
            )

            if l == self.controller.get_current_game_id():
                background_color = (80, 80, 80)
            else:
                background_color = (0, 0, 0)
            b = pygame.draw.rect(
                self.screen, background_color,
                pygame.Rect(base_width + margin_size, base_height - margin_size,
                            self.level_selector_width - (2 * margin_size), rectangle_height - (2 * margin_size))
            )

            text_img = self.font14.render(l, True, (255, 255, 255))
            self.screen.blit(
                text_img, (base_width + 2 * margin_size, base_height + 2 * margin_size))
            self.level_selection_buttons.append((b, l))

    def draw_search_buttons(self, button_width=85, button_height=20):
        self.search_buttons = []
        self.play_buttons = []

        for i, alg_name in enumerate(self.search_algs):
            start_width = i * button_width + (i + 1) * 10

            b = pygame.draw.rect(
                self.screen, (0, 200, 0),
                pygame.Rect(start_width, 10, button_width, button_height)
            )
            text_img = self.font14.render(alg_name.upper(), True, (255, 255, 255))
            self.screen.blit(text_img, (start_width, 10))

            self.search_buttons.append((b, alg_name))

            if self.controller.is_alg_ready(alg_name):
                results = self.controller.get_results(alg_name)
                n_moves = results['n_moves']
                exec_time = round(results['exec_time'], 2)
                memory_used = '%.2e' % Decimal(results['memory_used'])
                # info board
                pygame.draw.rect(
                    self.screen, (120, 120, 120),
                    pygame.Rect(start_width, 40, button_width, 90)
                )

                text_img = self.font11.render('n moves:', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 40))
                text_img = self.font11.render(str(n_moves), True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 54))

                text_img = self.font11.render('exec time:', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 70))
                text_img = self.font11.render(f'{exec_time} sec', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 84))

                text_img = self.font11.render('memory used:', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 100))
                text_img = self.font11.render(f'{memory_used} blocks', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 114))

                play_b = pygame.draw.rect(
                    self.screen, (0, 200, 0),
                    pygame.Rect(start_width, 140, button_width, button_height)
                )
                text_img = self.font14.render('PLAY', True, (255, 255, 255))
                self.screen.blit(text_img, (start_width, 140))

                self.play_buttons.append((play_b, alg_name))

