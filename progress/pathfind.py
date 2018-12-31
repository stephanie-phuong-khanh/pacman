from collections import namedtuple, defaultdict

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
    def heapify(self, original, size):
        index = original
        while (index < size):
            left_child = 2*index
            right_child = left_child + 1
            if left_child < size and self.arr[left_child][1] < self.arr[index][1]:
                index = left_child
            if right_child < size and self.arr[right_child][1] < self.arr[index][1]:
                index = right_child
            if index == original:
                return
            self.swap(original, index)
            original = index
    def build_heap(self):
        size = len(self.arr)
        i = int(size / 2 - 1)
        while (i >= 0):
            self.heapify(i, size)
            i -= 1
    def extract_min(self):
        if self.is_empty():
            return
        min_node = self.arr[0]
        self.arr.pop(0)
        self.heapify(0,len(self.arr))
        return min_node
    def heap_sort(self):
        self.build_heap()
        last = len(self.arr) - 1
        while (last > 0):
            print(self.arr[0])
            self.swap(0, last)
            self.heapify(0, last)
            last -= 1
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
        print('graph length:', len(self.adj_list))
        # for key, value in self.adj_list.items():
        #     print(key)
        #     for i in value:
        #         print(i)
        #     print('\n')
    def dijkstra(self, start, dest):
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

if __name__ == '__main__':
    maze_arr = []
    with open('mazes/maze_01.txt', 'r') as maze:
        m = maze.readlines()
        for i in m:
            line = list(i.rstrip())
            maze_arr.append(line)
    graph = maze_to_graph(maze_arr)
    # graph.print_graph()

    #TESTING REMOVAL
    # to_remove = Coord(23,23)
    # graph.remove_edge(to_remove)
    # graph.print_graph()

    #TESTING DIJKSTRA
    start = Coord(1,1)
    end = Coord(1,5)
    path = graph.dijkstra(start, end)
    for move in path:
        print(move)
