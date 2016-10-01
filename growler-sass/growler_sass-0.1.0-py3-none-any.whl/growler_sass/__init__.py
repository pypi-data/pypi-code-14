#
# growler_sass.py
#
"""
Sass middleware package for Growler applications
"""

from .__meta__ import (
    version as __version__,
    date as __date__,
    author as __author__,
    license as __license__,
)

from .middleware import SassMiddleware
