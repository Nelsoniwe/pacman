import pygame

SCREEN_WIDTH = 544
SCREEN_HEIGHT = 608

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    gameOver = False
    def __init__(self,x,y,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        # Load image which will be for the animation
        img = pygame.image.load("walk.png").convert()
        # Create the animations objects
        self.move_right_animation = Animation(img,32,32)
        self.move_left_animation = Animation(pygame.transform.flip(img,True,False),32,32)
        self.move_up_animation = Animation(pygame.transform.rotate(img,90),32,32)
        self.move_down_animation = Animation(pygame.transform.rotate(img,270),32,32)
        # Load explosion image
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img,30,30)
        # Save the player image
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self,blocked_blocks):
        if not self.explosion:
            # This will stop the user when he touch the block
            for block in pygame.sprite.spritecollide(self,blocked_blocks,False):
                self.rect.x -= (block.rect.x - self.rect.x)*0.1
                self.rect.y -= (block.rect.y - self.rect.y)*0.1
                self.change_x = 0
                self.change_y = 0
            
            # This will stop the user when he tries to go outside 
            if self.rect.right < 32:
                self.rect.x -= (self.rect.x)*0.1
                self.change_x = 0
                self.change_y = 0
            elif self.rect.left > SCREEN_WIDTH-32:
                self.rect.x -= (SCREEN_WIDTH - self.rect.x)*0.1
                self.change_x = 0
                self.change_y = 0
            if self.rect.bottom < 32:
                self.rect.y -= (self.rect.y)*0.1
                self.change_x = 0
                self.change_y = 0
            elif self.rect.top > SCREEN_HEIGHT-32:
                self.rect.y -= (SCREEN_HEIGHT - self.rect.y)*0.1
                self.change_x = 0
                self.change_y = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            #animate pacman when he moves
            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.getCurrentImage()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.getCurrentImage()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.getCurrentImage()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.getCurrentImage()   
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                pygame.time.wait(500)
                self.gameOver = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.getCurrentImage()
            

    def moveRight(self):
        self.change_x = 3

    def moveLeft(self):
        self.change_x = -3

    def moveUp(self):
        self.change_y = -3

    def moveDown(self):
        self.change_y = 3

    def stopMoveRight(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stopMoveLeft(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image,True,False)
        self.change_x = 0

    def stopMoveUp(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,90)
        self.change_y = 0

    def stopMoveDown(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,270)
        self.change_y = 0



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