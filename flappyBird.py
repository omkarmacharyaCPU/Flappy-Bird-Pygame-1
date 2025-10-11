import pygame
import random

pygame.init() 

score = 0
nextChangeInDistance = 100
font = pygame.font.SysFont (None, 60)
isAlive = True 
gameHasStarted = False
hitPlayed = False

CLOCK = pygame.time.Clock()
MAX_FPS = 60
SCROLL_SPEED = 5   

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption ("Flappy Birdy!")
icon = pygame.image.load (r"images/icon.png")
pygame.display.set_icon (icon)

# Functions:
def printText (text, font, textColor, x, y):
    textImg = font.render (text, True, textColor)
    screen.blit (textImg, (x, y))

def death():
    global SCROLL_SPEED, BIRD_ACCELERATION, birdVelocity, isAlive
    SCROLL_SPEED = 0
    BIRD_ACCELERATION = 0
    birdVelocity = 0
    isAlive = False 

def reset():
    global SCROLL_SPEED, BIRD_ACCELERATION, birdVelocity, isAlive, hitPlayed, pipes, gameHasStarted, score, birdPositionX, birdPositionY
    SCROLL_SPEED = 5
    BIRD_ACCELERATION = 0.5
    birdVelocity = 0
    isAlive = True 
    pipes.clear ()
    birdPositionX = 100
    birdPositionY = 250
    score = 0
    gameHasStarted = False
    hitPlayed = False

# Background:
BG_WIDTH = 500
BG_HEIGHT = 600
bg = pygame.image.load (r"images/bg.png")
bg = pygame.transform.scale (bg, (BG_WIDTH, BG_HEIGHT))

# Ground:
ground = pygame.image.load (r"images/ground.png")
GROUND_WIDTH = ground.get_width()
GROUND_HEIGHT = ground.get_height()

ground1 = ground
groundPositionX1 = 0
ground2 = ground
groundPositionX2 = GROUND_WIDTH

# Bird:
flapUp = pygame.image.load (r"images/flapUp.png")
flapDown = pygame.image.load (r"images/flapDown.png")
flapMid = pygame.image.load (r"images/flapMid.png")
bird = flapMid
birdDead = pygame.image.load (r"images/birdDead.png")
BIRD_WIDTH = bird.get_width()
BIRD_HEIGHT = bird.get_height()
changeBirdFrameIndex = 0
birdPositionX = 100
birdPositionY = 250
birdVelocity = 0
BIRD_ACCELERATION = 0.5
BIRD_PE = 8

# Pipes:
pipes = []
pipeBottom = pygame.image.load (r"images/pipeBottom.png")
pipeTop = pygame.transform.flip (pipeBottom, False, True)
PIPE_DISTANCE = 200
pipeCooldown = 0 # 60
PIPE_WIDTH = pipeBottom.get_width()
PIPE_HEIGHT = pipeBottom.get_height()

# Sounds:
flapSound = pygame.mixer.Sound (r"sounds/jump.wav")
hitSound = pygame.mixer.Sound (r"sounds/hit.wav")

isRunning = True
while (isRunning):

    CLOCK.tick (MAX_FPS)

    screen.blit (bg, (0, 0))
    screen.blit (ground1, (groundPositionX1, BG_HEIGHT))
    screen.blit (ground2, (groundPositionX2, BG_HEIGHT))

    groundPositionX1 -= SCROLL_SPEED
    groundPositionX2 -= SCROLL_SPEED
    if (groundPositionX1 <= -GROUND_WIDTH):
        groundPositionX1 = GROUND_WIDTH
    if (groundPositionX2 <= -GROUND_WIDTH):
        groundPositionX2 = GROUND_WIDTH

    birdRect = pygame.Rect (birdPositionX, birdPositionY, BIRD_WIDTH, BIRD_HEIGHT)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            isRunning = False 
        if gameHasStarted:
            if e.type == pygame.KEYDOWN:
                if isAlive and e.key == pygame.K_SPACE:
                    birdVelocity = -BIRD_PE
                    flapSound.play()
                if not isAlive:
                    if e.key == pygame.K_RETURN:
                        reset()
        else:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    gameHasStarted = True 
                    birdVelocity = -BIRD_PE
                    flapSound.play()

    if gameHasStarted:
        birdPositionY += birdVelocity
        birdVelocity += BIRD_ACCELERATION

        angle = birdVelocity * -4
        rotatedBird = pygame.transform.rotate (bird, angle)

        if (pipeCooldown == 0):
            x = SCREEN_WIDTH
            y = random.randint (225, 575)
            pipes.append ([x, y, False]) # x, y, scored?
            pipeCooldown = 60
        else:
            pipeCooldown -= 1

        for p in pipes[:]:
            if p[0] <= -PIPE_WIDTH:
                pipes.remove (p)
                continue 
            p[0] -= SCROLL_SPEED
            screen.blit (pipeBottom, (p[0], p[1]))
            screen.blit (pipeTop, (p[0], p[1] - PIPE_DISTANCE - PIPE_HEIGHT))

            if not p[2]:
                if birdPositionX > p[0] + PIPE_WIDTH // 2:
                    score += 1
                    p[2] = True

            pipeBottomRect = pygame.Rect (p[0], p[1], PIPE_WIDTH, PIPE_HEIGHT)
            pipeTopRect = pygame.Rect (p[0], p[1] - PIPE_DISTANCE - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)

            if (pipeBottomRect.colliderect (birdRect) or pipeTopRect.colliderect (birdRect)):
                death()
                if not hitPlayed:
                    hitSound.play ()
                    hitPlayed = True 

        if (birdPositionY >= BG_HEIGHT - BIRD_HEIGHT):
            death()
        elif (birdPositionY <= 0):
            death()

        screen.blit (rotatedBird, (birdPositionX, birdPositionY))

        if (score >= nextChangeInDistance):
            PIPE_DISTANCE -= 5
            nextChangeInDistance += 100
            

    else:
        printText ("Press Space To Start!", font, (0, 0, 0), 35, 300)
        screen.blit (bird, (birdPositionX, birdPositionY))

    if (isAlive):
        changeBirdFrameIndex += 1
        if (changeBirdFrameIndex < 5):
            bird = flapUp
        elif (changeBirdFrameIndex < 10):
            bird = flapMid 
        elif (changeBirdFrameIndex < 15):
            bird = flapDown 
        elif (changeBirdFrameIndex < 20):
            bird = flapMid
            if (changeBirdFrameIndex == 19):
                changeBirdFrameIndex = 0
    else:
        bird = birdDead
        printText ("Press Enter to Restart!", font, (0, 0, 0), 25, 300)

    printText (f"{score}", font, (0, 0, 0), SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2 - 300)


    pygame.display.flip()

pygame.quit()