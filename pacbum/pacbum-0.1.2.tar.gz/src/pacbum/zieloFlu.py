#! /usr/bin/env python
import pygame
import time
from FGAme import *
from pygame.locals import *
from sys import exit
from math import *

class zieloFlu:

    def __init__(self):

        self.fgameS = world.add.circle(25, pos = (500,500), color = 'orange', mass = 25)
        self.lifes = 10
        self.vel_in_x = 2
        self.vel_in_y = 2

