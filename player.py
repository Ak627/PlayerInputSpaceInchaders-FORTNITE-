import pygame
import time

pygame.init()
pygame.display.set_caption("Inchaders")
ScreenWidth = 800
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
clock = pygame.time.Clock()
green = (0, 255,0)

timer = 0

frameWidth = 50
frameHeight = 38
RowNum = 0
frameNum = 0

doExit = False
Px = 0
Py = ScreenHeight - 50
Vx = 0
#constants
LEFT = 0
RIGHT = 1
SPACE = 2
keys = [False, False, False]

shoot = False

class Wall:
    def __init__ (self, xpos, ypos):#constructor
        self.xpos = xpos
        self.ypos = ypos
        self.numHits = 0
    def collide(self, BulletX, BulletY):
        if self.numHits < 3:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 30:
                    if BulletY < self.ypos + 30:
                        if BulletY > self.ypos:
                            print("hit!")
                            self.numHits += 1
                            return False
        return True
    
    def draw(self):
        if self.numHits == 0:
            pygame.draw.rect(screen, (37, 194, 79),(self.xpos, self.ypos, 30, 30))
        if self.numHits == 1:
            pygame.draw.rect(screen, (77, 184, 69), (self.xpos, self.ypos, 30,30))
        if self.numHits == 2:
            pygame.draw.rect(screen, (107, 174, 49), (self.xpos, self.ypos, 30,30))


walls = []
for k in range(4):
    for i in range(2):
        for j in range(3):
            walls.append(Wall(j*30+200*k+50, i*30+600))


alien = pygame.image.load('Enemy.png') #load your spritesheet
alien.set_colorkey((255,0,255))

AframeWidth = 50
AframeHeight = 20
ARowNum = 0
AframeNum = 0

class Alien:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = True
        self.direction = 1
    def move(self, time):
        if time % 500 == 0:
            self.ypos +=100
            self.direction *=-1
            return 0
        
        if time%150==0:
            self.xpos+=50*self.direction
            
        return time
    def collide(self, BulletX, BulletY):
        if self.isAlive:
            if BulletX > self.xpos:
                if BulletX < self.xpos + 50:
                    if BulletY < self.ypos + 20:
                        if BulletY > self.ypos:
                            print("hit!")
                            self.isAlive = False
                            return False
        return True
    
    def draw(self):
        if self.isAlive == True:
            screen.blit(alien, (self.xpos, self.ypos), (AframeWidth*AframeNum, ARowNum*AframeHeight, AframeWidth, AframeHeight))

armada = []
for i in range(4):
    for j in range(9):
        armada.append(Alien(j*60+50, i*50+50))
        

class Bullet:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = False
    def move(self, xpos, ypos):
        if self.isAlive == True:
            self.ypos -=5
        if self.ypos < 0:
            self.isAlive = False
            self.xpos = xpos
            self.ypos = ypos
    
    
    def draw(self):
            pygame.draw.rect(screen, (250, 250, 250), (self.xpos, self.ypos, 3, 20))

bullet = Bullet(Px+25, Py)

player = pygame.image.load('Player.png') #load your spritesheet
player.set_colorkey((255,255,255))

death = pygame.image.load("Death.png")
death.set_colorkey((255,0,255))


while not doExit:
    font = pygame.font.SysFont('calibri.ttf', 38)
    PlayerDeath = False
    clock.tick(60)
    timer += 1
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
        
        if event.type == pygame.KEYUP: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
            if event.key == pygame.K_SPACE:
                keys[SPACE] = False
        
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True
            if event.key == pygame.K_SPACE:
                keys[SPACE] = True
    #left movement            
    if keys[LEFT]==True:
        Vx = -5
        direction = LEFT
        
    #Right Movement
    elif keys[RIGHT]==True:
        Vx = 5
        direction = RIGHT
    else:
        Vx = 0
        
        
    if keys[SPACE] == True:
        shoot = True
    else:
        shoot = False
        
    
    #updating player
    Px += Vx
    if shoot == True:
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(Px+25, Py)
        if bullet.isAlive == True:
            for i in range(len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
            for i in range(len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
    
    else:
        bullet.xpos = Px + 25
        bullet.ypos = Py
        
        
    

    for i in range(len(armada)):
        timer = armada[i].move(timer)
    screen.fill((0,0,0))
    bullet.draw()
    #pygame.draw.rect(screen, (green), (Px, Py, 70, 50))
    screen.blit(player, (Px, Py), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    
    for i in range(len(armada)):
        armada[i].draw()
    for i in range(len(walls)):
        walls[i].draw()
    pygame.display.flip()
pygame.quit()

