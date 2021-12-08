from datetime import datetime
from typing import NamedTuple
from numpy import array, fabs, true_divide
import numpy
import pygame
from pygame.constants import RESIZABLE
from pygame.surfarray import array2d

from algorithms import euclideanSquared, euclidean
from player import Player
from objects import *
import random
import pandas
import maxalgs
import csv

SCREENWIDTH = 160
SCREENHEIGHT = 160

WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,0)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.timestart = datetime.now()
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
        #score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        self.isWin = False

        self.ChoosenMaxAlg = maxalgs.expectimax

        self.arra = []
        self.field = []
        self.calculatePath = False
        self.weightField = []
        self.heuristicCalc = False
        self.euclideanCalc = False
        self.euclideanSquaredCalc = False
        self.path = []
        self.mousePoint = None
        self.testGrid = testGrid
        
        self.timerToTakePoint = 30
        
        for i,row in enumerate(testGrid):
            for j,item in enumerate(row):
                if item == 0:
                    self.blocksGroup.add(Block(j*32+4,i*32+4,BLUE,20,20))

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
                    self.player = Player(j*32,i*32,"player.png",False)
                if item == 3:
                    self.enemies.add(Ghost(j*32,i*32,0))
                if item == 4:
                    self.enemies.add(Ghost(j*32,i*32,1))
                if item == 5:
                    self.dotsGroup.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))
        
        self.randEnemies = []
        self.dirEnemies = []

        for e in self.enemies:
            if e.type == 0:
                self.randEnemies.append(e)
            else:
                self.dirEnemies.append(e)
        
        #FOOD
        foodCount = 0
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
                        self.dotsGroup.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))
        
        #self.PointToGoPlayer = self.ChoosenMaxAlg(testGrid,self.player,self.enemies,self.dotsGroup)

    def PlayNextMove(self, action):
        self.player.MoveToPosition(action)
        PlayerXPos,PlayerYPos =  self.player.GetCordsInMaze()
        nearestEnemy = maxalgs.FindNearestPoint([PlayerXPos, PlayerYPos], self.enemies)
        nearestFood = maxalgs.FindNearestPoint([PlayerXPos,PlayerYPos], self.dotsGroup)
        #[PlayerXPos, PlayerYPos, GhostXpoz, GhostYpoz, mazeMatrix, FoodCordsList]
        return [self.ScoreCAlculate(nearestEnemy,nearestFood), PlayerXPos, PlayerYPos, nearestEnemy, nearestFood]

    def ScoreCAlculate(self,nearestEnemy,nearestFood):
        PlayerXPos, PlayerYPos = self.player.GetCordsInMaze()
        playerFoodDistance = euclideanSquared([PlayerXPos, PlayerYPos],nearestFood)
        playerEnemyDistance = euclideanSquared([PlayerXPos, PlayerYPos],nearestEnemy)
        #return  (10/(playerFoodDistance+1)) * playerEnemyDistance/10 - 10
        a = self.score
        self.score = 0
        return a


    def inputHandler(self):
        if self.gameOver == True:
            return True
        # User did something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
                
            if event.type == pygame.KEYDOWN:
                if self.player.gameControled == False:
                    if event.key == pygame.K_RIGHT:
                        #self.player.moveRight()
                        self.player.MoveToPosition(2)
                    elif event.key == pygame.K_LEFT:
                        #self.player.moveLeft()
                        self.player.MoveToPosition(3)
                    elif event.key == pygame.K_UP:
                        #self.player.moveUp()
                        self.player.MoveToPosition(0)
                    elif event.key == pygame.K_DOWN:
                        #self.player.moveDown()
                        self.player.MoveToPosition(1)
                if event.key == pygame.K_ESCAPE:
                    self.score -= 100
                    self.gameOver = True

            #elif event.type == pygame.KEYUP:
            #    if event.key == pygame.K_RIGHT:
            #        self.player.stopMoveRight()
            #    elif event.key == pygame.K_LEFT:
            #        self.player.stopMoveLeft()
            #    elif event.key == pygame.K_UP:
            #        self.player.stopMoveUp()
            #    elif event.key == pygame.K_DOWN:
            #        self.player.stopMoveDown()
            #    elif event.key == pygame.K_o:
            #        self.ChoosenMaxAlg = maxalgs.expectimax
            

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # self.player.explosion = True
                self.mousePoint =  pygame.mouse.get_pos()
                    
        return False

    def logic(self):
        if not self.gameOver:
            self.player.update(self.blocksGroup)
            #detecting colide with ghost or food
            dotsHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup,True)
            blockHitList = pygame.sprite.spritecollide(self.player,self.enemies,False)
            if len(blockHitList) > 0:
                self.player.explosion = True
            if len(self.dotsGroup)==0:
                self.player.explosion = True
                self.isWin = True
            if len(dotsHitList)>0:
                self.score += 50
            self.gameOver = self.player.gameOver
            
            ind = random.randint(0,self.pathCellCount)

            self.timerToTakePoint-=1
            if self.timerToTakePoint<=0:
              self.timerToTakePoint = 30
              self.score -=30

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

            if self.player.gameControled:
                if self.player.isGoingByGame == False:
                  self.PointToGoPlayer = self.ChoosenMaxAlg(testGrid,self.player,self.enemies,self.dotsGroup)
                  self.player.isGoingByGame = True
                self.player.goTo(self.PointToGoPlayer)
        else:
            data = [self.ChoosenMaxAlg.__name__, self.isWin, datetime.now() - self.timestart, self.score]
            print(data)
            with open('stats.csv', 'a', encoding='UTF8') as file:
                writer = csv.writer(file)
                writer.writerow(data)

    def displayFrame(self,screen):
        #clear screen from previous frame
        screen.fill(BLACK)
        #draw walls
        testDrawEnviroment(screen)
        
        #draw ghosts
        self.enemies.draw(screen)
        #draw player on field
        screen.blit(self.player.image,self.player.rect)
        

        # for item in self.dotsGroup:
        #  food = (item.rect)
        #  break
        # endPos = [None,None]
        # if(self.mousePoint!=None and testGrid !=None):
        #     if (testGrid[int(self.mousePoint[1]/32)][int(self.mousePoint[0]/32)]==1):  
        #         endPos = (int(self.mousePoint[1]/32),int(self.mousePoint[0]/32))

        

        # self.field = []
        text = self.font.render("Score: " + str(self.score),True,(0,255,0))
        screen.blit(text,[30,240])

        # if self.calculatePath == True:
        #     self.path = []
            # if self.heuristicCalc:
            #     self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.heuristic)
            # elif self.euclideanCalc:
            #     self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.euclidean)
            # elif self.euclideanSquaredCalc:
            #     self.arra, self.field  = algorithms.multyAStar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,endPos[0],endPos[1],self.dotsGroup,algorithms.euclideanSquared)
            #     self.field *= 10
            # self.heuristicCalc = False
            # self.euclideanCalc = False
            # self.euclideanSquaredCalc = False

            # self.calculatePath = False

            # self.weightField = []
            # for i in range(len(self.field)):
            #   if i % 2 == 0:
            #       self.weightField.append([])
            #       for j in range(len(self.field[0]) ):
            #           if j % 2 == 0:
            #               self.weightField[-1].append(self.field[i][j])

            # for i in range(len(self.weightField)):
            #     for j in range(len(self.weightField[0])):
            #         if self.weightField[i][j] > 250:
            #           self.weightField[i][j] = 250
        
        # for i in self.arra:
        #     for item in i:
        #      a =  i.index(item)*10
        #      if a > 255:
        #        a = 255 
        #      pygame.draw.rect(screen,(100,a,100) , pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 12,12))
                 
        # for i in range(len(self.weightField)):
        #     for j in range(len(self.weightField[0])):
        #         x = self.weightField[i][j] *10
        #         if x > 255:
        #           x = 255 
        #         pygame.draw.rect(screen, (x,x,x), pygame.Rect(j*32 + 12, i*32 + 12, 8, 8))


        #draw food
        self.dotsGroup.draw(screen)
        #update screen
        pygame.display.flip()
