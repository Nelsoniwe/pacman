import pygame

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

testGrid =      ((1,1,1,1,5,),
                 (1,0,0,0,1,),
                 (1,1,3,1,1,),
                 (1,0,0,0,1,),
                 (1,1,2,1,1,))

class Player(pygame.sprite.Sprite):
    changeX = 0
    changeY = 0
    explosion = False
    gameOver = False
    def __init__(self,x,y,filename,gameControled = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        # Load image which will be for the animation
        img = pygame.image.load("walk.png").convert()
        # Create the animations objects
        #self.moveRightAnimation = Animation(img,32,32)
        #self.moveLeftAnimation = Animation(pygame.transform.flip(img,True,False),32,32)
        #self.moveUpAnimation = Animation(pygame.transform.rotate(img,90),32,32)
        #self.moveDownAnimation = Animation(pygame.transform.rotate(img,270),32,32)
        # Load explosion image
        img = pygame.image.load("explosion.png").convert()
        self.explosionAnimation = Animation(img,30,30)
        # Save the player image
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)
        self.gameControled = gameControled
        self.isGoingByGame = False

        self.nextX = -5
        self.nextY = -5



    def update(self,blockedBlocks):
        if not self.explosion:
            # This will stop the user when he touch the block
            for block in pygame.sprite.spritecollide(self,blockedBlocks,False):
                self.rect.x -= (block.rect.x - self.rect.x)*0.1
                self.rect.y -= (block.rect.y - self.rect.y)*0.1
                #self.changeX = 0
                #self.changeY = 0


            if (((self.rect.x) / 32) == self.nextX or self.nextY == ((self.rect.y) / 32)):
                self.nextX = -5
                self.nextY = -5
                self.changeX = 0
                self.changeY = 0
                self.isGoingByGame = False

            # This will stop the user when he tries to go outside 
            if self.rect.right < 30:
               self.rect.x -= (self.rect.x)*0.1
               self.changeX = 0
               self.changeY = 0
            elif self.rect.left > SCREEN_WIDTH-30:
               self.rect.x -= (SCREEN_WIDTH - self.rect.x)*0.1
               self.changeX = 0
               self.changeY = 0
            if self.rect.bottom < 30:
               self.rect.y -= (self.rect.y)*0.1
               self.changeX = 0
               self.changeY = 0
            elif self.rect.top > SCREEN_HEIGHT-30:
               self.rect.y -= (SCREEN_HEIGHT - self.rect.y)*0.1
               self.changeX = 0
               self.changeY = 0
            self.rect.x += self.changeX
            self.rect.y += self.changeY

            #animate pacman when he moves
            #if self.changeX > 0:
            #    self.moveRightAnimation.update(10)
            #    self.image = self.moveRightAnimation.getCurrentImage()
            #elif self.changeX < 0:
            #    self.moveLeftAnimation.update(10)
            #    self.image = self.moveLeftAnimation.getCurrentImage()
#
            #if self.changeY > 0:
            #    self.moveDownAnimation.update(10)
            #    self.image = self.moveDownAnimation.getCurrentImage()
            #elif self.changeY < 0:
            #    self.moveUpAnimation.update(10)
            #    self.image = self.moveUpAnimation.getCurrentImage()
        else:
           # if self.explosionAnimation.index == self.explosionAnimation.get_length() -1:
           #     pygame.time.wait(500)
            self.gameOver = True
            #self.explosionAnimation.update(12)
            #self.image = self.explosionAnimation.getCurrentImage()


    def goTo(self,point):
        x = ((self.rect.x)/32)
        y = ((self.rect.y)/32)

        if (point.Y) == x and (point.X) == y:
            self.changeX = 0
            self.changeY = 0
            self.isGoingByGame = False
        if abs((x) - point.Y) == 0:
            self.changeX = 0
            if y - point.X < 0:
                self.moveDown()
            if y - point.X > 0:
                self.moveUp()
        if (y) - point.X == 0:
            self.changeY = 0
            if x - point.Y < 0:
                self.moveRight()
            if x - point.Y > 0:
                self.moveLeft()

    def GetPosibilityToMoveCords(self,field, y, x):
        x = round(x)
        y = round(y)
        envHight = len(field)
        envWidth = len(field[0])

        if x >= 0 and y < envWidth and y >= 0 and x < envHight and field[x][y] > 0:
            return True
        return False

    def GetCordsInMaze(self):
        return ((self.rect.x)/32),((self.rect.y)/32)

    def moveRight(self):
        if(self.GetPosibilityToMoveCords(testGrid, (((self.rect.x) / 32) + 1), (((self.rect.y) / 32)))):
            self.changeX = 2
            return True
        else:
            return False

    def moveLeft(self):
        if (self.GetPosibilityToMoveCords(testGrid, (((self.rect.x) / 32) - 1), (((self.rect.y) / 32)))):
            self.changeX = -2
            return True
        else:
            return False

    def moveUp(self):
        if (self.GetPosibilityToMoveCords(testGrid, (((self.rect.x) / 32)), (((self.rect.y) / 32)-1))):
            self.changeY = -2
            return True
        else:
            return False

    def moveDown(self):
        if (self.GetPosibilityToMoveCords(testGrid, (((self.rect.x) / 32)), (((self.rect.y) / 32) + 1))):
            self.changeY = 2
            return True
        else:
            return False

    def stopMoveRight(self):
        if self.changeX != 0:
            self.image = self.playerImage
        self.changeX = 0

    def stopMoveLeft(self):
        if self.changeX != 0:
            self.image = pygame.transform.flip(self.playerImage,True,False)
        self.changeX = 0

    def stopMoveUp(self):
        if self.changeY != 0:
            self.image = pygame.transform.rotate(self.playerImage,90)
        self.changeY = 0

    def stopMoveDown(self):
        if self.changeY != 0:
            self.image = pygame.transform.rotate(self.playerImage,270)
        self.changeY = 0

    # 0:Up, 1:Down,2:right,3:down
    def MoveToPosition(self,Action):
        if (self.isGoingByGame == False):
            if (Action == 0):
                self.nextY = ((self.rect.y)/32)-1
                self.isGoingByGame = self.moveUp()
            if (Action == 1):
                self.nextY = ((self.rect.y)/32)+1
                self.isGoingByGame = self.moveDown()
            if (Action == 2):
                self.nextX = ((self.rect.x)/32)+1
                self.isGoingByGame = self.moveRight()
            if (Action == 3):
                self.nextX = ((self.rect.x)/32)-1
                self.isGoingByGame = self.moveLeft()

class Animation(object):
    def __init__(self,img,width,height):
        # Load the sprite sheet
        self.spriteSheet = img
        # Create a list to store the images
        self.imageList = []
        self.loadImages(width,height)
        # Create a variable which will hold the current image of the list
        self.index = 0
        # Create a variable that will hold the time
        self.clock = 1
        
    def loadImages(self,width,height):
        # Go through every single image in the sprite sheet
        for y in range(0,self.spriteSheet.get_height(),height):
            for x in range(0,self.spriteSheet.get_width(),width): 
                # load images into a list
                img = self.getImage(x,y,width,height)
                self.imageList.append(img)

    def getImage(self,x,y,width,height):
        # Create a new blank image
        image = pygame.Surface([width,height]).convert()
        # Copy the sprite from the large sheet onto the smaller
        image.blit(self.spriteSheet,(0,0),(x,y,width,height))
        # Assuming black works as the transparent color
        image.set_colorkey((0,0,0))
        # Return the image
        return image

    def getCurrentImage(self):
        return self.imageList[self.index]

    def get_length(self):
        return len(self.imageList)

    def update(self,fps=30):
        step = 30 // fps
        l = range(1,30,step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Increase index
            self.index += 1
            if self.index == len(self.imageList):
                self.index = 0