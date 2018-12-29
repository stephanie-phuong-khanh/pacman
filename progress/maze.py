import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

maze_arr = []
with open('mazes/maze_01.txt', 'r') as maze:
    m = maze.readlines()
    for i in m:
        line = i.rstrip()
        maze_arr.append(line)

maze_height = len(maze_arr)
maze_width = len(maze_arr[0])
pixel_height = WINDOW_HEIGHT / maze_height
pixel_width = WINDOW_WIDTH / maze_width

pygame.init()
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('maze')

keepGoing = True

# clock = pygame.time.Clock()

# print(maze_arr)

while keepGoing:
    for event in pygame.event.get():    #event handler
        if event.type == pygame.QUIT:
            keepGoing = False
    lead_x = 0
    lead_y = 0
    for row in maze_arr:
        for col in row:
            if col == '#':
                pygame.draw.rect(gameDisplay, BLUE, (lead_x, lead_y, pixel_width, pixel_height))
            else:
                pygame.draw.rect(gameDisplay, BLACK, (lead_x, lead_y, pixel_width, pixel_height))
            lead_x += pixel_width
        lead_y += pixel_height
        lead_x = 0

    # gameDisplay.fill(BLACK)
    # pygame.draw.rect(gameDisplay, RED, (obj_x, obj_y, obj_width, obj_height))
    pygame.display.update()
    # clock.tick(30)

pygame.quit()
quit() 