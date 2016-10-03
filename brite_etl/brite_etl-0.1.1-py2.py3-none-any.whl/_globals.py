# flake8: noqa
from __future__ import division, absolute_import, print_function


__all__ = [
    'logger', 'NoValue'
]


# Disallow reloading this module so as to preserve the identities of the
# classes defined here.
if '_is_loaded' in globals():
    raise RuntimeError('Reloading numpy._globals is not allowed')
_is_loaded = True


class NoValue(object):
    """Represents an unset value. Used to differeniate between an explicit
    ``None`` and an unset value.
    """
    pass


# Setup typechecking on parameters
from typedecorator import setup_typecheck
setup_typecheck()


# Colored Logs
import coloredlogs, logging
coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
coloredlogs.install(level='DEBUG')
logger = logging.getLogger('brite_etl')
