from numpy import fabs, true_divide
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

        self.arra = []
        self.field = []
        self.calculatePath = False
        self.weightField = []
        self.heuristicCalc = False
        self.euclideanCalc = False
        self.euclideanSquaredCalc = False

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
        #arra = algorithms.findPathDFS(algorithms.testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
        a = (self.player.rect.bottomright[1]-16)*2/32
        b = (self.player.rect.bottomright[0]-16)*2/32
        c = food[1]*2/32
        e = food[0]*2/32

        


        self.field = []
        if self.calculatePath == True:
            #    self.arra = algorithms.findPathBFS(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32)
            if self.heuristicCalc:
                self.arra, self.field  = algorithms.Astar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32,algorithms.heuristic)
                self.heuristicCalc = False
            elif self.euclideanCalc:
                self.arra, self.field  = algorithms.Astar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32,algorithms.euclidean)
                self.euclideanCalc = False
            elif self.euclideanSquaredCalc:
                self.arra, self.field  = algorithms.Astar(testGrid,(self.player.rect.bottomright[1]-16)/32,(self.player.rect.bottomright[0]-16)/32,food[1]/32,food[0]/32,algorithms.euclideanSquared)
                self.euclideanSquaredCalc = False
                self.field *= 10
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
        

        for item in self.arra:
            pygame.draw.rect(screen, BLUE, pygame.Rect(item[1]*32 + 9, item[0]*32 + 9, 16, 16))

        for i in range(len(self.weightField)):
            for j in range(len(self.weightField[0])):
                pygame.draw.rect(screen, (self.weightField[i][j],self.weightField[i][j],self.weightField[i][j]), pygame.Rect(j*32 + 12, i*32 + 12, 8, 8))


        

        #update screen
        pygame.display.flip()
