import pygame
from collections import namedtuple, defaultdict
from pathfind import MinHeap, Graph, is_edge, maze_to_graph

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
MAZE_ARR = []
with open('mazes/maze_01.txt', 'r') as maze:
    m = maze.readlines()
    for i in m:
        line = list(i.rstrip())
        MAZE_ARR.append(line)

maze_height = len(MAZE_ARR)
maze_width = len(MAZE_ARR[0])
pixel_height = GAME_HEIGHT / maze_height
pixel_width = GAME_WIDTH / maze_width

target_score = sum(row.count('@') for row in MAZE_ARR)
MAZE_NODE_LIST = maze_to_graph(MAZE_ARR).return_node_list()

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

#Ghosts
class Ghost():
    def __init__(self, start_x, start_y):
        global obj_x
        global obj_y
        self.x = start_x
        self.y = start_y
        self.graph = maze_to_graph(MAZE_ARR)
        start = Coord(self.x, self.y)
        end = Coord(obj_x, obj_y)
        self.path = self.graph.dijkstra(start, end)
        self.target_index = 0
    def move(self):
        target_x = self.path[self.target_index].x
        target_y = self.path[self.target_index].y
        # [ghost_change_x, ghost_change_y]
        if target_x > self.x:
            self.x += 1
        elif target_x < self.x:
            self.x -= 1
        elif target_y > self.y:
            self.y += 1
        elif target_y < self.y:
            self.y -= 1
        if target_x == self.x and target_y == self.y:
            self.target_index += 1
        if self.target_index == len(self.path):
            self.recalculate()
        return [self.x, self.y]
    def recalculate(self):
        global obj_x
        global obj_y
        self.target_index = 0
        start = Coord(self.x, self.y)
        end = Coord(obj_x, obj_y)
        if start not in MAZE_NODE_LIST:
            dist = 1 #UP
            while(True):
                if MAZE_ARR[start.y-dist][start.x] == '#':
                    break
                if is_edge(MAZE_ARR, start.y-dist, start.x):
                    dest = Coord(start.x, start.y-dist)
                    self.graph.add_edge(start, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #DOWN
            while(True):
                if MAZE_ARR[start.y+dist][start.x] == '#':
                    break
                if is_edge(MAZE_ARR, start.y+dist, start.x):
                    dest = Coord(start.x, start.y+dist)
                    self.graph.add_edge(start, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #LEFT
            while(True):
                if MAZE_ARR[start.y][start.x-dist] == '#':
                    break
                if is_edge(MAZE_ARR, start.y, start.x-dist):
                    dest = Coord(start.x-dist, start.y)
                    self.graph.add_edge(start, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #RIGHT
            while(True):
                if MAZE_ARR[start.y][start.x+dist] == '#':
                    break
                if is_edge(MAZE_ARR, start.y, start.x+dist):
                    dest = Coord(start.x+dist, start.y)
                    self.graph.add_edge(start, dest, dist) #src, dest, cost
                    break
                dist += 1
        if end not in MAZE_NODE_LIST:
            dist = 1 #UP
            while(True):
                if MAZE_ARR[end.y-dist][end.x] == '#':
                    break
                if is_edge(MAZE_ARR, end.y-dist, end.x):
                    dest = Coord(end.x, end.y-dist)
                    self.graph.add_edge(end, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #DOWN
            while(True):
                if MAZE_ARR[end.y+dist][end.x] == '#':
                    break
                if is_edge(MAZE_ARR, end.y+dist, end.x):
                    dest = Coord(end.x, end.y+dist)
                    self.graph.add_edge(end, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #LEFT
            while(True):
                if MAZE_ARR[end.y][end.x-dist] == '#':
                    break
                if is_edge(MAZE_ARR, end.y, end.x-dist):
                    dest = Coord(end.x-dist, end.y)
                    self.graph.add_edge(end, dest, dist) #src, dest, cost
                    break
                dist += 1
            dist = 1    #RIGHT
            while(True):
                if MAZE_ARR[end.y][end.x+dist] == '#':
                    break
                if is_edge(MAZE_ARR, end.y, end.x+dist):
                    dest = Coord(end.x+dist, end.y)
                    self.graph.add_edge(end, dest, dist) #src, dest, cost
                    break
                dist += 1
        self.path = self.graph.dijkstra(start, end)
        if start not in MAZE_NODE_LIST:
            self.graph.remove_edge(start)
        if end not in MAZE_NODE_LIST:
            self.graph.remove_edge(end)
    def catch(self):
        global obj_x, obj_y
        if self.x == obj_x and self.y == obj_y:
            return True
        return False
    def return_path(self):
        return self.path

ghost_recalculate_counter = 0

red_ghost = Ghost(23, 23) 
red_ghost_obj = pygame.image.load('img/red.png')
red_ghost_obj = pygame.transform.scale(red_ghost_obj, (16, 16))  

yellow_ghost = Ghost(23, 15) 
yellow_ghost_obj = pygame.image.load('img/yellow.png')
yellow_ghost_obj = pygame.transform.scale(yellow_ghost_obj, (16, 16))

blue_ghost = Ghost(23, 1) 
blue_ghost_obj = pygame.image.load('img/blue.png')
blue_ghost_obj = pygame.transform.scale(blue_ghost_obj, (16, 16)) 

pink_ghost = Ghost(1, 23) 
pink_ghost_obj = pygame.image.load('img/pink.png')
pink_ghost_obj = pygame.transform.scale(pink_ghost_obj, (16, 16)) 

#Game loop
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
                if MAZE_ARR[obj_y-1][obj_x] != '#':
                    change_x = 0
                    change_y = -1
                    next_move = 0
                else:
                    next_move = MOVE_UP
            elif event.key == pygame.K_DOWN:
                if MAZE_ARR[obj_y+1][obj_x] != '#':
                    change_x = 0
                    change_y = 1
                    next_move = 0
                else:
                    next_move = MOVE_DOWN
            elif event.key == pygame.K_LEFT:
                if MAZE_ARR[obj_y][obj_x-1] != '#':
                    change_x = -1
                    change_y = 0
                    next_move = 0
                else:
                    next_move = MOVE_LEFT
            elif event.key == pygame.K_RIGHT:
                if MAZE_ARR[obj_y][obj_x+1] != '#':
                    change_x = 1
                    change_y = 0
                    next_move = 0
                else:
                    next_move = MOVE_RIGHT

    if red_ghost.catch() or blue_ghost.catch() or yellow_ghost.catch() or pink_ghost.catch():
        print('CAUGHT!')
        gameDisplay.fill(BLACK)
        final_font = pygame.font.SysFont('Comic Sans MS', 50)
        stop_text = final_font.render('GAME OVER...', True, WHITE)
        gameDisplay.blit(stop_text,(0,0))
        pygame.display.update()
        pygame.time.delay(1000)
        keepGoing = False
        continue

    if next_move > 0:
        if next_move == MOVE_UP and MAZE_ARR[obj_y-1][obj_x] != '#':
            change_x = 0
            change_y = -1
        elif next_move == MOVE_DOWN and MAZE_ARR[obj_y+1][obj_x] != '#':
            change_x = 0
            change_y = 1
        elif next_move == MOVE_LEFT and MAZE_ARR[obj_y][obj_x-1] != '#':
            change_x = -1
            change_y = 0
        elif next_move == MOVE_RIGHT and MAZE_ARR[obj_y][obj_x+1] != '#':
            change_x = 1
            change_y = 0
    if MAZE_ARR[obj_y+change_y][obj_x+change_x] == '#':
        change_x = 0
        change_y = 0
    elif MAZE_ARR[obj_y+change_y][obj_x+change_x] == '@':
        MAZE_ARR[obj_y+change_y][obj_x+change_x] = ' '
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
    new_red_pos = red_ghost.move()
    new_yellow_pos = yellow_ghost.move()
    new_blue_pos = blue_ghost.move()
    new_pink_pos = pink_ghost.move()

    ghost_recalculate_counter += 1
    mod = ghost_recalculate_counter % 4
    if mod == 0:
        red_ghost.recalculate()
    elif mod == 1:
        yellow_ghost.recalculate()
    elif mod == 2:
        blue_ghost.recalculate()
    elif mod == 3:
        pink_ghost.recalculate()
    
    #Draw maze
    gameDisplay.fill(BLACK)
    lead_x = 0
    lead_y = 0
    for row in MAZE_ARR:
        for col in row:
            if col == '#':
                pygame.draw.rect(gameDisplay, BLUE, (lead_x, top_offset+lead_y, pixel_width, pixel_height))
            elif col == '@':
                pygame.draw.circle(gameDisplay, WHITE, (int(lead_x + pixel_width/2), int(top_offset + lead_y + pixel_height/2)), 3, 0)
            lead_x += pixel_width
        lead_y += pixel_height
        lead_x = 0

    gameDisplay.blit(pacman, (obj_x*pixel_width+1,top_offset+obj_y*pixel_height+1))
    gameDisplay.blit(red_ghost_obj, (new_red_pos[0]*pixel_width+2, top_offset+new_red_pos[1]*pixel_height+2))
    gameDisplay.blit(yellow_ghost_obj, (new_yellow_pos[0]*pixel_width+2, top_offset+new_yellow_pos[1]*pixel_height+2))
    gameDisplay.blit(blue_ghost_obj, (new_blue_pos[0]*pixel_width+2, top_offset+new_blue_pos[1]*pixel_height+2))
    gameDisplay.blit(pink_ghost_obj, (new_pink_pos[0]*pixel_width+2, top_offset+new_pink_pos[1]*pixel_height+2))
   
    score_text = myfont.render('score: '+ str(score), True, WHITE)
    gameDisplay.blit(score_text,(WINDOW_WIDTH/30, top_offset/5))
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit() 