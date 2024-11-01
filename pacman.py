#IMPORTS ================================================================================================================================================================================================================================================
import pygame; pygame.init()
import random
from copy import deepcopy
from queue import Queue

import constants
from constants import screen as sc
from constants import COLOURS
from constants import SCREEN_HEIGHT as HEIGHT
from constants import SCREEN_WIDTH as WIDTH
from constants import clock
from constants import font

import mazegeneration
from mazegeneration import generategrid
from mazegeneration import classic

icon = pygame.image.load(f"sprites/logo.png")
pygame.display.set_caption(constants.eastereggnames[random.randint(0, 10)])
pygame.display.set_icon(icon)


def showmatrix(maze, directions):
    maze_row = ''

    for row in maze:
        for tile in row:
            maze_row += ' ' + str(tile)
        print(maze_row)
        maze_row = ''

    print(directions)

#OBJECTS ================================================================================================================================================================================================================================================
class Pacman:
    def __init__(self, pacid, x, y, direction, directioncommand, lives, score, imgs, deadframes, alive, deathcounter, deadframenum, pacspeed, effect):
        self.PacID = pacid
        self.x, self.y = x, y
        self.direction = direction
        self.directioncommand = directioncommand
        self.lives = lives
        self.score = score
        self.frames = imgs
        self.deadframes = deadframes
        self.speed = pacspeed
        self.turns = [False, False, False, False]
        self.alive = alive
        self.deathcounter = deathcounter
        self.deathframenum = deadframenum
        self.effect = effect

        self.hitbox = pygame.rect.Rect(self.x + 2, self.y + 2, 36, 36)
        pygame.draw.rect(sc, constants.COLOURS[constants.BLACK], self.hitbox)

        #PacID
            #Player1 = 0
            #Player2 = 1
        
        #x, y
            #Top left of hitbox

        #Direction
            #Up = 0
            #Right = 1
            #Down = 2
            #Left = 3

    def generate(self):
        if self.direction == 0:
            sc.blit(pygame.transform.rotate(self.frames[pacframenum], 90), (self.x, self.y))
        if self.direction == 1:
            sc.blit(pygame.transform.rotate(self.frames[pacframenum], 0), (self.x, self.y))
        if self.direction == 2:
            sc.blit(pygame.transform.rotate(self.frames[pacframenum], -90), (self.x, self.y))
        if self.direction == 3:
            sc.blit(pygame.transform.flip(self.frames[pacframenum], True, False), (self.x, self.y))
        
        if self.effect:
            if activepowerups[4]:
                val = 2
            if activepowerups[6]:
                val = 1
            if activepowerups[10]:
                val = 0.5
            self.generateeffect(val)
          
    def generateeffect(self, effect):
        if effect == 2:
            sc.blit(paceffectsframes[1], (self.x, self.y))
        if effect == 1:
            sc.blit(paceffectsframes[0], (self.x, self.y))
        if effect == 0.5:
            sc.blit(paceffectsframes[2], (self.x, self.y))

    def directionchange(self, input, level):
        self.checkpos(level)
        if input == "w" and self.turns[0]:
            self.direction = 0
            return 0
        elif input == "d" and self.turns[1]:
            self.direction = 1
            return 1
        elif input == "s" and self.turns[2]:
            self.direction = 2
            return 2
        elif input == "a" and self.turns[3]:
            self.direction = 3
            return 3
        else:
            return self.direction
        
    def checkpos(self, level):
        validmatrixval = [1, 4, 9]
        #playerindex = [y][x]
        #Checkmovementup
        topleftx, toplefty = self.x, self.y
        toprightx, toprighty = self.x + 40, self.y
        bottomleftx, bottomlefty = self.x, self.y + 40
        bottomrightx, bottomrighty = self.x + 40, self.y + 40

        topleftx, toplefty = (topleftx - constants.indentx) // 45, (toplefty - constants.indenty) // 45
        toprightx, toprighty = (toprightx - constants.indentx) // 45, (toprighty - constants.indenty) // 45
        bottomleftx, bottomlefty = (bottomleftx - constants.indentx) // 45, (bottomlefty - constants.indenty) // 45
        bottomrightx, bottomrighty = (bottomrightx - constants.indentx) // 45, (bottomrighty - constants.indenty) // 45

        if level[bottomlefty - 1][bottomleftx] in validmatrixval and level[bottomrighty - 1][bottomrightx] in validmatrixval:
            self.turns[0] = True
        if level[toplefty][topleftx + 1] in validmatrixval and level[bottomlefty][bottomleftx + 1] in validmatrixval:
            self.turns[1] = True
        if level[toplefty + 1][topleftx] in validmatrixval and level[toprighty + 1][toprightx] in validmatrixval:
            self.turns[2] = True
        if level[toprighty][toprightx - 1] in validmatrixval and level[bottomrighty][bottomrightx - 1] in validmatrixval:
            self.turns[3] = True
        
        return self.turns

    def move(self, level):
        self.checkpos(level)
        if self.direction == 0 and self.turns[0]:
            self.y -= self.speed
            return -self.speed
        if self.direction == 1 and self.turns[1]:
            self.x += self.speed
            return self.speed
        if self.direction == 2 and self.turns[2]:
            self.y += self.speed
            return self.speed
        if self.direction == 3 and self.turns[3]:
            self.x -= self.speed
            return -self.speed
        
        return 0
    
    def consumepellet(self, maze, powerup):
        index_x, index_y = (self.x + 20 - constants.indentx) // 45, (self.y + 20 - constants.indenty) // 45
        if maze[index_y][index_x] == 1:
            self.score += (10 * scoremultiplier)
            return index_x, index_y, self.score, powerup
        
        if maze[index_y][index_x] == 9:
            self.score += (50 * scoremultiplier)
            powerup = True

            return index_x, index_y, self.score, powerup
        
        return 0, 0, self.score, powerup
  
    def getindex(self):
        indx_x, indx_y = ((self.x + 20) - constants.indentx) // 45, ((self.y + 20) - constants.indenty) // 45
        return indx_x, indx_y

    def checkcollision(self, ghost1, ghost2, ghost3, ghost4):
        if self.hitbox.colliderect(ghost1.hitbox):
            return False
        if self.hitbox.colliderect(ghost2.hitbox):
            return False
        if self.hitbox.colliderect(ghost3.hitbox):
            return False
        if self.hitbox.colliderect(ghost4.hitbox):
            return False
        
        return True

    def deathgeneration(self):
        self.alive = False
        sc.blit(self.deadframes[self.deathframenum], (self.x, self.y))
        if self.deathcounter < 6:
            self.deathcounter += 1
            return self.alive, self.deathcounter, self.deathframenum, False
        else:
            self.deathcounter = 0
            if self.deathframenum < 15:
                self.deathframenum += 1
                return self.alive, self.deathcounter, self.deathframenum, False
            else:
                self.alive = True
                self.deathframenum = 0
                return self.alive, self.deathcounter, self.deathframenum, True

    def changespeed(self, speed):
        self.speed = speed

    def teleport(self):
        newindexx = 0
        newindexy = 0
        while level[newindexy][newindexx] == 0:
            newindexx = random.randint(0, 18)
            newindexy = random.randint(0, 20)
        
        palyerposx = (newindexx * 45) + constants.indentx
        palyerposy = (newindexy * 45) + constants.indenty
        return palyerposx, palyerposy

class Ghost:
    def __init__(self, ghostid, x, y, target, speed, imgs, directionarray, direction):
        self.GhostID = ghostid
        self.posx, self.posy = x, y
        self.index_x, self.index_y = (x - constants.indentx) // 45, (y - constants.indenty) // 45
        self.target = target
        self.speed = speed
        self.imgs = imgs
        self.direction = direction
        self.pathmatrix = levelghostfinder
        self.pathdirections = directionarray
        self.turns = [False, False, False, False]
        if not invisibleghosts:
            self.hitbox = pygame.rect.Rect(self.posx, self.posy, 40, 40)
        else:
            self.hitbox = pygame.rect.Rect(0, 0, 1, 1)
        pygame.draw.rect(sc, constants.COLOURS[constants.BLACK], self.hitbox)

        def explanations():
            #GhostID:
                #Blinky = 0
                #Pinky = 1
                #Inky = 2
                #Clyde = 3
            
            #posx, posy
                #Positions in relation to pygame window
            
            #index_x, index_y
                #Positions in relation to maze matrix

            #target
                #Hunt = 0
                #Scatter = 1
                #Scared = 2
                #Dead = 3

            #speed
                #2 is normal speed
                #1 is speed when scared
                #4 is speed when dead
            
            #direction
                #Up = 0
                #Right = 1
                #Down = 2
                #Left = 3

            #dead
                #Boolean value indicating whether alive or not

            #in_box
                #Boolean value indicating whether in ghost box or not
            collapsable = True
    
    def generate(self):
        sc.blit(self.imgs[self.GhostID], (self.posx, self.posy))
    
    def getindex(self):
        index_x, index_y = (self.posx + 20 - constants.indentx) // 45, (self.posy + 20 - constants.indenty) // 45
        return index_y, index_x

    def getpath(self, endposx, endposy):
        row = len(self.pathmatrix)
        col = len(self.pathmatrix[0])
        for i in range(0, row):
            for j in range(0, col):
                if self.pathmatrix[i][j] == 3:
                    self.pathmatrix[i][j] = 1

        starty, startx = self.getindex()
        if not ((starty == endposy) and (startx == endposx)):
            graph = creategraph(self.pathmatrix)
            startnode = (starty, startx)
            endnode = (endposy, endposx)
            self.pathmatrix = findpath(self.pathmatrix, graph, startnode, endnode)
            self.pathmatrix[endposy][endposx] = 3
            self.pathdirections = findpathdirections(self.pathmatrix, startx, starty, endposx, endposy)
            self.pathmatrix[starty][startx] = 1
        else:
            self.pathmatrix = levelghostfinder
            self.pathdirections = []

        return self.pathmatrix, self.pathdirections
        
    def checkpos(self):
        #playerindex = [y][x]
        posy, posx = self.posy + 20, self.posx + 20
        indexy, indexx = self.getindex()
        currentcellposy, currentcellposx = (indexy * 45) + constants.indenty + 23, (indexx * 45) + constants.indentx + 22
        try:
            nextindexy, nextindexx = self.pathdirections[0][0], self.pathdirections[0][1]
        except:
            if self.direction == 0 and self.pathmatrix[indexy - 1][indexx] != 0:
                nextindexy, nextindexx = indexy - 1, indexx
            if self.direction == 1 and self.pathmatrix[indexy][indexx + 1] != 0:
                nextindexy, nextindexx = indexy, indexx + 1
            if self.direction == 2 and self.pathmatrix[indexy + 1][indexx] != 0:
                nextindexy, nextindexx = indexy + 1, indexx
            if self.direction == 3 and self.pathmatrix[indexy][indexx - 1] != 0:
                nextindexy, nextindexx = indexy, indexx - 1

        try:
            cellposy, cellposx = (nextindexy * 45) + constants.indenty + 23, (nextindexx * 45) + constants.indentx + 22
        except:
            cellposy, cellposx = (indexy * 45) + constants.indenty + 23, (indexx * 45) + constants.indentx + 22

        if (posy == currentcellposy or posx == currentcellposx) and (self.direction == 0 or self.direction == 2):
            if cellposx != posx:
                self.direction = 1
        elif (posy == currentcellposy or posx == currentcellposx) and (self.direction == 1 or self.direction == 3):
            if cellposy != posy:
                self.direction = 0

        if self.direction == 0 or self.direction == 2:
            if posy > cellposy:
                self.turns[0] = True
            if posy < cellposy:
                self.turns[2] = True
        if self.direction == 1 or self.direction == 3:
            if posx < cellposx:
                self.turns[1] = True
            if posx > cellposx:
                self.turns[3] = True

    def move(self):
        self.checkpos()
        if self.turns[0]:
            self.posy -= self.speed
            self.direction = 0
            return self.posx, self.posy, self.direction
        if self.turns[1]:
            self.posx += self.speed
            self.direction = 1
            return self.posx, self.posy, self.direction
        if self.turns[2]:
            self.posy += self.speed
            self.direction = 2
            return self.posx, self.posy, self.direction
        if self.turns[3]:
            self.posx -= self.speed
            self.direction = 3
            return self.posx, self.posy, self.direction
        
        return self.posx, self.posy, self.direction

#SUBROUTINES ============================================================================================================================================================================================================================================
#Breadth-First Search Pathfinding
def creategraph(array):
    graph = {}
    mazesize = len(array)
    rowsize = len(array[0])
    for row in range(0, mazesize):
        for column in range(0, rowsize):
            if array[row][column] != 0:
                adjacentnodes = []

                if row + 1 < mazesize and array[row + 1][column] != 0: #DOWN
                    adjacentnodes.append((row + 1, column))
                if row - 1 >= 0 and array[row - 1][column] != 0: #UP
                    adjacentnodes.append((row - 1, column))
                if column + 1 < rowsize and array[row][column + 1] != 0: #RIGHT
                    adjacentnodes.append((row, column + 1))
                if column - 1 >= 0 and array[row][column - 1] != 0: #LEFT
                    adjacentnodes.append((row, column - 1))

                graph[(row, column)] = adjacentnodes
    return graph

def findpath(array, graph, startnode, endnode):
    visitednodes = []
    startpath = [startnode]
    queue = Queue()
    queue.put(startpath)

    while not queue.empty():
        path = queue.get()
        neighbours = graph[path[-1]]
        
        for n in neighbours:
            if n == endnode:
                for coordinate in path:
                    row, column = coordinate
                    array[row][column] = 3
                return array
            
            if n not in visitednodes:
                visitednodes.append(n)
                newpath = path + [n]
                queue.put(newpath)

def findpathdirections(array, startx, starty, endx, endy):
    directionsqueue = Queue()
    while not (starty == endy and startx == endx):
        valabove = array[starty - 1][startx]
        if valabove == 3:
            directionsqueue.put([starty, startx, 0])
            array[starty][startx] = 5
            starty -= 1
        
        valright = array[starty][startx + 1]
        if valright == 3:
            directionsqueue.put([starty, startx, 1])
            array[starty][startx] = 5
            startx += 1
        
        valbottom = array[starty + 1][startx]
        if valbottom == 3:
            directionsqueue.put([starty, startx, 2])
            array[starty][startx] = 5
            starty += 1
        
        valleft = array[starty][startx - 1]
        if valleft == 3:
            directionsqueue.put([starty, startx, 3])
            array[starty][startx] = 5
            startx -= 1

    for i in range(0, len(array)):
        for j in range(0,len(array[i])):
            if array[i][j] == 5:
                array[i][j] = 3
    
    directionsqueue.get()
    return list(directionsqueue.queue)

#Displaying in-game UI
def displaystats():
    scoretext = font.render(f'Score: {int(playerscore)}', False, constants.COLOURS[constants.WHITE])
    livestext = font.render(f'Lives:', True, constants.COLOURS[constants.WHITE])
    quittextline1 = font.render(f'Press ESCAPE', True, constants.COLOURS[constants.WHITE])
    quittextline2 = font.render(f'to Quit', True, constants.COLOURS[constants.WHITE])
    timer = font.render(f'{time // 60}', True, constants.COLOURS[constants.WHITE])
    text = font.render(f'Pacman', True, constants.COLOURS[constants.YELLOW])
    sc.blit(text, (870, 15))
    sc.blit(livestext, (870, 45))
    sc.blit(quittextline1, (870, 875))
    sc.blit(quittextline2, (870, 905))
    sc.blit(timer, (20, 18))
    for i in range(playerlives):
        sc.blit(pygame.transform.scale(paclives, (30, 30)), (1000 + i * 40, 45))
    
    sc.blit(scoretext, (870, 75))

    displaycontrols()

def displaycontrols():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        sc.blit(controls[4], (950, 150))
    else:
        sc.blit(controls[0], (950, 150))

    if keys[pygame.K_a]:
        sc.blit(controls[5], (900, 200))
    else:
        sc.blit(controls[1], (900, 200))

    if keys[pygame.K_s]:
        sc.blit(controls[6], (950, 200))
    else:
        sc.blit(controls[2], (950, 200))
    
    if keys[pygame.K_d]:
        sc.blit(controls[7], (1000, 200))
    else:
        sc.blit(controls[3], (1000, 200))

def displaystarttimer(val):
    val = (val // 60) + 1
    timertext = font.render(f'{val}', True, constants.COLOURS[constants.WHITE])
    sc.blit(timertext, (424, 467))

def displaygameendmenu():
    gameovertext = font.render(f'Game Over', True, constants.COLOURS[constants.DARKRED])
    scoretext = font.render(f'Score: {int(playerscore)}', True, constants.COLOURS[constants.WHITE])
    text = font.render(f'Pacman', True, constants.COLOURS[constants.YELLOW])
    quittext = font.render(f'Press ESCAPE to Quit', True, constants.COLOURS[constants.WHITE])
    timer = time // 60
    if timer // 60 == 0:
        timertext = font.render(f'{timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    elif timer // 60 == 1:
        timertext = font.render(f'{timer // 60} minute, {timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    else:
        timertext = font.render(f'{timer // 60} minutes, {timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    outlinerect = pygame.rect.Rect(215, 365, 520, 195)
    bgrect = pygame.rect.Rect(225, 375, 500, 175)
    pygame.draw.rect(sc, constants.COLOURS[constants.GREY], outlinerect, border_radius = 12)
    pygame.draw.rect(sc, constants.COLOURS[constants.LIGHTGREY], bgrect, border_radius = 10)

    sc.blit(text, (250, 400))
    sc.blit(gameovertext, (250, 425))
    sc.blit(scoretext, (250, 450))
    sc.blit(timertext, (250, 475))
    sc.blit(quittext, (250, 500))

def displaygamewonmenu():
    gamewontext = font.render(f'Maze Cleared', True, constants.COLOURS[constants.GREEN])
    scoretext = font.render(f'Score: {int(playerscore)}', True, constants.COLOURS[constants.WHITE])
    text = font.render(f'Pacman', True, constants.COLOURS[constants.YELLOW])
    continuetext = font.render(f'Press SPACEBAR to Continue', True, constants.COLOURS[constants.WHITE])
    timer = time // 60
    if timer // 60 == 0:
        timertext = font.render(f'{timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    elif timer // 60 == 1:
        timertext = font.render(f'{timer // 60} minute, {timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    else:
        timertext = font.render(f'{timer // 60} minutes, {timer % 60} seconds', True, constants.COLOURS[constants.WHITE])
    outlinerect = pygame.rect.Rect(215, 365, 580, 195)
    bgrect = pygame.rect.Rect(225, 375, 560, 175)
    pygame.draw.rect(sc, constants.COLOURS[constants.GREY], outlinerect, border_radius = 12)
    pygame.draw.rect(sc, constants.COLOURS[constants.LIGHTGREY], bgrect, border_radius = 10)

    sc.blit(text, (250, 400))
    sc.blit(gamewontext, (250, 425))
    sc.blit(scoretext, (250, 450))
    sc.blit(timertext, (250, 475))
    sc.blit(continuetext, (250, 500))

#LOADING IMAGES =========================================================================================================================================================================================================================================
normalghostframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/blinky.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/pinky.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/inky.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/clyde.png"), (40, 40)),
    ]

slowghostframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/blinkyslow.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/pinkyslow.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/inkyslow.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/clydeslow.png"), (40, 40)),
    ]

speedghostframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/blinkyspeed.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/pinkyspeed.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/inkyspeed.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/clydespeed.png"), (40, 40)),
    ]

frozenghostframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/blinkystop.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/pinkystop.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/inkystop.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/ghosts/powerups/clydestop.png"), (40, 40)),
    ]

pacframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac2.png"), (40, 40))
    ]

pacimmuneframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacimmune2.png"), (40, 40))
    ]

pacspeedframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacspeed2.png"), (40, 40))
    ]

pacslowframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacslow2.png"), (40, 40))
    ]

pacfrozenframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/pacstop2.png"), (40, 40))
    ]

paceffectsframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/controlreverse.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/doublescore.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/powerups/halfscore.png"), (40, 40))
    ]

pacdeadframes = [
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead4.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead5.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead6.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead7.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead8.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead9.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead9.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead10.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead11.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead12.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead13.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead13.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead/pacdead13.png"), (40, 40))
    ]

controls = [
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/winactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/ainactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/sinactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/dinactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/wactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/aactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/sactive.png"), (32, 32)),
    pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/dactive.png"), (32, 32))
    ]

#VARIABLES ==============================================================================================================================================================================================================================================
run = True
counter = 0
fps = 60
time = 0

playertimer = 180
playersalive = True
playerscore = -10
playerlives = 3
playerposx = 415
playerposy = 685
playerdirections = 3
playerdirectioncommands = 3
pacspeed = 2
playersalive = True
collision = False
deathcounter = 0
deadframenum = 0
respawn = False
gameover = False
gamewon = False
usedframes = pacframes
ghostimages = normalghostframes

paclives = pygame.transform.scale(pygame.image.load(f"sprites/pacman/paclives.png"), (25, 25))
pacframenum = 0

ghostposx = [370, 400, 430, 460]
ghostposy = [415, 415, 415, 415]
ghosttargets = 0
ghostspeeds = 2
ghostdirections = [0, 0, 0, 0]
randomselectiontimer = 0
blinkymove = 0
pinkymove = 0
inkymove = 0
clydemove = 0
blinkytimer = random.randint(0, 60)
pinkytimer = random.randint(90, 210)
inkytimer = random.randint(240, 360)
clydetimer = random.randint(390, 510)

activepowerups = [
    False,  #PACSPEEDBOOST          0
    False,  #GHOSTSLOW              1
    False,  #GHOSTSTUN              2
    False,  #INVINCIBILITY          3
    False,  #DOUBLESCORE            4
    False,  #PLAYERSLOW             5
    False,  #REVERSECONTROLS        6
    False,  #INVISIBLEGHOSTS        7
    False,  #GHOSTSVULNERABLE       8
    False,  #PLAYERSTUN             9
    False,  #HALFSCORE              10
    None,   #TELEPORTGHOSTSTOBOX    11
    None    #RANDOMTELEPORT         12
]

timeractive = False
powerup = False
poweruptimer = 0
playermovementallowed = True
ghostmovementallowed = True
pacvulnerable = True
scoremultiplier = 1
reversecontrols = False
invisibleghosts = False
teleportghosts = False
effect = False

classicmaze = False
if classicmaze:
    leveltemp = classic
    level = deepcopy(leveltemp)
else:
    leveltemp = mazegeneration.createmaze(mazegeneration.mazetemplate)
    level = deepcopy(leveltemp)

levelghostfinder = deepcopy(level)

starttimer = 180

graphoflevel = creategraph(levelghostfinder)
regulateloop = 0

continuelevel = False

previousdirectionarrayblinky = []
previousdirectionarraypinky = []
previousdirectionarrayinky = []
previousdirectionarrayclyde = []

#GAME LOOP ==============================================================================================================================================================================================================================================
while run:
    clock.tick(fps)
    #fill background as black
    sc.fill(COLOURS[constants.BLACK])

    generategrid(level)
    pelletsmaze = mazegeneration.defaultpelletspawn(level)
    mazegeneration.generatepellets(pelletsmaze)

    if respawn:
        playertimer = 180
        playersalive = True
        playerlives -= 1
        playerposx = 415
        playerposy = 685
        playerdirections = 3
        playerdirectioncommands = 3
        powerup = False
        collision = False
        deathcounter = 0
        deadframenum = 0
        respawn = False

        ghostposx = [370, 400, 430, 460]
        ghostposy = [415, 415, 415, 415]
        ghosttargets = [0, 0, 0, 0]
        ghostspeeds = 2
        ghostdirections = [0, 0, 0, 0]
        inboxes = [True, True, True, True]

        regulateloop = 0
        starttimer = 180
        movementallowed = False
        
        blinkymove = 0
        pinkymove = 0
        inkymove = 0
        clydemove = 0
        blinkytimer = random.randint(0, 120)
        pinkytimer = random.randint(180, 420)
        inkytimer = random.randint(480, 720)
        clydetimer = random.randint(780, 1020)

        activepowerups = [
            False,  #PACSPEEDBOOST          0
            False,  #GHOSTSLOW              1
            False,  #GHOSTSTUN              2
            False,  #INVINCIBILITY          3
            False,  #DOUBLESCORE            4
            False,  #PLAYERSLOW             5
            False,  #REVERSECONTROLS        6
            False,  #INVISIBLEGHOSTS        7
            None,   #ONEUP                  8
            False,  #PLAYERSTUN             9
            False,  #HALFSCORE              10
            None,   #TELEPORTGHOSTSTOBOX    11
            None    #RANDOMTELEPORT         12
        ]

        timeractive = False
        powerup = False
        poweruptimer = 0
        playermovementallowed = True
        ghostmovementallowed = True
        pacvulnerable = True
        scoremultiplier = 1
        reversecontrols = False
        invisibleghosts = False
        teleportghosts = False
        effect = False
        pacspeed = 2

        usedframes = pacframes
        ghostimages = normalghostframes
    
        if playerlives >= 0:
            playersalive = True
        else:
            gameover = True

    if gameover:
        displaygameendmenu()

    if gamewon:
        displaygamewonmenu()

    if continuelevel:
        playertimer = 180
        playersalive = True
        playerposx = 415
        playerposy = 685
        playerdirections = 3
        playerdirectioncommands = 3
        powerup = False
        collision = False
        deathcounter = 0
        deadframenum = 0
        respawn = False

        ghostposx = [370, 400, 430, 460]
        ghostposy = [415, 415, 415, 415]
        ghosttargets = [0, 0, 0, 0]
        ghostspeeds = 2
        ghostdirections = [0, 0, 0, 0]
        inboxes = [True, True, True, True]

        regulateloop = 0
        starttimer = 180
        movementallowed = False
        
        blinkymove = 0
        pinkymove = 0
        inkymove = 0
        clydemove = 0
        blinkytimer = random.randint(0, 120)
        pinkytimer = random.randint(180, 420)
        inkytimer = random.randint(480, 720)
        clydetimer = random.randint(780, 1020)

        activepowerups = [
            False,  #PACSPEEDBOOST          0
            False,  #GHOSTSLOW              1
            False,  #GHOSTSTUN              2
            False,  #INVINCIBILITY          3
            False,  #DOUBLESCORE            4
            False,  #PLAYERSLOW             5
            False,  #REVERSECONTROLS        6
            False,  #INVISIBLEGHOSTS        7
            None,   #ONEUP                  8
            False,  #PLAYERSTUN             9
            False,  #HALFSCORE              10
            None,   #TELEPORTGHOSTSTOBOX    11
            None    #RANDOMTELEPORT         12
        ]

        timeractive = False
        powerup = False
        poweruptimer = 0
        playermovementallowed = True
        ghostmovementallowed = True
        pacvulnerable = True
        scoremultiplier = 1
        reversecontrols = False
        invisibleghosts = False
        teleportghosts = False
        effect = False
        pacspeed = 2

        usedframes = pacframes
        ghostimages = normalghostframes

        gamewon = False
        gameover = False

        level = deepcopy(leveltemp)
        continuelevel = False

    if not gameover and not gamewon:
        time += 1
        displaystats()
        #OBJECTS GENERATION

        pacP1 = Pacman(0, playerposx, playerposy, playerdirections, playerdirectioncommands, playerlives, playerscore, usedframes, pacdeadframes, playersalive, deathcounter, deadframenum, pacspeed, effect)
        if playersalive:
            blinky = Ghost(0, ghostposx[0], ghostposy[0], ghosttargets, ghostspeeds, ghostimages, previousdirectionarrayblinky, ghostdirections[0])
            pinky = Ghost(1, ghostposx[1], ghostposy[1], ghosttargets, ghostspeeds, ghostimages, previousdirectionarraypinky, ghostdirections[1])
            inky = Ghost(2, ghostposx[2], ghostposy[2], ghosttargets, ghostspeeds, ghostimages, previousdirectionarrayinky, ghostdirections[2])
            clyde = Ghost(3, ghostposx[3], ghostposy[3], ghosttargets, ghostspeeds, ghostimages, previousdirectionarrayclyde, ghostdirections[3])

        #PATHFINDING
        if regulateloop == 12 and playersalive:
            pacindx_x, pacindx_y = pacP1.getindex()

            #BLINKY PATHFINDING
            if True:
                matrixthing = blinky.getpath(pacindx_x, pacindx_y)
                previousdirectionarrayblinky = matrixthing[1]
                #print("Blinky")
                #showmatrix(matrixthing[0], matrixthing[1])

            #PINKY PATHFINDING
            if True:
                pindx_x, pindx_y = pacindx_x, pacindx_y
                if playerdirections == 0:
                    pindx_y -= 4
                    while pindx_y < 0:
                        pindx_y += 1
                    while level[pindx_y][pindx_x] == 0:
                        pindx_y += 1
                
                if playerdirections == 1:
                    pindx_x += 4
                    while pindx_x >= constants.gridx:
                        pindx_x -= 1
                    while level[pindx_y][pindx_x] == 0:
                        pindx_x -= 1

                if playerdirections == 2:
                    pindx_y += 4
                    while pindx_y >= constants.gridy:
                        pindx_y -= 1
                    while level[pindx_y][pindx_x] == 0:
                        pindx_y -= 1

                if playerdirections == 3:
                    pindx_x -= 4
                    while pindx_x < 0:
                        pindx_x += 1
                    while level[pindx_y][pindx_x] == 0:
                        pindx_x += 1

                matrixthing = pinky.getpath(pindx_x, pindx_y)
                previousdirectionarraypinky = matrixthing[1]
                #print("Pinky")
                #showmatrix(matrixthing[0], matrixthing[1])

            #INKY PATHFINDING
            if True:
                iindx_x, iindx_y = pacindx_x, pacindx_y
                if playerdirections == 0:
                    iindx_y -= 4
                    while iindx_y < 0:
                        iindx_y += 1
                    while level[iindx_y][iindx_x] == 0:
                        iindx_y += 1
                
                if playerdirections == 1:
                    iindx_x -= 4
                    while iindx_x < 0:
                        iindx_x += 1
                    while level[iindx_y][iindx_x] == 0:
                        iindx_x += 1

                if playerdirections == 2:
                    iindx_y += 4
                    while iindx_y >= constants.gridy:
                        iindx_y -= 1
                    while level[iindx_y][iindx_x] == 0:
                        iindx_y -= 1

                if playerdirections == 3:
                    iindx_x += 4
                    while iindx_x >= constants.gridx:
                        iindx_x -= 1
                    while level[iindx_y][iindx_x] == 0:
                        iindx_x -= 1

                matrixthing = inky.getpath(iindx_x, iindx_y)
                previousdirectionarrayinky = matrixthing[1]
                #print("Inky")
                #showmatrix(matrixthing[0], matrixthing[1])

            #CLYDE PATHFINDING
            if True:
                matrixthing = clyde.getpath(pacindx_x, pacindx_y)
                previousdirectionarrayclyde = matrixthing[1]
                #print("Clyde")
                #showmatrix(matrixthing[0], matrixthing[1])
                #print()

            regulateloop = 0
        else:
            regulateloop += 1

        #STARTUP TIMER
        if starttimer > 0:
            displaystarttimer(starttimer)
            starttimer -= 1
            movementallowed = False
        else:
            movementallowed = True

        #MOVING
        if movementallowed and playersalive:
            if playermovementallowed:
                if playerdirections == 0:
                    playerposy += pacP1.move(level)
                if playerdirections == 1:
                    playerposx += pacP1.move(level)
                if playerdirections == 2:
                    playerposy += pacP1.move(level)
                if playerdirections == 3:
                    playerposx += pacP1.move(level)

            if ghostmovementallowed:
                if blinkymove >= blinkytimer:
                    ghostposx[0], ghostposy[0], ghostdirections[0] = blinky.move()
                if pinkymove >= pinkytimer:
                    ghostposx[1], ghostposy[1], ghostdirections[1] = pinky.move()
                if inkymove >= inkytimer:
                    ghostposx[2], ghostposy[2], ghostdirections[2] = inky.move()
                if clydemove >= clydetimer:
                    ghostposx[3], ghostposy[3], ghostdirections[3] = clyde.move()

        #PACMAN FRAME TICKER
        if playersalive:
            if counter < 6:
                counter += 1
            else:
                counter = 0
                if pacframenum < 5:
                    pacframenum += 1
                else:
                    pacframenum = 0
            if movementallowed:
                blinkymove += 1
                pinkymove += 1
                inkymove += 1
                clydemove += 1

        #GENERATING
        if playersalive:
            pacP1.generate()
            if not invisibleghosts:
                blinky.generate()
                pinky.generate()
                inky.generate()
                clyde.generate()

        if not playersalive:
            playersalive, deathcounter, deadframenum, respawn = pacP1.deathgeneration()

        if ghosttargets == 0 and randomselectiontimer >= 1200:
            ghosttargets = 1
            randomselectiontimer = 0
        elif ghosttargets == 1 and randomselectiontimer >= 420:
            ghosttargets = 0
            randomselectiontiemr = 0
        else:
            randomselectiontimer += 1

        #COLLISION CHECK
        if playersalive and pacvulnerable:
            playersalive = pacP1.checkcollision(blinky, pinky, inky, clyde)

    #EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_BACKSPACE:
                crashvariable = int("a")

        if gamewon:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gamewon = False
                    gameover = False
                    continuelevel = True

        if not gameover:
            if event.type == pygame.KEYDOWN:
                if not reversecontrols:
                    if event.key == pygame.K_w:
                        playerdirectioncommands = 0
                    if event.key == pygame.K_d:
                        playerdirectioncommands = 1
                    if event.key == pygame.K_s:
                        playerdirectioncommands = 2
                    if event.key == pygame.K_a:
                        playerdirectioncommands = 3
                else:
                    if event.key == pygame.K_w:
                        playerdirectioncommands = 2
                    if event.key == pygame.K_d:
                        playerdirectioncommands = 3
                    if event.key == pygame.K_s:
                        playerdirectioncommands = 0
                    if event.key == pygame.K_a:
                        playerdirectioncommands = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    playerdirectioncommands = playerdirections
                if event.key == pygame.K_d:
                    playerdirectioncommands = playerdirections
                if event.key == pygame.K_s:
                    playerdirectioncommands = playerdirections
                if event.key == pygame.K_a:
                    playerdirectioncommands = playerdirections

    if not gameover and not gamewon:
        #MOVING
        validturnsP1 = pacP1.checkpos(level)
        if playerdirectioncommands == 0 and validturnsP1[0]:
            playerdirections = pacP1.directionchange("w", level)
        if playerdirectioncommands == 1 and validturnsP1[1]:
            playerdirections = pacP1.directionchange("d", level)
        if playerdirectioncommands == 2 and validturnsP1[2]:
            playerdirections = pacP1.directionchange("s", level)
        if playerdirectioncommands == 3 and validturnsP1[3]:
            playerdirections = pacP1.directionchange("a", level)

        #PELLET CONSUMPTION
        positionx, positiony, playerscore, powerup = pacP1.consumepellet(level, powerup)
        if positionx != 0 and positiony != 0:
            level[positiony][positionx] = 4
        if powerup:
            if not timeractive:
                powerupused = random.randint(0, 12)
                if powerupused not in [8, 11, 12]:
                    activepowerups[powerupused] = True
                match powerupused:
                    case 0:
                        pacspeed = 3
                        usedframes = pacspeedframes
                        timeractive = True
                    case 1:
                        ghostspeeds = 1
                        ghostimages = slowghostframes
                        timeractive = True
                    case 2:
                        ghostmovementallowed = False
                        ghostimages = frozenghostframes
                        timeractive = True
                    case 3:
                        pacvulnerable = False
                        ghostspeeds = 1
                        usedframes = pacimmuneframes
                        timeractive = True
                    case 4:
                        scoremultiplier = 2
                        effect = True
                        timeractive = True
                    case 5:
                        pacspeed = 1
                        usedframes = pacslowframes
                        timeractive = True
                    case 6:
                        reversecontrols = True
                        effect = True
                        timeractive = True
                    case 7:
                        invisibleghosts = True
                        timeractive = True
                    case 8:
                        playerlives += 1
                        powerup = False
                    case 9:
                        playermovementallowed = False
                        usedframes = pacfrozenframes
                        timeractive = True
                    case 10:
                        scoremultiplier = 0.5
                        effect = True
                        timeractive = True
                    case 11:
                        ghostposx = [370, 400, 430, 460]
                        ghostposy = [415, 415, 415, 415]
                        blinkymove = 0
                        pinkymove = 0
                        inkymove = 0
                        clydemove = 0
                        powerup = False
                    case 12:
                        playerposx, playerposy = pacP1.teleport()
                        usedframes = pacframes
                        powerup = False

            if (activepowerups[0] or activepowerups[1] or activepowerups[2]) and poweruptimer >= 300:
                timeractive = False
                powerup = False
                poweruptimer = 0
                pacspeed = 2
                ghostspeeds = 2
                usedframes = pacframes
                ghostimages = normalghostframes
                ghostmovementallowed = True
            elif activepowerups[3] and poweruptimer >= 600:
                timeractive = False
                powerup = False
                poweruptimer = 0
                pacvulnerable = True
                ghostspeeds = 2
                usedframes = pacframes
                ghostimages = normalghostframes
            elif (activepowerups[4] or activepowerups[10]) and poweruptimer >= 750:
                timeractive = False
                powerup = False
                poweruptimer = 0
                scoremultiplier = 1
                usedframes = pacframes
                ghostimages = normalghostframes
                effect = False
            elif activepowerups[5] and poweruptimer >= 150:
                timeractive = False
                powerup = False
                poweruptimer = 0
                pacspeed = 2
                usedframes = pacframes
                ghostimages = normalghostframes
            elif activepowerups[6] and poweruptimer >= 270:
                timeractive = False
                powerup = False
                poweruptimer = 0
                reversecontrols = False
                usedframes = pacframes
                ghostimages = normalghostframes
                effect = False
            elif activepowerups[7] and poweruptimer >= 150:
                timeractive = False
                powerup = False
                poweruptimer = 0
                invisibleghosts = False
                usedframes = pacframes
                ghostimages = normalghostframes
            elif activepowerups[8] and poweruptimer >= 600:
                timeractive = False
                powerup = False
                poweruptimer = 0
                vulnerableghosts = False
                usedframes = pacframes
                ghostimages = normalghostframes
            elif activepowerups[9] and poweruptimer >= 90:
                timeractive = False
                powerup = False
                poweruptimer = 0
                playermovementallowed = True
                usedframes = pacframes
                ghostimages = normalghostframes
            else:
                poweruptimer += 1

        level[9][8] = 4
        level[9][9] = 4
        level[9][10] = 4
        oneinlevel = False
        for i in range(0, len(level)):
            if 1 in level[i]:
                oneinlevel = True
                break
        if oneinlevel:
            gamewon = False
            level[9][8] = 1
            level[9][9] = 1
            level[9][10] = 1
        else:
            gamewon = True

    pygame.display.update()

pygame.quit()