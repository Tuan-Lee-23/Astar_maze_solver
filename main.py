import numpy as np
import sys
import graphic as gp

class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent # Node
        self.position = position # list

        self.g = 0  # Distance from starting point (from parent)
        self.h = 0  # Distance from end point
        self.f = 0  # Sum: g + h


# Create test maze
# testMaze = [[1, 0, 0, 0, 0],
#             [1, 1, 1, 1, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0]]

# testMaze = [[0, 0, 0, 0, 0, 0],
#             [1, 1, 1, 1, 1, 1],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0]]


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



# TODO: calculate distance from starting node
# @input: start_pos (list), goal_pos (list)
def euclidean_distance(start_pos: list, goal_pos: list):
    goal_posX = goal_pos[1]
    goal_posY = goal_pos[0]

    start_posX = start_pos[1]
    start_posY = start_pos[0]

    distance = np.sqrt((goal_posX - start_posX)**2 + (goal_posY - start_posY) ** 2)

    return distance

# TODO: get adjacent nodes from current node
# @input: current (Node), maze_shape (list)
#         current: current node,    maze: shape of maze (m, n)

# Get neighbor of current node
def get_adjacent_indices(current, maze_shape):
    m, n = maze_shape[0], maze_shape[1]
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


# TODO: use A* algorithm to find optimal path in maze
# @input: maze (numpy array), start (list), goal (list)
# @output:
    # if goal is reached:    return [path (list), traversed (list)]
    #                       path: optimal path to finish a maze
    #                       traversed: all of nodes have opened

    # if can't reach the goal position:     return [[-1], traversed]
    #                       traversed: all of nodes have opened

def AStar_pathfinding(maze, start, goal):
    # initialize both open and closed list
    open_set = [] # set of nodes to be evaluated


    traversed = [] # set of nodes already evaluated and visited (position)

    obstacle = make_obstacles_list(maze)

    # Create start node and goal node
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
        # print("Smallest node: ", smallest.position)

        current = smallest
        # print("Current: ", current.position, "------------------------------------")


        # Add current node to traversed
        traversed.append(current.position)

        # print("Traversed: ", traversed)


        # remove current node from open_set
        open_set.remove(current)



        # if Current is the goal position
        if current.position == goal.position:

            print("\n\nTraversed: ")
            print(traversed)
            path = []

            notDone = 0
            while current is not None:
                par = current.parent
                if par != None and current.position[0] != par.position[0] and current.position[1] != par.position[1]:
                    notDone = 1
                    break
                path.append(current.position)
                current = par
            # print(path[::-1])
            # print("done")
            # print("Traversed: ", [x for x in traversed])
            if notDone != 1:
                return [path[::-1], traversed]

        # Generate children of current node
        children = get_adjacent_indices(current.position, maze.shape)
        # print("Children: ", children)

        children_nodes = [Node(current, child) for child in children]

        for child in children_nodes:
            print("Child: ", child.position, "---------------------")

            # TODO: continue if Child is on the traversed
            if child.position in obstacle or child.position in traversed:
                continue
            if child.position[0] != current.position[0] and child.position[1] != current.position[1]:
                continue

            # TODO: Create f, g, h values

            # Distance from child to current
            child.g = current.g + euclidean_distance(child.position, current.position)
            print("g: ", child.g)


            # TODO Distance from child to end
            child.h = euclidean_distance(child.position, goal.position)
            print("h: ", child.h)

            child.f = child.g + child.h

            print("f: ", child.f)


            open_node_positions = [x.position for x in open_set]
            open_node_g = [x.g for x in open_set]

            flag = 0
            for x in open_set:
                if child.g > x.g:
                    flag = 1
                    continue
                elif child.g < x.g:
                    adjacent_neighbor = get_adjacent_indices(child.position, maze.shape)
                    if x.position in adjacent_neighbor:
                        x.g = child.g + euclidean_distance(x.position, child.position)
                        x.f = x.g + x.h

            # If child not in open set
            if child.position in open_node_positions and flag == 1:
                continue



            # Add the child to the open_set
            open_set.append(child)
            print("append ", child.position)
            print("Now: ", [x.position for x in open_set], end = '\n\n\n\n')

    # Reach here when open list is emtpy --> can't find path
    return [[-1], traversed]


# TODO: draw maze as text with optimal path
# @input: maze (list), start: start position, goal: goal position
# if solver can reach goal position
#       @output: maze (numpy array), path (list)
#                                    path: optimal solution path
# if solver can't reach goal
#       @output: ['-1'] (list)
def draw_optimal_path(maze, start, goal):

    # convert maze into numpy array
    maze = np.array(maze)
    # maze_solver
    maze_solver = AStar_pathfinding(maze, start, goal)

    # Get optimal path
    path = maze_solver[0]
    print("did solve", maze_solver)
    # Get traversed
    traversed = maze_solver[1]
    # if solver can't reach goal position
    if path[0] == -1:
        print("Solver can't find path")
        return ['-1']

    # solver can reach the goal
    else:

        # convert maze into string
        maze = maze.astype('str')

        # print("path: ", path)
        # print("traversed: ", traversed)

        # Add obstacle as "o"
        maze[maze == "1"] = "o"

        # Add free cells as "-"
        maze[maze == "0"] = "-"
        print("\n\nSymbolize maze: \n")

        maze[start[0], start[1]] = "S"
        maze[goal[0], goal[1]] = "G"

        print(maze)

        print("\n\nOptimal path ----------- ")
        for cell in path[1:-1]:
            x = cell[0]
            y = cell[1]
            maze[x, y] = "X"

        # final maze
        print(maze)

        return [maze, path, traversed]


# TODO: read maze file and return matrix
# If file not found, exit and throw error
# @input: file dir
# @output: [maze, start, goal]
#           maze: map in matrix (numpy array)
#           start: start position (list)
#           end: end position (list)

def read_input_file(dir: str):

    try:
        with open(dir, 'r') as f:
            lines = f.readlines()

            maze = np.array([[]])

            for i, line in enumerate(lines):

                if i == 0:
                    maze_shape = line.strip()
                    maze_shape = maze_shape.split()
                    maze_shape = [int(maze_shape[0]), int(maze_shape[1])]

                elif i == 1:
                    start = line.strip()
                    start = start.split()
                    start = [int(start[0]), int(start[1])]

                elif i == 2:
                    goal = line.strip()
                    goal = goal.split()
                    goal = [int(goal[0]), int(goal[1])]

                else:
                    row = line.strip()
                    row = row.split()
                    row = np.array(row).astype('int')
                    maze = np.append(maze, row)

            maze = maze.reshape(maze_shape)
            maze = maze.astype('int')

            print("Shape: ", maze_shape)
            print("Start: ", start)
            print("Goal: ", goal)

            print("Input maze: ")

            print(maze)

            return [maze, start, goal]
    except FileNotFoundError:
        print("File not found:", dir, "\nplease fix your directory")
        sys.exit(1)


# TODO: receive maze and make output file
# @input: dir: string, maze (list), start (list), goal (list)
# @output: a text file
def make_output (dir, maze, start, goal):
    with open(dir, 'w') as f:
        result = draw_optimal_path(maze, start, goal)

        # If optimal path is not found
        if result == ['-1']:
            f.write('-1')
            f.close()

            return

        # Found
        else:

            num_of_steps = len(result[1])
            path = result[1]
            maze = result[0]

            # Convert path into tuple to export as string
            path = tuple(map(tuple,path))

            path_result = ""
            for x in path:
                path_result += str(x) + "  "

            # Convert maze numpy array to export as string
            temp = [" ".join(item) for item in maze.astype(str)]

            maze_map = ""
            for x in temp:
                maze_map += x + "\n"


            f.write(str(num_of_steps) + "\n")
            f.write((path_result) + "\n")
            f.write(maze_map)

            f.close()
        return result[1], result[-1]


# def main():

#     input_data = read_input_file('input.txt')



#     # Maze
#     maze = input_data[0]
#     start = input_data[1]
#     goal = input_data[2]


#     make_output('output.txt', maze, start, goal)


def main():

    arguments = sys.argv

    input_file = '/Users/macintoshhd/HOCDIIIII/AIProject1/big_maze.txt'#arguments[1]
    output_file = '/Users/macintoshhd/HOCDIIIII/AIProject1/res.txt'#arguments[2]

    input_data = read_input_file(input_file)

    # Get maze and start, goal position
    maze = input_data[0]
    start = input_data[1]
    goal = input_data[2]

    optimalPath, openPath = make_output(output_file, maze, start, goal)
    if len(optimalPath) != 0:
        gp.addStart(start)
        gp.addGoal(goal)
        gp.addMap(maze)
        gp.addOpenPath(openPath)
        gp.addOptimalPath(optimalPath)
        gp.main()

    # showUI(output_file)



if __name__ == '__main__':
    main()






