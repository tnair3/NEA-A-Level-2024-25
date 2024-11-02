import pygame
import pygame_menu.themes
import pygame_menu.widgets; pygame.init()
import pygame_menu

import tkinter
from pygame.locals import *

import pacman
import database
import constants

pygame.display.set_caption("A-Level Computer Science NEA")
pygame.display.set_icon(pygame.image.load(f"sprites/logo.png"))

width = constants.SCREEN_WIDTH
height = constants.SCREEN_HEIGHT
surface = pygame.display.set_mode((width, height))

username = "Tejas"

def checkusername(value):
    print(value)

def openplaygamemenu():
    mainmenu._open(playgamemenu)

def playgame():
    pacman.rungame(username, toggleswitch.get_value())
    playgamemenu._back()

def opensettingsmenu():
    mainmenu._open(settingsmenu)

def openaccountmanager():
    settingsmenu._open(accountmanager)

def openleaderboard():
    pass

def manageaccount():
    pass

mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
mytheme = pygame_menu.Theme(
                widget_font=pygame_menu.font.FONT_MUNRO,
                title_font=pygame_menu.font.FONT_MUNRO,
                title_font_size=75,
                widget_font_size=50,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE,
                background_color=(18, 18, 18))

#MAIN MENU ==========================================================================================================================================
mainmenu = pygame_menu.Menu("Pacman: Main Menu", width, height, 
                        center_content=True,
                        theme=mytheme,
                        mouse_enabled=False)
mainmenu.add.button('Play', openplaygamemenu)
mainmenu.add.button('Leaderboard', openleaderboard)
mainmenu.add.button('Settings', opensettingsmenu)
mainmenu.add.button('Exit', pygame_menu.events.EXIT)

#PLAY GAME MENU =====================================================================================================================================
playgamemenu = pygame_menu.Menu("Pacman: Play Game Settings", width, height, 
                        center_content=True,
                        theme=mytheme,
                        mouse_enabled=False)
toggleswitch = pygame_menu.widgets.ToggleSwitch(title="Maze Type", default_state=True, state_text=("Random", "Classic"), state_text_font_size=22)
playgamemenu.add.button('Play Game', playgame)
playgamemenu.add.generic_widget(toggleswitch, configure_defaults=True)
playgamemenu.add.button('Back', pygame_menu.events.BACK)

#SETTINGS ===========================================================================================================================================
settingsmenu = pygame_menu.Menu("Pacman: Settings", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
settingsmenu.add.button('Account Manager', openaccountmanager)
settingsmenu.add.button('Back', pygame_menu.events.BACK)

#ACCOUNTMANAGER =====================================================================================================================================
accountmanager = pygame_menu.Menu("Pacman: Account Manager", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
accountmanager.add.button('Account', manageaccount)
accountmanager.add.button('Back', pygame_menu.events.BACK)

#LOGIN MENU =========================================================================================================================================
loginmenu = pygame_menu.Menu("Pacman: Login", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
loginmenu.add.text_input('Username: ', default='', onreturn=checkusername)
loginmenu.add.text_input('Password: ', default='', password=True, onreturn=checkusername)
loginmenu.add.button('Login or Create Account')
loginmenu.add.button('Back', pygame_menu.events.BACK)

mainmenu.mainloop(surface)
print("hello")
