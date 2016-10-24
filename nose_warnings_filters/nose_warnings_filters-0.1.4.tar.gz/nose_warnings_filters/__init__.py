
"""
Nose plugin to add warnings filters (turn them into error) using nose.cfg file.
"""

from __future__ import absolute_import


__version__ = '0.1.4'
from .testing import utils
from .base import import_item, from_builtins, InvalidConfig, WarningFilter, WarningFilterRunner

