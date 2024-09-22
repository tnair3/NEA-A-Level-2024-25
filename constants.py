import pygame
import math
pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 950

CENTREX = SCREEN_WIDTH / 2
CENTREY = SCREEN_HEIGHT / 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
COLOURS = [(255, 0, 0),         #RED   
           (0, 255, 255),       #CYAN
           (255, 184, 82),      #ORANGE
           (255, 184, 255),     #PINK
           (255, 255, 0),       #YELLOW
           (0, 0, 0),           #BLACK
           (255, 255, 255),     #WHITE
           (5, 21, 156),        #BLUE
           (62, 62, 62),        #GREY
           (0, 255, 31),        #GREEN
           (110, 0, 0)          #DARKRED
           ] 
RED = 0
CYAN = 1
ORANGE = 2
PINK = 3
YELLOW = 4
BLACK = 5
WHITE = 6
BLUE = 7
GREY = 8
GREEN = 9
DARKRED = 10

PI = math.pi
