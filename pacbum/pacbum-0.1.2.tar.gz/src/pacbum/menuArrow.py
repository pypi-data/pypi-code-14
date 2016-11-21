#! /usr/bin/env python
import pygame
import time
from pygame.locals import *
from sys import exit

#Classe da seta dos menus
class selectArrow:

    def __init__(self):
        self.name = 'images/select.png'
        self.arr = pygame.image.load(self.name).convert_alpha()
        self.value = 0
        self.posX = 500
        self.posY = 250
