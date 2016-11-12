"""Main module for Editorial-Sphinx-Theme."""

import os.path

__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))


def get_html_theme_path():
    """Shortcut for users whose theme is next to their conf.py."""
    theme_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return theme_path
