import pygame
import random
import math
from pygame import mixer

# initialise pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_enemies = 6

for i in range(number_enemies):
    enemy_image.append(pygame.image.load('alien-ship.png'))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(25)

# bullet
bullet_image = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
over_font = pygame.font.Font('freesansbold.ttf', 70)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x, y - 5))


def is_collision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX > 768:
        playerX = 768
    elif playerX < 0:
        playerX = 0
    for i in range(number_enemies):
        if enemyY[i] > 440:
            for j in range(number_enemies):
                enemyY[j] = 4000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 768:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] < 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        collision = is_collision(enemyY[i], enemyX[i], bulletY, bulletX)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, 768)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)

    pygame.display.update()
