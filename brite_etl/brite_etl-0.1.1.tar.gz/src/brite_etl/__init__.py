# flake8: noqa
from __future__ import division, absolute_import, print_function

__version__ = "0.1.1"

from ._globals import logger, NoValue

from . import abstracts
from . import core
from . import frames
from . import lib
from . import utils

# # Make these guys available from package namespace
# from pkgutil import extend_path
# __path__ = extend_path(__path__, core.__name__)
# __path__ = extend_path(__path__, lib.__name__)
# del extend_path # removes from namespace
