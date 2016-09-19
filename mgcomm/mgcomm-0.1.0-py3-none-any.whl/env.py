"""
Functions to deal with system's environment.
"""

import os


def home():
    """Simply returns user's home directory."""
    return os.path.expanduser('~')


def var_split(var, default=None, sep=':'):
    """Returns a splitted list of strings specified in a given environment
    variable. Accepts default parameter which can be either a list which should
    be returned when var is not found or a string which should be splitted.

    Example:
        os.environ['PATH'] = "/usr/bin:/usr/local/bin"
        assert var_split('PATH') == ['/usr/bin', '/usr/local/bin']
        assert var_split('path') == []

        os.environ['abc'] = "a,b,c"
        assert var_split('abc', sep=',') == ['a', 'b', 'c']

        assert var_split('foo', 'my_val') == ['my_val']
    """

    if not default:
        default = []

    env_var = os.getenv(var, default)
    if env_var:
        try:
            return env_var.split(sep)
        except AttributeError:
            return list(env_var)
    return default
