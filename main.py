import pygame
from random import randint
from time import time

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Fighting")

WHITE = (255, 255, 255)
FENCE = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BORDER1 = pygame.Rect(WIDTH//2 - 2, 0, 4, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/bullet.mp3')
BONUS_SOUND = pygame.mixer.Sound('Assets/bonus.mp3')
WIN_SOUND = pygame.mixer.Sound('Assets/win.mp3') 
SPACE_SOUND = pygame.mixer.Sound('Assets/space.mp3')
SHIELD_SOUND = pygame.mixer.Sound('Assets/shield.mp3')
SHIELD_ON_SOUND = pygame.mixer.Sound('Assets/shield_on.mp3')
METEOR_HIT_SOUND = pygame.mixer.Sound('Assets/meto_hyk.mp3')

HEALTH_FONT = pygame.font.SysFont('Assets/Decrypted.ttf', 40)
WINNER_FONT = pygame.font.SysFont('Assets/Decrypted.ttf', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
METEORIT_VEL = 5
POINTS = 5
MIDDLE_TIME = 4
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
ELLIPSE_WIDTH, ELLIPSE_HEIGHT = 25, 25
METEORIT_WIDTH, METEORIT_HEIGHT = 25, 60
CROWN_WIDTH, CROWN_HEIGHT = 25, 20
SHIELD_WIDTH, SHIELD_HEIGHT = 65, 65

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/spaceship_yellow_on.png'), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/spaceship_red_on.png'), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

ELLIPSE = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/health.png'), (ELLIPSE_WIDTH, ELLIPSE_HEIGHT)), 0)

HEALTH = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/ellipse.png'), (ELLIPSE_WIDTH, ELLIPSE_HEIGHT)), 0)

DEATH = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/death.png'), (ELLIPSE_WIDTH, ELLIPSE_HEIGHT)), 0)

METEORIT = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/meteorit.png'), (METEORIT_WIDTH, METEORIT_HEIGHT)), 0)

SHIELD = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/shield.png'), (SHIELD_WIDTH, SHIELD_HEIGHT)), 0)

CROWN_YELLOW = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/crown.png'), (CROWN_WIDTH, CROWN_HEIGHT)), 90)

CROWN_RED = pygame.transform.rotate(pygame.transform.scale(
    pygame.image.load('Assets/crown.png'), (CROWN_WIDTH, CROWN_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load('Assets/space.jpg'), (WIDTH, HEIGHT))

def draw_window(red, yellow, ellipse, health, death1, death2, red_bullets, yellow_bullets, meteorits, red_health, 
                yellow_health, red_point, yellow_point, red_shield, yellow_shield):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, FENCE, BORDER1)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    red_point_text = HEALTH_FONT.render(
        "Point: " + str(red_point), 1, WHITE)
    yellow_point_text = HEALTH_FONT.render(
        "Point: " + str(yellow_point), 1, WHITE)
    WIN.blit(red_point_text, (WIDTH - red_point_text.get_width() - 10, 50))
    WIN.blit(yellow_point_text, (10, 50))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(ELLIPSE, (ellipse.x, ellipse.y))
    WIN.blit(HEALTH, (health.x, health.y))
    WIN.blit(DEATH, (death1.x, death1.y))
    WIN.blit(DEATH, (death2.x, death2.y))
    WIN.blit(SHIELD, (red_shield.x, red_shield.y))
    WIN.blit(SHIELD, (yellow_shield.x, yellow_shield.y))

    for bullet in red_bullets: pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets: pygame.draw.rect(WIN, YELLOW, bullet)
    for meteorit in meteorits: WIN.blit(METEORIT, (meteorit.x, meteorit.y))

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x - VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x - VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red, meteorits, red_shield, yellow_shield):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red_shield.colliderect(bullet):
            yellow_bullets.remove(bullet)
        elif red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            BULLET_HIT_SOUND.play()
            for i in range(2):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow_shield.colliderect(bullet):
            red_bullets.remove(bullet)
        elif yellow.colliderect(bullet):
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            for i in range(2):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def meteorits_fly(meteorits, red, yellow, red_shield, yellow_shield):
    for meteorit in meteorits:
        meteorit.y += METEORIT_VEL
        if red_shield.colliderect(meteorit):
            meteorits.remove(meteorit)
        elif yellow_shield.colliderect(meteorit):
            meteorits.remove(meteorit)
        elif yellow.colliderect(meteorit):
            METEOR_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            meteorits.remove(meteorit)
        elif red.colliderect(meteorit):
            METEOR_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
            meteorits.remove(meteorit)
        elif meteorit.y > 500:
            meteorits.remove(meteorit)

def handle_shields(red_time, yellow_time):
    red_shield_tf = False
    yellow_shield_tf = False
    if time()-red_time <= MIDDLE_TIME and red_time>0:
        red_shield_tf = True
        SHIELD_SOUND.play()
    else:
        red_shield_tf = False
    if time()-yellow_time <= MIDDLE_TIME and yellow_time>0:
        yellow_shield_tf = True
        SHIELD_SOUND.play()
    else:
        yellow_shield_tf = False
    return red_shield_tf, yellow_shield_tf

def draw_winner(text, red, yellow):
    WIN_SOUND.play()
    if text == "Yellow Wins!":
        WIN.blit(CROWN_YELLOW, (yellow.x-5, yellow.y+15))
    elif text == "Red Wins!":
        WIN.blit(CROWN_RED, (red.x+25, red.y+15)) 
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    SPACE_SOUND.play()

    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_shield = pygame.Rect(-150, -160, SHIELD_WIDTH, SHIELD_HEIGHT)
    yellow_shield = pygame.Rect(-150, -150, SHIELD_WIDTH, SHIELD_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ellipse = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)
    health = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)
    death1 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)
    death2 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    meteorits = []

    red_health = 10
    yellow_health = 10

    red_point = 0
    yellow_point = 0

    red_time = -1
    yellow_time = -1

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width-20, yellow.y + yellow.height//2+5, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2+5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LSHIFT and yellow_point >= POINTS:
                    yellow_time = time()
                    yellow_point -= POINTS
                    SHIELD_ON_SOUND.play()
                    
                if event.key == pygame.K_RSHIFT and red_point >= POINTS:
                    red_time = time()
                    red_point -= POINTS
                    SHIELD_ON_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        if yellow.colliderect(ellipse):
            BONUS_SOUND.play()
            yellow_point += 1
            ellipse = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        if red.colliderect(ellipse): 
            BONUS_SOUND.play()
            red_point += 1
            ellipse = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        if yellow.colliderect(health):
            BONUS_SOUND.play()
            if yellow_health < 7: yellow_health += 1
            health = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        if red.colliderect(health):
            BONUS_SOUND.play()
            if red_health < 7: red_health += 1
            health = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)
            
        if yellow.colliderect(death1):
            BONUS_SOUND.play()
            for i in range(3):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            death1 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        if red.colliderect(death1):
            BONUS_SOUND.play()
            for i in range(3):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            death1 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)
        
        if yellow.colliderect(death2):
            BONUS_SOUND.play()
            for i in range(3):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            death2 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        if red.colliderect(death2):
            BONUS_SOUND.play()
            for i in range(3):
                meteorit = pygame.Rect(randint(10, WIDTH-METEORIT_WIDTH-10), randint(-150, -20), METEORIT_WIDTH, METEORIT_HEIGHT)
                meteorits.append(meteorit)
            death2 = pygame.Rect(randint(10, WIDTH-ELLIPSE_WIDTH-10), randint(10, HEIGHT-ELLIPSE_HEIGHT-10), ELLIPSE_WIDTH, ELLIPSE_HEIGHT)

        red_shield_tf, yellow_shield_tf = handle_shields(red_time, yellow_time)
        if red_shield_tf: red_shield.x, red_shield.y = red.x-12, red.y-5
        else: red_shield.x, red_shield.y = -150, -150
        if yellow_shield_tf: yellow_shield.x, yellow_shield.y = yellow.x-15, yellow.y-5
        else: yellow_shield.x, yellow_shield.y = -150, -150

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        meteorits_fly(meteorits, red, yellow, red_shield, yellow_shield)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, meteorits, red_shield, yellow_shield)
        draw_window(red, yellow, ellipse, health, death1, death2, red_bullets, yellow_bullets, meteorits, red_health, yellow_health, 
                    red_point, yellow_point, red_shield, yellow_shield)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text, red, yellow)
            break

    main()

main()