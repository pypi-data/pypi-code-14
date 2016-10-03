from mklibpy.common.string import String, AnyString

from . import __builtin__

__author__ = 'Michael'

__import___ = __builtin__.__import__
__ImportError__ = __builtin__.ImportError


class AllowPolicy(object):
    NONE = 0
    ALL = 256
    ALLOW = 1
    DISALLOW = 2

    def __init__(self, value=ALL):
        self.__value = value
        self.__allowed = AnyString()
        self.__disallowed = AnyString()

    def allow_names(self, *names):
        self.__allowed.add(*names)

    def disallow_names(self, *names):
        self.__disallowed.add(*names)

    def allows(self, name):
        if self.__value == AllowPolicy.NONE:
            return False
        elif self.__value == AllowPolicy.ALL:
            return True

        def __match(s):
            return name == s or name.startswith(s + ".")

        if self.__value & AllowPolicy.ALLOW:
            return __match(self.__allowed)
        if self.__value & AllowPolicy.DISALLOW:
            return not __match(self.__disallowed)

        return False


class Import(object):
    def __init__(self, allow=True):
        self.__policy = AllowPolicy(AllowPolicy.ALL if allow else AllowPolicy.NONE)

    def set_policy(self, p):
        self.__policy = p

    def __make(self, __builtin_call):
        def __new_import(name, globals={}, locals={}, fromlist=[], level=-1):
            __name = String(name)

            def __builtin_call_():
                return __builtin_call(name, globals=globals, locals=locals, fromlist=fromlist, level=level)

            def __raise():
                raise __ImportError__("Importing \'{}\' is forbidden".format(name))

            if self.__policy.allows(__name):
                return __builtin_call_()
            else:
                __raise()

        return __new_import

    def make(self):
        return self.__make(__import___)
