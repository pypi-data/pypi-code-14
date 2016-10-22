"""
When backing off, jitter provides some useful randomness so that all
re-attempts don't cause a 'thundering' herd problem.
"""

import random

__all__ = [
    'jitter',
]


def full_jitter(value):
    """
    Jitter that will provide a random value between 0 and `value`.
    See `https://www.awsarchitectureblog.com/2015/03/backoff.html`.
    """
    return random.uniform(0, value)


def random_jitter(value):
    """
    Typical jitter that will add up to a second based on the provided `value`.
    """
    return value + random.random()


def no_jitter(value):
    """
    Don't provide any jitter.
    """
    return value


def jitter(strategy='full'):
    """
    Returns a function that satisfies the jitter strategy.

    A pre-made label can be used but also you can supply a function that takes
    one argument (the delay in seconds) and must return a value that represents
    the delay in seconds to use (delay with jitter applied).
    """
    if strategy == 'full':
        return full_jitter
    elif strategy == 'random':
        return random_jitter
    elif strategy == 'none':
        return no_jitter
    elif callable(strategy):
        return strategy

    raise ValueError('Unknown jitter strategy %r' % (strategy,))
