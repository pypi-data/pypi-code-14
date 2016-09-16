"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        emitter.py -- Emit messages

    FIRST RELEASE
        2016-07-06  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
from enum import IntEnum, unique
from cuebung_helper import __version__

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"
__all__ = ['emit', 'set_emit', 'MsgType']


@unique
class MsgType(IntEnum):
    """Message types"""
    message = 0
    passed = 1
    failed = 2
    failed_timedout = 3
    failed_returncode = 4
    failed_output_linecount = 5
    failed_stderr = 6
    failed_stdout = 7
    failed_error = 8


class Emitter():
    """Emitter class with singleton pattern"""
    emit = None

    def __init__(self):
        cls = self.__class__
        if cls.emit is None:  # pragma: no cover
            cls.emit = cls.default_emit

    def __call__(self, msg, *args, msgtype=MsgType.message, **kwargs):
        """Call the emit function"""
        assert isinstance(msg, dict)
        _msg = msg.copy()
        _msg['msgtype'] = msgtype
        cls = self.__class__
        return cls.emit(_msg, **kwargs)

    @staticmethod
    def default_emit(msg, **kwargs):  # pylint: disable=W0613
        """Emit the message dict"""
        print(msg)


emit = Emitter()  # pylint: disable=C0103


def set_emit(func):
    """Set a custom emit function"""
    Emitter.emit = func


def reset_emit():
    """reset the default emit function"""
    Emitter.emit = Emitter.default_emit

# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
