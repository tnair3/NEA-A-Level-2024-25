import pygame
import constants
pygame.init()


pygame.display.set_caption("NEA: Pacman Game")

#OBJECTS ============================================================================================================== OBJECTS
class Player():
    def __init__(self, speed, posX=constants.SCREEN_WIDTH/2, posY=constants.SCREEN_HEIGHT/2, size=16, colour=constants.COLOURS[constants.YELLOW]):
        self.colour = colour
        self.size = size
        self.posx = posX
        self.rightborder = self.posx + size
        self.posy = posY
        self.bottomborder = self.posy + size
        self.speed = speed
        self.character = pygame.Rect(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2, self.size, self.size)

    def movement(self, key):
        for k in range(0, self.speed):
            if key[pygame.K_a]:
                self.character.move_ip(-1, 0)
                self.posx -= 1
                self.rightborder -= 1

            elif key[pygame.K_d]:
                self.character.move_ip(1, 0)
                self.posx += 1
                self.rightborder += 1

            elif key[pygame.K_w]:
                self.character.move_ip(0, -1)
                self.posy -= 1
                self.bottomborder -= 1

            elif key[pygame.K_s]:
                self.character.move_ip(0, 1)
                self.posy += 1
                self.bottomborder += 1

    def getposx(self):
        return self.posx
    
    def getposy(self):
        return self.posy
    
    def getspeed(self):
        return self.speed

class Ghost():
    def __init__(self, colourchosen, speed, offset, posX=constants.SCREEN_WIDTH/2, posY=(constants.SCREEN_HEIGHT/2) + 100, size=16, colour=constants.COLOURS):
        self.colour = colour[colourchosen]
        self.colourindex = colourchosen
        self.size = size
        self.posx = posX + offset
        self.posy = posY
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
    ghosts[0].follow(user.getposx(), user.getposy())
    ghosts[1].follow(user.getposx(), user.getposy())
    ghosts[2].follow(user.getposx(), user.getposy())
    ghosts[3].follow(user.getposx(), user.getposy())

#DEFINING VARIABLES =================================================================================================== DEFINING VARIABLES
user = Player(2)
ghosts = [Ghost(constants.RED, 1, 500),
          Ghost(constants.CYAN, 1, 250),
          Ghost(constants.ORANGE, 1, -250),
          Ghost(constants.PINK, 1, -500)
          ]

clock = pygame.time.Clock()

run = True
import wallgeneration

#GAME LOOP ============================================================================================================ GAME LOOP
while run:
    clock.tick(120)
    constants.screen.fill(constants.COLOURS[5])

    displayEntities()
    wallgeneration.drawborderwalls()

    user.movement(pygame.key.get_pressed())
    ghostsFollow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()