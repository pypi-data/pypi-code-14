from builtins import super

import inspect
import logging
import sys

from collections import Iterable, namedtuple
from contextlib import contextmanager
from ctypes import cast, c_int, POINTER
from six import string_types

from .tecinterprocess import _tecutil
from ..constant import Color
from ..exception import TecplotAttributeError, TecplotTypeError

log = logging.getLogger(__name__)

maxint64 = 2**(64 - 1) - 1
minint64 = -maxint64 - 1
maxuint64 = 2**64 - 1


class Index(int):
    """Position identifier type.

    This type is used internally to represent a position in a list. It is
    used to indicate that a change between zero-based indexing and one-based
    indexing must occur at the TecUtil boundary.

    This type can be treated exactly like a Python native `int` and is only
    meaningful internally to the tecplot Python module.
    """


IndexRange = namedtuple('IndexRange', ['min', 'max', 'step'])
"""Index range specification along some axis.

This is similar to Python's `slice` object except that ``max`` is included
in the evaluated indexes. Here are some things to note:

    * All indices start with 0 and go to some maximum index ``m``.
    * Negative values represent the indexes starting with the maximum at -1
      and continuing back to the beginning of the range.
    * A step of `None`, 0 and 1 are all equivalent and mean that no elements
      are skipped.
    * A negative step indicates a skip less than the maximum.
"""
IndexRange.__new__.__defaults__ = (None, None, None)


def flatten_args(*args):
    flatargs = []
    for a in args:
        if isinstance(a, Iterable) and not isinstance(a, string_types):
            flatargs += list(a)
        else:
            flatargs.append(a)
    return tuple(flatargs)


def array_to_enums(array_pointer, array_size, enum_type):
    indexes = cast(array_pointer, POINTER(c_int))
    return tuple(enum_type(indexes[i]) for i in range(array_size))


def log_setattr(cls):
    def _setattr(self, name, value):
        if __debug__:
            if not name.startswith('_') and name not in dir(self):
                stacknames = [f[0].f_code.co_name for f in inspect.stack()[:3]]
                if '__init__' not in stacknames:
                    msg = 'No attribute: {}.{}'
                    classname = self.__class__.__name__
                    raise TecplotAttributeError(msg.format(classname, name))
        return super(cls, self).__setattr__(name, value)

    cls.__setattr__ = _setattr
    return cls


@contextmanager
def lock(with_recording=True):
    """
    ParentLockStart takes a boolean: ShutdownImplicitRecording
    ShutdownImplicitRecording = True -> No recording
    ShutdownImplicitRecording = False -> With Recording
    """
    _tecutil.ParentLockStart(not with_recording)
    try:
        yield
    finally:
        _tecutil.handle.tecUtilParentLockFinish()


if sys.version_info < (3, 3):
    """
    This allows the contextmanager lock
    to be used as a decorator as well as a
    context. (This is already included in Py 3.3+)
    """
    from functools import wraps

    _lock = lock

    class lock(object):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self._cm = _lock

        def __enter__(self, *args, **kwargs):
            self.cm = self._cm(*self.args, **self.kwargs)
            return self.cm.__enter__(*args, **kwargs)

        def __exit__(self, *args, **kwargs):
            return self.cm.__exit__(*args, **kwargs)

        def __call__(self, func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with self._cm(*self.args, **self.kwargs):
                    return func(*args, **kwargs)

            return wrapper

_VarInfo = namedtuple('VarInfo', ('types', 'values', 'names'))


def check_arglist_argtypes(function_name, *args):
    for arg in args:
        vinfo = _VarInfo(*arg)
        for name, value in zip(vinfo.names, vinfo.values):
            if value is not None:
                if not isinstance(value, tuple(vinfo.types)):
                    errfmt = '{}: Type of  parameter {} must be one of: {}'
                    types = ', '.join(t.__name__ for t in vinfo.types)
                    errmsg = errfmt.format(function_name, name, types)
                    raise TecplotTypeError(errmsg)


def color_spec(color, plot=None):
    """
        color_spec(Color.Blue, plot)        -> Color.Blue
        color_spec(Color.MultiColor, plot)  -> plot.contour(0)
        color_spec(Color.Blue)              -> Color.Blue
        color_spec(plot.contour(0))         -> Color.MultiColor
    """
    color_spec._indexes = {
        Color.MultiColor: Index(0),
        Color.MultiColor2: Index(1),
        Color.MultiColor3: Index(2),
        Color.MultiColor4: Index(3),
        Color.MultiColor5: Index(4),
        Color.MultiColor6: Index(5),
        Color.MultiColor7: Index(6),
        Color.MultiColor8: Index(7)}
    color_spec._multicolors = {v: k for k, v in color_spec._indexes.items()}
    try:
        if plot:
            return plot.contour(color_spec._indexes[Color(color)])
        else:
            return color_spec._multicolors[Index(color.index)]
    except (AttributeError, KeyError):
        return Color(color)
