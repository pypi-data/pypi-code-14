#! /usr/bin/env python
import pygame
import time
from pacbum.background import *
from pacbum.textClass import *
import pacbum.menuPacBum
from pygame.locals import *
from sys import exit



#Cria a tela dos créditos
def screenCredits():

    #Inicia os objetos na tela de créditos
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1300, 700), 0, 32)
    pygame.display.set_caption('PAC BUM! > Creditos')

    #Definição do background.
    bg = background()
    bg.image = "images/bg_menu_back.png"
    bg.rect = [0,0,1300,1300]

    #Definição dos textos na tela de cŕeditos
    text_list = list()

    textCred_1 = textScreen()
    textCred_1.text = "Universidade de Brasília - 2016"
    textCred_1.pygamePosition = [400, 700]

    textCred_2 = textScreen()
    textCred_2.text = "PacBum V - 0.1.0 por: Lucas S. Souza"
    textCred_2.pygamePosition = [400, 740]

    textCred_3 = textScreen()
    textCred_3.text = "Email: lucas.soaresouza@gmail.com"
    textCred_3.pygamePosition = [400,780]

    add_text(text_list, textCred_1)
    add_text(text_list, textCred_2)
    add_text(text_list, textCred_3)

    #Velocidade dos textos na tela.
    text_speed = 3


    #Laço de update da tela de cŕeditos
    clock = pygame.time.Clock()
    while True:

        #Desenha o plano de fundo
        draw_background(screen, bg)

        #Desenha os textos na tela
        draw_text(screen, text_list)

        #Movimento do texto na tela de créditos
        if textCred_1.pygamePosition[1] > 200:
            textCred_1.pygamePosition[1] -= text_speed
            textCred_2.pygamePosition[1] -= text_speed
            textCred_3.pygamePosition[1] -= text_speed
        else:
            textCred_1.pygamePosition[1] = 200
            textCred_2.pygamePosition[1] = 240
            textCred_3.pygamePosition[1] = 280


        #Habilita que a janela seja fechada no "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        #Habilita que a janela retorne para o menu principal ao "ESC" ser teclado.
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_r]:
            menuPacBum.mainMenu()

        #Atualiza a tela de acordo com o laço principal
        pygame.display.update()
        #Clock máximo do update.
        time_passed = clock.tick(30)

