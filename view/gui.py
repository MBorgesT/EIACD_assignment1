import pygame
from controller.controller import Controller


def run():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    clock = pygame.time.Clock()

    controller = Controller()

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        # Do logical updates here.
        # ...

        screen.fill('black')  # Fill the display with a solid color

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)    