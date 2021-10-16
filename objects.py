import random
import pygame
import algorithms
import labirinthalg
import enum

SCREENWIDTH = 544
SCREENHEIGHT = 608

# Define some colors
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)


# testGrid = labirinthalg.generateMaze(19,17)
# testGrid[10][10] = 2

testGrid =      ((4,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,),
                 (1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,),
                 (1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,),
                 (0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,),
                 (0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,),
                 (1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,),
                 (0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,),
                 (1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,),
                 (1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,),
                 (0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,),
                 (1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,),
                 (1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,),
                 (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,))

#environment hight and width
envHight = len(testGrid)
envWidth = len(testGrid[0])

#Block that keep player in playfield
class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

#Food
class Ellipse(pygame.sprite.Sprite):
    def __init__(self,x,y,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width,height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


class TypeOfGhost(enum.Enum):
    randomType = 0
    directType = 1


#Enemies   
class Ghost(pygame.sprite.Sprite):
    def __init__(self,x,y,t):
        pygame.sprite.Sprite.__init__(self)
        #image of ghost
        self.image = pygame.image.load("Ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.path = []
        self.speed = 2
        self.oldPoint = (0,0)
        self.newPoint = (0,0)
        self.type = t #0 - random, 1 - direct

    
    changeX = 0
    changeY = 0

    def update(self,point):
        
        self.newPoint = point

        if len(self.path) == 0 or self.newPoint != self.oldPoint:
            self.path = algorithms.findPathBFS(testGrid,(self.rect.y+16)/32,(self.rect.x+16)/32,point[0],point[1])
            self.oldPoint = self.newPoint
            self.path.reverse()
        self.goTo(self.path)

        self.rect.x += self.changeX
        self.rect.y += self.changeY
                

    def goTo(self,path):
        if len(path) >= 1:
            next = path[0]
            x = ((self.rect.x)/32)
            y = ((self.rect.y)/32)

            if next[1] == x and next[0] == y:
                path.remove(next)
                self.changeX = 0
                self.changeY = 0
                
            else:
                if abs(x - next[1]) == 0:
                    self.changeX = 0
                    if y - next[0] < 0:
                        self.changeY = self.speed
                    if y - next[0] > 0:
                        self.changeY = -self.speed
                if y - next[0] == 0:
                    self.changeY = 0
                    if x - next[1] < 0:
                        self.changeX = self.speed
                    if x - next[1] > 0:
                        self.changeX = -self.speed
                    
        
            

    
#Draw walls
def testDrawEnviroment(screen):
    for i,row in enumerate(testGrid):
        for j,item in enumerate(row):
            if item == 1 or item == 2 or item == 3:
                if(j+1< envWidth and testGrid[i][j+1]==0):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                elif(j+1== envWidth):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                if(testGrid[i][j-1]==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                elif(j==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                if(i+1< envHight and testGrid[i+1][j]==0):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                elif(i+1 == envHight):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                if( testGrid[i-1][j]==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                elif(i==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
