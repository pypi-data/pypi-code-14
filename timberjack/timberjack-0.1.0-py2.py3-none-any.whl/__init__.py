import structlog

__title__ = 'timberjack'
__author__ = 'Sebastian Vetter'
__version__ = '0.1.0'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Mobify Research & Development Inc.'


def get_logger(name=None, *args, **kwargs):
    """
    Get a new logger with a default name `brain` if none is specified.
    """
    if not name:
        name = 'brain'
    return structlog.get_logger(name, *args, **kwargs)
