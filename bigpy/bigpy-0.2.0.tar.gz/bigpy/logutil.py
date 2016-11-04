"""
A collection of useful logging utilities
"""
import logging
from . import ensure_not_blank


class LoggerProxy(object):
    """
    A "proxy" class that supports delayed logging instantiation (on first call to any method).

    This becomes very useful for defining module-global loggers that don't get prematurely
    initialized before the proper configuration can be read. An example of such situation
    would be a Flask application, especially using the factory method for creating the
    application object itself.
    """

    def __init__(self, name):
        self.name = ensure_not_blank(name, 'Logger name is required')
        self._logger = None

    def __getattr__(self, attr):
        if not self._logger:
            self._logger = logging.getLogger(self.name)
        return getattr(self._logger, attr)
