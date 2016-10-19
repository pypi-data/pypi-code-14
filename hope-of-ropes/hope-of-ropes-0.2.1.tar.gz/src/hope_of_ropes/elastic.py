'''TODO:
        Make a class simulation that includes all these functions
        Make a module for handling inputs?
        Make a module for constants?

'''
import sys; sys.path.append('./classes/')
from FGAme import *
from .rope import Rope
from .platforms import Platforms
from math import fabs
from .player import Player

MIN_ROPE_LENGTH = 50
MAX_ROPE_LENGTH = 300

# Change these pls
PLAYER = Player()
PLATFORM = Platforms()
ROPE = Rope(PLAYER.obj)


def start_simul():
    margin(10)
    PLATFORM.add(pos=pos.middle+(0, 200))
    PLATFORM.add(pos=pos.middle+(200, 500))

    run()

@listen('frame-enter')
def update():
    move_screen(0.5)
    ROPE.update()

dx = 10

@listen('long-press', 'left', dx=-dx)
@listen('long-press', 'right', dx=dx)
def wind(dx):
    PLAYER.obj.vel += (dx, 0)

@listen('key-down', 'space', color=(255, 0, 0), max_length=400)
def hook(color, max_length):
    if ROPE.platform == None:
        for platform in PLATFORM.items:
            if (fabs(platform.pos.x-PLAYER.obj.pos.x) < 30 and \
                platform.pos.y > PLAYER.obj.pos.y and \
                fabs(PLAYER.obj.pos.y - platform.pos.y) < max_length): #Hook only if platform is directly above
                platform.color = color
                PLAYER.obj.color = color
                ROPE.connect(platform)
    else:
        ROPE.remove()
        ROPE.platform.color = (0, 0, 0)
        PLAYER.obj.color = (0, 0, 0)
        ROPE.platform = None

@listen('long-press', 'up', climbing_distance=5)
@listen('long-press', 'down', climbing_distance=-5)
def climb_rope(climbing_distance):
    if ROPE.platform != None:
        direction = ROPE.platform.pos - PLAYER.obj.pos
        direction = direction.normalize()

        direction *= climbing_distance
        norm = ROPE.length - direction.norm()*(climbing_distance/fabs(climbing_distance))
        if norm > MIN_ROPE_LENGTH and norm < MAX_ROPE_LENGTH:
            ROPE.length = norm
        else:
            direction = Vec(0, 0)
        # if climbing_distance > 0:
        #     move_screen(climbing_distance)
        PLAYER.obj.move(direction)
    else:
        #Do nothing
        pass

def move_screen(dy):
    for obj in world:
        if type(obj) is not objects.AABB:
            obj.move(0, -dy)
        
def margin(dx):
    W, H = conf.get_resolution()

    world.add.aabb(shape=(10, H), pos=(dx/2, pos.middle.y), mass='inf')
    world.add.aabb(shape=(10, H), pos=(W - dx/2, pos.middle.y), mass='inf')

start_simul()