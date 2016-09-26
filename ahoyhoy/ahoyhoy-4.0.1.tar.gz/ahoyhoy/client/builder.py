import abc
import logging

from six import add_metaclass

from . import Client, SimpleClient
from ..retries import Retry


logger = logging.getLogger(__name__)


@add_metaclass(abc.ABCMeta)
class IClientBuilder(object):
    """
    Abstract Builder class. Contains required methods
    for all other client builders.
    """

    def __init__(self):
        self._session = None
        self._headers = {}
        self._retries = None

    def add_session(self, session):
        """
        Add your custom session here.
        """
        self._session = session
        return self

    def add_retries(self, retries):
        """
        Custom retries function. It has to accept function to retry w/ its args and kwargs.
        It's highly recommended to use :func:`ahoyhoy.retries.Retry` function with custom parameters.
        """
        self._retries = retries
        return self

    def add_headers(self, headers):
        """
        Provide your custom headers here.
        """
        self._headers = headers
        return self

    @abc.abstractmethod
    def _validate_required_params(self):
        """
        Check that all required parameters were provided.
        """
        return

    @abc.abstractmethod
    def build(self):
        """
        Build and return the client.
        """
        self._validate_required_params()
        return


class LBClientBuilder(IClientBuilder):
    """
    Usage examples:

    1. Round Robin LB

        >>> from ahoyhoy.utils import Host
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.lb import RoundRobinLB
        >>>
        >>> rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)))
        >>>
        >>> client = LBClientBuilder().add_lb(rrlb).build()
        >>> client.get('/')
        <Response [200]>

    2. Round Robin LB and custom session

        >>> import requests
        >>> s = requests.Session()
        >>> s.headers.update({'bla': 'foo'})
        >>> client = LBClientBuilder().add_lb(rrlb).add_session(s).build()
        >>> client.get('/')
        <Response [200]>

    3. Round Robin LB with custom HTTP retries

        >>> from ahoyhoy.retries import Retry
        >>> from requests.exceptions import ConnectTimeout
        >>>
        >>> retries = Retry(exceptions=ConnectTimeout, tries=3, delay=0, max_delay=None, backoff=2, jitter=0)
        >>> rrlb = RoundRobinLB(ListProvider(Host('google.com', 80)))
        >>>
        >>> client = LBClientBuilder().add_lb(rrlb).add_retries(retries).build()
        >>> client.get('/')
        <Response [200]>

    4. Set multiple updates for endpoints list

        >>> client = LBClientBuilder().add_lb(rrlb).set_endpoint_updates(3)

    """
    def __init__(self):
        super(LBClientBuilder, self).__init__()
        self._lb = None
        self._ep_updates = 1

    def add_lb(self, lb):
        """
        Add your load balancer instance here.
        """
        self._lb = lb
        return self

    def set_endpoint_updates(self, ep_updates):
        """
        Sets the number of times an endpoints list has to be updated.
        By default it's 1, which is the initial update of available endpoints.

        :param ep_updates: int, number of updates of ep list if there're no endpoints
         in the closed state
        """
        self._ep_updates = ep_updates
        return self

    def _validate_required_params(self):
        assert self._lb

    def build(self):
        super(LBClientBuilder, self).build()

        return Client(self._lb,
            session=self._session,
            headers=self._headers,
            retry_http_call_func=self._retries,
            ep_list_update_tries=self._ep_updates)


class SessionClientBuilder(IClientBuilder):
    """
    Usage example:

        >>> import requests
        >>> from ahoyhoy.client.builder import SessionClientBuilder
        >>>
        >>> s = requests.Session()
        >>>
        >>> client = SessionClientBuilder().add_session(s).build()
        >>> client.get('http://google.com')
        <Response [200]>

    Custom headers:

        >>> s.headers.update({'bla': 'foo'})
        >>> client = SessionClientBuilder().add_session(s).build()
        >>> response = client.get('http://google.com')
        >>> assert 'bla' in response.request.headers

    or

        >>> client = SessionClientBuilder().add_session(s).add_headers({'foo': 'bar'}).build()
        >>> response = client.get('http://google.com')
        >>> assert 'foo' in response.request.headers

    Custom retries:

        >>> from ahoyhoy.retries import Retry
        >>> from requests.exceptions import ConnectTimeout
        >>>
        >>> retries = Retry(exceptions=ConnectTimeout, tries=3, delay=0, max_delay=None, backoff=2, jitter=0)
        >>>
        >>> client = SessionClientBuilder().add_session(s).add_retries(retries).build()
        >>> client.get('http://google.com')
        <Response [200]>
    """
    def _validate_required_params(self):
        assert self._session

    def build(self):
        super(SessionClientBuilder, self).build()

        self._session.headers.update(self._headers)

        return SimpleClient(session=self._session,
            retry_http_call=self._retries)
