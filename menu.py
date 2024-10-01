import pygame
import pygame_menu
from pygame.locals import *


pygame.init()

def login():
    pass 


surface = pygame.display.set_mode((600, 400))
menu = pygame_menu.Menu("Tejas NEA", 600, 400, 
                        center_content=True, theme=pygame_menu.themes.THEME_DARK)
menu.add.button('Login', login())
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)