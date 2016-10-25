import functools
from time import sleep
from future.utils import reraise
import sys
from functools import reduce


def retry(num_attempts, exception_class, log):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(num_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_class as e:
                    if i == num_attempts - 1:
                        raise
                    else:
                        log.error('Failed with error %r, trying again', e)
                        sleep(1)

        return wrapper

    return decorator


def join_urls(*urls):
    return reduce(lambda url1, url2: url1.rstrip('/') + '/' + str(url2).lstrip('/'),
                  urls)


def add_exception_info(info):
    """
    Add the string info to the end of the message of the current exception while preserving the current traceback
    and also ensuring that the traceback shows the new information.
    Use with 'except Exception:' or something more specific, but not a bare except.
    Credit: http://stackoverflow.com/a/6062799/2482744
    """

    # Don't store the traceback (sys.exc_info()[2]) due to garbage collection problems:
    # see https://docs.python.org/2/library/sys.html#sys.exc_info
    exc_type, exc = sys.exc_info()[:2]
    reraise(exc_type, exc_type(str(exc) + "  \n  " + info), sys.exc_info()[2])


def strip_prefix(string, prefix):
    if string.startswith(prefix):
        return string[len(prefix):]
    return string
