"""
.. py:module:: brite_etl.core.operations

Operations in general are functions that are done on a single frame, but no specific frame.
Specific frame functions belong in the frame class themselves.
"""
# flake8: noqa
from __future__ import division, absolute_import, print_function

from .hash_cols import hash_cols

__all__ = [
	'hash_cols'
]
# __api__ = []