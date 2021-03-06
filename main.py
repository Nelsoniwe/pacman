import pygame
from game import Game

SCREENWIDTH = 160
SCREENHEIGHT = 160

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
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
        clock.tick(1000)
    pygame.quit()

if __name__ == '__main__':
    main()
