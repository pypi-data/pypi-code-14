from functools import wraps


def context(*context_funcs):
    """ Decorator to inject additional arguments taken by :param context_funcs:

    >>> data = {1: "user1", 2: "user2"}
    >>> @context(
    ...     lambda r, i: data.get(i),
    ... )
    ... def some_view(request, user_id, username):
    ...     print(username)
    ...
    >>>> some_view("request", 1)  # says user1
    """
    def dec(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            contexts = tuple(f(*args, **kwargs) for f in context_funcs)
            return func(*(args + contexts), **kwargs)
        return wrapped
    return dec
