import subprocess as _sp
import sys as _sys
from . import *
__license__ = 'MIT'
__author__ = 'G.M'
__email__ = 'G.Mpydev@gmail.com'
__quote__ = """Loop and recursion work together will produce
better result and better than any of the previous."""
__note__ = """I'm considering to add support for multiprocessing
module for all the search methods, since it is pretty slow if
you have a bunch of files on your computer, though the performance
if o(n)"""

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
