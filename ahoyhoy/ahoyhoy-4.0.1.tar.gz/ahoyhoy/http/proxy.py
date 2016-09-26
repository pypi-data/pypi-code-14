import logging
from functools import wraps

import requests

logger = logging.getLogger(__name__)


class SessionProxy(object):
    """
    Proxy adapter so a subclass can proxy methods of a Requests Session,
    but can alter behavior via pre, post, and exception callbacks.

    Can be used by itself, but is intended to be subclassed with
    overwritten callbacks.

        >>> from ahoyhoy.http import SessionProxy
        >>> sp = SessionProxy()
        >>> sp.get('http://google.com')
        <Response [200]>

    In order to be a bit more transparent, excpetion_callback will raise
    the thrown exception.

        >>> from ahoyhoy.http import SessionProxy
        >>> import requests
        >>> sp = SessionProxy(requests.Session())
        >>> try:
        ...     sp.get('http://wwwwww.google.com')
        ... except requests.exceptions.ConnectionError as e:
        ...     print("Error raised")
        ...
        Error raised

    You may override the pre|post|exception callbacks either by subclassing
    them or by runtime configuration.

        >>> from ahoyhoy.http import SessionProxy
        >>> import requests
        >>>
        >>> def pre_callback(url):
        ...     print('pre')
        ...     return url
        >>>
        >>> def post_callback(res):
        ...     print('post')
        >>>
        >>> def exception_callback(e):
        ...     print('Exception!!')
        >>>
        >>> sp = SessionProxy(requests.Session(), pre_callback=pre_callback, post_callback=post_callback, exception_callback=exception_callback)
        >>> sp.get('http://google.com')
        pre
        post
        >>> sp.get('http://google1.com')
        pre
        Exception!!
        post

    Test proxy for other methods and attributes:

        >>> sp.headers
        {...'User-Agent': ...}

    """

    HTTP_CALLS = (
        'get',
        'options',
        'post',
        'put',
        'head',
        'patch',
        'delete',
    )

    def __init__(self, session=None, pre_callback=None, post_callback=None, exception_callback=None):
        """
        :param session: custom session
        :param pre_callback: executed before the proxied method
        :param post_callback: executed after the proxied method
        :param exception_callback: the proxied method is wrapped in a try/except block,
            and when an exception occurs, the exception is passed to this callback
        """
        if session is not None:
            self._session = session
        else:
            self._session = requests.Session()

        self._pre = pre_callback
        self._post = post_callback
        self._exc = exception_callback

    def __getattr__(self, name):
        """
        Proxy Requests methods to self._session, but first calculate the
        correct load balanced url to use via `pre_callback`.
        """

        realfunc = getattr(self._session, name)

        # if the attribute is HTTP call - use callbacks
        if name in self.HTTP_CALLS:
            @wraps(realfunc)
            def func(*args, **kwargs):
                result = None
                # first positional param is always url
                url = self.pre_callback(args[0])
                try:
                    result = realfunc(url, **kwargs)  # matches Requests API
                except Exception as e:
                    self.exception_callback(e)
                return self.post_callback(result)
            return func

        # if the attribute is NOT HTTP call - return w/ arguments
        elif callable(realfunc):
            @wraps(realfunc)
            def func(*args, **kwargs):
                return realfunc(*args, **kwargs)
            return func

        # if the attribute is NOT callable - return w/o arguments
        else:
            return realfunc

    def pre_callback(self, urlpath):
        """
        Executed before the proxied Requests method.

        Intended to be overwritten or set by a derived class.

        :param urlpath: the arg[0] of the called proxied method.
            Requests Session methods all take 'url' as the first positional
            parameter. By default, returns what's passed in.
        """
        logger.debug("Entered pre-callback")
        if self._pre is None:
            return urlpath

        return self._pre(urlpath)

    def post_callback(self, result):
        """
        Executed after the proxied Requests method.

        Intended to be overwritten or set by a derived class.

        :param result: the return value of the proxied Requests
            method.  By default, returns what's passed in.
        """
        logger.debug("Entered post-callback")
        if self._post is None:
            return result

        return self._post(result)

    def exception_callback(self, exc):
        """
        Executed when an exception is thrown by the proxied Requests Session method.

        Intended to be overwritten or set by a derived class.

        :param exc: the exception raised by the proxied Requests
            Session method. By default, returns what's passed in.
        """
        logger.debug("Entered exception callback")
        if self._exc is None:
            raise exc

        return self._exc(exc)

    def __dir__(self):
        return list(self.__dict__.keys()) + dir(self.__class__) + requests.Session().__dir__
