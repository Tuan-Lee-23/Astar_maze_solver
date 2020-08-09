import pygame
import sys
import threading
import time
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# This sets the WIDTH and HEIGHT of each grid location
SIZE = 20

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][5] = 1

# Initialize pygame

# Loop until the user clicks the close button.
done = False


def read_input_file(dir: str):
    try:
        with open(dir, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if i == 1:
                    # line = line.split(' ')
                    line = line.replace("(", "").replace(")", "").replace(", ", ",").replace("\n","")
                    line = line.split("  ")
                    print(line)
                    pathList = []
                    for item in line:
                        if item is not '':
                            pathList.append([item.split(",")[0], item.split(",")[1]])

                    print(pathList)
                    return line


            return []
    except FileNotFoundError:
        print("File not found:", dir, "\nplease fix your directory")
        sys.exit(1)



# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# output_file = '/Users/macintoshhd/HOCDIIIII/AIProject1/res.txt'  # arguments[2]
#
# input_data = read_input_file(output_file)
#
# # Get maze and start, goal position
# maze = input_data[0]
# start = input_data[1]
# -------- Main Program Loop -----------
array = []
map = []
index = 0
drawArray = []
optimalPath = []
isOptimal = False
optimalPathForDraw = []
openPath = []
start = []
goal = []
speed = 0.15
def addStart(point):
    global start
    start = point
def addGoal(point):
    global goal
    goal = point
def addMap(arr):
    global map
    map = arr

def drawPath(array1):
    array = array1
    index = 0
    def drawL():
        global index
        global isOptimal
        global drawArray
        global optimalPathForDraw
        global speed
        for i in range(len(array)):
            if index <= len(array):
                if isOptimal == True:
                    optimalPathForDraw.append(array[index])
                else:
                    drawArray.append(array[index])
                index = index + 1
                time.sleep(speed)
        if index == len(array) and isOptimal != True:
            index = 0
            isOptimal = True
            drawPath(optimalPath)
            return

    # for i in range(10):
    t = threading.Thread(target=drawL)
    # threads.append(t)
    t.start()

def addOptimalPath(path):
    global optimalPath
    optimalPath = path
def addOpenPath(path):
    global openPath
    openPath = path
dd = 1

def main():
    global dd
    global isOptimal
    global openPath
    global speed
    global SIZE
    global MARGIN
    done = False
    pygame.init()

    w = 1900
    h = 1000

    wz = [len(map[0]) * SIZE + (len(map[0]) + 1 ) * MARGIN, len(map) * SIZE + (len(map) + 1 ) * MARGIN]
    if w < wz[0]:
        SIZE = int((w - (len(map[0]) + 1 ) * MARGIN) / len(map[0]))
        MARGIN = int(SIZE / 4)
        if MARGIN == 0:
            MARGIN = 1
        wz = [len(map[0]) * SIZE + (len(map[0]) + 1) * MARGIN, len(map) * SIZE + (len(map) + 1) * MARGIN]
    if h < wz[1]:
        SIZE = int((h - (len(map) + 1) * MARGIN) / len(map))
        MARGIN = int(SIZE / 4)
        if MARGIN == 0:
            MARGIN = 1
        wz = [len(map[0]) * SIZE + (len(map[0]) + 1) * MARGIN, len(map) * SIZE + (len(map) + 1) * MARGIN]
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = wz
    speed = 1.0/len(map)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()


        # Set the screen background
        screen.fill(BLACK)
        if dd == 1:
            drawPath(openPath)
            dd = 0
        # Draw the grid
        for row in range(len(map)):
            for column in range(len(map[row])):
                if map[row][column] == 0:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + SIZE) * column + MARGIN,
                                  (MARGIN + SIZE) * row + MARGIN,
                                  SIZE,
                                  SIZE])
        for item in drawArray:
            color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + SIZE) * item[1] + MARGIN,
                              (MARGIN + SIZE) * item[0] + MARGIN,
                              SIZE,
                              SIZE])
        if isOptimal:
            for item in optimalPathForDraw:
                color = RED
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + SIZE) * item[1] + MARGIN,
                                  (MARGIN + SIZE) * item[0] + MARGIN,
                                  SIZE,
                                  SIZE])
        pygame.draw.rect(screen,
                         BLUE,
                         [(MARGIN + SIZE) * start[1] + MARGIN,
                          (MARGIN + SIZE) * start[0] + MARGIN,
                          SIZE,
                          SIZE])
        pygame.draw.rect(screen,
                         YELLOW,
                         [(MARGIN + SIZE) * goal[1] + MARGIN,
                          (MARGIN + SIZE) * goal[0] + MARGIN,
                          SIZE,
                          SIZE])
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

