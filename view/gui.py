import pygame
import os
from controller.controller import Controller


class GUI:

    inputs_folder = 'inputs/'

    def __init__(self):
        self.screen_width, self.screen_height = 800, 600
        self.board_width = 550
        self.divider_width = 5
        self.level_selector_width = self.screen_width - self.board_width - self.divider_width

        self.level_id = 'board1'

    def run(self):
        pygame.init()

        self.font = pygame.font.SysFont('Arial', 16)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()

        self.controller = Controller()
        # temporary testing
        self.controller.load_game(self.level_id)

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
            board, goals = self.controller.get_current_board()
            self.draw_board(board, goals)

            pygame.display.flip()  # Refresh on-screen display
            self.clock.tick(60)

    def click_action(self):
        mouse_pos = pygame.mouse.get_pos()
        for b, l in self.buttons:
            if b.collidepoint(mouse_pos):
                self.controller.load_game(l)
                return

    def draw_board(self, board, goals, square_size=80, square_border=2, goal_size=16):
        margin = (self.board_width - (square_size * len(board[0]))) / 2

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell == -1:
                    color = (255, 255, 255)
                elif cell == 0:
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 0)

                height_pos = margin + (i * square_size) + square_border
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
            height_pos = margin + (goal_row * square_size) + ((square_size - goal_size) / 2)
            width_pos = margin + (goal_col * square_size) + ((square_size - goal_size) / 2)

            pygame.draw.rect(
                self.screen, (255, 50, 50),
                pygame.Rect(width_pos, height_pos,
                            goal_size, goal_size),
                            border_radius=2
            )

        # divider
        self.draw_divider()

        # selectors
        self.draw_level_selector()

    def draw_divider(self):
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            pygame.Rect(self.board_width, 0,
                        self.divider_width, self.screen_height)
        )

    def draw_level_selector(self, margin_size=2, rectangle_height=65):
        levels = [x.replace('.txt', '') for x in os.listdir(self.inputs_folder)]
        base_width = self.board_width + self.divider_width
        
        self.buttons = []
        for i, l in enumerate(levels):
            base_height = i*rectangle_height

            pygame.draw.rect(
                self.screen, (255, 255, 255),
                pygame.Rect(base_width, base_height,
                            self.level_selector_width, rectangle_height)
            )
            pygame.draw.rect(
                self.screen, (0, 0, 0),
                pygame.Rect(base_width + margin_size, base_height - margin_size,
                            self.level_selector_width - (2 * margin_size), rectangle_height - (2 * margin_size))
            )

            text_img = self.font.render(l, True, (255, 255, 255))
            b = self.screen.blit(text_img, (base_width + 2 * margin_size, base_height + 2 * margin_size))
            self.buttons.append((b, l))


       