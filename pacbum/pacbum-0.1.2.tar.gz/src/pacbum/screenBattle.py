from pacbum.pacBum import *
from FGAme import *
from pacbum.objects import *
from pacbum.menuPacBum import*
from pacbum.colectScreen import *
from pacbum.zieloFlu import *
import pacbum.menuPacBum
conf.set_resolution(1260, 840)
zielo = zieloFlu()
"""
def update_pos_zielo_x(zielo, pacbum):
    if pacbum.fgameS.pos[0] > zielo.fgameS.pos[0]:
        zielo.fgameS.move(4, 0)
    else:
        zielo.fgameS.move(-4,0)

def update_pos_zielo_y(zielo, pacbum):
    if pacbum.fgameS.pos[1] > zielo.fgameS.pos[1]:
        zielo.fgameS.move(0, 4)
    else:
        zielo.fgameS.move(0,-4)

def update_pos_zielo(zielo, pacbum):

    update_pos_zielo_x(zielo, pacbum)
    update_pos_zielo_y (zielo, pacbum)
"""


"""
bomb_01 = world.add.circle(10, pos = (15, 585), color = 'black')
bomb_02 = world.add.circle(10, pos = (45, 585), color = 'black')
bomb_03 = world.add.circle(10, pos = (75, 585), color = 'black')
bomb_04 = world.add.circle(10, pos = (105, 585), color = 'black')
bomb_05 = world.add.circle(10, pos = (135, 585), color = 'black')
bomb_06 = world.add.circle(10, pos = (165, 585), color = 'black')
bomb_07 = world.add.circle(10, pos = (195, 585), color = 'black')
bomb_08 = world.add.circle(10, pos = (225, 585), color = 'black')
bomb_09 = world.add.circle(10, pos = (255, 585), color = 'black')
bomb_10 = world.add.circle(10, pos = (285, 585), color = 'black')


life_01 = world.add.circle(10, pos = (15, 15), color = 'green')
life_02 = world.add.circle(10, pos = (45, 15), color = 'green')
life_03 = world.add.circle(10, pos = (75, 15), color = 'green')
life_04 = world.add.circle(10, pos = (105, 15), color = 'green')
life_05 = world.add.circle(10, pos = (135, 15), color = 'green')
life_06 = world.add.circle(10, pos = (165, 15), color = 'green')
life_07 = world.add.circle(10, pos = (195, 15), color = 'green')
life_08 = world.add.circle(10, pos = (225, 15), color = 'green')
life_09 = world.add.circle(10, pos = (255, 15), color = 'green')
life_10 = world.add.circle(10, pos = (285, 15), color = 'green')

#Barra inferior - Vidas
inf_bar = world.add.aabb(shape=(1600, 5), pos=(0, 570), mass='inf')
#Barra superior - Bombas
sup_bar = world.add.aabb(shape=(1600, 5), pos=(0, 30), mass='inf')
#Barra lateral 1
lat_bar_1 = world.add.aabb(shape=(5,1800), pos=(0,0), mass = 'inf')
#Barra lateral 2
lat_bar_2 = world.add.aabb(shape=(5,1800), pos=(800,0), mass = 'inf')

#Barreira1
bar_1 = world.add.aabb(shape=(100,20), pos=(150,150), mass = 'inf', color = 'blue')
bar_2 = world.add.aabb(shape=(100,20), pos=(150,450), mass = 'inf', color = 'blue')
bar_3 = world.add.aabb(shape=(100,20), pos=(650,150), mass = 'inf', color = 'blue')
bar_4 = world.add.aabb(shape=(100,20), pos=(650,450), mass = 'inf', color = 'blue')
bar_5 = world.add.aabb(shape=(100,20), pos=(400,300), mass = 'inf', color = 'blue')
"""


def battleScreen(pacbum):

    #world.add(bar_5)
    bg_sound_battle = play('Cheesy-Science')
    @listen('frame-enter')
    def update_pos_zielo():
        if abs(zielo.fgameS.x - pacbum.fgameS.x) < 10:
            pass
        elif zielo.fgameS.x > pacbum.fgameS.x:
            zielo.fgameS.move(-zielo.vel_in_x, 0)
        else:
            zielo.fgameS.move(zielo.vel_in_x, 0)

        if abs(zielo.fgameS.y - pacbum.fgameS.y) < 10:
            pass
        elif zielo.fgameS.y > pacbum.fgameS.y:
            zielo.fgameS.move(0, -zielo.vel_in_y)
        else:
            zielo.fgameS.move(0, zielo.vel_in_y)


    #Movimenta personagem principal em Y
    @listen('long-press', 'up', dy = pacbum.vel_in_y)
    @listen('long-press', 'down', dy=-pacbum.vel_in_y)
    def pacbum_move_up(dy):


        #if pacbum.fgameS.pos[1] < 550 and pacbum.fgameS.pos[1] > 50:
        pacbum.fgameS.move(0, dy)

    @listen('key-down', 'r')
    def return_menu():
        bg_sound_battle.stop()
        menuPacBum.mainMenu()

    #Movimenta personagem principal em X
    @listen('long-press', 'right', dx = pacbum.vel_in_x)
    @listen('long-press', 'left', dx=-pacbum.vel_in_x)
    def pacbum_move_up(dx):
        #if pacbum.fgameS.pos[0] < 799 and pacbum.fgameS.pos[0] > 15:

           # if pacbum.fgameS.pos[0] > 788:
        #dx = -dx * 1.5
        pacbum.fgameS.move(dx, 0)

           # else:
              #  pacbum.fgameS.move(dx, 0)

    @listen('key-down', 'f')
    def kill_en():
        zielo.fgameS.visible = False
        bg_sound_battle.stop()

    run()