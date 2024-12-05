import pygame
import sys
from game import Game
from title_screen import TitleScreen


def main():
    pygame.init()
    WIN_WIDTH = 816
    WIN_HEIGHT = 816
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Pokémon Rafisa')

    title_screen = TitleScreen(screen)
    clock = pygame.time.Clock()
    game = Game(screen, WIN_WIDTH, WIN_HEIGHT)

    running = True
    on_title_screen = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game.in_dialogue:
                    game.in_dialogue = False  # Sort du dialogue une fois la touche pressée

                elif event.key == pygame.K_e:
                    game.update()  # Check les interactions

        if on_title_screen:
            title_screen.update()
            title_screen.draw()
            if title_screen.start_game:
                on_title_screen = False
        else:
            game.update()
            game.draw()

        pygame.display.flip()
        clock.tick(60) # vitesse du jeu (fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
