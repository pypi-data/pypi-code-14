
from ._text import text_file
from ._CLI import action as _action
import sys as _sys


__license__ = 'MO'
__author__ = 'G.M'
__email__ = 'G.Mpydev@gmail.com'
__quote__="""Loop and recursion work together will produce
better result and better than any of the previous."""


def cmd():
    '''call me when ever you want to enable command line control.'''
    _action(_sys.argv[1:])


def input_control():
    '''call me when ever you want to enable user input control.'''
    while True:
        temp = input('Please enter the command you want to execute(q to quit):')
        if temp == 'q':
            _sys.exit(1234567890)
        try:
            _action(temp)
        except ValueError:
            print('Invalid command.')
            continue

