#! /usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit

class background:

    def __init__(self):

        self.image = "images/bg_menu.png"
        self.pygameS = pygame.image.load(self.image).convert()
        self.rect = [0,0,1260,1260]
        self.for_rect_background = 0

#Função que desenha os planos de fundo
def draw_background(screen, self):
        self.pygameS = pygame.image.load(self.image).convert()
        screen.blit(self.pygameS,(0,0), self.rect)


