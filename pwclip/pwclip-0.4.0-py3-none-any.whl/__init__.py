import sys
from os import environ
from os.path import abspath, dirname
__lib = '%s/lib'%abspath(dirname(__file__))
if not __lib in sys.path:
	sys.path.append(__lib)

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

