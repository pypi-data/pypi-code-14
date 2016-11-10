import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


from .core import Donald # noqa


__version__ = "0.0.0"
__project__ = "Donald"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "BSD"
