import pygame
import sys
import threading
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SIZE = 20
MARGIN = 5
done = False

clock = pygame.time.Clock()

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

    t = threading.Thread(target=drawL)
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

    w = 1280
    h = 720

    wz = [len(map[0]) * SIZE + (len(map[0]) + 1) * MARGIN, len(map) * SIZE + (len(map) + 1) * MARGIN]
    if w < wz[0]:
        SIZE = int((w - (len(map[0]) + 1) * MARGIN) / len(map[0]))
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

    WINDOW_SIZE = wz
    speed = 1.0 / len(map)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("AStar")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)
        if dd == 1:
            drawPath(openPath)
            dd = 0
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

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
