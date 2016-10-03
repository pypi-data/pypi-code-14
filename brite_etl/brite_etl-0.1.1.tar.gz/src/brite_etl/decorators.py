from __future__ import absolute_import, print_function

from pydash import merge
from collections import namedtuple
import time
from brite_etl import logger
from brite_etl.utils.types import DeepDict


def time_it(method):
    """
        Put the @time_it decorator on a function to easy time the performance
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        logger.debug('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
        return result

    return timed


def return_tuple(method):
    """
        Put the @return_tuple decorator on a function to use standard return format
    """
    def wrapper(*args, **kw):
        result = namedtuple('result', 'success messages data')

        _info = {
            'success': True,
            'messages': [],
            'data': {}
        }

        try:
            _result = method(*args, **kw)
            _info['data'] = _result
        except Exception as e:
            _info['success'] = False
            _info['messages'].append(e)

        return result(**_info)

    return wrapper


class get_frames(object):
    """@get_frames decorator

        Put this on a function to intercept and send frames as an argument.
    """
    def __init__(self, *args, **kwargs):
        self._frames_to_get = args
        self._frames = DeepDict({})

    def __call__(self, fn, *args, **kwargs):
        def new_func(*args, **kwargs):

            # If a frameset is passed by arg instead of keyword, make it one.
            # This can happen if you're chaining frame sets.
            if (type(args[0]).__name__ is 'FrameSet'):
                kwargs['frame_set'] = args[0]
                args = list(args)
                del args[0]
                args = tuple(args)

            """
                Note that the order is important here. If they passed a set, we'll get frames from there first.
                If they also passed their own frames, regardless of being attached to a set, we'll merge those onto
                the frames from the set.
            """
            if 'frame_set' in kwargs:
                for frame in self._frames_to_get:
                    _frame = kwargs['frame_set'].frames.get(frame)
                    self._frames.set(frame, _frame)
                del kwargs['frame_set']

            if 'frames' in kwargs:
                self._frames = DeepDict(merge(self._frames, kwargs['frames']))

            kwargs['frames'] = self._frames
            return fn(*args, **kwargs)
        return new_func


def computation(fn):

    def wrapped(*args, **kwargs):
        if (type(args[0]).__name__ is not 'FrameSet'):
            msg = 'A computation was passed a type of "{1}", but requires a type of "FrameSet"'.format(fn.__name__, type(args[0]).__name__)
            msg += '\nHint: If you\'re trying to chain it, you can\'t chain a computation (multi-frame) after an operation (single-frame)'
            raise TypeError(msg)

        return fn(*args, **kwargs)

    return wrapped
