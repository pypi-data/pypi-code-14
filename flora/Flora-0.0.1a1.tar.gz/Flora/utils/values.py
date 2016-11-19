from os import path, mkdir
from sys import argv
PATH = path.expanduser('~/.Flora')
ALT_PATH = path.dirname(path.realpath(__file__))
CONFIG_FILE = path.join(PATH, 'config.yml')
PLUGIN_DIR = path.join(PATH, 'Plugins')

DATA_DIR = path.join(PATH, 'Data')

if '--selfbot' in argv:
    DB = path.join(DATA_DIR, 'SelfBot.db')
else:
    DB = path.join(DATA_DIR, 'Flora.db')
