import pygame
import pygame_menu.themes
import pygame_menu.widgets; pygame.init()
import pygame_menu
import datetime

from pygame.locals import *

import pacman
import database
import constants

pygame.display.set_caption("A-Level Computer Science NEA")
pygame.display.set_icon(pygame.image.load(f"sprites/logo.png"))

width = constants.SCREEN_WIDTH
height = constants.SCREEN_HEIGHT
surface = pygame.display.set_mode((width, height))

database.initialisedatabase()
username = "Anonymous"

def checkusername(value):
    print(value)

def openplaygamemenu():
    mainmenu._open(playgamemenu)

def playgame():
    user, score, time = pacman.rungame(username, toggleswitch.get_value())
    time = time // 60
    date = datetime.datetime.now()
    day, month, year = str(date.day), str(date.month), str(date.year)
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    date = day + "." + month + "." + year
    
    database.addnewscores(user, date, time, score)
    playgamemenu._back()

def opensettingsmenu():
    mainmenu._open(settingsmenu)

def openaccountmanager():
    pass

def openleaderboard(value):
    global scorestable
    scorestable = leaderboardmenu.add.table('Leaderboard Table')
    scorestable.default_cell_padding = 10
    scorestable.add_row(("Username", "Date", "Time", "Score"))
    filtermenu._open(leaderboardmenu)
    if value == "None":
        value = None
    leaderboard = database.selectfromscores(value)
    for match in leaderboard:
        match = list(match)
        for i in range(len(match)):
            if match[i] == None:
                match[i] = ""
        scorestable.add_row(match)

def openfiltermenu():
    mainmenu._open(filtermenu)

def leaveleaderboard():
    leaderboardmenu.remove_widget(scorestable)
    leaderboardmenu._back()
    filtermenu._back()

def openspritesheet():
    pass

def manageaccount():
    pass

mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
mytheme = pygame_menu.Theme(
                widget_font=pygame_menu.font.FONT_MUNRO,
                title_font_size=75,
                widget_font_size=50,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                background_color=(18, 18, 18))

#MAIN MENU ==========================================================================================================================================
mainmenu = pygame_menu.Menu("", width, height, 
                        center_content=True,
                        theme=mytheme,
                        mouse_enabled=False)
mainmenu.add.label('PACMAN', font_size=72)
mainmenu.add.label('Main Menu', font_size=32)
mainmenu.add.label('', font_size=32)
mainmenu.add.button('Play', openplaygamemenu)
mainmenu.add.button('Leaderboard', openfiltermenu)
mainmenu.add.button('Settings', opensettingsmenu)
mainmenu.add.button('Exit', pygame_menu.events.EXIT)

#PLAY GAME MENU =====================================================================================================================================
playgamemenu = pygame_menu.Menu("", width, height, 
                        center_content=True,
                        theme=mytheme,
                        mouse_enabled=False)
toggleswitch = pygame_menu.widgets.ToggleSwitch(title="Maze Type", default_state=True, state_text=("Random", "Classic"), state_text_font_size=22)
playgamemenu.add.label('PACMAN', font_size=72)
playgamemenu.add.label('Game Settings', font_size=32)
playgamemenu.add.label('', font_size=32)
playgamemenu.add.button('Play Game', playgame)
playgamemenu.add.generic_widget(toggleswitch, configure_defaults=True)
playgamemenu.add.button('Back', pygame_menu.events.BACK)

#SETTINGS ===========================================================================================================================================
settingsmenu = pygame_menu.Menu("", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
settingsmenu.add.label('PACMAN', font_size=72)
settingsmenu.add.label('Options', font_size=32)
settingsmenu.add.label('', font_size=32)
settingsmenu.add.button('Account Manager', openaccountmanager)
settingsmenu.add.button('View Spritesheet', openspritesheet)
settingsmenu.add.button('Back', pygame_menu.events.BACK)

#LEADERBOARDS =======================================================================================================================================
leaderboardmenu = pygame_menu.Menu("", width, height, 
                        center_content=True, 
                        theme=mytheme)
leaderboardmenu.add.label('PACMAN', font_size=72)
leaderboardmenu.add.label('Leaderboard', font_size=32)
leaderboardmenu.add.label('', font_size=2)
leaderboardmenu.add.button('Menu', leaveleaderboard, align=pygame_menu.locals.ALIGN_LEFT)

#FILTER MENU ========================================================================================================================================
filtermenu = pygame_menu.Menu("", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
filtermenu.add.label('PACMAN', font_size=72)
filtermenu.add.label('Filter Leaderboard', font_size=32)
filtermenu.add.label('', font_size=32)
filtermenu.add.text_input('Filter: ', default='None', onreturn=openleaderboard)
filtermenu.add.button('Back', pygame_menu.events.BACK)

#LOGIN MENU =========================================================================================================================================
loginmenu = pygame_menu.Menu("", width, height, 
                        center_content=True, 
                        theme=mytheme,
                        mouse_enabled=False)
loginmenu.add.label('PACMAN', font_size=72)
loginmenu.add.label('Login', font_size=32)
loginmenu.add.label('', font_size=32)
loginmenu.add.text_input('Username: ', default='', onreturn=checkusername)
loginmenu.add.text_input('Password: ', default='', password=True, onreturn=checkusername)
loginmenu.add.button('Login or Create Account')
loginmenu.add.button('Back', pygame_menu.events.BACK)

mainmenu.mainloop(surface)
print("hello")