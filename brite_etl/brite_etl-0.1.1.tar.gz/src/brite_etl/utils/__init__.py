"""
.. py:module:: brite_etl.utils

This is misc stuff. Probably needs to be reorganized.
"""
# flake8: noqa
from __future__ import absolute_import

from .chaining import _Chain

# Quick alias
_btl = _Chain()

__all__ = ['_btl', '_Chain']
__api__= []
