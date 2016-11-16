from FGAme import *
from math import sqrt
import pygame
from pygame.locals import *
from boy import *
from shot import Shot, randomize
import random
import time

#CONSTANTS
BASE_K = 1.05
RECOVER_INTERVAL = 150
TIME_TO_EXAUST = 200
SPAWN_TIME = 130
SCREEN_END = -10

world.add.margin(200, -500)
world.gravity = (0, 30)
PLAYER = Boy()
PLAYER.body.gravity = (0, 0)
gravity_x, gravity_y = PLAYER.body.gravity

shot_list = []
shot = Shot() # INITIAL SHOT
shot_list.append(shot)
count = 0
points = 0
is_exaust = False

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
main_sound = pygame.mixer.music.load("sounds/sound-adventure.mp3")
main_sound = pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.8);

@listen('long-press', 'up')
def increase_drag():
    if not is_exaust:
        PLAYER.body_pygame = pygame.image.load('images/2.png')
        for shot in shot_list:
            shot.k = 100
    else:
        PLAYER.body_pygame = pygame.image.load('images/1.png')

def decrease_drag():
    for shot in shot_list:
        shot.k = BASE_K

@listen('key-down', 'x')
def exit_game():
    exit()



# timers used on update
timer = 0 # GAME TIMER
exaustion_timer = 0
recover_timer = 0

def update(screen, text):
    global timer

    if timer >= SPAWN_TIME:
        timer = 0
        randomize(shot_list)

    for shot in shot_list:
        screen.blit(shot.body_pygame.convert_alpha(), 
                    shot.pos, [50, 50, 100, 80])
        shot.update()

        if shot.pos[1] < SCREEN_END:
            shot_list.remove(shot)
            world.remove(shot)
            global points
            global count
            count = count + 2
            points = points + 10 + count
            string_points = "%05d" % (points)

            point_label = text.get('point').render(
                    string_points,
                    1,
                    text.get('black'))

            screen.fill(text.get('white'))

            # render text
            screen.blit(text.get('tittle'), (10, 50))
            screen.blit(point_label, (10, 80))

    def colision():
        if abs((PLAYER.body.pos[1])-(shot.pos[1])) < 20:
            if ((PLAYER.body.pos[0])-(shot.pos[0])) > -25:
                if ((PLAYER.body.pos[0])-(shot.pos[0])) < 100:
                    return True

        return False

    for shot in shot_list:
        # END GAME (WORKING!!!!)
        if colision():
            print("GAME OVER")
            dash_sound =  pygame.mixer.music.load("sounds/battle_theme.mp3")
            dash_sound = pygame.mixer.music.play()
            time.sleep(1)
            exit()

    global exaustion_timer
    global is_exaust
    global recover_timer
    
    # TIMER INCREASING DEPENDS ON K VALUE
    if not shot_list:
        timer += 1
    elif (shot_list[0].k) == BASE_K:
        timer += 1
        if exaustion_timer >= TIME_TO_EXAUST:
            recover_timer += 1
            if recover_timer > RECOVER_INTERVAL:
                exaustion_timer = 0
                is_exaust = False
                recover_timer = 0
    else: # SLOW DOWN THE TIME
        timer += 0.5
        if exaustion_timer >= TIME_TO_EXAUST:
            for shot in shot_list:
                shot.k = BASE_K
            is_exaust = True
        else:
            exaustion_timer += 1
 

def render_game():
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    background = pygame.image.load('images/background.png').convert()

    # initialize font;
    title_font = pygame.font.SysFont("monospace", 25)
    point_font = pygame.font.SysFont("monospace", 15)
    
    #define colors
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    #define text
    title_label = title_font.render("Raining Man", 1, BLACK)
    point_label = point_font.render("00000", 1, BLACK)

    screen.fill(WHITE)

    # render text
    screen.blit(title_label, (10, 50))
    screen.blit(point_label, (10, 80))

    text = {
            'white': WHITE,
            'black': BLACK,
            'tittle': title_label,
            'point': point_font,
            }

    clock = pygame.time.Clock()
    while True:
        screen.blit(background, (200, 0))
        screen.blit(PLAYER.body_pygame.convert_alpha(), 
                    PLAYER.position,PLAYER.rect)

        update(screen, text)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()


        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_RIGHT]:
            if PLAYER.body.pos[0] <= 575:
                PLAYER.move_p1(2)
        elif pressed_keys[K_LEFT]:
            if PLAYER.body.pos[0] >= 200:
                PLAYER.move_p1(-2)
        else:
            # Do nothing
            pass

        if pressed_keys[K_UP]:
            increase_drag()
        elif not pressed_keys[K_UP] or is_exaust:
            PLAYER.body_pygame = pygame.image.load('images/1.png')
            decrease_drag()
        else:
            # Do nothing
            pass

        pygame.display.update()
        time_passed = clock.tick(60)


render_game()
