#! /usr/bin/env python
import pygame
import time
from FGAme import *
from random import randint
from pygame.locals import *
from sys import exit
from math import *

class environment:

    def __init__(self):
        self.objects = list()
        self.gravity = 60
        self.friction = list()
        self.for_new_object_in_screen = 1200
        self.position_pacBum = 0




#Função que adiciona "zonas de atrito"
def add_friction(self, friction):

    self.friction.append(friction)

#Função que adiciona um objeto à lista de objetos
def add_objects(self, obj):

    obj.gravity = self.gravity
    self.objects.append(obj)

#Função que marca se o objeto está em tela ou não.
def obj_inScreen(self):


    number = randint(0,4)
    boolean = randint(0,1)

    self.objects[number].inScreen = True

    self.objects[number].vel_in_x = 7

    if boolean == 0:
        self.objects[number].position[1] = 630
    else:
        self.objects[number].position[1] = 530



#Função que desenha e atualiza os objetos em tela.
def draw_and_update_objects(screen, self):

    for obj in self.objects:
        if obj.inScreen == True:
            animation_obj(obj)
            obj_update(self, obj)
            screen.blit(obj.pygameS,(obj.position),obj.rect)

#Função que produz a animação do objeto
def animation_obj(obj):

        obj.cont_animation += 0.1

        if obj.cont_animation < 0.75:
            obj.rect[0] = 0

        elif obj.cont_animation > 0.75:
            obj.rect[0] = obj.rect[2]

        if obj.cont_animation >= 1.25:
            obj.cont_animation = 0


#Atualiza a posição do objeto e garante se outro será criado na tela.
def obj_update(self, obj):


    if obj.position[0] > -50 :
        obj.position[0] -= obj.vel_in_x
        obj.position[1] += 0
        self.for_new_object_in_screen -= 7
    else:
        obj.position[0] = 1500
        obj.inScreen = False

    if self.for_new_object_in_screen < 500:
        obj_inScreen(self)
        self.for_new_object_in_screen = 1200

#Funçao que coleta as dimensões dos objetos
def get_rect(obj):

    width = obj.pygameS.get_width()
    width = width / 2
    width =  width - obj.split_range


    height = obj.pygameS.get_height()
    height = height / 2
    height = height - obj.split_range



    return Rect(obj.position[0], obj.position[1], width, height)



#Função que detecta as colisões
def update_colisions(self, pacbum):


    pacbum_rect = get_rect(pacbum)

    #Detectada a colisão, detecta-se o objeto que colidiu e seu efeito.
    for obj in self.objects:
        if pacbum_rect.colliderect(get_rect(obj)):
            result = obj.who_touch
            obj.position = [2000, 2000]
            obj.vel_in_x = 0

            if result == "skull":
                pacbum.lifes -= 1
                pacbum.points -= 40


            if result == "bomb":
                pacbum.bombs += 1
                pacbum.points += 10


            if result == "spoint":
                pacbum.points += 100


            if result == "life":
                pacbum.lifes += 1
                pacbum.points +=20


            if result == "venon":
                pacbum.lifes -= 1
                pacbum.points -= 100

            if pacbum.points < 0:
                pacbum_points = 0

            if pacbum.lifes < 0:
               pacbum.dead = True


#Função para desenhar a tela "RIP" quando pac bum está morto
def draw_pacbum_is_dead(screen, self):

        screen.blit(self.objects[5].pygameS,(self.objects[5].position))

