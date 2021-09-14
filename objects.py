import pygame
import algorithms

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 544

# Define some colors
BLACK = (0,0,0)
BLUE = (0,0,255)

#game field
test_grid =     ((1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,),
                 (1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,),
                 (1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,),
                 (1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,),
                 (0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,),
                 (0,0,0,1,0,1,1,1,1,1,1,1,0,1,0,0,0,),
                 (0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,),
                 (1,1,1,1,1,1,0,3,3,3,0,1,1,1,1,1,1,),
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
envhight = len(test_grid)
envwidth = len(test_grid[0])

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

#Enemies   
class Ghost(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #image of ghost
        self.image = pygame.image.load("Ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
#Draw walls
def test_draw_enviroment(screen):
    for i,row in enumerate(test_grid):
        for j,item in enumerate(row):
            if item == 1 or item == 2 or item == 3:
                if(j+1< envwidth and test_grid[i][j+1]==0):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                elif(j+1== envwidth):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32+32,i*32], 3)
                if(test_grid[i][j-1]==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                elif(j==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                if(i+1< envhight and test_grid[i+1][j]==0):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                elif(i+1 == envhight):
                    pygame.draw.line(screen, BLUE , [j*32+32, i*32+32], [j*32,i*32+32], 3)
                if( test_grid[i-1][j]==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                elif(i==0):
                    pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
