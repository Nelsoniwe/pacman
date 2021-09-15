import pygame
from game import Game

SCREEN_WIDTH = 544
SCREEN_HEIGHT = 608

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN")
    #done game variable
    done = False
    #fps variable
    clock = pygame.time.Clock()
    # Create a game object
    game = Game()
    game.__init__()
    game.gameOver = False
    #game 
    while not done:
        #input handler
        done = game.inputHandler()
        game.logic()
        #draw frame
        game.displayFrame(screen)
        #30 frames per second
        clock.tick(30)
    pygame.quit()

if __name__ == '__main__':
    main()
