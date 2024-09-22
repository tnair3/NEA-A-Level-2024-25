import pygame
import math
import constants
import copy
from constants import PI as PI
from constants import screen as screen

pygame.init()
pygame.display.set_caption("NEA: Pacman Game")

#OBJECTS ============================================================================================================== OBJECTS
class Ghost():
    def __init__(self, ghostid, xcoord, ycoord, target, speed, direction, dead, box, img):
        self.ghostid = ghostid
        self.x_pos = xcoord
        self.y_pos = ycoord
        self.centrex = self.x_pos + 23
        self.centrey = self.y_pos + 23
        self.target = target
        self.speed = speed
        self.direction = direction
        self.dead = dead
        self.inbox = box
        self.image = img

        self.turns, self.inbox = self.checkcollisions()
        self.rect = self.drawghost()

    def checkcollisions(self):
        num1 = ((constants.SCREEN_HEIGHT - 50) // 32)
        num2 = (constants.SCREEN_WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.centrex // 30 < 29:
            if level[(self.centrey - num3) // num1][self.centrex // num2] == 9:
                self.turns[2] = True
            if level[self.centrey // num1][(self.centrex - num3) // num2] < 3 \
                    or (level[self.centrey // num1][(self.centrex - num3) // num2] == 9 and (
                    self.inbox or self.dead)):
                self.turns[1] = True
            if level[self.centrey // num1][(self.centrex + num3) // num2] < 3 \
                    or (level[self.centrey // num1][(self.centrex + num3) // num2] == 9 and (
                    self.inbox or self.dead)):
                self.turns[0] = True
            if level[(self.centrey + num3) // num1][self.centrex // num2] < 3 \
                    or (level[(self.centrey + num3) // num1][self.centrex // num2] == 9 and (
                    self.inbox or self.dead)):
                self.turns[3] = True
            if level[(self.centrey - num3) // num1][self.centrex // num2] < 3 \
                    or (level[(self.centrey - num3) // num1][self.centrex // num2] == 9 and (
                    self.inbox or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.centrex % num2 <= 18:
                    if level[(self.centrey + num3) // num1][self.centrex // num2] < 3 \
                            or (level[(self.centrey + num3) // num1][self.centrex // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[3] = True
                    if level[(self.centrey - num3) // num1][self.centrex // num2] < 3 \
                            or (level[(self.centrey - num3) // num1][self.centrex // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[2] = True
                if 12 <= self.centrey % num1 <= 18:
                    if level[self.centrey // num1][(self.centrex - num2) // num2] < 3 \
                            or (level[self.centrey // num1][(self.centrex - num2) // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[1] = True
                    if level[self.centrey // num1][(self.centrex + num2) // num2] < 3 \
                            or (level[self.centrey // num1][(self.centrex + num2) // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.centrex % num2 <= 18:
                    if level[(self.centrey + num3) // num1][self.centrex // num2] < 3 \
                            or (level[(self.centrey + num3) // num1][self.centrex // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[3] = True
                    if level[(self.centrey - num3) // num1][self.centrex // num2] < 3 \
                            or (level[(self.centrey - num3) // num1][self.centrex // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[2] = True
                if 12 <= self.centrey % num1 <= 18:
                    if level[self.centrey // num1][(self.centrex - num3) // num2] < 3 \
                            or (level[self.centrey // num1][(self.centrex - num3) // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[1] = True
                    if level[self.centrey // num1][(self.centrex + num3) // num2] < 3 \
                            or (level[self.centrey // num1][(self.centrex + num3) // num2] == 9 and (
                            self.inbox or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 540 and 370 < self.y_pos < 480:
            self.inbox = True
        else:
            self.inbox = False
        return self.turns, self.inbox

    def drawghost(self):
        if (not powerup and not self.dead) or (eatenghosts[self.ghostid] and powerup and not self.dead):
            screen.blit(self.image, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eatenghosts[self.ghostid]:
            screen.blit(scaredimg, (self.x_pos, self.y_pos))
        else:
            screen.blit(deadimg, (self.x_pos, self.y_pos))
        ghostrectangle = pygame.rect.Rect((self.centrex - 18, self.centrey - 18), (36, 36))
        return ghostrectangle

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

#MAZES ================================================================================================================ MAZES
mazes = [
   [[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 9, 9, 9, 9, 9, 9, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
    [4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
    [5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
    [3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
    [3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
    [3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
    [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]]
]

maze0name = "The Classic"

#SUBROUTINES ========================================================================================================== SUBROUTINES
def draw_map():
    num1 = ((constants.SCREEN_HEIGHT - 50) // 32)
    num2 = (constants.SCREEN_WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, constants.COLOURS[constants.WHITE], (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if level[i][j] == 3:
                pygame.draw.line(screen, constants.COLOURS[constants.BLUE], (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, constants.COLOURS[constants.BLUE], (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, constants.COLOURS[constants.BLUE], [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, constants.COLOURS[constants.BLUE],
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, constants.COLOURS[constants.BLUE], [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, constants.COLOURS[constants.BLUE],
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, constants.COLOURS[constants.WHITE], (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def displayplayer():
    #0RIGHT, 1LEFT, 2UP, 3DOWN
    if direction == 0:
        screen.blit(playerimgs[counter // 7], (playerx, playery))
    elif direction == 1:
        screen.blit(pygame.transform.flip(playerimgs[counter // 7], True, False), (playerx, playery))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(playerimgs[counter // 7], 90), (playerx, playery))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(playerimgs[counter // 7], -90), (playerx, playery))

def checkplayerpos(centrex, centrey):
    turns = [False, False, False, False]
    num1 = (constants.SCREEN_HEIGHT - 50) // 32
    num2 = (constants.SCREEN_WIDTH // 30)
    num3 = 15

    if centrex // 30 < 29:
        if direction == 0:
            if level[centrey // num1][(centrex - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centrey // num1][(centrex + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centrey + num3) // num1][centrex // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centrey - num3) // num1][centrex // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centrex % num2 <= 18:
                if level[(centrey + num3) // num1][centrex // num2] < 3:
                    turns[3] = True
                if level[(centrey - num3) // num1][centrex // num2] < 3:
                    turns[2] = True
            if 12 <= centrey % num1 <= 18:
                if level[centrey // num1][(centrex - num2) // num2] < 3:
                    turns[1] = True
                if level[centrey // num1][(centrex + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centrex % num2 <= 18:
                if level[(centrey + num1) // num1][centrex // num2] < 3:
                    turns[3] = True
                if level[(centrey - num1) // num1][centrex // num2] < 3:
                    turns[2] = True
            if 12 <= centrey % num1 <= 18:
                if level[centrey // num1][(centrex - num3) // num2] < 3:
                    turns[1] = True
                if level[centrey // num1][(centrex + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def playermovement(x, y):
    if direction == 0 and turnvalid[0]:
        x += playerspeed
    elif direction == 1 and turnvalid[1]:
        x -= playerspeed
    elif direction == 2 and turnvalid[2]:
        y -= playerspeed
    elif direction == 3 and turnvalid[3]:
        y += playerspeed
    
    return x, y

def gettargets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if playerx < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if playery < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eatenghosts[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eatenghosts[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (playerx, playery)
        else:
            blink_target = return_target
        if not inky.dead and not eatenghosts[1]:
            ink_target = (runaway_x, playery)
        elif not inky.dead and eatenghosts[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (playerx, playery)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (playerx, runaway_y)
        elif not pinky.dead and eatenghosts[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (playerx, playery)
        else:
            pink_target = return_target
        if not clyde.dead and not eatenghosts[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eatenghosts[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (playerx, playery)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (playerx, playery)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (playerx, playery)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (playerx, playery)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (playerx, playery)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

def checkifcollide(score, powerup, powersconsumed, eatenghosts):
    num1 = (constants.SCREEN_HEIGHT - 50) // 32
    num2 = constants.SCREEN_WIDTH // 30
    if 0 < playerx < 870:
        if level[playercentrey // num1][playercentrex // num2] == 1: #PELLET
            level[playercentrey // num1][playercentrex // num2] = 0
            score += 10
        if level[playercentrey // num1][playercentrex // num2] == 2: #POWERUP
            level[playercentrey // num1][playercentrex // num2] = 0
            score += 50
            powerup = True
            powersconsumed = 0
            eatenghosts = [False, False, False, False]
        
    return score, powerup, powersconsumed, eatenghosts

def displaymisc():
    scoretext = font.render(f'Score: {score}', True, constants.COLOURS[constants.WHITE])
    livestext = font.render(f'Lives:', True, constants.COLOURS[constants.WHITE])
    screen.blit(scoretext, (10, 920))
    screen.blit(livestext, (630, 920))
    if powerup:
        poweruptext = font.render(f'Powerup', True, constants.COLOURS[constants.WHITE])
        screen.blit(poweruptext, ((constants.SCREEN_WIDTH // 2) - 70, (constants.SCREEN_HEIGHT // 2) - 10))

        powerupcountdown = 10 - (powertimer // 60)
        if powerupcountdown == 0:
            powerupcountdown = 1
        poweruptimer = font.render(f'{powerupcountdown}', True, constants.COLOURS[constants.WHITE])
        screen.blit(poweruptimer, ((constants.SCREEN_WIDTH // 2) - 10, 920))
    
    for i in range(lives):
        screen.blit(pygame.transform.scale(playerimgs[len(playerimgs) - 1], (30, 30)), (750 + i * 40, 917))
    
    if gameover:
        gameovertextline1 = font.render(f'Game Over', True, constants.COLOURS[constants.DARKRED])
        gameovertextline2 = font.render(f'Spacebar to restart', True, constants.COLOURS[constants.WHITE])
        gameovertextline3 = font.render(f'Escape to exit', True, constants.COLOURS[constants.WHITE])

        screen.blit(gameovertextline1, (350, constants.SCREEN_HEIGHT // 2 - 140))
        screen.blit(gameovertextline2, (270, constants.SCREEN_HEIGHT // 2 - 90))
        screen.blit(gameovertextline3, (320, constants.SCREEN_HEIGHT // 2 - 40))

    if gamewon:
        gamewontextline1 = font.render(f'Game won', True, constants.COLOURS[constants.GREEN])
        gamewontextline2 = font.render(f'Spacebar to restart', True, constants.COLOURS[constants.WHITE])
        gamewontextline3 = font.render(f'Escape to exit', True, constants.COLOURS[constants.WHITE])

        screen.blit(gamewontextline1, (350, constants.SCREEN_HEIGHT // 2 - 140))
        screen.blit(gamewontextline2, (270, constants.SCREEN_HEIGHT // 2 - 90))
        screen.blit(gamewontextline3, (320, constants.SCREEN_HEIGHT // 2 - 40))

def displaystartuptimer(starttime):
    Time = 3
    if 60 < starttime < 120:
        Time = 2
    elif starttime >= 120:
        Time = 1
    timertext = font.render(f'{Time}', True, constants.COLOURS[constants.WHITE])
    if not gameover and not gamewon:
        screen.blit(timertext, (constants.SCREEN_WIDTH // 2 - 10, constants.SCREEN_HEIGHT // 2 - 140))

def loadplayerimgs():
    for i in range(0, 4):
        playerimgs.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacman{i}.png"), (45, 45)))
    for i in range(2, 0, -1):
        playerimgs.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacman{i}.png"), (45, 45)))
    playerimgs.append(pygame.transform.scale(pygame.image.load(f"sprites/pacman/pacman4.png"), (30, 30)))

#DEFINING VARIABLES =================================================================================================== DEFINING VARIABLES
clock = pygame.time.Clock()
fps = 60
run = True
font = pygame.font.Font('emulogic.ttf', 20)

level = copy.deepcopy(mazes[0])
turnvalid = [False, False, False, False]

flicker = False
counter = 0

score = 0
lives = 5
powerup = False
powertimer = 0
eatenghosts = [False, False, False, False]
movementallowed = False
startuptimer = 0
gameover = False
gamewon = False

playerimgs = []
loadplayerimgs()
playerx = (constants.SCREEN_WIDTH // 2) - 20
playery = 665
playerspeed = 2
direction = 0
directioncommand = 0

blinkyimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/blinky.png'), (45, 45))
pinkyimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/pinky.png'), (45, 45))
inkyimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/inky.png'), (45, 45))
clydeimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/clyde.png'), (45, 45))
scaredimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/scared.png'), (45, 45))
deadimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/dead.png'), (45, 45))

blinkyx = 56
blinkyy = 58
blinkydirection = 0

pinkyx = 370
pinkyy = 416
pinkydirection = 2

inkyx = 430
inkyy = 416
inkydirection = 2

clydex = 490
clydey = 416
clydedirection = 2

ghosttargets = [(playerx, playery), (playerx, playery), (playerx, playery), (playerx, playery)]
blinkydead = False
pinkydead = False
inkydead = False
clydedead = False

blinkybox = False
pinkybox = False
inkybox = False
clydebox = False

ghostspeeds = [2, 2, 2, 2]

spookyimg = pygame.transform.scale(pygame.image.load(f'sprites/ghosts/spooky.png'), (45, 45))

#GAME LOOP ============================================================================================================ GAME LOOP

while run:
    clock.tick(fps)
    if counter < 41:
        counter += 1
        if counter > 20:
            flicker = False
    else:
        counter = 0
        flicker = True

    if powerup and powertimer < 600:
        powertimer += 1
    elif powerup and powertimer >= 600:
        powertimer = 0
        powerup = False
        eatenghosts = [False, False, False, False]
    if startuptimer < 180 and not gameover and not gamewon:
        movementallowed = False
        startuptimer += 1
    elif startuptimer < 180 and (gameover or gamewon):
        pass
    else:
        movementallowed = True

    constants.screen.fill(constants.COLOURS[constants.BLACK])

    draw_map()
    playercentrex = playerx + 22
    playercentrey = playery + 22

    if powerup:
        ghostspeeds = [1, 1, 1, 1]
    else:
        ghostspeeds = [2, 2, 2, 2]
    if eatenghosts[0]:
        ghostspeeds[0] = 2
    if eatenghosts[1]:
        ghostspeeds[1] = 2
    if eatenghosts[2]:
        ghostspeeds[2] = 2
    if eatenghosts[3]:
        ghostspeeds[3] = 2
    if blinkydead:
        ghostspeeds[0] = 4
    if pinkydead:
        ghostspeeds[1] = 4
    if inkydead:
        ghostspeeds[2] = 4
    if clydedead:
        ghostspeeds[3] = 4

    gamewon = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            gamewon = False

    playercircle = pygame.draw.circle(screen, constants.COLOURS[constants.BLACK], (playercentrex, playercentrey), 21, 2)
    displayplayer()
    displaymisc()

    blinky = Ghost(0, blinkyx, blinkyy, ghosttargets[0], ghostspeeds[0], blinkydirection, blinkydead, blinkybox, blinkyimg)
    pinky = Ghost(1, pinkyx, pinkyy, ghosttargets[1], ghostspeeds[1], pinkydirection, pinkydead, pinkybox, pinkyimg)
    inky = Ghost(2, inkyx, inkyy, ghosttargets[2], ghostspeeds[2], inkydirection, inkydead, inkybox, inkyimg)
    clyde = Ghost(3, clydex, clydey, ghosttargets[3], ghostspeeds[3], clydedirection, clydedead, clydebox, clydeimg)
    ghosttargets = gettargets(blinkyx, blinkyy, pinkyx, pinkyy, inkyx, inkyy, clydex, clydey)

    turnvalid = checkplayerpos(playercentrex, playercentrey)
    if movementallowed:
        playerx, playery = playermovement(playerx, playery)
        blinkyx, blinkyy, blinkydirection = blinky.move_blinky()
        pinkyx, pinkyy, pinkydirection = pinky.move_pinky()
        inkyx, inkyy, inkydirection = inky.move_inky()
        clydex, clydey, clydedirection = clyde.move_clyde()
    else:
        displaystartuptimer(startuptimer)
    score, powerup, powertimer, eatenghosts = checkifcollide(score, powerup, powertimer, eatenghosts)


    if not powerup:
        if (playercircle.colliderect(blinky.rect) and not blinky.dead) or \
            (playercircle.colliderect(pinky.rect) and not pinky.dead) or \
            (playercircle.colliderect(inky.rect) and not inky.dead) or \
            (playercircle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startuptimer = 0

                blinkyx = 56
                blinkyy = 58
                blinkydirection = 0
                pinkyx = 370
                pinkyy = 416
                pinkydirection = 2
                inkyx = 430
                inkyy = 416
                inkydirection = 2
                clydex = 490
                clydey = 416
                clydedirection = 2
                playerx = (constants.SCREEN_WIDTH // 2) - 20
                playery = 665
                direction = 0
                directioncommand = 0
                ghostspeeds = [2, 2, 2, 2]

                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False

                powerup = False
                powertimer = 0
                eatenghosts = [False, False, False, False]
                movementallowed = False
            else:
                gameover = True
                startuptimer = 0
                blinkyx = 9000
                blinkyy = 9000
                blinkydirection = 0
                pinkyx = 9000
                pinkyy = 9000
                pinkydirection = 2
                inkyx = 9000
                inkyy = 9000
                inkydirection = 2
                clydex = 9000
                clydey = 9000
                clydedirection = 2
                playerx = 9000
                playery = 9000
                direction = 0
                directioncommand = 0
                ghostspeeds = [2, 2, 2, 2]

                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False

                powerup = False
                powertimer = 0
                eatenghosts = [False, False, False, False]
                movementallowed = False
  
    if powerup and (playercircle.colliderect(blinky.rect) and eatenghosts[0] and not blinky.dead):
        if lives > 0:
            lives -= 1
            startuptimer = 0

            blinkyx = 56
            blinkyy = 58
            blinkydirection = 0
            pinkyx = 370
            pinkyy = 416
            pinkydirection = 2
            inkyx = 430
            inkyy = 416
            inkydirection = 2
            clydex = 490
            clydey = 416
            clydedirection = 2
            playerx = (constants.SCREEN_WIDTH // 2) - 20
            playery = 665
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
        else:
            gameover = True
            startuptimer = 0
            blinkyx = 9000
            blinkyy = 9000
            blinkydirection = 0
            pinkyx = 9000
            pinkyy = 9000
            pinkydirection = 2
            inkyx = 9000
            inkyy = 9000
            inkydirection = 2
            clydex = 9000
            clydey = 9000
            clydedirection = 2
            playerx = 9000
            playery = 9000
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
    if powerup and (playercircle.colliderect(pinky.rect) and eatenghosts[1] and not pinky.dead):
        if lives > 0:
            lives -= 1
            startuptimer = 0

            blinkyx = 56
            blinkyy = 58
            blinkydirection = 0
            pinkyx = 370
            pinkyy = 416
            pinkydirection = 2
            inkyx = 430
            inkyy = 416
            inkydirection = 2
            clydex = 490
            clydey = 416
            clydedirection = 2
            playerx = (constants.SCREEN_WIDTH // 2) - 20
            playery = 665
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
        else:
            gameover = True
            startuptimer = 0
            blinkyx = 9000
            blinkyy = 9000
            blinkydirection = 0
            pinkyx = 9000
            pinkyy = 9000
            pinkydirection = 2
            inkyx = 9000
            inkyy = 9000
            inkydirection = 2
            clydex = 9000
            clydey = 9000
            clydedirection = 2
            playerx = 9000
            playery = 9000
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
    if powerup and (playercircle.colliderect(inky.rect) and eatenghosts[2] and not inky.dead):
        if lives > 0:
            lives -= 1
            startuptimer = 0

            blinkyx = 56
            blinkyy = 58
            blinkydirection = 0
            pinkyx = 370
            pinkyy = 416
            pinkydirection = 2
            inkyx = 430
            inkyy = 416
            inkydirection = 2
            clydex = 490
            clydey = 416
            clydedirection = 2
            playerx = (constants.SCREEN_WIDTH // 2) - 20
            playery = 665
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
        else:
            gameover = True
            startuptimer = 0
            blinkyx = 9000
            blinkyy = 9000
            blinkydirection = 0
            pinkyx = 9000
            pinkyy = 9000
            pinkydirection = 2
            inkyx = 9000
            inkyy = 9000
            inkydirection = 2
            clydex = 9000
            clydey = 9000
            clydedirection = 2
            playerx = 9000
            playery = 9000
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
    if powerup and (playercircle.colliderect(clyde.rect) and eatenghosts[3] and not clyde.dead):
        if lives > 0:
            lives -= 1
            startuptimer = 0

            blinkyx = 56
            blinkyy = 58
            blinkydirection = 0
            pinkyx = 370
            pinkyy = 416
            pinkydirection = 2
            inkyx = 430
            inkyy = 416
            inkydirection = 2
            clydex = 490
            clydey = 416
            clydedirection = 2
            playerx = (constants.SCREEN_WIDTH // 2) - 20
            playery = 665
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False
        else:
            gameover = True
            startuptimer = 0
            blinkyx = 9000
            blinkyy = 9000
            blinkydirection = 0
            pinkyx = 9000
            pinkyy = 9000
            pinkydirection = 2
            inkyx = 9000
            inkyy = 9000
            inkydirection = 2
            clydex = 9000
            clydey = 9000
            clydedirection = 2
            playerx = 9000
            playery = 9000
            direction = 0
            directioncommand = 0
            ghostspeeds = [2, 2, 2, 2]

            blinkydead = False
            pinkydead = False
            inkydead = False
            clydedead = False

            powerup = False
            powertimer = 0
            eatenghosts = [False, False, False, False]
            movementallowed = False

    if powerup and playercircle.colliderect(blinky.rect) and not blinky.dead and not eatenghosts[0]:
        blinkydead = True
        eatenghosts[0] = True
        score += (2 ** eatenghosts.count(True)) * 100
    if powerup and playercircle.colliderect(pinky.rect) and not pinky.dead and not eatenghosts[1]:
        pinkydead = True
        eatenghosts[1] = True
        score += (2 ** eatenghosts.count(True)) * 100
    if powerup and playercircle.colliderect(inky.rect) and not inky.dead and not eatenghosts[2]:
        inkydead = True
        eatenghosts[2] = True
        score += (2 ** eatenghosts.count(True)) * 100
    if powerup and playercircle.colliderect(clyde.rect) and not clyde.dead and not eatenghosts[3]:
        clydedead = True
        eatenghosts[3] = True
        score += (2 ** eatenghosts.count(True)) * 100
    
    if gamewon:
        startuptimer = 0
        blinkyx = 9000
        blinkyy = 9000
        blinkydirection = 0
        pinkyx = 9000
        pinkyy = 9000
        pinkydirection = 2
        inkyx = 9000
        inkyy = 9000
        inkydirection = 2
        clydex = 9000
        clydey = 9000
        clydedirection = 2
        playerx = 9000
        playery = 9000
        direction = 0
        directioncommand = 0
        ghostspeeds = [2, 2, 2, 2]

        blinkydead = False
        pinkydead = False
        inkydead = False
        clydedead = False

        powerup = False
        powertimer = 0
        eatenghosts = [False, False, False, False]
        movementallowed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                directioncommand = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                directioncommand = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                directioncommand = 2
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                directioncommand = 3
            
            if event.key == pygame.K_SPACE and (gameover or gamewon):
                lives = 3
                startuptimer = 0

                blinkyx = 56
                blinkyy = 58
                blinkydirection = 0
                pinkyx = 370
                pinkyy = 416
                pinkydirection = 2
                inkyx = 430
                inkyy = 416
                inkydirection = 2
                clydex = 490
                clydey = 416
                clydedirection = 2
                playerx = (constants.SCREEN_WIDTH // 2) - 20
                playery = 665
                direction = 0
                directioncommand = 0
                ghostspeeds = [2, 2, 2, 2]

                blinkydead = False
                pinkydead = False
                inkydead = False
                clydedead = False

                powerup = False
                powertimer = 0
                eatenghosts = [False, False, False, False]
                movementallowed = False

                gameover = False
                gamewon = False

                level = copy.deepcopy(mazes[0])

            if event.key == pygame.K_ESCAPE and (gameover or gamewon):
                run = False

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and directioncommand == 0:
                directioncommand = direction
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and directioncommand == 1:
                directioncommand = direction
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and directioncommand == 2:
                directioncommand = direction
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and directioncommand == 3:
                directioncommand = direction

    if directioncommand == 0 and turnvalid[0]:
        direction = 0
    if directioncommand == 1 and turnvalid[1]:
        direction = 1
    if directioncommand == 2 and turnvalid[2]:
        direction = 2
    if directioncommand == 3 and turnvalid[3]:
        direction = 3

    if playerx > constants.SCREEN_WIDTH:
        playerx = -47
    elif playerx < -50:
        playerx = 897

    if playery > constants.SCREEN_HEIGHT:
        playery = -50
    elif playery < -50:
        playery = constants.SCREEN_HEIGHT

    if blinky.inbox and blinkydead:
        blinkydead = False
    if pinky.inbox and pinkydead:
        pinkydead = False
    if inky.inbox and inkydead:
        inkydead = False
    if clyde.inbox and clydedead:
        clydedead = False

    pygame.display.update()

pygame.quit()
