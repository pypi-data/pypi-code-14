import os
from functools import partial

# These are so short that they're really just examples.
InputFile = partial(open, mode='r')
OutputFile = partial(open, mode='w')

def InputDirectory(x):
    if os.path.isdir(x):
        return x
    else:
        raise ValueError('No such directory: ' + str(x))

def OutputDirectory(x):
    os.makedirs(x, exist_ok=True)
    return x
