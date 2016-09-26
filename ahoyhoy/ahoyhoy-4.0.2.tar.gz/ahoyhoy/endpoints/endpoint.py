"""
Endpoint

A host and port endpoint
"""

import logging
import requests

from functools import wraps

from ..circuit import Circuit
from ..servicediscovery import ServiceDiscoveryHttpClient


logger = logging.getLogger(__name__)


class Endpoint(Circuit):
    """
    Accepts a duck-typed session (a "Session" in Requests terms)
    and allows it to work as a Circuit (open|closed state).

    Endpoint simply proxies to `session` methods, so it's just as easy
    to use as ServiceDiscoveryHttpClient.

        >>> from ahoyhoy.endpoints import Endpoint
        >>> from ahoyhoy.utils import Host
        >>> host = Host('google.com', '443')
        >>> ep = Endpoint(host)
        >>> ep.get('/')
        <Response [200]>
        >>> ep.open()
        >>> ep.get('/')
        Traceback (most recent call last):
        ...
        RuntimeError: Circuit state is open, no connections possible.

    When using service discovery, this fits nicely with the way that Load Balancers
    work.

        >>> from ahoyhoy.lb import RoundRobinLB
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.utils import Host
        >>> lb = RoundRobinLB(ListProvider(Host('google.com', '80')))
        >>> ep = lb.pick()
        >>> ep.get('/')
        <Response [200]>
        >>> ep.open()
        >>> ep.get('/')
        Traceback (most recent call last):
         ...
        RuntimeError: Circuit state is open, no connections possible.

    Here's an example of how circuit opens automatically:

        >>> from ahoyhoy.lb import RoundRobinLB
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.utils import Host
        >>> lb = RoundRobinLB(ListProvider(Host('google1.com1', '80')))
        >>> ep = lb.pick()
        >>> ep
        <Endpoint/.../Host(address='google1.com1', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>
        >>> ep.get('/')
        Traceback (most recent call last):
         ...
        requests.exceptions.ConnectionError: HTTPConnectionPool(host='google1.com1', port=80): Max retries exceeded with url:...
        >>> ep
        <Endpoint/.../Host(address='google1.com1', port='80')/<class 'ahoyhoy.circuit.circuit.OpenState'>

    Before you gasp at the number of lines there, remember that Endpoint is a
    relatively low-level component.  Higher-level components are easier to use,
    but Endpoints allow full flexibility.

    The SimpleHttpEndpoint factory function can be used when you don't need
    service discovery.

        >>> from ahoyhoy.endpoints import SimpleHttpEndpoint
        >>> sep = SimpleHttpEndpoint()
        >>> sep.get('http://google.com')
        <Response [200]>

    Custom exception callback function

        >>> def exc(e):
        ...     return 'I caught it!'
        >>> ep = Endpoint(Host('google1.com1', '80'), exception_callback=exc)
        >>> ep.get('/')
        'I caught it!'

    """

    def __init__(self, host=None, pre_callback=None, post_callback=None, exception_callback=None,
                 classify=None, retry=None, session=None, *args, **kwargs):
        """
        :param host: collections.namedtuple, Host(address, port)
        :param pre_callback:
        :param post_callback:
        :param exception_callback:
        :param classify: response clissifier. By default it's :attr:`Circuit's classify <ahoyhoy.circuit.circuit.StateClassifier.classify>`.
        :param retry: function for retrying HTTP calls
        :param session: custom session
        :param args: positional argument for ServiceDiscoveryHttpClient
        :param kwargs: keyword argument for ServiceDiscoveryHttpClient
        """

        super(Endpoint, self).__init__()

        self._host = host
        self._pre = pre_callback
        self._post = post_callback
        self._exc = exception_callback

        self._retry = retry

        # override classify if it was passed as a parameter
        if classify:
            self.classify = classify

        if self._host is not None:
            self._session = ServiceDiscoveryHttpClient(self._host, session=session, *args, **kwargs)
        else:
            self._session = session

        logger.debug("Create an Endpoint with session %s", self._session)

    @property
    def host(self):
        return self._host

    @property
    def state(self):
        return self._state

    def __eq__(self, other):
        return self.host == other.host

    # TODO: make this better
    def __repr__(self):
        return "<{}/{}/{}/{}".format(self.__class__.__name__,
                                     id(self), self.host, self.state)

    def __hash__(self):
        return hash(self._host)

    def get(self, *args, **kwargs):
        f = self.dispatch("get")
        return self.classify(f, *args, **kwargs)

    def options(self, *args, **kwargs):
        f = self.dispatch("options")
        return self.classify(f, *args, **kwargs)

    def head(self, *args, **kwargs):
        f = self.dispatch("head")
        return self.classify(f, *args, **kwargs)

    def post(self, *args, **kwargs):
        f = self.dispatch("post")
        return self.classify(f, *args, **kwargs)

    def put(self, *args, **kwargs):
        f = self.dispatch("put")
        return self.classify(f, *args, **kwargs)

    def patch(self, *args, **kwargs):
        f = self.dispatch("patch")
        return self.classify(f, *args, **kwargs)

    def delete(self, *args, **kwargs):
        f = self.dispatch("delete")
        return self.classify(f, *args, **kwargs)

    def set_retry(self, retry_func):
        self._retry = retry_func

    def set_headers(self, headers):
        self._session.headers.update(headers)

    def __getattr__(self, name):
        """
        For all other endpoint methods we don't need retries.
        """

        logger.debug("Calling __getattr__: %s", name)

        realfunc = getattr(self._session, name)

        if callable(realfunc):
            @wraps(realfunc)
            def func(*args, **kwargs):
                logger.debug("Return callable with attributes: %s, %s", args, kwargs)
                return realfunc(*args, **kwargs)
            return func
        else:
            logger.debug("Return an attribute.")
            return realfunc


def SimpleHttpEndpoint(session=None, retry=None):
    """
    Simple CircuitBreaking Endpoint that uses a default
    (non-service discoverable) client
    """
    if session is None:
        session = requests.Session()

    logger.debug("Create SimpleHttpEndpoint with session %s and retry %s" , session, retry)

    return Endpoint(session=session, retry=retry)