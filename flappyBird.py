import pygame
import random 

pygame.init()

clock = pygame.time.Clock()
MAX_FPS = 60
SCROLL_SPEED = 5
score = 0
gameHasStarted = False

minecraftFont = pygame.font.Font (r"fonts/Minecraft.ttf", 25)
flappyBirdFontRegular = pygame.font.Font (r"fonts/flappybirdyregularfonty.ttf", 50)

def writeText (text, textColor, font, x, y):
    textImg = font.render (text, True, textColor)
    screen.blit (textImg, (x, y))

def death():
    global BIRD_ACCELERATION, canFly, isAlive, birdVelocity, SCROLL_SPEED
    BIRD_ACCELERATION = 0
    birdVelocity = 0
    canFly = False 
    isAlive = False 
    SCROLL_SPEED = 0
    writeText ("You Died!", (0, 0, 0), flappyBirdFontRegular, 180, 300)
    writeText ("Press Enter To Start Again!", (0, 0, 0), flappyBirdFontRegular, 30, 350)

def reset():
    global birdPositionX, gameHasStarted, birdPositionY, BIRD_ACCELERATION, canFly, isAlive, birdVelocity, SCROLL_SPEED, score 
    BIRD_ACCELERATION = 0.5
    canFly = True 
    isAlive = True 
    birdVelocity = 0
    SCROLL_SPEED = 5
    pipes.clear()
    score = 0
    birdPositionX = 100
    birdPositionY = 300
    gameHasStarted = False

# Screen
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
BG_WIDTH = 500
BG_HEIGHT = 550
bg = pygame.image.load (r"images/bg.png")
bg = pygame.transform.scale (bg, (BG_WIDTH, BG_HEIGHT))

# Ground
ground1 = pygame.image.load (r"images/ground.png")
gpx1 = 0
GROUND_WIDTH = ground1.get_width()
GROUND_HEIGHT = ground1.get_height()
ground2 = pygame.image.load (r"images/ground.png")
gpx2 = GROUND_WIDTH 

# Bird
birdFlapUp = pygame.image.load (r"images/flapUp.png")
birdFlapMid = pygame.image.load (r"images/flapMid.png")
birdFlapDown = pygame.image.load (r"images/flapDown.png")
birdDead = pygame.image.load (r"images/deadBird.png")
bird = birdFlapMid 
BIRD_WIDTH = bird.get_width()
BIRD_HEIGHT = bird.get_height()
BIRD_ACCELERATION = 0.5 # pixels / frame ^ 2
birdVelocity = 0 # pixels / frame
birdPE = -8 
changeBirdFrameIndex = 0
birdPositionX = 100 
birdPositionY = 300 
canFly = True
isAlive = True 

# Pipe
pipes = []
pipeBottom = pygame.image.load (r"images/pipeBottom.png")
pipeTop = pygame.transform.flip (pipeBottom, False, True)
pipeSpawnCoolDown = 60
PIPE_DISTANCE = 200 
PIPE_WIDTH = pipeBottom.get_width()
PIPE_HEIGHT = pipeBottom.get_height()

isRunning = True 
while isRunning:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            isRunning = False
        if gameHasStarted:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and canFly:
                    birdVelocity = birdPE
                if not isAlive:
                    if e.key == pygame.K_RETURN:
                        reset() 
        if not gameHasStarted:
            screen.blit (bg, (0, 0))
            screen.blit (ground1, (gpx1, BG_HEIGHT))
            writeText ("Press Space To Start", (0, 0, 0), minecraftFont, 100, 300)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                        gameHasStarted = True
            pygame.display.update()

    if gameHasStarted:
        clock.tick (MAX_FPS)
        screen.blit (bg, (0, 0))

        screen.blit (ground1, (gpx1, BG_HEIGHT))
        screen.blit (ground2, (gpx2, BG_HEIGHT))
        
        gpx1 -= SCROLL_SPEED
        gpx2 -= SCROLL_SPEED
        if (gpx1 <= - GROUND_WIDTH):
            gpx1 = GROUND_WIDTH
        if (gpx2 <= - GROUND_WIDTH):
            gpx2 = GROUND_WIDTH

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
                if changeBirdFrameIndex == 20:
                    changeBirdFrameIndex = 0
        else:
            bird = birdDead

        birdVelocity += BIRD_ACCELERATION
        birdPositionY += birdVelocity
        
        angle = birdVelocity * -3
        rotatedBird = pygame.transform.rotate (bird, angle)

        birdRect = pygame.Rect (birdPositionX, birdPositionY, BIRD_WIDTH, BIRD_HEIGHT)

        if (pipeSpawnCoolDown == 0):
            x = 500
            y = random.randint (300, 550)
            pipes.append ([x, y, False]) # x, y, scored? 
            pipeSpawnCoolDown = 60
        else:
            pipeSpawnCoolDown -= 1

        for p in pipes [:]:
            if p[0] <= -PIPE_WIDTH:
                pipes.remove (p)
            p[0] -= SCROLL_SPEED
            screen.blit (pipeBottom, (p[0], p[1]))
            screen.blit (pipeTop, (p[0], p[1] - PIPE_DISTANCE - PIPE_HEIGHT))

            if birdPositionX > p[0] and not p[2]:
                score += 1
                p[2] = True 
            
            pipeBottomRect = pygame.Rect (p[0], p[1], PIPE_WIDTH, PIPE_HEIGHT)
            pipeTopRect = pygame.Rect (p[0], p[1] - PIPE_HEIGHT - PIPE_DISTANCE, PIPE_WIDTH, PIPE_HEIGHT)

            if (birdRect.colliderect (pipeBottomRect) or birdRect.colliderect (pipeTopRect)):
                death()

        screen.blit (rotatedBird, (birdPositionX, birdPositionY))

        if (birdPositionY + BIRD_HEIGHT >= BG_HEIGHT):
            death()

        writeText (f"{score}", (0, 0, 0), minecraftFont, 225, 100)

        pygame.display.update()

pygame.quit()
