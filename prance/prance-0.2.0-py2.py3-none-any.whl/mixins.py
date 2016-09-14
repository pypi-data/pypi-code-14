# -*- coding: utf-8 -*-
"""
Defines Mixins for parsers.

The Mixins are here mostly for separation of concerns.
"""

__author__ = 'Jens Finkhaeuser'
__copyright__ = 'Copyright (c) 2016 Jens Finkhaeuser'
__license__ = 'MIT +no-false-attribs'
__all__ = ()


class CacheSpecsMixin(object):
  """
  CacheSpecsMixin helps determine if self.specification changed.

  It does so by caching a shallow copy on-demand.
  """

  __CACHED_SPECS = '__cached_specs'

  def specs_updated(self):
    """
    Test if self.specficiation changed.

    :return: Whether the specs changed.
    :rtype: bool
    """
    # Cache specs and return true if no specs have been cached
    if not getattr(self, self.__CACHED_SPECS, None):
      setattr(self, self.__CACHED_SPECS, self.specification.copy())
      return True

    # If specs have been cached, compare them to the current
    # specs.
    cached = getattr(self, self.__CACHED_SPECS)
    if cached != self.specification:
      setattr(self, self.__CACHED_SPECS, self.specification.copy())
      return True

    # Return false if they're the same
    return False


class YAMLMixin(CacheSpecsMixin):
  """
  YAMLMixin returns a YAML representation of the specification.

  It uses :py:class:`CacheSpecsMixin` for lazy evaluation.
  """

  __YAML = '__yaml'

  def yaml(self):
    """Return a YAML representation of the specifications."""
    # Query specs_updated first to start caching
    if self.specs_updated() or not getattr(self, self.__YAML, None):
      import yaml
      setattr(self, self.__YAML, yaml.dump(self.specification))
    return getattr(self, self.__YAML)


class JSONMixin(CacheSpecsMixin):
  """
  JSONMixin returns a JSON representation of the specification.

  It uses :py:class:`CacheSpecsMixin` for lazy evaluation.
  """

  __JSON = '__json'

  def json(self):
    """Return a JSON representation of the specifications."""
    # Query specs_updated first to start caching
    if self.specs_updated() or not getattr(self, self.__JSON, None):
      import json
      setattr(self, self.__JSON, json.dumps(self.specification))
    return getattr(self, self.__JSON)
