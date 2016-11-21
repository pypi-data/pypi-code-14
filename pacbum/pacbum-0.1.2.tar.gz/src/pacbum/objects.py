#! /usr/bin/env python
import pygame
import time
from FGAme import *
from pygame.locals import *
from sys import exit

class obj_game:

    def __init__(self):

        self.image = 'images/'
        self.inScreen = False
        self.pygameS = 0
        self.rect = [0,0,60,60]
        self.cont_animation = 0
        self.who_touch = "default"
        self.split_range = 0

        """ATRIBUTOS FISICOS"""

        self.mass = 100
        self.position  = [50,625]
        self.gravity = 0
        self.friction_tax = 0.01
        self.total_force_in_x = 0
        self.acel_in_x = 0.5
        self.vel_in_x = 15
        self.vel_in_y = 0