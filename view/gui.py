import pygame
from controller.controller import Controller


class GUI:

    def __init__(self):
        pass

    def run(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))

        self.clock = pygame.time.Clock()

        self.controller = Controller()
        # temporary testing
        self.controller.load_game('board1')
        board, goals = self.controller.get_current_board()

        while True:
            # Process player inputs.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            # Do logical updates here.
            # ...

            self.screen.fill('black')  # Fill the display with a solid color

            # Render the graphics here.
            # ...
            self.draw_board(board, goals)

            pygame.display.flip()  # Refresh on-screen display
            self.clock.tick(60)

    def draw_board(self, board, goals, margin=100, square_size=60, square_border=2, goal_size=16):
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

        # goals
        for goal_row, goal_col in goals:
            height_pos = margin + (goal_row * square_size) + ((square_size - goal_size) / 2)
            width_pos = margin + (goal_col * square_size) + ((square_size - goal_size) / 2)

            pygame.draw.rect(
                self.screen, (255, 0, 0),
                pygame.Rect(width_pos, height_pos,
                            goal_size, goal_size),
                            border_radius=2
            )
       