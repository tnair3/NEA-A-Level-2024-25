#IMPORTS ================================================================================================================================================================================================================================================
import pygame; pygame.init()
import random
from copy import deepcopy
from queue import Queue
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import constants
from constants import screen as sc
from constants import COLOURS as COLOURS
from constants import SCREEN_HEIGHT as HEIGHT
from constants import SCREEN_WIDTH as WIDTH
from constants import clock as clock
from constants import font as font

import mazegeneration
from mazegeneration import generategrid as generategrid
from mazegeneration import classic as classic

icon = pygame.image.load(f"sprites/logo.png")
pygame.display.set_caption("Non-Exam Pacman")
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
    def __init__(self, pacid, x, y, direction, directioncommand, lives, score, imgs, deadframes, alive, deathcounter, deadframenum):
        self.PacID = pacid
        self.x, self.y = x, y
        self.direction = direction
        self.directioncommand = directioncommand
        self.lives = lives
        self.score = score
        self.frames = imgs
        self.deadframes = deadframes
        self.speed = 2
        self.turns = [False, False, False, False]
        self.alive = alive
        self.deathcounter = deathcounter
        self.deathframenum = deadframenum

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
            self.score += 10
            return index_x, index_y, self.score, powerup
        if maze[index_y][index_x] == 9:
            self.score += 50
            powerup = True
            return index_x, index_y, self.score, powerup
        return 0, 0, self.score, powerup
  
    def getindex(self):
        indx_x, indx_y = ((self.x + 20) - constants.indentx) // 45, ((self.y + 20) - constants.indenty) // 45
        return indx_x, indx_y

    def checkcollision(self, ghost1, ghost2, ghost3, ghost4):
        if self.hitbox.colliderect(ghost1.hitbox):
            return False
        elif self.hitbox.colliderect(ghost2.hitbox):
            return False
        elif self.hitbox.colliderect(ghost3.hitbox):
            return False
        elif self.hitbox.colliderect(ghost4.hitbox):
            return False
        else:
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

class Ghost:
    def __init__(self, ghostid, x, y, target, speed, dead, inbox, imgs, directionarray, direction):
        self.GhostID = ghostid
        self.posx, self.posy = x, y
        self.index_x, self.index_y = (x - constants.indentx) // 45, (y - constants.indenty) // 45
        self.target = target
        self.speed = speed
        self.dead = dead
        self.in_box = inbox
        self.imgs = imgs
        self.direction = direction
        self.pathmatrix = levelghostfinder
        self.pathdirections = directionarray
        self.turns = [False, False, False, False]
        self.hitbox = pygame.rect.Rect(self.posx + 2, self.posy + 2, 36, 36)
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
        if powerup and not self.dead:
            sc.blit(self.imgs[4], (self.posx, self.posy))
        elif self.dead:
            sc.blit(self.imgs[5], (self.posx, self.posy))
        else:
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
        graph = creategraph(self.pathmatrix)
        startnode = (starty, startx)
        endnode = (endposy, endposx)
        self.pathmatrix = findpath(self.pathmatrix, graph, startnode, endnode)
        self.pathmatrix[endposy][endposx] = 3
        self.pathdirections = findpathdirections(self.pathmatrix, startx, starty, endposx, endposy)
        self.pathmatrix[starty][startx] = 1

        return self.pathmatrix, self.pathdirections
    
    def checkpos(self):
        validmatrixval = [3]
        #playerindex = [y][x]
        posy, posx = self.posy + 20, self.posx + 20
        indexy, indexx = self.getindex()
        currentcellposy, currentcellposx = (indexy * 45) + constants.indenty + 23, (indexx * 45) + constants.indentx + 22
        try:
            nextindexy, nextindexx = self.pathdirections[0][0], self.pathdirections[0][1]
        except:
            if self.direction == 0:
                nextindexy, nextindexx = indexy - 1, indexx
            if self.direction == 1:
                nextindexy, nextindexx = indexy, indexx + 1
            if self.direction == 2:
                nextindexy, nextindexx = indexy + 1, indexx
            if self.direction == 3:
                nextindexy, nextindexx = indexy, indexx - 1
        cellposy, cellposx = (nextindexy * 45) + constants.indenty + 23, (nextindexx * 45) + constants.indentx + 22

        if (posy == currentcellposy or posx == currentcellposx) and (self.direction == 0 or self.direction == 2):
            if cellposx != posx:
                self.direction = 1
        if (posy == currentcellposy or posx == currentcellposx) and (self.direction == 1 or self.direction == 3):
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
#Get image subroutines
def pacframes():
    pacframes = []
    for i in range(1, 8):
        if i <= 4:
            pacframes.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac{i}.png"), (40, 40)))
        else:
            i = 8 - i
            pacframes.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pac{i}.png"), (40, 40)))

    return pacframes

def pacdeadframes():
    pacdeadframes = []
    for i in range(1, 17):
        pacdeadframes.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacdead{i}.png"), (40, 40)))
    
    return pacdeadframes

def loadghostimages():
    blinky = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/blinky.png"), (40, 40))
    pinky = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/pinky.png"), (40, 40))
    inky = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/inky.png"), (40, 40))
    clyde = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/clyde.png"), (40, 40))
    scared = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/scared.png"), (40, 40))
    dead = pygame.transform.scale(pygame.image.load(f"sprites/ghosts/dead.png"), (40, 40))

    return [blinky, pinky, inky, clyde, scared, dead]

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
    scoretext = font.render(f'Score: {playerscore}', True, constants.COLOURS[constants.WHITE])
    livestext = font.render(f'Lives:', True, constants.COLOURS[constants.WHITE])
    text = font.render(f'Pacman', True, constants.COLOURS[constants.YELLOW])
    sc.blit(text, (870, 15))
    sc.blit(livestext, (870, 45))
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

def displaypoweruptimer(val):
    val = (val // 60) + 1
    poweruptext = font.render('Powerup', True, constants.COLOURS[constants.WHITE])
    timertext = font.render(f'{val}', True, constants.COLOURS[constants.WHITE])
    if val >= 10:
        sc.blit(timertext, (418, 467))
    else:
        sc.blit(timertext, (424, 467))
    sc.blit(poweruptext, (870, 105))

#VARIABLES ==============================================================================================================================================================================================================================================
run = True
counter = 0
fps = 60

playertimer = 180
playersalive = True
playerscore = -10
playerlives = 3
playerposx = 415
playerposy = 685
playerdirections = 3
playerdirectioncommands = 3
playersalive = True
powerup = False
poweruptimer = 599
collision = False
deathcounter = 0
deadframenum = 0
respawn = False

paclives = pygame.transform.scale(pygame.image.load(f"sprites/pacman/paclives.png"), (25, 25))
pacframenum = 0

controls = [pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/winactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/ainactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/sinactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/dinactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/wactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/aactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/sactive.png"), (32, 32)),
            pygame.transform.scale(pygame.image.load(f"sprites/playercontrols/dactive.png"), (32, 32))]

ghostposx = [370, 400, 430, 460]
ghostposy = [415, 415, 415, 415]
ghosttargets = [0, 0, 0, 0]
ghostspeeds = [2, 2, 2, 2]
deadghosts = [False, False, False, False]
ghostdirections = [0, 0, 0, 0]
inboxes = [True, True, True, True]

ghostimages = loadghostimages()

classicmaze = True
if classicmaze:
    level = classic
    levelghostfinder = deepcopy(classic)
else:
    level = mazegeneration.mazetemplate
    levelghostfinder = deepcopy(mazegeneration.mazetemplate)

starttimer = 180

graphoflevel = creategraph(levelghostfinder)
regulateloop = 0

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
    displaystats()
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
        playersalive = True
        powerup = False
        poweruptimer = 599
        collision = False
        deathcounter = 0
        deadframenum = 0
        respawn = False

        ghostposx = [370, 400, 430, 460]
        ghostposy = [415, 415, 415, 415]
        ghosttargets = [0, 0, 0, 0]
        ghostspeeds = [2, 2, 2, 2]
        deadghosts = [False, False, False, False]
        ghostdirections = [0, 0, 0, 0]
        inboxes = [True, True, True, True]

        regulateloop = 0
        starttimer = 180
        movementallowed = False

    #OBJECTS GENERATION
    pacP1 = Pacman(0, playerposx, playerposy, playerdirections, playerdirectioncommands, playerlives, playerscore, pacframes(), pacdeadframes(), playersalive, deathcounter, deadframenum)
    if playersalive:
        blinky = Ghost(0, ghostposx[0], ghostposy[0], ghosttargets[0], ghostspeeds[0], deadghosts[0], inboxes[0], ghostimages, previousdirectionarrayblinky, ghostdirections[0])
        pinky = Ghost(1, ghostposx[1], ghostposy[1], ghosttargets[1], ghostspeeds[1], deadghosts[1], inboxes[1], ghostimages, previousdirectionarraypinky, ghostdirections[1])
        inky = Ghost(2, ghostposx[2], ghostposy[2], ghosttargets[2], ghostspeeds[2], deadghosts[2], inboxes[2], ghostimages, previousdirectionarrayinky, ghostdirections[2])
        clyde = Ghost(3, ghostposx[3], ghostposy[3], ghosttargets[3], ghostspeeds[3], deadghosts[3], inboxes[3], ghostimages, previousdirectionarrayclyde, ghostdirections[3])

    #PATHFINDING
    if regulateloop == 12 and playersalive:
        if not powerup:
            pacindx_x, pacindx_y = pacP1.getindex()

            print("Blinky")
            matrixthing = blinky.getpath(pacindx_x, pacindx_y)
            previousdirectionarrayblinky = matrixthing[1]
            showmatrix(matrixthing[0], matrixthing[1])

            print("Pinky")
            matrixthing = pinky.getpath(pacindx_x, pacindx_y)
            previousdirectionarraypinky = matrixthing[1]
            showmatrix(matrixthing[0], matrixthing[1])

            print("Inky")
            matrixthing = inky.getpath(pacindx_x, pacindx_y)
            previousdirectionarrayinky = matrixthing[1]
            showmatrix(matrixthing[0], matrixthing[1])

            print("Clyde")
            matrixthing = clyde.getpath(pacindx_x, pacindx_y)
            previousdirectionarrayclyde = matrixthing[1]
            showmatrix(matrixthing[0], matrixthing[1])
            print()
        elif powerup:
            pass
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
        if playerdirections == 0:
            playerposy += pacP1.move(level)
        if playerdirections == 1:
            playerposx += pacP1.move(level)
        if playerdirections == 2:
            playerposy += pacP1.move(level)
        if playerdirections == 3:
            playerposx += pacP1.move(level)
        
        ghostposx[0], ghostposy[0], ghostdirections[0] = blinky.move()
        ghostposx[1], ghostposy[1], ghostdirections[1] = pinky.move()
        ghostposx[2], ghostposy[2], ghostdirections[2] = inky.move()
        ghostposx[3], ghostposy[3], ghostdirections[3] = clyde.move()

    #PACMAN FRAME TICKER
    if playersalive:
        if counter < 6:
            counter += 1
        else:
            counter = 0
            if pacframenum < 6:
                pacframenum += 1
            else:
                pacframenum = 0

    #GENERATING
    if playersalive:
        pacP1.generate()
        blinky.generate()
        pinky.generate()
        inky.generate()
        clyde.generate()

    if not playersalive:
        playersalive, deathcounter, deadframenum, respawn = pacP1.deathgeneration()

    if playersalive:
        playersalive = pacP1.checkcollision(blinky, pinky, inky, clyde)

    #EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playerdirectioncommands = 0
            if event.key == pygame.K_d:
                playerdirectioncommands = 1
            if event.key == pygame.K_s:
                playerdirectioncommands = 2
            if event.key == pygame.K_a:
                playerdirectioncommands = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                playerdirectioncommands = playerdirections
            if event.key == pygame.K_d:
                playerdirectioncommands = playerdirections
            if event.key == pygame.K_s:
                playerdirectioncommands = playerdirections
            if event.key == pygame.K_a:
                playerdirectioncommands = playerdirections

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
        displaypoweruptimer(poweruptimer)
        poweruptimer -= 1
        if poweruptimer <= 0:
            powerup = False
            poweruptimer = 599

    pygame.display.update()

pygame.quit()
