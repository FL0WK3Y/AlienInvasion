import pygame
import os
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((900,800))
pygame.display.set_caption("breaking bricks")
bat = pygame.image.load(os.path.join('/Users/gregorirodriguez/Desktop/Games/brake out /images/DurrrSpaceShip.png'))
bat = bat.convert_alpha() 
bat_rect = bat.get_rect()
bat_rect[1] = screen.get_height() - 100

ball = pygame.image.load(os.path.join('/Users/gregorirodriguez/Desktop/Games/brake out /images/Fire-Ball.png'))
ball = ball.convert_alpha() 
ball_rect = ball.get_rect()
ball_start = (450, 400)
ball_speed = (3.0, 3.0)
ball_served = False
sx, sy = ball_speed
ball_rect.topleft = ball_start
ball_spriteWidth = 150
ball_spriteheight = 150

ball = pygame.transform.scale(ball,(ball_spriteWidth,ball_spriteheight))

brick = pygame.image.load(os.path.join('/Users/gregorirodriguez/Desktop/Games/brake out /images/ship_blue.png'))
brick = brick.convert_alpha() 
brick_rect = brick.get_rect()

b_spriteWidth = 100
b_spriteheight = 60

brick = pygame.transform.scale(brick,(b_spriteWidth,b_spriteheight))

bricks =[]
brick_rows = 2
brick_gap = 0 
brick_cols = screen.get_width() // (brick_rect[2]+ brick_gap)
side_gap = (screen.get_width() - (brick_rect[2]+brick_gap) *brick_cols + brick_gap)//2


for y in range(brick_rows):
    brickY = y * (brick_rect[3]+ brick_gap)
    for x in range(brick_cols):
        brickX = x* (brick_rect[2] + brick_gap ) + side_gap
        bricks.append((brickX, brickY))


clock = pygame.time.Clock()
game_over = False
while not game_over:
    dt =clock.tick(50)
    screen.fill((255,255,255))
    
    for b in bricks:
        screen.blit(brick, b)
    
    screen.blit(bat, bat_rect)
    screen.blit(ball, ball_rect)
    
    pressed = pygame.key.get_pressed()
    if pressed[K_LEFT]:
        x-=.5 * dt
    if pressed[K_RIGHT]:
        x+=0.5 * dt
    if pressed[K_SPACE]:
        ball_served = True
    # this is the collision of the bat and the ball 
    if bat_rect[0]+ bat_rect.width >= ball_rect[0] >= bat_rect[0] and ball_rect[1] + ball_rect.height >= bat_rect[1] and sy > 0:
        sy*=- 1
        #this  will increase the speed of the ball after the ball hits the paddle  
        sx*=1.1
        sy*=1.1
        continue
    delete_bricks = None
    # this if statment  is collision ditection of the ball and the bricks 
    for b in bricks:
        bx,by = b
        if bx <= ball_rect[0] <= bx+ brick_rect.width and by <= ball_rect[1]<= by +brick_rect.height:
            delete_bricks = b
            if ball_rect[0]<= bx + .5:
                sx *= -1
            elif ball_rect[0] >= bx + brick_rect.width - .5 :
                sx *= -1
            if ball_rect[1] <= by + .5:
                sy*= -1
            elif ball_rect[1] <= by +brick_rect.height - .5:
                sy*= -1
            break


        
    # this if statment check if a collision happend an then it deletes the brick 
    if delete_bricks is not None:
        bricks.remove(delete_bricks)
    
    # top border
    if ball_rect[1] <= 0:
        ball_rect[1] = 0
        sy *= -1

    # Bottom border
    if ball_rect[1] >= screen.get_height() - ball_rect.height:
       #ball_rect[1] = screen.get_height() - ball_rect.height
       #sy *= -1
       ball_served = False
       ball_rect.topleft = ball_start

    # left border for the ball 
    if ball_rect[0] <= 0:
        ball_rect[0] = 0
        sx *= -1
    if x > (screen.get_width() - bat_rect.width):
        x = screen.get_width() - bat_rect.width
    #this code makes the paddle teleport to the right side of the screen after the paddle tries to go to the left side past x = 0
    if x < 0:
        x = screen.get_width() - bat_rect.width
    # Right border 
     
    if ball_rect[0] >= screen.get_width() - ball_rect.width:
        ball_rect[0] = screen.get_width() - ball_rect.width
        sx *= -1

    bat_rect[0] = x
    # this controls the speed ball moves
    if ball_served:
        ball_rect[0] += sx
        ball_rect[1] += sy
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    pygame.display.update()
pygame.quit()
