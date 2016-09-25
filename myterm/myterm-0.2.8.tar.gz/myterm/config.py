#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import types
import errno
import sys

PY2 = sys.version_info[0] == 2
if not PY2:
    string_types = (str,)
    iteritems = lambda d: iter(d.items())

else:
    string_types = (str, unicode)
    iteritems = lambda d: d.iteritems()

class Config(dict):

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_pyfile(self, filename, silent=False):
        """
        Updates the values in the config from a Python file.  
        """
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename) as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True
  
    def from_env(self, namespace):
        for key in os.environ:
            if key.startswith(namespace) and key.isupper():
                try:
                    self[key] = int(os.environ.get(key))
                except:
                    self[key] = os.environ.get(key)

    def from_object(self, obj):
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)



    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
