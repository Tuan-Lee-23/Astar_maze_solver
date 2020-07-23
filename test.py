import numpy as np



class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent # Node
        self.position = position # list

        self.g = 0
        self.h = 0
        self.f = 0

# Create test maze
testMaze = [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]


testMaze = np.array(testMaze)

start_pos = [3, 3]
goal_pos = [0, 1]

testMaze[start_pos[0], start_pos[1]] = -5
testMaze[goal_pos[0], goal_pos[1]] = 5

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

print(euclidean_distance(start_pos, goal_pos))



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

    start = Node(None, start)
    goal = Node(None, goal)

    traversed_node = []

    open_set.append(start)



    # Frontier structure:  [[positionX, positionY], f_cost]

    # test set
    target = [[3, 3], 0]
    test = [[[1, 1], 30], [[0, 1], 10], [[1, 0], 10]]
    open_set = test
    #test set

    # Find node in open_set with lowest f_cost
    smallest = open_set[0][1]
    indexes = 0
    for x in test:
        if x[1] < smallest:
            smallest = x[1]
            indexes = test.index(x)

    # current = node in open_set with the loest f_cost
    current = test[indexes]

    # remove current from open_set
    open_set.remove(current)

    # add current to close_set
    close_set.append(current)

    # if current is the target node
    if current[0] == target:
        return
    
    print('current: ', current)

    neighbors =  get_adjacent_indices(current[0], [4, 4])
    # print(neighbors)


AStar_pathfinding(testMaze, start_pos, goal_pos)


print(get_adjacent_indices([1, 1,], [4, 4]))







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