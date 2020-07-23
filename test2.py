import numpy as np



class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent # Node
        self.position = position # list

        self.f = 0

    def update_distance(self, start, end):
        g = euclidean_distance(self.position, start.position)
        h = euclidean_distance(self.position, end.position)
        self.f = g + h

# Create test maze
testMaze = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


testMaze = np.array(testMaze)


print(testMaze)



# TODO: calculate distance from starting node
# @input: start_pos (list), goal_pos (list)
def euclidean_distance(start_pos: list, goal_pos: list):
    goal_posX = goal_pos[1]
    goal_posY = goal_pos[0]

    start_posX = start_pos[1]
    start_posY = start_pos[0]

    distance = np.sqrt((goal_posX - start_posX)**2 + (goal_posY - start_posY) ** 2)

    return distance




# Get neighbor of current node
def get_adjacent_indices(current, maze):
    m, n = maze[0], maze[1]
    i, j = current[0], current[1]
    adjacent_indices = []

    # up left
    if i > 0 and j > 0:
        adjacent_indices.append((i - 1, j - 1))

    # Up
    if i > 0:
        adjacent_indices.append((i-1,j))
    
    # up right
    if i > 0 and j + 1 < n:
        adjacent_indices.append((i - 1, j + 1))

    # right
    if j + 1 < n:
        adjacent_indices.append((i,j+1))
    
    # down right
    if j + 1 < n and i + 1 < m:
        adjacent_indices.append((i + 1, j + 1))
    
    # down
    if i + 1 < m:
        adjacent_indices.append((i+1,j))

    # down left
    if j > 0 and i + 1 < m:
        adjacent_indices.append((i + 1, j - 1))

    # left
    if j > 0:
        adjacent_indices.append((i,j-1))

    return adjacent_indices


def AStar_pathfinding(maze, start, goal):
    open_set = [] # set of nodes to be evaluated
    close_set = [] # set of nodes already evaluated
    obstacle = []

    start = Node(None, start)
    goal = Node(None, goal)

    traversed_node = []

    open_set.append(start)


    # test
    test1 = Node(None, [0, 0])
    test2 = Node(None, [3, 3])

    start = Node(None, [0, 0])
    goal = Node(None, [3, 3])

    test1.update_distance(start, goal)
    print(test1.f)
    # test

    while True:
        smallest_node = open_set[0]
        for node in open_set:
            if node.f < smallest_node.f:
                smallest_node = node
        
        current = smallest_node
        
        if current.position == goal:
            return 
        
    
    


    

start_pos = [0, 0]
goal_pos = [4, 4]

AStar_pathfinding(testMaze, start_pos, goal_pos)









def printMaze(maze, path=""):
    for x, pos in enumerate(maze[0]):
        if pos == "O":
            start = x

    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1

        elif move == "R":
            i += 1

        elif move == "U":
            j -= 1

        elif move == "D":
            j += 1
        pos.add((j, i))
    
    for j, row in enumerate(maze):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(col + " ", end="")
        print()