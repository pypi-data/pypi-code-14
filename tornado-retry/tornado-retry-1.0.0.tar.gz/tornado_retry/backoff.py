"""
Basic backoff strategies
"""

__all__ = [
    'backoff',
]


def exponential(max_value, base=2, factor=1):
    """
    Generator for exponential delay.

    :param base: The mathematical base of the exponentiation operation
    :param factor: Factor to multiply the exponentation by.
    """
    n = 0
    a = factor * base ** n

    while True:
        if max_value and max_value < a:
            yield max_value
        else:
            a = factor * base ** n

            yield a

            n += 1


def fibonacci(max_value):
    """
    Generator for fibonacci delay.
    """
    a = 1
    b = 1

    while True:
        if max_value and max_value < a:
            yield max_value
        else:
            yield a

            a, b = b, a + b


def constant(value):
    while True:
        yield value


def get_iter(strategy, max_delay):
    """
    Returns an iterable that will provide the number of seconds to backoff
    based on the supplied strategy.

    :param strategy: A string that represents the strategy or a callable that
        will take `max_delay` as the first argument. The return of that call
        must be an iterable.
    """
    if strategy in ['exponential', 'exp']:
        return exponential(max_delay)
    elif strategy in ['fibonacci', 'fib']:
        return fibonacci(max_delay)
    elif strategy in ['constant', 'const']:
        return constant(max_delay)
    elif callable(strategy):
        return strategy(max_delay)

    raise ValueError(
        'Unknown backoff strategy {!r}'.format(strategy)
    )


def backoff(delay_iter, jitter, min_delay, max_delay, max_retries):
    """
    Generator that yields the number of seconds that the backoff should be
    applied.

    :param delay_iter: An iterable that produces the number of seconds to
        backoff. This can be used to change backoff strategies (e.g.
        exponential vs fibonacci). This iterable must produce floats/ints in
        seconds. See :ref:`get_iter` for more.
    :param jitter_func: A callable accepts the output of the delay_iter and
        introduces some jitter. The return of this function must be an
        int/float. See :ref:`tornado_retry.jitter` for more.
    :param min_delay: The minimum number of seconds to backoff.
    :param max_delay: The maximum number of seconds to backoff.
    :param max_retries: The maximum number of retries before the generator is
        cancelled. Set to `0` for infinite backoff.
    """
    count = 1

    while True:
        if max_retries and count >= max_retries:
            return

        try:
            delay = delay_iter.next()
        except StopIteration:
            return

        if delay < min_delay:
            delay = min_delay
        else:
            delay = min(delay, max_delay)

        delay = jitter(delay)

        yield float(delay)

        count += 1
