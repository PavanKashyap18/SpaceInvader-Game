import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create a game window
# 1st valve is a width and 2nd value is height of the window
screen = pygame.display.set_mode((800, 600))

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# New background
background = pygame.image.load('background.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Player.png
playerImg = pygame.image.load('player.png')
playerX = 370  # half of the width
playerY = 500  # half of the height
playerX_change = 0

# Enemy.png
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy 2.png'))
    enemyX.append(
        random.randint(0, 800))  # specifying random values for enemy to occur i.e the stating and the end values
    enemyY.append(
        random.randint(50, 200))  # specifying random values for enemy to occur i.e the stating and the end values
    enemyX_change.append(0.8)  # speed
    enemyY_change.append(30)  # speed

# Bullet.png
# Ready -> can't see the bullet on the screen
# Fire -> The bullet is currently moving
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 1.2  # Bullet speed
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 40)
textX = 10
textY = 10

# GAME OVER TEXT
over_font = pygame.font.Font('freesansbold.ttf', 70)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (100, 80, 190))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!...", True, (100, 30, 100))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # used to draw the player on the game window


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # used to draw the enemy on the game window


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # To check the input controls(keyboard events)
        if event.type == pygame.KEYDOWN:  # KEYDOWN is event of pressing the key
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = +1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    Bullet_Sound = mixer.Sound('laser.wav')
                    Bullet_Sound.play()
                    # Get the current x co-ordinate of the spaceship
                    BulletX = playerX
                    fire_bullet(BulletX, BulletY)

        if event.type == pygame.KEYUP:  # KEYUP is event of releasing the key tha is been pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # moving of the player should be stooped when ever the key is been released

    # Checking the boundaries for player spaceship so that it does not crosses the current window size
    playerX += playerX_change  # arithmetic operation which increases and decreases the value of playerX
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:  # because the size of the space ship is 64pixel (ie 800-64)
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # GAME OVER
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]  # arithmetic operation which increases and decreases the value of playerX
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:  # because the size of the enemy is 64pixel (ie 800-64)
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            BulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # to update the display
    pygame.display.update()
