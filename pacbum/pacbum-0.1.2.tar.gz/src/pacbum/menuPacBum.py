#! /usr/bin/env python
import pygame
import time
from pacbum.menuArrow import *
from FGAme import *
from pacbum.colectScreen import *
from pacbum.screenCredits import *
from pacbum.background import *
from pygame.locals import *
from sys import exit

#Inicializa o menu principal
def mainMenu():

    bg_sound = play("Blob-Monsters-on-the-Loose")

    #inicializa os objetos do menu principal
    pygame.font.init()
    screen = pygame.display.set_mode((1300, 700), 0, 32)
    pygame.display.set_caption('PAC BUM! > Menu Principal')

    #Definição do background.
    bg = background()
    bg.image = "images/bg_menu.png"
    bg.rect = [0,0,1300,1300]



    init = pygame.image.load('images/opt_init.png').convert_alpha()
    options = pygame.image.load('images/opt_options.png').convert_alpha()
    credits = pygame.image.load('images/opt_credits.png').convert_alpha()
    exit = pygame.image.load('images/opt_exit.png').convert_alpha()


    #textos que aparecem no menu principal
    list_text = list()
    textVersion = textScreen()
    textVersion.text = "V - 0.1.0"
    textVersion.pygamePosition = [1210,675]
    add_text(list_text, textVersion)

    arrow = 0
    #Clock e laço de update do menu principal
    clock = pygame.time.Clock()
    while True:

        #Desenha o plano de fundo.
        draw_background(screen, bg)

        if arrow == 0:
            screen.blit(init,(60,300),[300,0,300,300])
        else:
            screen.blit(init,(60,300),[0,0,300,300])

        if arrow == 1:
            screen.blit(options,(360, 300),[300,0,300,300])
        else:
            screen.blit(options,(360, 300),[0,0,300,300])

        if arrow == 2:
            screen.blit(credits,(710, 300),[341,0,341,341])
        else:
            screen.blit(credits,(710, 300),[0,0,341,341])

        if arrow == 3:
            screen.blit(exit,(1030, 300),[300,0,300,300])
        else:
            screen.blit(exit,(1030, 300),[0,0,300,300])

        #Desenha os textos da tela.
        draw_text(screen, list_text)

        #Habilita que a janela seja fechada pelo "x"
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


        #Habilita os controles do jogo pelo teclado
        pressed_keys = pygame.key.get_pressed()

        #Comandos da seta de controle do menu principal
        #Para cima
        if pressed_keys[K_LEFT]:
            select_sound = play("UI_Quirky27")
            arrow -= 1
            time.sleep(1/7)
            if arrow < 0:
                arrow = 3


        #Para baixo
        if pressed_keys[K_RIGHT]:
            select_sound = play("UI_Quirky27")
            arrow += 1
            time.sleep(1/7)
            if arrow > 3:
                arrow = 0

        #Confrima opção
        if pressed_keys[K_RETURN]:
            play("PowerUp10")
            if arrow == 0:
                bg_sound.stop()
                colectScreen()
            elif arrow == 1:
                print('1')
            elif arrow == 2:
                bg_sound.stop()
                screenCredits()
            if arrow == 3:
                pygame.quit()
                exit()

        #Atualização dos objetos na tela
        pygame.display.update()

        #Clock máximo do uptade
        time_passed = clock.tick(30)
