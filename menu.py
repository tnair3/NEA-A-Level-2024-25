import pygame
import pygame_menu.themes
import pygame_menu.widgets; pygame.init()
import pygame_menu
import datetime

from pygame.locals import *

import pacman
import database

from constants import SCREEN_WIDTH as width
from constants import SCREEN_HEIGHT as height

pygame.display.set_caption("A-Level Computer Science NEA")
pygame.display.set_icon(pygame.image.load(f"sprites/logo.png"))
surface = pygame.display.set_mode((width, height))

database.initialisedatabase()

username = "Anonymous"
reversecontrols = "sprites/pacman/powerups/controlreverse.png"
doublescore = "sprites/pacman/powerups/doublescore.png"
halfscore = "sprites/pacman/powerups/halfscore.png"
invincible = "sprites/pacman/powerups/pacimmune1.png"
pacslow = "sprites/pacman/powerups/pacslow1.png"
speed = "sprites/pacman/powerups/pacspeed1.png"
pacstun = "sprites/pacman/powerups/pacstop1.png"
ghostslow = "sprites/ghosts/powerups/blinkyslow.png"
ghoststun = "sprites/ghosts/powerups/blinkystop.png"
spritesheet = "sprites/NEA Spritesheet.png"

#SUBROUTINES ==========================================================================================================================================================================================
def checkusername(value):
    print(value)

def openplaygamemenu():
    mainmenu._open(playgamemenu)

def playgame():
    user, score, time, cleared, classic = pacman.rungame(username, toggleswitch.get_value())
    time = time // 60
    date = datetime.datetime.now()
    day, month, year = str(date.day), str(date.month), str(date.year)
    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    date = day + "." + month + "." + year
    
    database.addnewscores(user, date, time, score, cleared, classic)
    playgamemenu._back()

def opensettingsmenu():
    mainmenu._open(settingsmenu)

def openaccountmanager():
    if username == "Anonymous":
        settingsmenu._open(accountmanagernotsignedin)
    else:
        settingsmenu._open(accountmanager)

def openleaderboard(value):
    global scorestable
    scorestable = leaderboardmenu.add.table('Leaderboard Table')
    scorestable.default_cell_padding = 10
    scorestable.add_row(("Username", "Date", "Time", "Score", "Cleared", "Classic"))
    filtermenu._open(leaderboardmenu)
    if value == "None":
        value = None
    leaderboard = database.selectfromscores(value)
    for game in leaderboard:
        game = list(game)
        for i in range(len(game)):
            if game[i] == None:
                game[i] = ""
        scorestable.add_row(game)

def openfiltermenu():
    mainmenu._open(filtermenu)

def leaveleaderboard():
    leaderboardmenu.remove_widget(scorestable)
    leaderboardmenu._back()
    filtermenu._back()

def openpowerupmenu():
    playgamemenu._open(powerupmenu)

def openbadpowermenu():
    playgamemenu._open(badpowermenu)

def openspritesheet():
    settingsmenu._open(spritesheetmenu)

def signin():
    global username
    inputusername = usernamebox.get_value()
    inputpassword = passwordbox.get_value()
    accountexists, validpass = database.checklogindetails(inputusername, inputpassword)
    if not accountexists:
        accountmanagernotsignedin.add.label(f'Account Does Not Exist', font_size=22)
    elif accountexists:
        if validpass:
            username = inputusername
            resetaccountmanager()
            accountmanagernotsignedin._open(accountmanager)
        elif not validpass:
            accountmanagernotsignedin.add.label(f'Incorrect Password', font_size=22)

def resetaccountmanager():
    global margin, text
    accountmanager.remove_widget(margin)
    accountmanager.remove_widget(text)

    margin = pygame_menu.widgets.VMargin(100)
    text = pygame_menu.widgets.Label(f'Signed in as {username}')
    accountmanager.add.generic_widget(margin, configure_defaults=True)
    accountmanager.add.generic_widget(text, configure_defaults=True)

def createaccount():
    global username
    inputusername = usernamebox.get_value()
    inputpassword = passwordbox.get_value()
    accountadded = database.addnewlogindetails(inputusername, inputpassword)
    if not accountadded:
        accountmanagernotsignedin.add.label(f'Username already used', font_size=22)
    else:
        username = inputusername
        resetaccountmanager()
        accountmanagernotsignedin._open(accountmanager)

def logout():
    global username
    username = "Anonymous"
    resetaccountmanagernotsignedin()
    resetaccountmanager()
    accountmanager._back()
    accountmanagernotsignedin._back()
    settingsmenu._back()

def exitaccountmanager():
    accountmanager._back()
    accountmanagernotsignedin._back()
    settingsmenu._back()

def resetaccountmanagernotsignedin():
    global usernamebox, passwordbox, signinbox, createaccountbox, backbox
    accountmanagernotsignedin.clear()

    accountmanagernotsignedin.add.label('PACMAN', font_size=72)
    accountmanagernotsignedin.add.label('Account Manager', font_size=32)
    accountmanagernotsignedin.add.label('Not Signed In', font_size=22)
    accountmanagernotsignedin.add.label('', font_size=32)

    usernamebox = pygame_menu.widgets.TextInput(title="Username: ", default="")
    passwordbox = pygame_menu.widgets.TextInput(title="Password: ", password=True, default="")
    signinbox = pygame_menu.widgets.Button("Sign In", onreturn=signin)
    createaccountbox = pygame_menu.widgets.Button("Create Account", onreturn=createaccount)
    backbox = pygame_menu.widgets.Button("Back", onreturn=back)
    accountmanagernotsignedin.add.generic_widget(usernamebox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(passwordbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(signinbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(createaccountbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(backbox, configure_defaults=True)

def back():
    accountmanagernotsignedin._back()

def openchangeusernamemenu():
    accountmanager._open(changeusernamemenu)

def openchangepasswordmenu():
    accountmanager._open(changepasswordmenu)

def changeusername(newusername):
    global username, text
    success = database.updatelogindetails(username, newusername, None)
    if success:
        username = newusername
        accountmanager.remove_widget(text)
        text = pygame_menu.widgets.Label(f'Signed in as {username}')
        accountmanager.add.generic_widget(text, configure_defaults=True)
        changeusernamemenu._back()

def changepassword(newpassword):
    database.updatelogindetails(username, None, newpassword)
    changepasswordmenu._back()

#MENUS ================================================================================================================================================================================================
mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
mytheme = pygame_menu.Theme(
                widget_font=pygame_menu.font.FONT_MUNRO,
                title_font_size=75,
                widget_font_size=50,
                title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                background_color=(18, 18, 18))

#MAIN MENU
if True:
    mainmenu = pygame_menu.Menu("", width, height, 
                            center_content=True,
                            theme=mytheme,
                            mouse_enabled=False)
    mainmenu.add.label('PACMAN', font_size=72)
    mainmenu.add.label('Main Menu', font_size=32)
    mainmenu.add.label('Game created by Tejas Nair', font_size=32)
    mainmenu.add.label('', font_size=32)
    mainmenu.add.button('Play', openplaygamemenu)
    mainmenu.add.label('', font_size=12)
    mainmenu.add.button('Leaderboard', openfiltermenu)
    mainmenu.add.button('Settings', opensettingsmenu)
    mainmenu.add.button('Exit', pygame_menu.events.EXIT)


#PLAY GAME MENU 
if True:
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
    playgamemenu.add.button('View Powerup Effects', openpowerupmenu)
    playgamemenu.add.button('View Bad Power Pellet Effects', openbadpowermenu)
    playgamemenu.add.button('Back', pygame_menu.events.BACK)

#POWERUP MENU 
if True:
    powerupmenu = pygame_menu.Menu("", width, height, 
                            center_content=True,
                            theme=mytheme)
    powerupmenu.add.label('PACMAN', font_size=72)
    powerupmenu.add.label('Powerups', font_size=32)
    powerupmenu.add.label('', font_size=32)

    powerupmenu.add.button('Back', pygame_menu.events.BACK, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Speed', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.image(speed, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Pacman travels at a faster speed for 5 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Credit: Victor A', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Slowness', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.image(ghostslow, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Ghosts travel at a slower speed for 5 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Stunned', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.image(ghoststun, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Ghosts cannot move for 5 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Credit: Victor B', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Imprisoned', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Ghosts reset at the ghost box', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Invincibility', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.image(invincible, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Pacman cannot be killed by the ghosts for 10 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Credit: Adeshola', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Good Luck', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.image(doublescore, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Pellets and fruits consumed give double score for 12 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Credit: Victor A', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('+1', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Get an extra life', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

    powerupmenu.add.label('Warp', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('Get teleported to a random location on the map', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    powerupmenu.add.label('', font_size=22)

#BAD POWER MENU 
if True:
    badpowermenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,)
    badpowermenu.add.label('PACMAN', font_size=72)
    badpowermenu.add.label('Bad Power Pellet Effects', font_size=32)
    badpowermenu.add.label('', font_size=32)

    badpowermenu.add.button('Back', pygame_menu.events.BACK, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)

    badpowermenu.add.label('Slowness', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.image(pacslow, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Player is slowed for 2 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Credit: Raven', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)

    badpowermenu.add.label('Confusion', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.image(reversecontrols, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Controls are reversed for 5 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Credit: Raven', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)

    badpowermenu.add.label('Invisibility', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Ghosts are invisible for 2 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Credit: Antonis', font_size=28, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)

    badpowermenu.add.label('Stunned', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.image(pacstun, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Player cannot move for 1 second', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)

    badpowermenu.add.label('Bad Luck', font_size=48, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.image(halfscore, scale=(2, 2),align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('Pellets and fruits consumed give half score for 12 seconds', font_size=32, align=pygame_menu.locals.ALIGN_LEFT)
    badpowermenu.add.label('', font_size=22)


#SETTINGS 
if True:
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

#ACCOUNT MANAGER NOT SIGNED IN 
if True:
    accountmanagernotsignedin = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    accountmanagernotsignedin.add.label('PACMAN', font_size=72)
    accountmanagernotsignedin.add.label('Account Manager', font_size=32)
    accountmanagernotsignedin.add.label('Not Signed In', font_size=22)
    accountmanagernotsignedin.add.label('', font_size=32)

    usernamebox = pygame_menu.widgets.TextInput(title="Username: ", default="")
    passwordbox = pygame_menu.widgets.TextInput(title="Password: ", password=True, default="")
    signinbox = pygame_menu.widgets.Button("Sign In", onreturn=signin)
    createaccountbox = pygame_menu.widgets.Button("Create Account", onreturn=createaccount)
    backbox = pygame_menu.widgets.Button("Back", onreturn=back)

    accountmanagernotsignedin.add.generic_widget(usernamebox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(passwordbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(signinbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(createaccountbox, configure_defaults=True)
    accountmanagernotsignedin.add.generic_widget(backbox, configure_defaults=True)

#ACCOUNT MENU 
if True:
    accountmanager = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    accountmanager.add.label('PACMAN', font_size=72)
    accountmanager.add.label('Account Manager', font_size=32)
    accountmanager.add.label('', font_size=32)
    accountmanager.add.button('Change Username', openchangeusernamemenu)
    accountmanager.add.button('Change Password', openchangepasswordmenu)
    accountmanager.add.button('Log Out', logout)
    accountmanager.add.button('Back', exitaccountmanager)

    margin = pygame_menu.widgets.VMargin(100)
    text = pygame_menu.widgets.Label(f'Signed in as {username}')
    accountmanager.add.generic_widget(margin, configure_defaults=True)
    accountmanager.add.generic_widget(text, configure_defaults=True)

#CHANGE USERNAME MENU
if True:
    changeusernamemenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    changeusernamemenu.add.label('PACMAN', font_size=72)
    changeusernamemenu.add.label('Change Username', font_size=32)
    changeusernamemenu.add.label('', font_size=32)
    changeusernamemenu.add.text_input('New Username: ', default='', onreturn=changeusername)
    changeusernamemenu.add.button('Back', pygame_menu.events.BACK)

#CHANGE PASSWORD MENU
if True:
    changepasswordmenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    changepasswordmenu.add.label('PACMAN', font_size=72)
    changepasswordmenu.add.label('Change Password', font_size=32)
    changepasswordmenu.add.label('', font_size=32)
    changepasswordmenu.add.text_input('New Password: ', default='', password=True, onreturn=changepassword)
    changepasswordmenu.add.button('Back', pygame_menu.events.BACK)

#SPRITESHEET 
if True:
    spritesheetmenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    spritesheetmenu.add.label('PACMAN', font_size=72)
    spritesheetmenu.add.label('Spritesheet', font_size=32)
    spritesheetmenu.add.label('Sprites created by me', font_size=28)
    spritesheetmenu.add.label('', font_size=32)
    spritesheetmenu.add.button('Back', pygame_menu.events.BACK)
    spritesheetmenu.add.image(spritesheet, scale=(2, 2))


#FILTER MENU 
if True:
    filtermenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme,
                            mouse_enabled=False)
    filtermenu.add.label('PACMAN', font_size=72)
    filtermenu.add.label('Filter Leaderboard', font_size=32)
    filtermenu.add.label('', font_size=32)
    filtermenu.add.text_input('Filter: ', default='None', onreturn=openleaderboard)
    filtermenu.add.button('Back', pygame_menu.events.BACK)

#LEADERBOARDS 
if True:
    leaderboardmenu = pygame_menu.Menu("", width, height, 
                            center_content=True, 
                            theme=mytheme)
    leaderboardmenu.add.label('PACMAN', font_size=72)
    leaderboardmenu.add.label('Leaderboard', font_size=32)
    leaderboardmenu.add.label('', font_size=2)
    leaderboardmenu.add.button('Menu', leaveleaderboard, align=pygame_menu.locals.ALIGN_LEFT)

mainmenu.mainloop(surface)