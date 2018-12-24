import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (0,0,255)

pygame.init()
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('pacman')

# Maze
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

# Object
obj_width = 10
obj_height = 10
obj_x = 1
obj_y = 1

# Movement
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4
next_move = 0
change_x = 0
change_y = 0

keepGoing = True
clock = pygame.time.Clock()

while keepGoing:
    for event in pygame.event.get():    #event handler
        if event.type == pygame.QUIT:
            keepGoing = False
        if event.type == pygame.KEYDOWN:      
            if event.key == pygame.K_UP:
                if maze_arr[obj_y-1][obj_x] != '#':
                    change_x = 0
                    change_y = -1
                    next_move = 0
                else:
                    next_move = MOVE_UP
            elif event.key == pygame.K_DOWN:
                if maze_arr[obj_y+1][obj_x] != '#':
                    change_x = 0
                    change_y = 1
                    next_move = 0
                else:
                    next_move = MOVE_DOWN
            elif event.key == pygame.K_LEFT:
                if maze_arr[obj_y][obj_x-1] != '#':
                    change_x = -1
                    change_y = 0
                    next_move = 0
                else:
                    next_move = MOVE_LEFT
            elif event.key == pygame.K_RIGHT:
                if maze_arr[obj_y][obj_x+1] != '#':
                    change_x = 1
                    change_y = 0
                    next_move = 0
                else:
                    next_move = MOVE_RIGHT
    if next_move > 0:
        if next_move == MOVE_UP and maze_arr[obj_y-1][obj_x] != '#':
            change_x = 0
            change_y = -1
        elif next_move == MOVE_DOWN and maze_arr[obj_y+1][obj_x] != '#':
            change_x = 0
            change_y = 1
        elif next_move == MOVE_LEFT and maze_arr[obj_y][obj_x-1] != '#':
            change_x = -1
            change_y = 0
        elif next_move == MOVE_RIGHT and maze_arr[obj_y][obj_x+1] != '#':
            change_x = 1
            change_y = 0
    if maze_arr[obj_y+change_y][obj_x+change_x] == '#':
        change_x = 0
        change_y = 0
    obj_x += change_x
    obj_y += change_y

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

    pygame.draw.rect(gameDisplay, RED, (obj_x*pixel_width+5, obj_y*pixel_height+5, 10, 10)) #top left coords, width, height
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit() 