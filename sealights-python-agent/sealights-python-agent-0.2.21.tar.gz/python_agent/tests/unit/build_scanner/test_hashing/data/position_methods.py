import functools


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer


@memoize
@memoize
@memoize
def foo(a, b):
    return a + b


@memoize
def bar(a, b):
    return a + b


def sum_two(a, b):
    return a + b
