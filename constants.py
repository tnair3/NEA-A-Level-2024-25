import pygame
import math
pygame.init()

SCREEN_WIDTH = 1175
SCREEN_HEIGHT = 960
font = pygame.font.Font('emulogic.ttf', 20)

gridx = 19
gridy = 21
indenty = (SCREEN_HEIGHT - (gridy * 45)) // 2
indentx = indenty

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
           (46, 12, 200),       #BLUE
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

clock = pygame.time.Clock()

def binary_Search(array, low, high, searchval):
    while low <= high:
        mid = low + (high - low) // 2
        
        if array[mid] == searchval:
            return mid
        
        elif array[mid] < searchval:
            low = mid + 1

        else:
            high = mid + 1
        
        return -1
