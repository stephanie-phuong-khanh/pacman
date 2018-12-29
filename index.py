import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (5,21,104)

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 50)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500
top_offset = (WINDOW_HEIGHT - GAME_HEIGHT) / 2
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('pacman')

# Maze
maze_arr = []
with open('mazes/maze_01.txt', 'r') as maze:
    m = maze.readlines()
    for i in m:
        line = list(i.rstrip())
        maze_arr.append(line)

target_score = sum(row.count('@') for row in maze_arr)
print(target_score)

maze_height = len(maze_arr)
maze_width = len(maze_arr[0])
pixel_height = GAME_HEIGHT / maze_height
pixel_width = GAME_WIDTH / maze_width

# Object
obj_width = 18
obj_height = 18
pacman_orig = pygame.image.load('img/pacman.png')
pacman_orig = pygame.transform.scale(pacman_orig, (obj_width, obj_height))
pacman_right = pygame.transform.rotate(pacman_orig, 0)
pacman_left = pygame.transform.rotate(pacman_orig, 180)
pacman_up = pygame.transform.rotate(pacman_orig, 90)
pacman_down = pygame.transform.rotate(pacman_orig, 270)
obj_x = 1
obj_y = 1
score = 0

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
pacman = pacman_orig

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
    elif maze_arr[obj_y+change_y][obj_x+change_x] == '@':
        maze_arr[obj_y+change_y][obj_x+change_x] = ' '
        score += 1
        if score == target_score:
            keepGoing = False

    if change_x == 1: #right
        pacman = pacman_right
    elif change_x == -1: #left
        pacman = pacman_left
    elif change_y == -1: #up
        pacman = pacman_up
    elif change_y == 1: #down
        pacman = pacman_down

    obj_x += change_x
    obj_y += change_y
    

    #Draw maze
    gameDisplay.fill(BLACK)
    lead_x = 0
    lead_y = 0
    for row in maze_arr:
        for col in row:
            if col == '#':
                pygame.draw.rect(gameDisplay, BLUE, (lead_x, top_offset+lead_y, pixel_width, pixel_height))
            elif col == '@':
                pygame.draw.circle(gameDisplay, WHITE, (int(lead_x + pixel_width/2), int(top_offset + lead_y + pixel_height/2)), 3, 0)
            lead_x += pixel_width
        lead_y += pixel_height
        lead_x = 0

    gameDisplay.blit(pacman, (obj_x*pixel_width+1,top_offset+obj_y*pixel_height+1))
    #pygame.draw.rect(gameDisplay, RED, (obj_x*pixel_width+5, top_offset+obj_y*pixel_height+5, 10, 10)) #top left coords, width, height
    score_text = myfont.render('score: '+ str(score), True, WHITE)
    gameDisplay.blit(score_text,(WINDOW_WIDTH/30, top_offset/5))
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit() 