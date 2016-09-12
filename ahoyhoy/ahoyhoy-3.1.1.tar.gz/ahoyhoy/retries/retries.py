from retry.api import retry_call
from functools import partial


def Retry(retry_func=retry_call, **kwargs):
    """

    Usage example:

    >>> import requests
    >>> s = requests.Session()
    >>> retry = Retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0)
    >>> response = retry(s.get, fargs=('http://google.com', ), fkwargs={'headers': {'bla': 'foo'}})

    :param retry_func callable: function which accepts input function and its parameters
    :param kwargs: retry_func kwargs
    """
    return partial(retry_func, **kwargs)