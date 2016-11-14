import statsd
import logging


log = logging.getLogger(__name__)
_config = {}


def configure(*args, **kwargs):
    """Configure the module level statsd client that will
    be used in all library operations.

    Frequently used from application initialization code.

    >>> import statsdecor
    >>> statsdecor.configure(
            host='localhost',
            port=8125,
            prefix='myapp',
            maxudpsize=25)
    """
    log.debug('statsd.configure(%s)' % kwargs)
    _config.update(kwargs)


def client():
    """Get a client instance with the module level configuration.

    For docs on the statsd client, see
    http://statsd.readthedocs.org/en/latest/types.html

    For the code, see
    https://github.com/jsocol/pystatsd/blob/master/statsd/client.py
    """
    return statsd.StatsClient(**_config)


def incr(name, value=1, rate=1):
    """Increment a metric by value.

    >>> import statsdecor
    >>> statsdecor.incr('my.metric')
    """
    client().incr(name, value, rate)


def decr(name, value=1, rate=1):
    """Decrement a metric by value.

    >>> import statsdecor
    >>> statsdecor.decr('my.metric')
    """
    client().decr(name, value, rate)


def gauge(name, value, rate=1):
    """Set the value for a gauge.

    >>> import statsdecor
    >>> statsdecor.gauge('my.metric', 10)
    """
    client().gauge(name, value, rate)


def timer(name):
    """Time a block of code with a context manager.

    >>> import statsdecor
    >>> with statsdecor.timer('my.timer'):
    >>>     print('Some output')
    Some output
    """
    return client().timer(name)

def timing(name, delta, rate=1):
    """Sends new timing information. `delta` is in milliseconds.

    >>> import statsdecor
    >>> statsdecor.timing('my.metric', 314159265359)
    """
    return client().timing(name, delta, rate)
