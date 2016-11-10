"""
  Module for queus which store crawl state.
"""

from .Local import LocalQueue
from .RedisQueue import RedisQueue

__all__ = ['LocalQueue', 'RedisQueue']

