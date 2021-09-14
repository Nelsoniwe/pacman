import pygame
from pygame.constants import RESIZABLE
from pygame.surfarray import array2d
from player import Player
from objects import *
import random
SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,0)

class Game(object):
    def __init__(self):
        self.lock = True
        self.font = pygame.font.Font(None,40)
        # Create the player
        self.player = Player(32,128,"player.png")
        # Create a group for the blocks
        self.blocks_group = pygame.sprite.Group()
        # Create a group for the food
        self.dots_group = pygame.sprite.Group()
        # Create a group for the ghosts
        self.enemies = pygame.sprite.Group()

        for i,row in enumerate(test_grid):
            for j,item in enumerate(row):
                if item == 0:
                    self.blocks_group.add(Block(j*32+4,i*32+4,BLUE,24,24))

        #count of patch cells
        pathcellcount = 0
        for i, row in enumerate(test_grid):
            for j, item in enumerate(row):
                if item != 0:
                    pathcellcount=pathcellcount+1
        a = random.randrange(0,pathcellcount)

        # Add the food
        for i, row in enumerate(test_grid):
            for j, item in enumerate(row):
                if item != 0:
                    a-=1
                    if a == 0:
                        self.dots_group.add(Ellipse(j*32+12,i*32+12,YELLOW,8,8))
                if item == 2:
                    self.player = Player(j*32,i*32,"player.png")
                if item == 3:
                    self.enemies.add(Ghost(j*32,i*32))

        

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

        # print(self.dots_group[0].rect)
        

        for item in self.dots_group:
         food = (item.rect)
         break


        
        if(self.lock):
            arrb = algorithms.findPathBFS(algorithms.test_grid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
            arra = algorithms.findPathDFS(algorithms.test_grid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
            for item in arra:
                pygame.draw.rect(screen, BLUE, pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 16, 16))
            for item in arrb:
                pygame.draw.rect(screen, YELLOW, pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 16, 16))
        # self.lock = False

        #update screen
        pygame.display.flip()
