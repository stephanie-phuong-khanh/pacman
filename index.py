import pygame
pygame.init()

window_width = 500
window_height = 400

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pacman')
clock = pygame.time.Clock()

crashed = False

circleX = 0
circleY= 200
circleVelX = 0
circleVelY = 0

while not crashed:
    window.fill((0,0,0))
    pygame.draw.rect(window, (255,80,80), (circleX,circleY,30,30))
    #pygame.draw.circle(window, (255,80,80), (circleX, circleY), 20, 0)
    #pygame.draw.lines(window, white, True, ((400,400), (300,300), (400,300)))
    #pygame.draw.circle(WHERE TO DRAW, (RED, GREEN, BLUE), (X COORDINATE, Y COORDINATE), RADIUS, HEIGHT, WIDTH)
    #pygame.draw.lines(WHERE TO DRAW, COLOUR, CLOSE THE SHAPE FOR US?, THE POINTS TO DRAW, LINE WIDTH)
    circleX += circleVelX
    #circleY += circleVelY
    circleVelX += 0.1
    #circleVelY += 0.1

    
    for event in pygame.event.get():    #get any events that happen -> get list of events per frame per second
        if event.type == pygame.QUIT:
            crashed = True
        #print(event)
    pygame.display.update() #.update can update particular thing, not whole surface
    clock.tick(60)

pygame.quit()
quit()