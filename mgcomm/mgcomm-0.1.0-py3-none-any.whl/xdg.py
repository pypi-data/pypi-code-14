"""
Utility functions to conform to XDG's specifications
"""

import os

from mgcomm.env import var_split, home


def config(app_name, config_name, default=None):
    """Search for application's configuration file.

    Search order is the following (first match is returned):
    1. $XDG_CONFIG_HOME/`app_name`/`config_name`
       (or ~/.config/`app_name`/`config_name`)
    2. each of $XDG_CONFIG_DIRS{/`app_name`/`config_name`}
       (or /etc/xdg/`app_name`/`config_name`)

    Example:
        assert '/home/user/.config/app/cfg.ini' == config('app', 'cfg.ini')
    """
    def _exists(path):
        try:
            with open(path):
                return True
        except IOError:
            return False

    for cfg_dir in _xdg_base_dirs():
        rcfile = os.path.join(cfg_dir, app_name, config_name)
        if _exists(rcfile):
            return rcfile
    return default


def config_dir(app_name, default=None):
    """Search for a directory with stored application's configuration.

    Example:
        assert '/home/user/.config/app/' == config_dir('app')
    """
    for cfg_dir in _xdg_base_dirs():
        dirname = os.path.join(cfg_dir, app_name)
        if os.path.isdir(dirname):
            return dirname
    return default


def _xdg_base_dirs():
    """XDG Base Directory search, according to this spec:
    http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """
    config_home = var_split('XDG_CONFIG_HOME', os.path.join(home(), '.config'))
    config_dirs = var_split('XDG_CONFIG_DIRS', '/etc/xdg')

    # XDG_CONFIG_HOME is the most important directory and should be searched
    # before anything
    return config_home + config_dirs
