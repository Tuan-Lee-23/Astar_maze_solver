import numpy as np

class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent # Node
        self.position = position # list

        self.g = 0  # Distance from starting point (from parent)
        self.h = 0  # Distance from end point
        self.f = 0  # Sum: g + h



# Create test maze
testMaze = [[1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]]

testMaze = [[1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]       


# testMaze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] 


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
    # initialize both open and closed list
    open_set = [] # set of nodes to be evaluated
    close_set = [] # set of nodes already evaluated

    traversed = []

    obstacle = make_obstacles_list(maze)

    start = Node(None, start)
    start.f = 0
    goal = Node(None, goal)
    

    open_set.append(start)


    # Loop until fidn the end
    while len(open_set) > 0:


        # Get the current node and let it equal the node with smallest f value
        smallest = open_set[0]
        for node in open_set:
            if node.f < smallest.f:
                smallest = node
        
        print("\n\nOpen set: ", [x.position for x in open_set])
        print("Smallest node: ", smallest.position)

        current = smallest
        print("Current: ", current.position, "------------------------------------")

        # test if current has been in traversed
        if current.position in traversed:
            print("Current: ", current.position, " in traversed")
            open_set.remove(current)
            continue
        # test
        else:
            traversed.append(current.position)
        #test 
        print("Traversed: ", traversed)


        # remove current node from open_set
        open_set.remove(current)



        # if Current is the goal position
        if current.position == goal.position:
            path = []
            
            while current is not None:
                path.append(current.position)
                current = current.parent
            print(path[::-1])
            print("done")

            return
        
        # Generate children of current node
        children = get_adjacent_indices(current.position, maze.shape)
        # print("Children: ", children)

        children_nodes = [Node(current, child) for child in children]

        for child in children_nodes:
            print("Child: ", child.position, "---------------------")

            # Child is on the traversed
            if child.position in obstacle or child.position in traversed:
                continue
            
            # if child not in open_set:
            #     # open_set.append(child)
            #     child.parent = current

            # Create f, g, h values
            # Distance from child to current
            child.g = current.g + euclidean_distance(child.position, current.position)
            print("g: ", child.g)

            # test
            # child.g = child.parent.g + 1
            # print("g : ", child.g)
            # test

            # Distance from child to end
            child.h = euclidean_distance(child.position, goal.position)
            print("h: ", child.h)
            child.f = child.g + child.h

            print("f: ", child.f)

            # Child is already in open_set
            print("All open node")

            open_node_positions = [x.position for x in open_set]
            open_node_g = [x.g for x in open_set]
            
            flag = 0
            for x in open_node_g:
                if child.g > x:
                    flag = 1
                    continue

                        
            if child.position in open_node_positions and flag == 1:
                continue
                
                

            # Add the child to the open_set
            open_set.append(child)
            print("append ", child.position)
            print("Now: ", [x.position for x in open_set], end = '\n\n\n\n')



        
        



AStar_pathfinding(testMaze, [3, 4], [0, 1])
# AStar_pathfinding(testMaze, [0, 0], [9, 9])
