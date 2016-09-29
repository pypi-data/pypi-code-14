"""jinja2-registry: Easy handling of multiple loaders and default contexts"""

from __future__ import absolute_import

__version__ = '0.0.4'
__author__ = '3point Science'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 3point Science'

from .base import Renderer, register_loader, register_filesystem_loader
