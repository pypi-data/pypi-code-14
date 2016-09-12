import logging

from . import Client, SimpleClient
from ..retries import Retry


logger = logging.getLogger(__name__)


class ClientBuilder(object):
    """
    Provide client with all required information.

    Examples:

    1. Round Robin LB

        >>> from ahoyhoy.utils import Host
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.lb import RoundRobinLB
        >>> rrlb = RoundRobinLB(ListProvider(Host('badhost2.bla', 80), Host('google.com', 80), Host('badhost3.bla', 80)))
        >>> client = ClientBuilder.with_lb(rrlb)
        >>> client.get('/')
        <Response [200]>

    2. Round Robin LB with custom HTTP retries

        >>> from ahoyhoy.retries import Retry
        >>> from requests.exceptions import ConnectTimeout
        >>> retry = Retry(exceptions=ConnectTimeout, tries=3, delay=0, max_delay=None, backoff=2, jitter=0)
        >>> rrlb = RoundRobinLB(ListProvider(Host('google.com', 80)))
        >>> client = ClientBuilder.with_lb(rrlb, retry_http_call=retry)
        >>> client.get('/')
        <Response [200]>

    3. Simple session

        >>> import requests
        >>> s = requests.Session()
        >>> s.headers.update({'bla': 'foo'})
        >>> from ahoyhoy.client.builder import ClientBuilder
        >>> client = ClientBuilder.with_session(s, headers={'bar': 'foo'})
        >>> response = client.get('http://google.com')
        >>> assert 'bla' in response.request.headers.keys()
        >>> assert 'bar' in response.request.headers.keys()

    """

    def __init__(self):
        raise RuntimeError("Builder can't be instantiated. Use `with_session` or `with_lb` methods to build the client.")

    @staticmethod
    def with_session(session, headers=None, retry_http_call=None):
        """
        :param session: session instance (required)
        :param headers: custom headers
        :type headers: dict
        :return: :class:`~ahoyhoy.client.Client` instance
        """
        if retry_http_call is None:
            retry_http_call = Retry(tries=3)  # only try 3 times by default

        if headers:
            session.headers.update(headers)
        logger.debug(session)
        return SimpleClient(session=session, retry_http_call=retry_http_call)

    @staticmethod
    def with_lb(lb, session=None, headers=None, retry_http_call=None, ep_list_update_tries=1):
        """
        :param lb: LB instance (required)
        :param session: custom session
        :param headers: custom headers
        :type headers: dict
        :param retry_http_call: function for retrying HTTP calls (see examples above).
         By default: :func:`ahoyhoy.retries.Retry` with one try.
        :type retry_http_call: partial
        :param ep_list_update_tries: number of retries to update an Endpoints list
        :type ep_list_update_tries: int
        :return: :class:`~ahoyhoy.client.Client` instance
        """
        if retry_http_call is None:
            retry_http_call = Retry(tries=3)  # only try 3 times by default

        return Client(lb, session=session, headers=headers, retry_http_call_func=retry_http_call, ep_list_update_tries=ep_list_update_tries)
