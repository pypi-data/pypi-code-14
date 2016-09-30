'''
Implement the Lazy class for use with the @lazy decorator
'''
class Lazy(object):
    '''
    the Lazy class for use with the @lazy decorator
    '''
    special_names = {'__LazyValue__', '_Lazy__evaluated', '_Lazy__func',
                     '_Lazy__args', '_Lazy__value', '_Lazy__kwargs'}

    def __init__(self, func, args, kwargs):
        # print('as called __init__(%s, %s, %s)' % (func, args, kwargs,))
        self.__args = tuple(args)
        self.__kwargs = frozenset(kwargs.items())
        self.__func = func
        self.__evaluated = False
        self.__value = None

    def __LazyValue__(self):
        if not self.__evaluated:
            # print('now evaluating what the function call would be')
            # print('args: %s and %s' % (self.__args, self.__kwargs,))
            self.__value = self.__func.__call__(*(self.__args), **(dict(self.__kwargs)))
            self.__evaluated = True
            # print('value is now %s' % (self.__value,))

    def __eq__(self, other):
        self.__LazyValue__()
        return self.__value == other

    def __bool__(self):
        self.__LazyValue__()
        return bool(self.__value)

    def __nonzero__(self):
        self.__LazyValue__()
        return bool(self.__value)

    def __str__(self):
        self.__LazyValue__()
        return str(self.__value)

    def __repr__(self):
        self.__LazyValue__()
        return repr(self.__value)

    def __setattr__(self, name, value):
        # print('__setattribute__(self, %s, %s)' % (name, value,))
        if name in Lazy.special_names:
            return object.__setattr__(self, name, value)
        self.__LazyValue__()
        setattr(self.__value, name, value)

    def __getattribute__(self, name):
        # print('__getattribute__(self, %s)' % (name,))
        if name in Lazy.special_names:
            return object.__getattribute__(self, name)
        self.__LazyValue__()
        return getattr(self.__value, name)
