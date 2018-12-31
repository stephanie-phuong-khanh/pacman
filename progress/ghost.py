import pygame
from collections import namedtuple, defaultdict
from pathfind import MinHeap, Graph, is_edge, maze_to_graph

Coord = namedtuple('Coord', 'x, y')
Move = namedtuple('Move', 'dest, cost')

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
BLUE = (5,21,104)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
GAME_WIDTH = 500
GAME_HEIGHT = 500
top_offset = (WINDOW_HEIGHT - GAME_HEIGHT) / 2
gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('ghost')

# Maze
maze_arr = []
with open('mazes/maze_01.txt', 'r') as maze:
    m = maze.readlines()
    for i in m:
        line = list(i.rstrip())
        maze_arr.append(line)

maze_height = len(maze_arr)
maze_width = len(maze_arr[0])
pixel_height = GAME_HEIGHT / maze_height
pixel_width = GAME_WIDTH / maze_width

# Object
ghost_width = 18
ghost_height = 18
ghost_x = 1
ghost_y = 1
change_x = 0
change_y = 0

keepGoing = True
clock = pygame.time.Clock()

graph = maze_to_graph(maze_arr)
start = Coord(ghost_x,ghost_y)
end = Coord(23,23)
path = graph.dijkstra(start, end)
for move in path:
    print(move.dest)
target_index = 0

while keepGoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False

    ghost_change_x = 0
    ghost_change_y = 0

    target_x = path[target_index].dest.x
    target_y = path[target_index].dest.y
    if target_x > ghost_x:
        ghost_change_x = 1
    elif target_x < ghost_x:
        ghost_change_x = -1
    elif target_y > ghost_y:
        ghost_change_y = 1
    elif target_y < ghost_y:
        ghost_change_y = -1
    
    ghost_x += ghost_change_x
    ghost_y += ghost_change_y
    
    if target_x == ghost_x and target_y == ghost_y:
        target_index += 1
    if ghost_x == obj_x and ghost_y == obj_y:
        keepGoing = False

    #Draw maze
    gameDisplay.fill(BLACK)
    lead_x = 0
    lead_y = 0
    for row in maze_arr:
        for col in row:
            if col == '#':
                pygame.draw.rect(gameDisplay, BLUE, (lead_x, top_offset+lead_y, pixel_width, pixel_height))
            # elif col == '@':
            #     pygame.draw.circle(gameDisplay, WHITE, (int(lead_x + pixel_width/2), int(top_offset + lead_y + pixel_height/2)), 3, 0)
            lead_x += pixel_width
        lead_y += pixel_height
        lead_x = 0

    pygame.draw.rect(gameDisplay, RED, (ghost_x*pixel_width+5, top_offset+ghost_y*pixel_height+5, 10, 10))
    #gameDisplay.blit(pacman, (obj_x*pixel_width+1,top_offset+obj_y*pixel_height+1))
    pygame.display.update()
    clock.tick(5)

pygame.quit()
quit() 


# if __name__ == '__main__':
#     maze_arr = []
#     with open('mazes/maze_01.txt', 'r') as maze:
#         m = maze.readlines()
#         for i in m:
#             line = list(i.rstrip())
#             maze_arr.append(line)
#     graph = maze_to_graph(maze_arr)
#     # graph.print_graph()

#     #TESTING REMOVAL
#     # to_remove = Coord(23,23) 
#     # graph.remove_edge(to_remove)
#     # graph.print_graph()

#     #TESTING DIJKSTRA
#     start = Coord(1,1)
#     end = Coord(23,23)
#     path = graph.dijkstra(start, end)
#     for move in path:
#         print(move.dest)