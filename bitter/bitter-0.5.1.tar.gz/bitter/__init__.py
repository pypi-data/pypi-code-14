"""
Bitter module. A library and cli for Twitter using python-twitter.
http://github.com/balkian/bitter
"""

from future.standard_library import install_aliases
install_aliases()

import os

from .version import __version__

__all__ = ['cli', 'config', 'crawlers', 'models', 'utils' ]
