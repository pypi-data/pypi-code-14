#! /usr/bin/env python
import pygame
import time
from pygame.locals import *
from sys import exit

class textScreen:

    def __init__(self):

        self.text = "default"
        self.pygamePosition = [100,100]
        self.color = (0,0,0)
        self.font = pygame.font.get_default_font()
        self.d_font = 28
        self.game_font = pygame.font.SysFont(self.font, self.d_font)


#Função que adiciona um objeto do tipo texto à lista de textos
def add_text(text_list, text):

    text_list.append(text)

#Função que desenha os textos em tela.
def draw_text(screen, text_list):

    for text in text_list:
        obj = text.game_font.render(text.text,1,text.color)
        screen.blit(obj, (text.pygamePosition))