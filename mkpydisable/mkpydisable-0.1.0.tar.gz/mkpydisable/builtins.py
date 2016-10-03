from . import __builtin__

__author__ = 'Michael'

__hasattr__ = __builtin__.hasattr
__getattr__ = __builtin__.getattr
__setattr__ = __builtin__.setattr
__delattr__ = __builtin__.delattr


def override_builtin(name, obj):
    __setattr__(__builtin__, name, obj)


class Builtins(object):
    def __init__(self, allow_builtins=True):
        self.__allow_all = allow_builtins
        self.__allowed = set()
        self.__disabled = set()
        self.__overridden = {}

    def allow(self, *names):
        self.__allowed.update(names)

    def disable(self, *names):
        self.__disabled.update(names)

    def override(self, name=None, value=None, **kwargs):
        if name is not None:
            self.__overridden[name] = value
        else:
            for key in kwargs:
                self.__overridden[key] = kwargs[key]

    def __setattr__(self, key, value):
        if key.startswith("_Builtins__") or __hasattr__(self, key):
            object.__setattr__(self, key, value)
        else:
            self.override(key, value)

    def __delattr__(self, item):
        if __hasattr__(self, item):
            object.__delattr__(self, item)
        else:
            self.disable(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __del(self, name):
        __delattr__(__builtin__, name)

    def __override(self, name):
        __setattr__(__builtin__, name, self.__overridden[name])

    def do(self):
        if self.__allow_all:
            for name in __builtin__.__dict__.keys():
                if name in self.__disabled:
                    self.__del(name)
                elif name in self.__overridden:
                    self.__override(name)
        else:
            for name in __builtin__.__dict__.keys():
                if name in self.__allowed:
                    continue
                elif name in self.__overridden:
                    self.__override(name)
                else:
                    self.__del(name)
