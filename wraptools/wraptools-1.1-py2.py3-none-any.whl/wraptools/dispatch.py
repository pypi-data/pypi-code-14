def dispatch(*dispatchers, **kwargs):
    """ Dispatch

    :arg dispatchers: will be a iterable of pair tuple
    which has dispatcher function as first element
    and target function as second element.

    The dispatcher function will take same arguments with target functions
    and will return True or False.
    When it is a True, corresponding target function will be called.

    >>> f = dispatch(
    ...     (lambda x: x % 2, lambda x: str(x) + "is odd"),
    ...     default=lambda x: str(x) + "is even",
    ... )
    ...
    >>> print(f(3))  # say 3 is odd

    :arg default: function will be called if all of dispatchers will return False.
    default function is optional so when default is not specified, it will return None.
    """
    # JUST FOR SUPPORTING PYTHON 2 SYNTAX
    default = kwargs.get('default')

    def wrapped(*args, **kwargs):
        for dispatcher, func in dispatchers:
            if dispatcher(*args, **kwargs):
                return func(*args, **kwargs)

        if default:
            return default(*args, **kwargs)

    return wrapped


def all_(*dispatchers):
    """ Taking :arg dispatchers: functions and routing when all of dispatchers returns True
    """
    def dispatcher(*args, **kwargs):
        return all(d(*args, **kwargs) for d in dispatchers)
    return dispatcher


def any_(*dispatchers):
    """ Taking :arg dispatchers: and routing when some dispatchers returns True
    """
    def dispatcher(*args, **kwargs):
        return any(d(*args, **kwargs) for d in dispatchers)
    return dispatcher


def not_(dispatcher):
    """ Taking :arg dispatcher: and routing when the dispatcher returns False
    """
    def _dispatcher(*args, **kwargs):
        return not dispatcher(*args, **kwargs)
    return _dispatcher


class dispatcher:
    """ Decorator applying utilities for wrapped function.
    Basically dispatcher is just a function which returns bool values, but when
    decorating this, dispatcher functions can be combined and inverted.

    >>> @dispatcher
    ... def even(n):
    ...     return n % 2 == 0
    ...
    >>> @dispatcher
    ... def multiple_three(n):
    ...     return n % 3 == 0
    ...
    >>> even & multiple_three  # New dispatcher that routes when multiple of 6.
    >>> even | multiple_three  # New dispatcher that routes when multiple of 2 or 3.
    >>> ~even  # New dispatcher that routes when odd
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __and__(self, other):
        return self.__class__(all_(self.func, other.func))

    def __or__(self, other):
        return self.__class__(any_(self.func, other.func))

    def __invert__(self):
        return self.__class__(not_(self.func))
