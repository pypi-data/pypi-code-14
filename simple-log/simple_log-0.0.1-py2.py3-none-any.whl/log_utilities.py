"""
Wrapper around the standard logging module to provide a simplified interface with sensible defaults

Written in and tested against Python 3 only.

Licensed under the MIT license - https://opensource.org/licenses/MIT
"""
__version__ = (0, 1, 0)
__date__ = (2016, 9, 21)
__author__ = "Andrew J Todd esq. <andy47@halfcooked.com>"

import logging

MESSAGE_FORMAT = '%(asctime)s %(levelname)s:: %(message)s'
DATE_FORMAT = '%Y.%m.%d %T'

logs = {}


def get_log(logname=None):
    if not logname:
        log_name = 'default'
    else:
        log_name = logname
    if log_name in logs:
        return logs[log_name]
    else:
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(MESSAGE_FORMAT, DATE_FORMAT)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logs[log_name] = logger
        return logger


def set_level(log_name, level):
    """Set the level on <log_name> to <level>

    See the standard documentation for the valid list of levels. They are all implemented as module attributes so
    we just getattr in the call to setLevel
    """
    if log_name in logs:
        logs[log_name].setLevel(getattr(logging, level))
    else:
        raise AttributeError('{} is not a valid log'.format(log_name))
