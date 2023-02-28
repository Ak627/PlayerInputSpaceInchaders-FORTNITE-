import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Inchaders")
ScreenWidth = 800
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
clock = pygame.time.Clock()
green = (0, 255,0)

timer = 0
back = pygame.image.load('Stars.png') #load your spritesheet

pew = pygame.mixer.Sound('pew.ogg')
scream1 = pygame.mixer.Sound('scream.mp3')

frameWidth = 50
frameHeight = 38
RowNum = 0
frameNum = 0

doExit = False
Px = 0
Py = ScreenHeight - 50
Vx = 0

lives = 3

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
        if time % 520 == 0:
            self.ypos +=50
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
            
class Missle:
    def __init__(self, xpos, ypos):
        self.xpos = -10
        self.ypos = -10
        self.isAlive = False
    def move(self):
        if self.isAlive == True:
            self.ypos += 5
        if self.ypos > 800:
            self.isAlive = False
            self.xpos = -10
            self.ypos = -10
    def draw(self):
        if self.isAlive == True:
            pygame.draw.rect(screen, (250, 0, 250), (self.xpos, self.ypos, 3, 20))

missles = []
for i in range(10):
    missles.append(Missle(i*80+75, 100))
    
    
bullet = Bullet(Px+25, Py)

player = pygame.image.load('Player.png') #load your spritesheet
player.set_colorkey((255,255,255))

death = pygame.image.load("Death.png")
death.set_colorkey((255,0,255))


while lives > 0:
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
        pygame.mixer.Sound.play(pew)

        shoot = True

    else:
        shoot = False
        
    
    
    if shoot == True:
        bullet.isAlive = True
        
    if bullet.isAlive == True:
        bullet.move(Px+25, Py)
        if bullet.isAlive == True:
            for i in range(len(armada)):
                bullet.isAlive = armada[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    pygame.mixer.Sound.play(scream1)
                    break
        if bullet.isAlive == True:
            for i in range(len(walls)):
                bullet.isAlive = walls[i].collide(bullet.xpos, bullet.ypos)
                if bullet.isAlive == False:
                    break
    
    else:
        bullet.xpos = Px + 25
        bullet.ypos = Py
    
    for i in range(len(walls)):
        for j in range(len(missles)):
            if missles[j].isAlive == True:
                if walls[i].collide(missles[j].xpos, missles[j].ypos) == False:
                    missles[j].isAlive = False
                    break
        
    

    for i in range(len(armada)):
        timer = armada[i].move(timer)
    for i in range(len(missles)):
        missles[i].move()
        
    ran = random.randrange(100)
    if ran < 2:
        pick = random.randrange(0, len(armada))
        if armada[pick].isAlive == True:
            for i in range(len(missles)):
                if missles[i].isAlive == False:
                    missles[i].isAlive = True
                    missles[i].xpos = armada[pick].xpos+25
                    missles[i].ypos = armada[pick].ypos
                    break 
    
    for i in range(len(missles)):
        if missles[i].xpos > Px:
            if missles[i].xpos < Px + 50:
                if missles[i].ypos > Py:
                    if missles[i].ypos < Py + 38:
                        lives -= 1
                        time.sleep(1)
                        Px = 0
                        
    for i in range(len(armada)):
            if armada[i].ypos > Py:
                        lives -= 3
                        time.sleep(1)
            
    #updating player
    Px += Vx
    screen.fill((0,0,0))
    screen.blit(back ,(0,0))
    bullet.draw()
    #pygame.draw.rect(screen, (green), (Px, Py, 70, 50))
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render('LIVES:', False, (255, 0, 0))
    number = my_font.render(str(lives), False, (255,0,0))
    
    screen.blit(player, (Px, Py), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    for i in range(len(missles)):
        missles[i].draw()
    for i in range(len(armada)):
        armada[i].draw()
    for i in range(len(walls)):
        walls[i].draw()
    screen.blit(text_surface, (0,0))
    screen.blit(number, (100,0))
    pygame.display.flip()
pygame.quit()

