import mklibpy.util.osinfo as osinfo

__author__ = 'Michael'

if osinfo.PYTHON2:
    import __builtin__
else:
    import builtins as __builtin__
__builtin__ = __builtin__


def cleanup(globals, locals, *exceptions):
    for key in set(globals.keys()):
        if globals[key] in exceptions:
            continue
        globals.pop(key)
    for key in set(locals.keys()):
        if locals[key] in exceptions:
            continue
        locals.pop(key)


from . import builtins
from . import import_
from . import open
