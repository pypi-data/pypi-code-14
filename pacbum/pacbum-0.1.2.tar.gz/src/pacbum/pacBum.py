#! /usr/bin/env python
import pygame
import time
from FGAme import *
from pygame.locals import *
from sys import exit
from math import *


#Classe do personagem principal
class pacBum:

    def __init__(self):
        self.image = 'images/pacbum_front.png'
        self.lifes = 0
        self.dead = False
        self.split_range = 10
        self.pygameS = pygame.image.load(self.image).convert_alpha()
        self.fgameS = world.add.circle(20, pos=(400, 300), color='green', mass = 20)
        self.rect = [0,0,60,60]
        self.cont_animation = 0
        self.points = 0
        self.bombs = 0

        """ATRIBUTOS FISICOS"""

        self.mass = 100
        self.position = [625,655]
        self.gravity = 0
        self.friction_tax = 0.01
        self.total_force_in_x = 0
        self.acel_in_x = 0.5
        self.vel_in_x = 15
        self.vel_in_y = 0

def update_Phys_pacBum(self):

    v_abs = sqrt(self.vel_in_x**2)
    self.acel_in_x = self.vel_in_x / v_abs
    self.friction_in_x = -self.friction_tax * self.gravity * self.acel_in_x

    if self.vel_in_x > 4:
        self.vel_in_x += self.friction_in_x
    else:
        self.vel_in_x = 4



#Função da animação do personagem principal.
def animation_pacBum(self):

    self.cont_animation += 0.1

    if self.cont_animation < 0.75:
        self.rect[0] = 0

    elif self.cont_animation > 0.75:
        self.rect[0] = 60

    if self.cont_animation >= 1.25:
        self.cont_animation = 0

#Função que desenha o Pac Bum
def draw_pacbum(screen, self):

    screen.blit(self.pygameS,(self.position),self.rect)

#Função que atualiza o lado para o qual o pac bum está virado
def animation_update(self, image):
    self.image = image
    self.pygameS = pygame.image.load(self.image).convert_alpha()


#Função e detecção de colisão do movimento do personagem principal na tela colectScreen
def forward_colectScreen(self):

    if self.dead == False:
        animation_update(self, 'images/pacbum_front.png')
        update_Phys_pacBum(self)

        if self.position[0] >= 1000:
            self.position[0] = 999


        self.position[0] = self.position[0] + self.vel_in_x
    else:
        pass



#Função e detecção de colisão do movimento do personagem principal na tela colectScreen
def backward_colectScreen(self):

    if self.dead == False:
        animation_update(self, 'images/pacbum_back.png')
        update_Phys_pacBum(self)

        if self.position[0] <= 200:
            self.position[0] = 201


        self.position[0] = self.position[0] - self.vel_in_x
    else:
        pass

#Função que marca o Pac Bum como morto
def pacbum_is_dead(self):

        if self.dead == True:
            self.vel_in_x = 0
            self.position = [3000,3000]
            return True
        else:
            pass




