import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)

pygame.init()
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('pacman')

obj_width = 10
obj_height = 10
obj_x = 245
obj_y = 245
change_x = 0
change_y = 0

keepGoing = True

clock = pygame.time.Clock()

while keepGoing:
    for event in pygame.event.get():    #event handler
        if event.type == pygame.QUIT:
            keepGoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_y = 0
                change_x = -10
            elif event.key == pygame.K_RIGHT:
                change_y = 0
                change_x = 10
            elif event.key == pygame.K_UP:
                change_x = 0
                change_y = -10
            elif event.key == pygame.K_DOWN:
                change_x = 0
                change_y = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                change_y = 0
    if obj_x+change_x > 0 and obj_x+change_x+obj_width<WINDOW_WIDTH:
        obj_x += change_x
    if obj_y+change_y > 0 and obj_y+change_y+obj_height<WINDOW_HEIGHT:
        obj_y += change_y

    gameDisplay.fill(BLACK)
    pygame.draw.rect(gameDisplay, RED, (obj_x, obj_y, obj_width, obj_height)) #top left coords, width, height
    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit() 