import pygame
from pygame.constants import RESIZABLE
from player import Player
from objects import *
SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None,40)
        # Create the player
        self.player = Player(32,128,"player.png")
        # Create a group for the blocks
        self.blocks_group = pygame.sprite.Group()
        # Create a group for the food
        self.dots_group = pygame.sprite.Group()

        for i,row in enumerate(test_grid):
            for j,item in enumerate(row):
                if item == 0:
                    self.blocks_group.add(Block(j*32+4,i*32+4,BLUE,24,24))

        # Create the ghosts
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Ghost(224,256))
        self.enemies.add(Ghost(256,256))
        self.enemies.add(Ghost(288,256))
        self.enemies.add(Ghost(256,224))
        
        # Add the food
        for i, row in enumerate(test_grid):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,YELLOW,8,8))

    def input_handler(self):
        if self.game_over == True:
            return True
        # User did something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif event.key == pygame.K_UP:
                    self.player.move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                    
        return False

    def logic(self):
        if not self.game_over:
            self.player.update(self.blocks_group)
            #detecting colide with ghost or food
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,False)
            if len(block_hit_list) > 0:
                self.player.explosion = True
            if len(self.dots_group)==0:
                self.player.explosion = True
            self.game_over = self.player.game_over

    def display_frame(self,screen):
        #clear screen from previous frame
        screen.fill(BLACK)
        #draw blocks
        #self.blocks_group.draw(screen)
        #draw walls
        test_draw_enviroment(screen)
        #draw food
        self.dots_group.draw(screen)
        #draw ghosts
        self.enemies.draw(screen)
        #draw player on field
        screen.blit(self.player.image,self.player.rect)
        #update screen
        pygame.display.flip()