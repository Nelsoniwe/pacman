from typing import NamedTuple
from numpy import array, fabs, true_divide
import numpy
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
RED = (255,0,0)


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

        self.arra = []
        self.field = []
        self.calculatePath = False
        self.weightField = []
        self.heuristicCalc = False
        self.euclideanCalc = False
        self.euclideanSquaredCalc = False
        self.path = []
        self.mousePoint = None

        for i,row in enumerate(testGrid):
            for j,item in enumerate(row):
                if item == 0:
                    self.blocksGroup.add(Block(j*32+4,i*32+4,BLUE,24,24))

        #count of patch cells
        self.pathCellCount = 0
        for i, row in enumerate(testGrid):
            for j, item in enumerate(row):
                if item != 0:
                    self.pathCellCount=self.pathCellCount+1

        

        # Add objects to the field
        for i, row in enumerate(testGrid):
            for j, item in enumerate(row):
                if item == 2:
                    self.player = Player(j*32,i*32,"player.png")
                if item == 3:
                    self.enemies.add(Ghost(j*32,i*32,0))
                if item == 4:
                    self.enemies.add(Ghost(j*32,i*32,1))
        
        self.randEnemies = []
        self.dirEnemies = []

        for e in self.enemies:
            if e.type == 0:
                self.randEnemies.append(e)
            else:
                self.dirEnemies.append(e)

        
        #FOOD
        foodCount = self.pathCellCount
        foodCords = []
        food = 0
        g = 0

        while g < foodCount:
            a = random.randrange(0,self.pathCellCount)
            if not foodCords.__contains__(a):
                foodCords.append(a)
                g+=1
        #add food to the field
        for i, row in enumerate(testGrid):
            for j, item in enumerate(row):
                if item != 0:
                    food+=1
                    if foodCords.__contains__(food):
                        self.dotsGroup.add(Ellipse(j*32+12,i*32+12,RED,8,8))

        

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
                elif event.key == pygame.K_p:
                    self.calculatePath = True
                elif event.key == pygame.K_o:
                    self.heuristicCalc = True
                elif event.key == pygame.K_i:
                    self.euclideanCalc = True
                elif event.key == pygame.K_u:
                    self.euclideanSquaredCalc = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stopMoveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.stopMoveLeft()
                elif event.key == pygame.K_UP:
                    self.player.stopMoveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.stopMoveDown()
                elif event.key == pygame.K_o:
                    self.Astar = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # self.player.explosion = True
                self.mousePoint =  pygame.mouse.get_pos()
                    
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
            
            ind = random.randint(0,self.pathCellCount)
            

            # self.enemies.update(rp)

            for ghost in self.randEnemies:
                rp = ghost.oldPoint
                if len(ghost.path) == 0:
                   for i, row in enumerate(testGrid):
                    for j, item in enumerate(row):
                        if ind != 0:
                            ind = ind - 1
                            rp = (j,i)
                ghost.update(rp)


            for ghost in self.dirEnemies:
                
                rp = ((self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32)

                ghost.update(rp)
                
                

                


    def displayFrame(self,screen):
        #clear screen from previous frame
        screen.fill(BLACK)
        #draw walls
        testDrawEnviroment(screen)
        
        #draw ghosts
        self.enemies.draw(screen)
        #draw player on field
        screen.blit(self.player.image,self.player.rect)
        

        for item in self.dotsGroup:
         food = (item.rect)
         break
        endPos = [None,None]
        if(self.mousePoint!=None and testGrid !=None):
            if (testGrid[int(self.mousePoint[1]/32)][int(self.mousePoint[0]/32)]==1):  
                endPos = (int(self.mousePoint[1]/32),int(self.mousePoint[0]/32))

        self.field = []

        if self.calculatePath == True:
            self.path = []
            if self.heuristicCalc:
                self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.heuristic)
            elif self.euclideanCalc:
                self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.euclidean)
            elif self.euclideanSquaredCalc:
                self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.euclideanSquared)
                self.field *= 10
            self.heuristicCalc = False
            self.euclideanCalc = False
            self.euclideanSquaredCalc = False

            self.calculatePath = False

            self.weightField = []
            for i in range(len(self.field)):
              if i % 2 == 0:
                  self.weightField.append([])
                  for j in range(len(self.field[0]) ):
                      if j % 2 == 0:
                          self.weightField[-1].append(self.field[i][j])

            for i in range(len(self.weightField)):
                for j in range(len(self.weightField[0])):
                    if self.weightField[i][j] > 250:
                      self.weightField[i][j] = 250
        
        for i in self.arra:
            for item in i:
             a =  i.index(item)*10
             if a > 255:
               a = 255 
             pygame.draw.rect(screen,(100,a,100) , pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 12,12))
                 
        for i in range(len(self.weightField)):
            for j in range(len(self.weightField[0])):
                x = self.weightField[i][j] *10
                if x > 255:
                  x = 255 
                pygame.draw.rect(screen, (x,x,x), pygame.Rect(j*32 + 12, i*32 + 12, 8, 8))


        #draw food
        self.dotsGroup.draw(screen)
        #update screen
        pygame.display.flip()
