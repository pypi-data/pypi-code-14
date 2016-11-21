# importando o FGame
from FGAme import *
# pygame
import pygame
from pygame.locals import *

# Contadores e marcadores globais
special_count = 0
jump_count = 0

# Mundo
world = World()

# Personagem
char1 = AABB(shape=(15, 25), pos=(35, 35), color='blue', mass='150')
char1.inertia /= 2
char1.restitution = 0

# Inimigo
enemy1 = RegularPoly(
    3, length=150, pos=(400, 300), color='red', mass='5000')
enemy1.inertia = 'inf'
enemy1.restitution = 0
enemy1.omega += 35
enemy1.vel = vel.random()

# Terreno
terrain = AABB(shape=(800, 20), pos=(400, 10), mass='inf', color='green')

# Plataformas
platform1 = AABB(shape=(115, 2), pos=(300, 75), mass='inf')
platform2 = AABB(shape=(50, 2), pos=(200, 50), mass='inf')
platform3 = AABB(shape=(50, 2), pos=(400, 50), mass='inf')
platform4 = AABB(shape=(115, 2), pos=(650, 75), mass='inf')
platform5 = AABB(shape=(50, 2), pos=(550, 50), mass='inf')
platform6 = AABB(shape=(50, 2), pos=(750, 50), mass='inf')

# Forca de atracao (gravidade)
char1.gravity = 2400

# Adiciona elementos ao mundo
world.add(char1)
world.add(enemy1)
world.add(platform1)
world.add(platform2)
world.add(platform3)
world.add(platform4)
world.add(platform5)
world.add(platform6)
world.add(terrain)
world.add.margin(0)


# Comando de movimentacao pra direita
@listen('long-press', 'right')
def move_right():
    char1.move(6, 0)
    # O personagem pode perder o controle no jogo por causa de impactos,
    # esse é o metodo do player retomá-lo.
    if char1.vel.x != 0:
        char1.vel = (0, char1.vel.y)


# Comando de movimentacao pra esquerda
@listen('long-press', 'left')
def move_left():
    char1.move(-6, 0)
    # O personagem pode perder o controle no jogo por causa de impactos,
    # esse e o metodo do player retomá-lo.
    if char1.vel.x != 0:
        char1.vel = (0, char1.vel.y)


# Comando de pulo
@listen('key-down', 'up')
def jump():
    if jump_count < 2:
        char1.vel = (char1.vel.x, 400)
        global jump_count
        jump_count += 1


# Comando de tiro para cima
@listen('key-down', 'w')
def shot_left():
    shot = world.add.aabb(
        shape=(2, 3),
        pos=(char1.pos.x, char1.pos.y+10),
        vel=(0, 600),
        mass='inf')


# Comando de tiro para a esquerda
@listen('key-down', 'a')
def shot_left():
    shot = world.add.aabb(
        shape=(3, 2),
        pos=(char1.pos.x-10, char1.pos.y),
        vel=(-600, 0),
        mass='inf')


# Comando de tiro para a direita
@listen('key-down', 'd')
def shot_right():
    shot = world.add.aabb(
        shape=(3, 2),
        pos=(char1.pos.x+10, char1.pos.y),
        vel=(600, 0),
        mass='inf')


# Comando de especial
@listen('key-down', 'space')
def special_move():
    if special_count < 2:
        blast_count = 0
        char1.inertia = 'inf'
        while blast_count < 10:
            shot = Circle(5, pos=(char1.pos.x, char1.pos.y+25), mass='inf')
            shot.vel = vel.random()
            world.add(shot)
            blast_count += 1
        char1.inertia /= 2

    elif special_count == 2:
        if enemy1.pos.x < char1.pos.x:
            shot = Circle(50,
                        pos=(char1.pos.x - 35, char1.pos.y),
                        mass='inf')
            shot.vel = ((enemy1.pos.x - char1.pos.x),
                        (enemy1.pos.y - char1.pos.y)) # Ainda meio quebrado

        elif enemy1.pos.x > char1.pos.x:
            shot = Circle(50,
                        pos=(char1.pos.x + 35,
                        char1.pos.y),
                        mass='inf')
            shot.vel = ((enemy1.pos.x - char1.pos.x),
                        (enemy1.pos.y - char1.pos.y)) # Ainda meio quebrado

        else:
            shot = Circle(50,
                        pos=(char1.pos.x, char1.pos.y+35),
                        mass='inf')
            shot.vel = ((enemy1.pos.x - char1.pos.x),
                        (enemy1.pos.y - char1.pos.y)) # Ainda meio quebrado

        # shot.vel = (
        #         ((enemy1.pos.x - char1.pos.x)/abs(enemy1.pos.x - char1.pos.x))*500,
        #         ((enemy1.pos.y - char1.pos.y)/abs(enemy1.pos.y - char1.pos.y))*500)

        world.add(shot)

    else:
        return

    global special_count
    special_count += 1


# Reset de pulos
@listen('frame-enter')
def update():
    if char1.pos.y < 35:
        global jump_count
        jump_count = 0


# Altura do inimigo
@listen('frame-enter')
def enemy_heigh():
    if abs(enemy1.y - char1.y) < 20:
        pass
    elif enemy1.y > char1.y:
        enemy1.move(0, -10)
    else:
        enemy1.move(0, 10)

    if enemy1.y >= 450:
        enemy1.vel += (0,-enemy1.vel.y-150)


# Movimentacao do inimigo
@listen('frame-enter')
def enemy_movement():
    if abs(enemy1.x - char1.x) < 10:
        pass
    elif enemy1.x > char1.x:
        enemy1.move(-1, 10)
    else:
        enemy1.move(1, 10)


# Condicao de fim de jogo
@listen('frame-enter')
def check_player_lose():
    if char1.x < -10 or char1.x > 810 or char1.y < -10 or char1.y > 610:
        world.pause()


# @listen('pre-collision')
# def on_collision(col):
#     print('bateu')

world.run()
