import pygame
import constants
pygame.init()

class Wall():
    def __init__(self, spawnx, spawny, width, height, colour=constants.COLOURS[constants.BLUE]):
        self.spawnx = spawnx
        self.spawny = spawny
        self.width = width
        self.height = height
        self.colour = colour
        self.wall = pygame.Rect(self.spawnx, self.spawny, self.width, self.height)
    
    def getXPositions(self):
        return self.positionsTop, self.positionsBottom
    
    def getYPositions(self):
        return self.positionsLeft, self.positionsRight

def drawborderwalls():
    pygame.draw.rect(constants.screen, constants.COLOURS[constants.BLUE], walls[0][0].wall)
    pygame.draw.rect(constants.screen, constants.COLOURS[constants.BLUE], walls[0][1].wall)
    pygame.draw.rect(constants.screen, constants.COLOURS[constants.BLUE], walls[0][2].wall)
    pygame.draw.rect(constants.screen, constants.COLOURS[constants.BLUE], walls[0][3].wall)

walls = [[Wall(0, 0, constants.SCREEN_WIDTH, 32),                               #TOP    0
          Wall(0, constants.SCREEN_HEIGHT - 32 , constants.SCREEN_WIDTH, 32),   #BOTTOM 1
          Wall(0, 0, 32, constants.SCREEN_HEIGHT),                              #LEFT   2
          Wall(constants.SCREEN_WIDTH - 32, 0, 32, constants.SCREEN_HEIGHT)]    #RIGHT  3
         ]
