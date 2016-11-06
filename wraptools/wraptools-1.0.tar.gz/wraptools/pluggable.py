from functools import wraps


_enable_pluggable_decorators = True


def pluggable(*decorators):
    """ Pluggable decorators

    @pluggable(
        require_POST,
        login_required,
    )
    def some_view(request):
        ''' Your view func here. '''

    ## Decorated behavior.
    res = some_view(request)

    ## Original behavior.
    res = some_view.original_func(request)

    ## decorators
    some_view.decorators

    ## Disabling temporarily
    With ``purge_pluggable_decorators`` you can disable all of decorators in it.
    See docs on ``purge_pluggable_decorators``.
    """
    def dec(func):
        _original_func = func
        for d in reversed(decorators):
            func = d(func)

        @wraps(func)
        def wrapped(*args, **kwargs):
            global _enable_pluggable_decorators
            if _enable_pluggable_decorators:
                return func(*args, **kwargs)
            else:
                return _original_func(*args, **kwargs)

        wrapped.original_func = _original_func
        wrapped.decorators = decorators

        return wrapped
    return dec


class purge_pluggable_decorators:
    """ decorator or context manager to disable applied decorators in it.
    This decorator/context manager is useful when you want to test decorated functions by
    ``pluggable`` decorator.

    >>> def hello(func):
    ...    def wrapped():
    ...         print("hello")
    ...         func()
    ...     return wrapped
    ...
    >>> @pluggable(
    ...     hello
    ... )
    ... def goodbye():
    ...     print("goodbye")
    ...
    >>> # As context manager
    >>> with purge_pluggable_decorators:
    ...     goodbye()  # Just say "goodbye"
    ...
    >>> # As decorator
    >>> @purge_pluggable_decorators
    ... def test():
    ...     goodbye()
    ...
    >>> test()  # Just say "goodbye"
    """
    @classmethod
    def purge(cls):
        global _enable_pluggable_decorators
        _enable_pluggable_decorators = False

    @classmethod
    def wrap(cls):
        global _enable_pluggable_decorators
        _enable_pluggable_decorators = True

    def __enter__(self):
        self.purge()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wrap()

    def __init__(self, func=None):
        self.func = func

    def __call__(self, *args, **kwargs):
        """ As decorator
        """
        with self:
            return self.func(*args, **kwargs)
