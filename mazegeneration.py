import pygame; pygame.init()
import numpy as np
from enum import Enum

import constants
from constants import SCREEN_HEIGHT as HEIGHT
from constants import SCREEN_WIDTH as WIDTH
from constants import screen as sc
from constants import clock as clock
from constants import COLOURS as COLOURS
from constants import indentx as indentx
from constants import indenty as indenty

class CellType(Enum):
    empty = 0
    solid = 1
    pellet = 2
    powerpellet = 3

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.celltype = 1
        self.visited = False

    def receivevar(self):
        return self.x, self.y



def createcells():
    for i in range(0, constants.gridx):
        for j in range(0, constants.gridy):
            cells.append(Cell((i * 45) + indentx, (j * 45) + indenty))

def generategrid(level):
    createcells()
    mazesize = len(level)
    rowsize = len(level[0])
    for row in range(0, mazesize):
        for column in range(0, rowsize):
            if level[row][column] == 0 or level[row][column] == 2:
                cellnum = (column * 21) + (row)
                x, y = cells[cellnum].receivevar()

                if row + 1 < mazesize and level[row + 1][column] == 1: #DOWN
                    cells[cellnum].walls["bottom"] = False
                if row - 1 >= 0 and level[row - 1][column] == 1: #UP
                    cells[cellnum].walls["top"] = False
                if column + 1 < rowsize and (level[row][column + 1] == 1 or level[row][column + 1] == 2): #RIGHT
                    cells[cellnum].walls["right"] = False
                if column - 1 < rowsize and (level[row][column - 1] == 1 or level[row][column - 1] == 2): #LEFT
                    cells[cellnum].walls["left"] = False
                
                if row + 1 >= mazesize: #DOWN
                    cells[cellnum].walls["bottom"] = False
                if row - 1 < 0: #UP
                    cells[cellnum].walls["top"] = False
                if column + 1 >= rowsize: #RIGHT
                    cells[cellnum].walls["right"] = False
                if column - 1 < 0: #LEFT
                    cells[cellnum].walls["left"] = False

                spriteuse = 0
                if cells[cellnum].walls["top"] == True:
                    spriteuse += 1
                if cells[cellnum].walls["right"] == True:
                    spriteuse += 2
                if cells[cellnum].walls["bottom"] == True:
                    spriteuse += 4
                if cells[cellnum].walls["left"] == True:
                    spriteuse += 8

                if column == 9 and row == 8:
                    spriteuse = 16
                
                sc.blit(mazeelements[spriteuse], (x, y))




mazeelements = []
for i in range(0, 17):
    mazeelements.append(pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall{i}.png'), (45, 45)))

run = True
i = 0
xpos = 0
ypos = 0
classic = True
classic = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
cells = []

