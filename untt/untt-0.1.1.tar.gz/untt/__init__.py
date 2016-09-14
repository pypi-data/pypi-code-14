"""
Right, It's uEntity.

For more information see child modules and the `README.md`.
"""
import logging

from untt.entity import Entity  # noqa

logging.getLogger('untt').addHandler(logging.NullHandler())

__version__ = '0.1.1'
