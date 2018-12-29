import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
pygame.init()
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pacman = pygame.image.load('pacman.png')
pacman = pygame.transform.scale(pacman, (50, 50))
pacman = pygame.transform.rotate(pacman, 90) #up

keepGoing = True


while keepGoing:
    for event in pygame.event.get():    #event handler
        if event.type == pygame.QUIT:
            keepGoing = False
    gameDisplay.fill(BLACK)

    gameDisplay.blit(pacman, (0,0))
    pygame.display.update()

pygame.quit()
quit() 