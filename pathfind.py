from collections import namedtuple, defaultdict

Move = namedtuple('Move', 'dest, cost')

# Graph represented by adjacency list
class Graph():
    def __init__(self):
        self.adj_list = defaultdict(list)  #dictionary w/ key=node, value=list of namedtuples (destination, cost)
    def add_edge(self, src, dest, cost):
        forward_node = Move(dest, cost)
        self.adj_list[src].insert(0, forward_node)
        backward_node = Move(src, cost)
        self.adj_list[dest].insert(0, backward_node)
    def print_graph(self):
        print (self.adj_list)


Coord = namedtuple('Coord', 'x, y')

def is_edge(maze_arr, down, right):
    if maze_arr[down][right] == '#':
        return False
    if maze_arr[down][right-1] and maze_arr[down][right+1] == '#':
        return False
    if maze_arr[down-1][right] and maze_arr[down+1][right] == '#':
        return False
    return True

def maze_to_graph(maze_arr):
    #Detect vertices, create array of nodes
    node_list = []
    height = len(maze_arr)
    width = len(maze_arr[0])
    for down in range(0,height):
        for right in range(0,width):
            if is_edge(maze_arr, down, right):
                new_node = Coord(right, down)
                node_list.append(new_node)
    graph = Graph()
    #For each node, detect edges and add to graph
    for node in node_list:
        #print(node)
        dist = 1 #UP
        while(True):
            if maze_arr[node.y-dist][node.x] == '#':
                break
            if is_edge(maze_arr, node.y-dist, node.x):
                dest = Coord(node.x, node.y-dist)
                graph.add_edge(node, dest, dist) #src, dest, cost
            dist += 1
        dist = 1    #DOWN
        while(True):
            if maze_arr[node.y+dist][node.x] == '#':
                break
            if is_edge(maze_arr, node.y+dist, node.x):
                dest = Coord(node.x, node.y+dist)
                graph.add_edge(node, dest, dist) #src, dest, cost
            dist += 1
        dist = 1    #LEFT
        while(True):
            if maze_arr[node.y][node.x-dist] == '#':
                break
            if is_edge(maze_arr, node.y, node.x-dist):
                dest = Coord(node.x-dist, node.y)
                graph.add_edge(node, dest, dist) #src, dest, cost
            dist += 1
        dist = 1    #RIGHT
        while(True):
            if maze_arr[node.y][node.x+dist] == '#':
                break
            if is_edge(maze_arr, node.y, node.x+dist):
                dest = Coord(node.x+dist, node.y)
                graph.add_edge(node, dest, dist) #src, dest, cost
            dist += 1
    return graph


# Read in Maze
maze_arr = []
with open('mazes/maze_01.txt', 'r') as maze:
    m = maze.readlines()
    for i in m:
        line = list(i.rstrip())
        maze_arr.append(line)
graph = maze_to_graph(maze_arr)
graph.print_graph()
