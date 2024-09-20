import pygame
import constants
import wallgeneration

pygame.init()

screen = constants.screen
pygame.display.set_caption("NEA: Pacman Game")

#OBJECTS ============================================================================================================== OBJECTS
class Player():
    def __init__(self, speed, posX=constants.CENTREX, posY=constants.CENTREY + 100, size=20, colour=constants.COLOURS[constants.YELLOW]):
        self.colour = colour
        self.size = size
        self.posx = posX - self.size/2
        self.posy = posY - self.size/2
        self.speed = speed
        self.character = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def movement(self, key):
        if key == 0:
            return 0
        
        else:
            nocollisions = 0
            for i in range(0, len(wallgeneration.walls[0])):
                if not self.character.colliderect(wallgeneration.walls[0][i].wall):
                    nocollisions += 1

            if nocollisions == 4:
                for k in range(0, self.speed):
                    if key == "a":
                        self.character.move_ip(-1, 0)
                        self.posx -= 1

                    elif key == "d":
                        self.character.move_ip(1, 0)
                        self.posx += 1

                    elif key == "w":
                        self.character.move_ip(0, -1)
                        self.posy -= 1

                    elif key == "s":
                        self.character.move_ip(0, 1)
                        self.posy += 1 
                return key
            
            else:
                for k in range(0, self.speed):
                    if key == "a":
                        self.character.move_ip(1, 0)
                        self.posx += 1

                    elif key == "d":
                        self.character.move_ip(-1, 0)
                        self.posx -= 1

                    elif key == "w":
                        self.character.move_ip(0, 1)
                        self.posy += 1

                    elif key == "s":
                        self.character.move_ip(0, -1)
                        self.posy -= 1
                return 0

    def detectghostcollision(self):
        if (self.character.colliderect(ghosts[0].entity) or 
            self.character.colliderect(ghosts[1].entity) or 
            self.character.colliderect(ghosts[2].entity) or 
            self.character.colliderect(ghosts[3].entity)):
            return True
        else:
            return False

    def getposx(self):
        return self.posx
    
    def getposy(self):
        return self.posy
    
    def getspeed(self):
        return self.speed

class Ghost():
    def __init__(self, colourchosen, speed, offset, posX=constants.CENTREX, posY=(constants.CENTREY) - 100, size=20, colour=constants.COLOURS):
        self.colour = colour[colourchosen]
        self.colourindex = colourchosen
        self.size = size
        self.posx = posX + offset - (self.size/2)
        self.posy = posY - self.size/2
        self.speed = speed
        self.entity = pygame.Rect(self.posx, self.posy, self.size, self.size)

    def follow(self, playerposx, playerposy):
        for i in range(0, self.speed):
            if self.posx < playerposx:
                self.entity.move_ip(1, 0)
                self.posx += 1

            elif self.posx > playerposx:
                self.entity.move_ip(-1, 0)
                self.posx -= 1

            elif self.posy < playerposy:
                self.entity.move_ip(0, 1)
                self.posy += 1

            elif self.posy > playerposy:
                self.entity.move_ip(0, -1)
                self.posy -= 1

    def getcolour(self):
        return self.colourindex

#SUBROUTINES ========================================================================================================== SUBROUTINES
def displayEntities():
    pygame.draw.rect(constants.screen, constants.COLOURS[4], user.character)

    pygame.draw.rect(constants.screen, constants.COLOURS[ghosts[0].getcolour()], ghosts[0].entity)
    pygame.draw.rect(constants.screen, constants.COLOURS[ghosts[1].getcolour()], ghosts[1].entity)
    pygame.draw.rect(constants.screen, constants.COLOURS[ghosts[2].getcolour()], ghosts[2].entity)
    pygame.draw.rect(constants.screen, constants.COLOURS[ghosts[3].getcolour()], ghosts[3].entity)

def ghostsFollow():
    for i in range(0, 4):
        ghosts[i].follow(user.getposx(), user.getposy())

def checkforcollisions(objectselfvar):
    pass

def displaygameover():
    pass

#DEFINING VARIABLES =================================================================================================== DEFINING VARIABLES
user = Player(2)
ghosts = [Ghost(constants.RED, 1, 500),
          Ghost(constants.CYAN, 1, 250),
          Ghost(constants.ORANGE, 1, -250),
          Ghost(constants.PINK, 1, -500)
          ]

clock = pygame.time.Clock()

run = True
continueloop = True
gameover = False
centreofscreen = pygame.Rect(constants.CENTREX, constants.CENTREY, 1, 1)
mostrecentkey = "0"

#GAME LOOP ============================================================================================================ GAME LOOP
while continueloop:
    clock.tick(120)
    constants.screen.fill(constants.COLOURS[constants.BLACK])
    if run:
        displayEntities()
        wallgeneration.drawborderwalls()
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            mostrecentkey = "w"
        elif key[pygame.K_a]:
            mostrecentkey = "a"
        elif key[pygame.K_s]:
            mostrecentkey = "s"
        elif key[pygame.K_d]:
            mostrecentkey = "d"
        mostrecentkey = user.movement(mostrecentkey)
        ghostsFollow()

        pygame.draw.rect(constants.screen, constants.COLOURS[constants.WHITE], centreofscreen)

        gameover = user.detectghostcollision()
        if gameover:
            run = False
    else:
        wallgeneration.drawborderwalls()
        displaygameover()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continueloop = False
    pygame.display.update()

pygame.quit()
