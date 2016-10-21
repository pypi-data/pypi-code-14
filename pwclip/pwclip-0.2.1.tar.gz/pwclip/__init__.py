import sys
from os import environ

from pwclip.clipper import clipgui

def pwclipper():
    mode = 'yk'
    if [a for a in sys.argv if a == '-c']:
        del sys.argv[sys.argv.index('-c')]
        mode = 'pc'
    wait = 3
    if len(sys.argv) > 1:
        wait = int(sys.argv[1])
    elif 'PWCLIPTIME' in environ.keys():
        wait = int(environ['PWCLIPTIME'])
    clipgui(mode, wait)

