#IMPORTS ================================================================================================================================================================================================================================================
import pygame; pygame.init()
import random
import math
from enum import Enum
from queue import Queue

#MAZE IS 19x31

import constants
from constants import screen as sc
from constants import COLOURS as COLOURS
from constants import SCREEN_HEIGHT as HEIGHT
from constants import SCREEN_WIDTH as WIDTH
from constants import clock as clock

import mazegeneration
from mazegeneration import generategrid as generategrid
from mazegeneration import classic as classic

#OBJECTS ================================================================================================================================================================================================================================================
class Ghost:
    def __init__(self, ghostid):
        self.ghostid = ghostid #Blinky0, Pinky1, Inky2, Clyde3

class Pacman:
    def __init__(self):
        pass

#SUBROUTINES ============================================================================================================================================================================================================================================
def pacframes(pacframes):
    for i in range(1, 8):
        if i <= 4:
            pacframes.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac{i}.png"), (40, 40)))
        else:
            i = 8 - i
            pacframes.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac{i}.png"), (40, 40)))

    return pacframes

def loadghostimages():
    blinky = pygame.image.load(f"sprites/ghosts/blinky.png")
    pinky = pygame.image.load(f"sprites/ghosts/pinky.png")
    inky = pygame.image.load(f"sprites/ghosts/inky.png")
    clyde = pygame.image.load(f"sprites/ghosts/clyde.png")
    scared = pygame.image.load(f"sprites/ghosts/scared.png")
    dead = pygame.image.load(f"sprites/ghosts/dead.png")

    return [blinky, pinky, inky, clyde, scared, dead]


def findstart(level, position):
    mazesize = len(level)
    rowsize = len(level[0])

    for row in range(0, mazesize):
        for column in range(0, rowsize):
            if level[row][column] == position:
                return (row, column)

def findend(level, end):
    mazesize = len(level)
    rowsize = len(level[0])

    for row in range(0, mazesize):
        for column in range(0, rowsize):
            if level[row][column] == end:
                return (row, column)
            
def creategraph(level):
    graph = {}
    mazesize = len(level)
    rowsize = len(level[0])
    for row in range(0, mazesize):
        for column in range(0, rowsize):
            if level[row][column] != 0:
                adjacentnodes = []

                if row + 1 < mazesize and level[row + 1][column] != 0: #DOWN
                    adjacentnodes.append(row + 1, column)
                if row - 1 >= 0 and level[row - 1][column] != 0: #UP
                    adjacentnodes.append(row - 1, column)
                if column + 1 < rowsize and level[row][column + 1] != 0: #RIGHT
                    adjacentnodes.append(row, column + 1)
                if column - 1 < 0 and level[row][column - 1] != 0: #LEFT
                    adjacentnodes.append(row, column - 1)

                graph[(row, column)] = adjacentnodes
    return graph

def findpath(level, graph, startnode, endnode):
    visitednodes = []
    startpath = [startnode]
    queue = Queue()
    queue.put(startpath)

    while not queue.empty():
        path = queue.get()
        neighbours = graph[path[-1]]
        for i in neighbours:
            if i == endnode:
                for coordinate in path:
                    row, column = coordinate
                    level[row][column] = 2
                return level
            
            if i not in visitednodes:
                visitednodes.append(i)
                newpath = path + [i]
                queue.put(newpath)


#VARIABLES ==============================================================================================================================================================================================================================================
run = True
counter = 0
fps = 60

pacmanframes = pacframes([])
pacframenum = 0

ghostimages = loadghostimages()

#GAME LOOP ==============================================================================================================================================================================================================================================
while run:
    clock.tick(fps)
    #fill background as black
    sc.fill(COLOURS[constants.BLACK])

    generategrid(classic)

    #pacmanframeticker
    if counter < 6:
        counter += 1
    else:
        counter = 0
        if pacframenum < 6:
            pacframenum += 1
        else:
            pacframenum = 0
    sc.blit(pacmanframes[pacframenum], (415, 685))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()

pygame.quit()