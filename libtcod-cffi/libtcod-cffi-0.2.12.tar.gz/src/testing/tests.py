
import tcod as libtcod

def run():
    libtcod.init_root(40, 30, 'test', fullscreen=False, renderer=_tcod.RENDERER_GLSL)
