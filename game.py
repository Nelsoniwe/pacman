import pygame
from pygame.constants import RESIZABLE
from pygame.surfarray import array2d
from player import Player
from objects import *
import random
SCREENWIDTH = 608
SCREENHEIGHT = 544

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
        self.blocksGroup = pygame.sprite.Group()
        # Create a group for the food
        self.dotsGroup = pygame.sprite.Group()
        # Create a group for the ghosts
        self.enemies = pygame.sprite.Group()

        for i,row in enumerate(testGrid):
            for j,item in enumerate(row):
                if item == 0:
                    self.blocksGroup.add(Block(j*32+4,i*32+4,BLUE,24,24))

        #count of patch cells
        pathCellCount = 0
        for i, row in enumerate(testGrid):
            for j, item in enumerate(row):
                if item != 0:
                    pathCellCount=pathCellCount+1
        a = random.randrange(0,pathCellCount)

        # Add the food
        for i, row in enumerate(testGrid):
            for j, item in enumerate(row):
                if item != 0:
                    a-=1
                    if a == 0:
                        self.dotsGroup.add(Ellipse(j*32+12,i*32+12,YELLOW,8,8))
                if item == 2:
                    self.player = Player(j*32,i*32,"player.png")
                if item == 3:
                    self.enemies.add(Ghost(j*32,i*32))

        

    def inputHandler(self):
        if self.gameOver == True:
            return True
        # User did something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.moveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.moveLeft()
                elif event.key == pygame.K_UP:
                    self.player.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.moveDown()
                elif event.key == pygame.K_ESCAPE:
                    self.gameOver = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stopMoveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.stopMoveLeft()
                elif event.key == pygame.K_UP:
                    self.player.stopMoveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.stopMoveDown()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                    
        return False

    def logic(self):
        if not self.gameOver:
            self.player.update(self.blocksGroup)
            #detecting colide with ghost or food
            blockHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup,True)
            blockHitList = pygame.sprite.spritecollide(self.player,self.enemies,False)
            if len(blockHitList) > 0:
                self.player.explosion = True
            if len(self.dotsGroup)==0:
                self.player.explosion = True
            self.gameOver = self.player.gameOver


    def displayFrame(self,screen):
        #clear screen from previous frame
        screen.fill(BLACK)
        #draw walls
        testDrawEnviroment(screen)
        #draw food
        self.dotsGroup.draw(screen)
        #draw ghosts
        self.enemies.draw(screen)
        #draw player on field
        screen.blit(self.player.image,self.player.rect)
        

        for item in self.dotsGroup:
         food = (item.rect)
         break
        
        # if(self.lock):
            # arrb = algorithms.findPathBFS(algorithms.testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
        arra = algorithms.findPathDFS(algorithms.testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
        # self.lock = False
        for item in arra:
            pygame.draw.rect(screen, BLUE, pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 16, 16))
            # for item in arrb:
            #     pygame.draw.rect(screen, YELLOW, pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 16, 16))
        

        #update screen
        pygame.display.flip()
