from collections import namedtuple, defaultdict
import random

Coord = namedtuple('Coord', 'x, y')
Move = namedtuple('Move', 'dest, cost')

#Min heap
class MinHeap():
    def __init__(self):
        self.arr = []
    def add_node(self, coordinate, cost):
        new_node = [coordinate, cost]
        self.arr.append(new_node)
    def swap(self, first, second):
        temp = self.arr[first]
        self.arr[first] = self.arr[second]
        self.arr[second] = temp
    def heapify(self, i):
        size = len(self.arr)
        smallest_index = i
        left_child = 2*i+1
        right_child = 2*i+2
        if left_child < size and self.arr[left_child][1] < self.arr[smallest_index][1]:
            smallest_index = left_child
        if right_child < size and self.arr[right_child][1] < self.arr[smallest_index][1]:
            smallest_index = right_child
        if smallest_index != i:
            self.swap(smallest_index, i)
            self.heapify(smallest_index)
    def build_heap(self):
        start = len(self.arr)//2-1
        i = start
        while(i >= 0):
            self.heapify(i)
            i -= 1
    def extract_min(self):
        if self.is_empty():
            return
        min_node = self.arr[0]
        self.arr.pop(0)
        self.heapify(0)
        return min_node
    def is_present(self, node):
        for i in self.arr:
            if i[0] == node:
                return i
        return False
    def change_cost(self, node, new_cost):
        for i in range(0, len(self.arr)):
            if self.arr[i][0] == node:
                self.arr[i][1] = new_cost
    def is_empty(self):
        if len(self.arr) is 0:
            return True
        return False
    def print_heap(self):
        for i in self.arr:
            print (i)

# Graph represented by adjacency list
class Graph():
    def __init__(self):
        self.adj_list = defaultdict(set)  #dictionary w/ key=node, value=set of namedtuples (destination, cost)
    def return_node_list(self):
        ret = []
        for key in self.adj_list.keys():
            ret.append(key)
        return ret
    def add_edge(self, src, dest, cost):
        forward_node = Move(dest, cost)
        self.adj_list[src].add(forward_node)
        backward_node = Move(src, cost)
        self.adj_list[dest].add(backward_node)
    def remove_edge(self, node):
        for move in self.adj_list[node]:
            for edge in self.adj_list[move.dest]:
                if edge.dest == node:
                    self.adj_list[move.dest].remove(edge)
                    break
        del self.adj_list[node]
    def print_graph(self):
        # print('graph length:', len(self.adj_list))
        for key, value in self.adj_list.items():
            print(key)
            for i in value:
                print(i)
    def dijkstra(self, start, dest):
        # if start.x == dest.x or start.y == dest.y:
        #     return [dest]
        visited = {}
        best_paths = {}
        heap = MinHeap()
        for node in self.adj_list.keys():
            best_paths[node] = []
            if start == node:
                heap.add_node(node, 0)
            else:
                heap.add_node(node, 10000)
        heap.build_heap()
        while heap.is_empty() == False:
            curr = heap.extract_min()
            curr_node = curr[0]
            curr_cost = curr[1]
            for move in self.adj_list[curr_node]:
                heap_node = heap.is_present(move.dest)
                if heap_node == False:
                    continue
                new_cost = curr_cost + move.cost
                if new_cost < heap_node[1]:
                    heap.change_cost(move.dest, new_cost)
                    best_paths[move.dest] = best_paths[curr_node].copy()
                    best_paths[move.dest].append(move.dest)
            visited[curr_node] = curr_cost
            heap.build_heap()
        return best_paths[dest]


# Graph creation from Maze
def is_edge(maze_arr, down, right):
    if maze_arr[down][right] == '#' or maze_arr[down][right-1] == '#' and maze_arr[down][right+1] == '#' or maze_arr[down-1][right] == '#' and maze_arr[down+1][right] == '#':
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
        dist = 1 #UP
        while(True):
            if maze_arr[node.y-dist][node.x] == '#':
                break
            if is_edge(maze_arr, node.y-dist, node.x):
                dest = Coord(node.x, node.y-dist)
                graph.add_edge(node, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #DOWN
        while(True):
            if maze_arr[node.y+dist][node.x] == '#':
                break
            if is_edge(maze_arr, node.y+dist, node.x):
                dest = Coord(node.x, node.y+dist)
                graph.add_edge(node, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #LEFT
        while(True):
            if maze_arr[node.y][node.x-dist] == '#':
                break
            if is_edge(maze_arr, node.y, node.x-dist):
                dest = Coord(node.x-dist, node.y)
                graph.add_edge(node, dest, dist) #src, dest, cost
                break
            dist += 1
        dist = 1    #RIGHT
        while(True):
            if maze_arr[node.y][node.x+dist] == '#':
                break
            if is_edge(maze_arr, node.y, node.x+dist):
                dest = Coord(node.x+dist, node.y)
                graph.add_edge(node, dest, dist) #src, dest, cost
                break
            dist += 1
    return graph


#TESTING PURPOSES
if __name__ == '__main__':
    maze_arr = []
    with open('mazes/maze_01.txt', 'r') as maze:
        m = maze.readlines()
        for i in m:
            line = list(i.rstrip())
            maze_arr.append(line)
    graph = maze_to_graph(maze_arr)

    #TESTING DIJKSTRA
    node_list = graph.return_node_list()
    #print('node list:', node_list)
    start = Coord(5,6)
    end = Coord(1,1)
    if start not in node_list:
        print('NOT IN -> SHOULD ADD')
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
    node_list = graph.return_node_list()
    #print('after list:', node_list)
    if start in node_list:
        print('IT IS IN IT')
    else:
        print('NOT IN')
    path = graph.dijkstra(start, end)
    print(path)