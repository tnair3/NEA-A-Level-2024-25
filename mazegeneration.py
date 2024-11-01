import pygame; pygame.init()
import random
from random import choice

import constants
from constants import SCREEN_HEIGHT as HEIGHT
from constants import SCREEN_WIDTH as WIDTH
from constants import clock
from constants import COLOURS
from constants import indentx
from constants import indenty
from constants import TILE
from constants import screen as sc

#OBJECTS ================================================================================================================================================================================================================================================
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, (0, 0, 0), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, (46, 12, 200), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, (46, 12, 200), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(sc, (46, 12, 200), (x, y + TILE), (x + TILE, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(sc, (46, 12, 200), (x, y), (x, y + TILE), 2)

    def drawcurrentcell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, constants.COLOURS[constants.RED], (x + 2, y + 2, TILE - 2, TILE - 2))

    def checkcell(self, x, y):
        findindex = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return gridcells[findindex(x, y)]
    
    def checkneighbours(self):
        neighbours = []
        top = self.checkcell(self.x, self.y - 1)
        right = self.checkcell(self.x + 1, self.y)
        bottom = self.checkcell(self.x, self.y + 1)
        left = self.checkcell(self.x - 1, self.y)
        if top and not top.visited:
            neighbours.append(top)
        if right and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.visited:
            neighbours.append(left)

        return choice(neighbours) if neighbours else False
    
    def receivevar(self):
        return self.x, self.y
    
    def printcell(self):
        return self.walls

#SUBROUTINES ============================================================================================================================================================================================================================================
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

                if row + 1 < mazesize and (level[row + 1][column] == 1 or level[row + 1][column] == 9): #DOWN
                    cells[cellnum].walls["bottom"] = False
                if row - 1 >= 0 and (level[row - 1][column] == 1 or level[row - 1][column] == 9): #UP
                    cells[cellnum].walls["top"] = False
                if column + 1 < rowsize and (level[row][column + 1] == 1 or level[row][column + 1] == 2 or level[row][column + 1] == 9): #RIGHT
                    cells[cellnum].walls["right"] = False
                if column - 1 < rowsize and (level[row][column - 1] == 1 or level[row][column - 1] == 2 or level[row][column - 1] == 9): #LEFT
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

def defaultpelletspawn(maze):
    row = len(maze)
    col = len(maze[0])
    for i in range(row):
        for j in range(col):
            if maze[i][j] == 1 and not (i == 9 and (j == 8 or j == 9 or j == 10)):
                maze[i][j] = 3
    
    return maze

def generatepellets(level):
    row = len(level)
    col = len(level[0])
    for i in range(row):
        for j in range(col):
            if level[i][j] == 3:
                xpos, ypos = (j * 45) + indentx + 7, (i * 45) + indenty + 7
                sc.blit(pellets[0], (xpos, ypos))
            if level[i][j] == 9:
                xpos, ypos = (j * 45) + indentx + 7, (i * 45) + indenty + 7
                sc.blit(pellets[1], (xpos, ypos))

    row = len(level)
    col = len(level[0])
    for i in range(row):
        for j in range(col):
            if level[i][j] == 3 and not (i == 9 and (j == 8 or j == 9 or j == 10)):
                level[i][j] = 1

def generate():
    def removewalls(current, next):
        dx = current.x - next.x
        dy = current.y - next.y
        match dx:
            case 1:
                current.walls['left'] = False
                next.walls['right'] = False
            case -1:
                current.walls['right'] = False
                next.walls['left'] = False
        
        match dy:
            case 1:
                current.walls['top'] = False
                next.walls['bottom'] = False
            case -1:
                current.walls['bottom'] = False
                next.walls['top'] = False

    currentcell = gridcells[0]
    stack = []
    complete = False
    while not complete:
        clock.tick(60)
        sc.fill(constants.COLOURS[constants.BLACK])

        [cell.draw() for cell in gridcells]
        currentcell.visited = True
        currentcell.drawcurrentcell()

        nextcell = currentcell.checkneighbours()
        if nextcell:
            nextcell.visited = True
            stack.append(currentcell)
            removewalls(currentcell, nextcell)
            currentcell = nextcell
        elif stack:
            currentcell = stack.pop()
        
        if len(stack) == 0:
            complete = True

        pygame.display.update()

    cells = []

    for i in range(0, rows):
        row = []
        for j in range(0, cols):
            index = j + i * cols
            row.append(gridcells[index].printcell())
        cells.append(row)
    
    return cells

def showarray(array):
    for i in range(0, len(array)):
        print("Row", i)
        for j in range(len(array[i])):
            print("Index", j, "=", array[i][j])

        print()

def showmatrix(maze):
    maze_row = ''

    for row in maze:
        for tile in row:
            maze_row += ' ' + str(tile)
        print(maze_row)
        maze_row = ''

# =======================================================================================================================================================================================================================================================
mazeelements = [pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall0.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall1.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall2.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall3.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall4.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall5.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall6.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall7.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall8.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall9.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall10.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall11.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall12.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall13.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall14.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall15.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/wall16.png'), (45, 45))]

pellets = [pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/pellet.png'), (32, 32)),
           pygame.transform.scale(pygame.image.load(f'sprites/mazeelements/powerpellet.png'), (32, 32))
           ]

classic = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
            [0, 9, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 9, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 9, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 9, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

mazetemplate = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

cells = []
cols, rows = 9, 10
gridcells = [Cell(col, row) for row in range(rows) for col in range(cols)]

def createmaze(maze):
    array = generate()
    queue = []
    for i in range(0, len(array)):
        for j in range(0, len(array[i])):
            queue.append(array[i][j])
    mazesize = len(maze)
    rowsize = len(maze[0])
    for i in range(1, mazesize, 2):
        for j in range(1, rowsize, 2):
            maze[i][j] = 1
            currentcellwalls = queue[0]
            if not currentcellwalls['top']:
                maze[i - 1][j] = 1
            if not currentcellwalls['right']:
                maze[i][j + 1] = 1
            if not currentcellwalls['bottom']:
                maze[i + 1][j] = 1
            if not currentcellwalls['left']:
                maze[i][j - 1] = 1
            queue.pop(0)

    for i in range(6, 13):
        maze[7][i] = 1
        maze[11][i] = 1
    for i in range(7, 12):
        maze[i][6] = 1
        maze[i][12] = 1
    for i in range(8, 11):
        maze[9][i] = 1
    for i in range(12, 16):
        maze[i][9] = 1

    maze[8][9] = 2

    for i in range(8, 11):
        maze[i][7] = 0
        maze[i][11] = 0
    for i in range(7, 12):
        maze[10][i] = 0
    maze[8][8] = 0
    maze[8][10] = 0
    
    for i in range(0, 4):
        row = random.randint(0, 20)
        col = random.randint(0, 18)
        while maze[row][col] == 0:
            row = random.randint(0, 20)
            col = random.randint(0, 18)
        maze[row][col] = 9

    mazecuts = random.randint(26, 75)
    for i in range(0, mazecuts):
        row = random.randint(0, 20)
        col = random.randint(0, 18)
        while maze[row][col] != 0:
            row = random.randint(0, 20)
            col = random.randint(0, 18)
        maze[row][col] = 0

    return maze