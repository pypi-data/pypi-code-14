import subprocess as _sp
from .__CLI import action as _action
import sys as _sys

__license__ = 'MIT'
__author__ = 'G.M'
__email__ = 'G.Mpydev@gmail.com'
__quote__ = """Loop and recursion work together will produce
better result and better than any of the previous."""
__note__ = """I'm considering to add support for multiprocessing
module for all the search methods, since it is pretty slow if
you have a bunch of files on your computer, though the performance
if o(n)"""


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


def reinstall():
    """Make sure you have pip added to the environment variable."""
    _sp.Popen(r'resources/reinstall.bat')
    _sys.exit(0)



class open:
    def __new__(cls, file_type: str, *args, **kwargs):
        from .file import TextFile, BinaryFile
        temp = {'text':   TextFile,
                'binary': BinaryFile}
        assert file_type.lower() in temp, "Pyil doesn't currently support this type of file."
        return temp.get(file_type.lower())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
