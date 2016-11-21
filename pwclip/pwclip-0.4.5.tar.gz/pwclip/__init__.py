import sys

from os import environ

from os.path import abspath, dirname

__lib = '%s/lib'%abspath(dirname(__file__))
if not __lib in sys.path:
	sys.path.append(__lib)

from pwclip.cmdline import cli

def pwclipper():
	cli()
