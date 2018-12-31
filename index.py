import pygame
from collections import namedtuple, defaultdict
from progress.pathfind import MinHeap, Graph, is_edge, maze_to_graph

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

Coord = namedtuple('Coord', 'x, y')
Move = namedtuple('Move', 'dest, cost')

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

# Pacman
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

# Pacman movement
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3
MOVE_LEFT = 4
next_move = 0
change_x = 0
change_y = 0

# Ghost
ghost_width = 16
ghost_height = 16
ghost = pygame.image.load('img/red.png')
ghost = pygame.transform.scale(ghost, (ghost_width, ghost_height))
ghost_x = 23
ghost_y = 23
ghost_change_x = 0
ghost_change_y = 0

orig_graph = maze_to_graph(maze_arr)
orig_path = orig_graph.return_node_list()
# print('ORIG_PATH:', orig_path)
# print('ORIG_PATH SIZE:', len(orig_path))

ghost_recalculate_counter = 0
graph = maze_to_graph(maze_arr)
start = Coord(ghost_x,ghost_y)
end = Coord(obj_x,obj_y)
path = graph.dijkstra(start, end)
target_index = 0
def ghost_recalculate():
    global start
    global end
    global path
    global graph
    global orig_path
    start = Coord(ghost_x,ghost_y)
    end = Coord(obj_x,obj_y)
    if start not in orig_path:
        dist = 1 #UP
        while(True):
            if maze_arr[start.y-dist][start.x] == '#':
                break
            if is_edge(maze_arr, start.y-dist, start.x):
                dest = Coord(start.x, start.y-dist)
                graph.add_edge(start, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #DOWN
        while(True):
            if maze_arr[start.y+dist][start.x] == '#':
                break
            if is_edge(maze_arr, start.y+dist, start.x):
                dest = Coord(start.x, start.y+dist)
                graph.add_edge(start, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #LEFT
        while(True):
            if maze_arr[start.y][start.x-dist] == '#':
                break
            if is_edge(maze_arr, start.y, start.x-dist):
                dest = Coord(start.x-dist, start.y)
                graph.add_edge(start, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #RIGHT
        while(True):
            if maze_arr[start.y][start.x+dist] == '#':
                break
            if is_edge(maze_arr, start.y, start.x+dist):
                dest = Coord(start.x+dist, start.y)
                graph.add_edge(start, dest, dist) #src, dest, cost
                break
            dist += 1

    if end not in orig_path:
        dist = 1 #UP
        while(True):
            if maze_arr[end.y-dist][end.x] == '#':
                break
            if is_edge(maze_arr, end.y-dist, end.x):
                dest = Coord(end.x, end.y-dist)
                graph.add_edge(end, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #DOWN
        while(True):
            if maze_arr[end.y+dist][end.x] == '#':
                break
            if is_edge(maze_arr, end.y+dist, end.x):
                dest = Coord(end.x, end.y+dist)
                graph.add_edge(end, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #LEFT
        while(True):
            if maze_arr[end.y][end.x-dist] == '#':
                break
            if is_edge(maze_arr, end.y, end.x-dist):
                dest = Coord(end.x-dist, end.y)
                graph.add_edge(end, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #RIGHT
        while(True):
            if maze_arr[end.y][end.x+dist] == '#':
                break
            if is_edge(maze_arr, end.y, end.x+dist):
                dest = Coord(end.x+dist, end.y)
                graph.add_edge(end, dest, dist) #src, dest, cost
                break
            dist += 1
        
    path = graph.dijkstra(start, end)
    if start not in orig_path:
        graph.remove_edge(start)
    if end not in orig_path:
        graph.remove_edge(end)

keepGoing = True
pause = False
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

    if ghost_x == obj_x and ghost_y == obj_y:
        print('CAUGHT!')
        gameDisplay.fill(BLACK)
        final_font = pygame.font.SysFont('Comic Sans MS', 50)
        stop_text = final_font.render('GAME OVER...', True, WHITE)
        gameDisplay.blit(stop_text,(0,0))
        pygame.display.update()
        pygame.time.delay(2000)
        keepGoing = False
        continue

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

    #GHOST MOVEMENT
    target_x = path[target_index].x
    target_y = path[target_index].y
    if target_x > ghost_x:
        ghost_change_x = 1
        ghost_change_y = 0
    elif target_x < ghost_x:
        ghost_change_x = -1
        ghost_change_y = 0
    elif target_y > ghost_y:
        ghost_change_y = 1
        ghost_change_x = 0
    elif target_y < ghost_y:
        ghost_change_y = -1
        ghost_change_x = 0
    
    ghost_x += ghost_change_x
    ghost_y += ghost_change_y

    ghost_recalculate_counter += 1
    if target_x == ghost_x and target_y == ghost_y:
        target_index += 1          
    if target_index == len(path) or ghost_recalculate_counter == 5:
        ghost_recalculate_counter = 0
        ghost_recalculate()
        target_index = 0
    print('path_length:', len(path))
    print('target_index:', target_index, '\n')

    
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
    gameDisplay.blit(ghost, (ghost_x*pixel_width+2,top_offset+ghost_y*pixel_height+2))
    #pygame.draw.rect(gameDisplay, RED, (ghost_x*pixel_width+5, top_offset+ghost_y*pixel_height+5, 10, 10))
    score_text = myfont.render('score: '+ str(score), True, WHITE)
    gameDisplay.blit(score_text,(WINDOW_WIDTH/30, top_offset/5))
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit() 