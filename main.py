import pygame
import random
import math

from pygame import mixer
# 1. Initialize the pyagame
pygame.init()

# 2. Create the screen
screen = pygame.display.set_mode((800,600))

# Soundtrack
# Music: Eric Skiff - Song Name - Resistor Anthems
# Available at http://EricSkiff.com/music
mixer.music.load('./assets/sounds/10_Arpanauts.mp3')
mixer.music.play(-1)

# 2.1 Background
background = pygame.image.load('./assets/images/background.png')
# 3. Caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./assets/images/ufo.png')
pygame.display.set_icon(icon)

# 4. Player
playerImg = pygame.image.load('./assets/images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# 5 Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./assets/images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# 5 Bullet

# Ready You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('./assets/images/bullet.png')
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('./assets/fonts/SketchRockwell-Bold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('./assets/fonts/bombfact.ttf', 90)

# Score Function
def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# 4.1 Create function Player
def player(x, y):
    screen.blit(playerImg, (x,y))

# 5 Enemy Function
 
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x,y))

#   Bullet Fujnction
def fire_bullet( x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit (bulletImg, (x+16, y+10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False

# 6. Game Loop
running = True
while running:

    # RGB = RED, GREEN, BLUE
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # if keystroke is pressed check wheter is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('./assets/effects/hit.wav')
                    bullet_sound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0
    # 5 = 5 + 0.1

    # Checking for boundaries of spaceship so 
    # it doesn't go out of bounds
    playerX += playerX_change

    if( playerX <=0 ):
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >= 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            mixer.music.stop()
            break

        enemyX[i] += enemyX_change[i]
        if( enemyX[i] <=0 ):
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('./assets/effects/alien_death.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    
    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
    
