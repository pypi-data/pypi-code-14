'''TODO:
        Make a class simulation that includes all these functions
        Make a module for handling inputs?
        Make a module for constants?
        Remove all those globals. pls
'''
import sys; sys.path.append('./classes/')
from FGAme import *
from rope import Rope
from platforms import Platforms
from math import fabs
from light import Light

MIN_ROPE_LENGTH = 50
MAX_ROPE_LENGTH = 300

# Change these pls
ROPE = None
PLAYER = None
LIGHT = Light(pos=pos.middle)
PLATFORM = Platforms()

def start_simul():
    s = world.add.rectangle(shape=(50, 50), pos=pos.middle-(100, 0), mass='inf')
    s = world.add.rectangle(shape=(50, 50), pos=pos.middle+(50, 50), mass='inf')
    
    run()

@listen('frame-enter')
def update():
    LIGHT.draw_lines()

dx = 10

@listen('long-press', 'left', dx=-dx)
@listen('long-press', 'right', dx=dx)
@listen('long-press', 'down', dy=-dx)
@listen('long-press', 'up', dy=dx)
def wind(dx=0, dy=0):
    LIGHT.obj.move((dx, dy))

@listen('key-down', 'space')
def hook():
    LIGHT.switch()

start_simul()