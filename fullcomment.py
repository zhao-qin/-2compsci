import os
import sys
import pygame
import random
from pygame import *# importing libraries and pygame

pygame.init()#initialize pygame

scr_size = (width,height) = (720,240)# setting the size of the screen
FPS = 60#setting frames per second of the game as a vriable to be used later
gravity = 0.6#setting the physics that will affect jump height as a variable to be used later

black = (0,0,0)# setting values for various colours
white = (255,255,255)
background_col = (235,235,235)

high_score = 0#userhighscore is initially 0

screen = pygame.display.set_mode(scr_size)#creates a window based on the size set above
clock = pygame.time.Clock()#how fast the page refreshes
pygame.display.set_caption("Supreme Rush")#title of the window

jump_sound = pygame.mixer.Sound('/home/robuntu/Downloads/jump.wav')#naming each sound
die_sound = pygame.mixer.Sound('/home/robuntu/Downloads/die.wav')
checkPoint_sound = pygame.mixer.Sound('/home/robuntu/Downloads/checkPoint.wav')

def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):#a function that loads images

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))#resize the image to a new resolution

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ): #loading sprites
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey is -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect

def disp_gameOver_msg(retbutton_image,gameover_image):#a function that displays a message upon the player's death
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height*0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)

def extractDigits(number):#creating a digit based on operations on a number
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

class Dinosaur():#defining a class that will be the in game dinosaur
    def __init__(self,sizex=-1,sizey=-1): #setting some parameters for the dinosaur
        self.images,self.rect = load_sprite_sheet('/home/robuntu/Downloads/dino.png',5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet('/home/robuntu/Downloads/dino_ducking.png',2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):#draws one image on top of another
        screen.blit(self.image,self.rect)

    def checkbounds(self):#setting boundaries for the dino
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):#how the various actions that the dinosaur perform work
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

class Cactus(pygame.sprite.Sprite): # defining a class that will be the in game cacti
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('/home/robuntu/Downloads/cacti-small.png',3,1,sizex,sizey,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]

    def draw(self):#draws one image onto another
        screen.blit(self.image,self.rect)

    def update(self):#checking if the cactus has collided with the player
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()

class Pteradactyl(pygame.sprite.Sprite):#defining a class that will be the pteradactyl in game
    def __init__(self,speed=5,sizex=-1,sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = load_sprite_sheet('/home/robuntu/Downloads/ptera.png',2,1,sizex,sizey,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):#draws one image on top of the other
        screen.blit(self.image,self.rect)

    def update(self):#checking if the pteradactyl has collided
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class Ground():#defining a class that will be the ground in game
    def __init__(self,speed=-5):
        self.image,self.rect = load_image('/home/robuntu/Downloads/ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('/home/robuntu/Downloads/ground.png',-1,-1,-1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):#draws one image on top of another
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):#function that updates the movement of the sprite
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right

class Cloud(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image,self.rect = load_image('/home/robuntu/Downloads/cloud.png',int(90*30/42),30,-1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed,0]

    def draw(self):#draws one image on top of another
        screen.blit(self.image,self.rect)

    def update(self):#updating the movement of the dino and checking if the sprite needs to be killed
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()
            
class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.tempimages,self.temprect = load_sprite_sheet('/home/robuntu/Downloads/numbers.png',12,1,11,int(11*6/5),-1) #finding sprites for numbers and the score
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1: #size of the scoreboard
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score): #function used to update score
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s],self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0


def introscreen(): #introscreen function which starts the game
    temp_dino = Dino(44,47)
    temp_dino.isBlinking = True
    gameStart = False

    temp_ground,temp_ground_rect = load_sprite_sheet('/home/robuntu/Downloads/ground.png',15,1,-1,-1,-1) #sprites for the groung
    temp_ground_rect.left = width/20
    temp_ground_rect.bottom = height

    logo,logo_rect = load_image('/home/robuntu/Downloads/logo.png',240,40,-1) #sprites for the logo on the title screen
    logo_rect.centerx = width*0.6
    logo_rect.centery = height*0.6
    while not gameStart: #if theres no display surface, then it will print: Couldn't load display surface
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else: #how the dinosaur moves on the screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN: #using keydown for ducking
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None: #display of dinosaur
            screen.fill(background_col)
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)
            temp_dino.draw()

            pygame.display.update()#the display

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

def gameplay(): #main gameplay function
    global high_score #highscore on screen
    gamespeed = 4 #speed of the game
    startMenu = False #starting menu
    gameOver = False#gameover
    gameQuit = False# quitting the game
    playerDino = Dino(44,47) #defining player
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0
    #defining sprites below
    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image,retbutton_rect = load_image('/home/robuntu/Downloads/replay_button.png',35,31,-1)#sprite for replay button
    gameover_image,gameover_rect = load_image('/home/robuntu/Downloads/game_over.png',190,11,-1)#sprite for gameover button

    temp_images,temp_rect = load_sprite_sheet('/home/robuntu/Downloads/numbers.png',12,1,11,int(11*6/5),-1)#sprite for numbers
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73

    while not gameQuit: #display of the game on screen
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN: #telling computer what to do when player jumps
                        if event.key == pygame.K_SPACE:
                            if playerDino.rect.bottom == int(0.98*height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1*playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN: #when player ducks
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False
            for c in cacti: #defining cacti and player death
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for p in pteras: #defining pteras and player death
                p.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,p):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            if len(cacti) < 2: #inputing values for the size of cacti and the spawn rate
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))
            #spawn rate and size of pteras
            if len(pteras) == 0 and random.randrange(0,200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))

            if len(clouds) < 5 and random.randrange(0,300) == 10: #size of clouds
                Cloud(width,random.randrange(height/5,height/2))
            #update screen
            playerDino.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(high_score)

            if pygame.display.get_surface() != None: #display
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0: #highscore
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                playerDino.draw()

                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead: #dinosaur death and highscore saving
                gameOver = True
                if playerDino.score > high_score:
                    high_score = playerDino.score

            if counter%700 == 699: #speed of ground scrolling
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit: #quitting the gane
            break

        while gameOver: #when the game is over
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN: #defining what keys to use
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: #using the key space
                            gameOver = False
                            gameplay()
            highsc.update(high_score) #updating highscore
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image,gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                pygame.display.update() #display update
            clock.tick(FPS)

    pygame.quit() #calling functions
    quit()

def main(): #main gameplay function to open intro screen
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()#calling main function