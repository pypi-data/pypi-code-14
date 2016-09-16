"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        __init__.py

    FIRST RELEASE
        2016-06-29  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""
import pkg_resources
try:
    __version__ = pkg_resources.get_distribution(__name__).version  # noqa  # pylint: disable=E1101
except:  # pragma: no cover  # pylint: disable=W0702
    __version__ = 'unknown'  # pragma: no cover

from .returnobject import *  # pylint: disable=W0401,C0413
from .runcode import *  # pylint: disable=W0401,C0413
from .emitter import *  # pylint: disable=W0401,C0413
from .helper import exchange_values  # pylint: disable=C0413

__all__ = (returnobject.__all__ +  # pylint: disable=E0602
           runcode.__all__ +  # pylint: disable=E0602
           helper.__all__ +  # pylint: disable=E0602
           emitter.__all__)  # pylint: disable=E0602
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
