import pygame
pygame.init()
pygame.display.set_caption("Inchaders")
ScreenWidth = 800
ScreenHeight = 800
screen = pygame.display.set_mode((ScreenWidth,ScreenHeight))
clock = pygame.time.Clock()
green = (0, 255,0)


player = pygame.image.load('Player.png') #load your spritesheet
player.set_colorkey((255,0,255))

frameWidth = 70
frameHeight = 50
RowNum = 0
frameNum = 0

doExit = False
Px = 0
Py = 700
Vx = 0
#constants
LEFT = 0
RIGHT = 1
keys = [False, False]
while not doExit:
    clock.tick(60)
    
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
      
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=True

            
        if event.type == pygame.KEYUP: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT]=False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT]=False
                
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
    #updating player
    Px += Vx
    
    screen.fill((0,0,0))
    #pygame.draw.rect(screen, (green), (Px, Py, 70, 50))
    screen.blit(player, (Px, Py), (frameWidth*frameNum, RowNum*frameHeight, frameWidth, frameHeight))
    pygame.display.flip()
pygame.quit()
