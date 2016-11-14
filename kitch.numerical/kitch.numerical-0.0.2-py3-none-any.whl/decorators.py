"""
This module contains numerical decorators.
"""

import numerical.conversions as conversions

__all__ = ['non_negative_args', 'decimal_args', 'rounding']


def non_negative_args(func):
    """Convert a function to only accept numeric arguments > 0."""

    def new_func(*args, **kwargs):
        if any(a < 0 for a in args + tuple(kwargs.values())):
            return None
        return func(*args, **kwargs)

    return new_func


def decimal_args(func):
    """Convert a function's numeric arguments to decimals."""

    def new_func(*args, **kwargs):
        args = [conversions.to_dec(a) for a in args]
        kwargs = {k: conversions.to_dec(v) for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return new_func


def rounding(prec=2):
    """Convert a function's returned value to the given rounding."""

    def decorator(func):

        def new_func(*args, **kwargs):
            result = func(*args, **kwargs)
            return round(result, prec)

        return new_func

    return decorator
