import numpy as np



class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent # Node
        self.position = position # list

        self.g = 0  # Distance from starting point (from parent)
        self.h = 0  # Distance from end point
        self.f = 0  # Sum: g + h


    def update_distance(self, start, end):
        self.h = euclidean_distance(self.position, end.position)

        # If parent's node is not None
        if self.parent != None:
            # print("parent: ", self.parent.position)
            dist_with_parent = euclidean_distance(self.position, self.parent.position)

            if self.g > self.parent.g + dist_with_parent:
                self.g = self.parent.g + dist_with_parent
            else:
                self.g = dist_with_parent

                # test
                dist = 0
                temp = self 
                print("BINGINBINGING")
                while temp.parent is not None:
                    print(temp.position, ': ', temp.g)
                    dist = dist + temp.g
                    temp = temp.parent
                print("Total g: ", dist)
                self.g = dist
                # test

        # If parent's node is None
        else:
            self.g = euclidean_distance(self.position, start.position)

        # g += parent.g recursively
        self.f = self.g + self.h
        print("h(x) = ", self.position, ": ", self.h)
        print("g(x) = ", self.position, ": ", self.g)
        print("f(x) = ", self.f, end = '\n\n\n')



# Create test maze
testMaze = [[1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
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
        adjacent_indices.append([i - 1, j - 1])

    # Up
    if i > 0:
        adjacent_indices.append([i-1,j])
    
    # up right
    if i > 0 and j + 1 < n:
        adjacent_indices.append([i - 1, j + 1])

    # right
    if j + 1 < n:
        adjacent_indices.append([i,j+1])
    
    # down right
    if j + 1 < n and i + 1 < m:
        adjacent_indices.append([i + 1, j + 1])
    
    # down
    if i + 1 < m:
        adjacent_indices.append([i+1,j])

    # down left
    if j > 0 and i + 1 < m:
        adjacent_indices.append([i + 1, j - 1])

    # left
    if j > 0:
        adjacent_indices.append([i,j-1])

    return adjacent_indices

def make_obstacles_list(maze):
    result = np.where(maze == 1)

    return list(map(list, zip(result[0], result[1])))
    


def AStar_pathfinding(maze, start, goal):
    open_set = [] # set of nodes to be evaluated
    close_set = [] # set of nodes already evaluated

    traversed = []

    obstacle = make_obstacles_list(maze)

    start = Node(None, start)
    goal = Node(None, goal)


    open_set.append(start)

    while True:

        # Get current = node in open with lowest f cost
        smallest_node = open_set[0]
        print("starting: ", open_set[0].position)
        # print("open now: ", [x.position for x in open_set])
        for node in open_set:
            # test
            print(node.position, ": ", node.f, " < ", smallest_node.f)
            # test
            if node.f < smallest_node.f and node.position not in obstacle:
                smallest_node = node
                print("smallest now: ", smallest_node.f)
        print("SMallest node: -----------", smallest_node.position)

        current = smallest_node


        traversed.append(current.position)
        try:
            open_set.remove(current)
        except ValueError:
            pass


        # Update f cost of current
        current.update_distance(start, goal)
        close_set.append(current)

        # If current is goal return
        if current.position == goal.position:
            print("open set: ")
            [print(x.position) for x in open_set]
            print("\n\n\n")
            print("close set: ")
            [print(x.position) for x in close_set]
            return [open_set, close_set]
        

        # Get neighbors of current
        indices = current.position
        neighbors = get_adjacent_indices(indices, maze.shape)
        
        #test
        neighbors = [x for x in neighbors if x not in obstacle]
        #test 
        print("Obstacle: ", obstacle)
        print("Neighbor hop le: ", neighbors)
        #test

        neighbors_nodes = [Node(current, neighbor) for neighbor in neighbors]
        
        print("Open: ", [x.position for x in open_set])

        # Update distance of neighbor
        for neighbor in neighbors_nodes:
            neighbor.parent = current
            print("Current: ", current.position)
            print("Neighbor: ", neighbor.position)
            neighbor.update_distance(start, goal)

        for neighbor in neighbors_nodes:
            # remove neighbor which is an obstacle
            if neighbor.position in obstacle or neighbor in close_set or neighbor.position in traversed:
                print("ping")
                continue
            
            open_set_position = [x.position for x in open_set]
            if neighbor.position not in open_set_position:
                print(neighbor.position, " not in ", [x.position for x in open_set])
                #test
                #test
                print("adding neighbor", neighbor.position)
                current = neighbor.parent


                open_set.append(neighbor)
                print("open list now: ", [x.position for x in open_set], end = "\n\n")

    

start_pos = [3, 4]
goal_pos = [0, 1]

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