import pygame; pygame.init()

SCREEN_WIDTH = 1290
SCREEN_HEIGHT = 960
TILE = 95
font = pygame.font.Font('emulogic.ttf', 20)

gridx = 19
gridy = 21
indenty = (SCREEN_HEIGHT - (gridy * 45)) // 2
indentx = indenty

eastereggnames = [
    "The Dot Eater",
    "The Yellow Hero",
    "The Pixelated Pursuit",
    "The Gulp and Go",
    "The Dot Dash",
    "The Nibble and Zoom",
    "The Maze Maze",
    "The Dot Devourer",
    "The Power Pellet Prowler",
    "The Midnight Munch",
    "The Dot Dilemma"
]

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
           (110, 0, 0),         #DARKRED
           (181, 180, 176)      #LIGHTGREY
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
LIGHTGREY = 11

clock = pygame.time.Clock()

def quicksort(array, min, max, indextosort):
    def partition(array, min, max, indextosort):
        pivot = array[max][indextosort]
        i = min - 1
        for j in range(min, max):
            if array[j][indextosort] >= pivot:
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])
        (array[i + 1], array[max]) = (array[max], array[i + 1])

        return i + 1
    
    if min < max:
        partitioni = partition(array, min, max, indextosort)

        quicksort(array, min, partitioni - 1, indextosort) #Recursive left
        quicksort(array, partitioni + 1, max, indextosort) #Recursive right
    
    return array