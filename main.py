import pygame
import random

pygame.init ()

score = 0
CLOCK = pygame.time.Clock ()
MAX_FPS = 60
SCROLL_SPEED = 3
MAX_SCROLL_SPEED = 15
CHANGE_IN_SCROLL_SPEED = 1
hasGameStarted = False 
isAlive = True 
hasPlayedHitSound = False 
nextIncreaseInDifficulty = score + 50 

font = pygame.font.Font (r"fonts/times.ttf", 50)

# Colors:
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)
WHITE = (255, 255, 255)

# Functions:
def printText (text, textColor, x, y): 
    textImg = font.render (text, True, textColor)
    screen.blit (textImg, (x, y))

def death ():
    global SCROLL_SPEED, isAlive, hasPlayedHitSound, score
    SCROLL_SPEED = 0
    
    if not hasPlayedHitSound:
        hitSound.play()
        hasPlayedHitSound = True 
        if score > 105:
            goofyTrumpet.play ()

    isAlive = False

def reset ():
    global SCROLL_SPEED, nextIncreaseInDifficulty, hasPlayedGoofyScream, isAlive, hasPlayedHitSound, hasGameStarted, score, birdPositionX, birdPositionY, pipes
    SCROLL_SPEED = 3
    score = 0
    hasGameStarted = False 
    hasPlayedHitSound = False 
    isAlive = True 
    birdPositionX = 50
    birdPositionY = 300
    pipes.clear ()
    nextIncreaseInDifficulty = score + 50
    hasPlayedGoofyScream = False

# Main Window:
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption ("Flappy Birdy")

icon = pygame.image.load (r"images/icon.png")
icon = pygame.transform.scale (icon, (32, 32))
pygame.display.set_icon (icon)

mainMenu = pygame.image.load (r"images/mainMenu.png")
gameOver = pygame.image.load (r"images/gameOver.png")

# Background:
BG_WIDTH = SCREEN_WIDTH
BG_HEIGHT = 550
bg = pygame.image.load (r"images/bg.png")
bg = pygame.transform.scale (bg, (BG_WIDTH, BG_HEIGHT))

# Ground:
ground = pygame.image.load (r"images/ground.png")
GROUND_WIDTH = ground.get_width ()
GROUND_HEIGHT = ground.get_height ()
ground1 = ground
gpx1 = 0 # Ground Position X
ground2 = ground 
gpx2 = GROUND_WIDTH
gpy = BG_HEIGHT # Ground Position Y

# Bird:
birdFlapUp = pygame.image.load (r"images/flapUp.png")
birdFlapMid = pygame.image.load (r"images/flapMid.png")
birdFlapDown = pygame.image.load (r"images/flapDown.png")
birdDead = pygame.image.load (r"images/birdDead.png")
changeBirdFrameIndex = 0
bird = birdFlapUp

BIRD_WIDTH = bird.get_width ()
BIRD_HEIGHT = bird.get_height ()

birdPositionX = 50
birdPositionY = 300
birdVelocity = 0 
BIRD_ACCELERATION = 0.5
BIRD_PE = 8 

# Pipes:
pipes = []
pipeBottom = pygame.image.load (r"images/pipeBottom.png")
pipeTop = pygame.transform.flip (pipeBottom, False, True)
PIPE_WIDTH = pipeBottom.get_width ()
PIPE_HEIGHT = pipeBottom.get_height ()
pipeDistance = 200
CHANGE_IN_PIPE_DISTANCE = 10
MINIMUM_PIPE_DISTANCE = 100
pipeSpawnCooldown = 0

# Sound:
flapSound = pygame.mixer.Sound (r"sounds/jump.wav")
hitSound = pygame.mixer.Sound (r"sounds/hit.wav")
scoreSound = pygame.mixer.Sound (r"sounds/score.wav")
goofyTrumpet = pygame.mixer.Sound (r"sounds/goofyTrumpet.wav")
goofyScream = pygame.mixer.Sound (r"sounds/goofyScream.wav")
hasPlayedGoofyScream = False 

isRunning = True 
while isRunning:

    CLOCK.tick (MAX_FPS)
    birdRect = pygame.Rect (birdPositionX, birdPositionY, BIRD_WIDTH, BIRD_HEIGHT)

    screen.blit (bg, (0, 0))
    screen.blit (ground1, (gpx1, gpy))
    screen.blit (ground2, (gpx2, gpy))

    # Move the ground:
    gpx1 -= SCROLL_SPEED
    gpx2 -= SCROLL_SPEED
    if (gpx1 <= -GROUND_WIDTH):
        gpx1 = GROUND_WIDTH
    if (gpx2 <= -GROUND_WIDTH):
        gpx2 = GROUND_WIDTH

    # Make the bird flap:
    if isAlive:
        changeBirdFrameIndex += 1
        if (changeBirdFrameIndex < 5):
            bird = birdFlapUp
        elif (changeBirdFrameIndex < 10):
            bird = birdFlapMid
        elif (changeBirdFrameIndex < 15):
            bird = birdFlapDown 
        elif (changeBirdFrameIndex <= 20):
            bird = birdFlapMid
            if (changeBirdFrameIndex == 20):
                changeBirdFrameIndex = 0
    else:
        bird = birdDead

    if hasGameStarted:
        # Spawn Pipes:
        for p in pipes [:]:
            if p[0] <= -PIPE_WIDTH:
                pipes.remove (p)
                continue
            p[0] -= SCROLL_SPEED
            
            screen.blit (pipeBottom, (p[0], p[1]))
            screen.blit (pipeTop, (p[0], p[1] - PIPE_HEIGHT - pipeDistance))

            if birdPositionX > p[0] + PIPE_WIDTH // 2 and not p[2]:
                score += 1
                p[2] = True
                scoreSound.play ()

            pipeBottomRect = pygame.Rect (p[0], p[1], PIPE_WIDTH, PIPE_HEIGHT)
            pipeTopRect = pygame.Rect (p[0], p[1] - PIPE_HEIGHT - pipeDistance, PIPE_WIDTH, PIPE_HEIGHT)
            if (pipeBottomRect.colliderect (birdRect) or pipeTopRect.colliderect (birdRect)):
                death ()

        if isAlive:
            birdVelocity += BIRD_ACCELERATION
            birdPositionY += birdVelocity

            # Rotate the bird:
            angle = birdVelocity * -6
            rotatedBird = pygame.transform.rotate (bird, angle)

            screen.blit (rotatedBird, (birdPositionX, birdPositionY))
        else:
            screen.blit (bird, (birdPositionX, birdPositionY))

        if pipeSpawnCooldown <= 0:
            x = SCREEN_WIDTH
            y = random.randint (250, 525)
            pipes.append ([x, y, False]) # x, y, hasScored
            pipeSpawnCooldown = 60
        
        pipeSpawnCooldown -= 1

        if (birdPositionY + BIRD_HEIGHT >= BG_HEIGHT or birdPositionY <= -100):
            death ()
        
        if (score >= nextIncreaseInDifficulty):
            nextIncreaseInDifficulty += 50
            if (SCROLL_SPEED < MAX_SCROLL_SPEED):
                SCROLL_SPEED += CHANGE_IN_SCROLL_SPEED
            if (pipeDistance > MINIMUM_PIPE_DISTANCE):
                pipeDistance -= CHANGE_IN_PIPE_DISTANCE

    else: 
        screen.blit (bird, (birdPositionX, birdPositionY))

    printText (f"{score}", BLACK, 225, 83)

    for e in pygame.event.get ():
        if e.type == pygame.QUIT:
            isRunning = False 
        if hasGameStarted:
            if e.type == pygame.KEYDOWN:
                if isAlive:
                    if e.key == pygame.K_SPACE:
                        birdVelocity = -BIRD_PE
                        flapSound.play()
                else:
                    if e.key == pygame.K_RETURN:
                        reset ()
                if e.key == pygame.K_q:
                    isRunning = False 
        else:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                hasGameStarted = True 
                birdVelocity = -BIRD_PE
                flapSound.play()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                isRunning = False 
    
    if not hasGameStarted:
        screen.blit (mainMenu, (50, -20))
        printText ("Press Space to Start", WHITE, 50, BG_HEIGHT - 40)

    if not isAlive:
        screen.blit (gameOver, (0, 0))

    if score == 100 and not hasPlayedGoofyScream:
        goofyScream.play ()
        hasPlayedGoofyScream = True

    printText ("Press Q to Quit", BLACK, 100, 10)
    
    pygame.display.flip ()

pygame.quit ()