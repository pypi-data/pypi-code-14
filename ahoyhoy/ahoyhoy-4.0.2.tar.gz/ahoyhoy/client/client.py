import abc
import logging

from requests.exceptions import RequestException
from retry.api import retry_call

from ..lb.exceptions import LbNoEndpointsException
from .exceptions import AhoyhoyRequestsException, ClientNoEndpointsException


logger = logging.getLogger(__name__)


class Client(object):
    """
    A load balancing, circuit breaking client.

    Accepts load balancer instance as an argument.
    Client can be a duck-typed requests object.

    Usage examples:

    1. Client with RoundRobin LB and bad hosts

    >>> from ahoyhoy.utils import Host
    >>> from ahoyhoy.lb.providers import ListProvider
    >>> from ahoyhoy.lb import RoundRobinLB

    >>> bad_host1 = Host('google1.com1', '80')
    >>> bad_host2 = Host('google2.com2', '80')
    >>> good_host = Host('google.com', '80')
    >>> rrlb = RoundRobinLB(ListProvider(bad_host1, bad_host2, good_host))
    >>> client = Client(rrlb)
    >>> client.get('/')
    <Response [200]>


    *Note! Client only accepts HTTP calls for now.*

    Session's attributes and methods (except HTTP calls) are unavailable for calls
    through the Client's instance.
    Because of the dynamic nature of :class:`~ahoyhoy.endpoints.Endpoint` s, all parameters (such as headers etc.)
    have to be changed through the client-specific API.

    Consider these examples:

    >>> client.headers.update({'bla': 'foo'})
    Traceback (most recent call last):
    ...
    AttributeError: No such attribute: 'headers'. Only HTTP methods can be called for now.

    >>> c = Client(rrlb, headers={'bla': 'foo'})
    >>> response = c.get('/')
    >>> assert 'bla' in response.request.headers.keys()

    """

#   Retries logic:

#                                   +---------------------+
#                                   |  client.get('/url') |
#                                   +---------------------+
#                                              |
#                                              v
#                                   +---------------------+
# +------>----+------------>------->| Resolve an Endpoint |
# |           |                     +---------------------+
# |           |                                |
# |           |                                v
# |           |                  /----------------------------\
# |           |                  | Did LB raise `no available |  No
# |           |                  |    endpoints` exception?   |---------+
# |           |                  \----------------------------/         |
# |           |                                | Yes                    |
# |           |                                v                        |
# |   +-----------------+  No  /---------------------------------\      |
# |   |Update endpoints |<-----| Did max retries amount for up-  |      |
# |   |      list       |      | dating endpoints list exceeded? |      |
# |   +-----------------+      \---------------------------------/      |
# |                                            | Yes                    |
# |                                            v                        |
# |                             +-------------------------------+       |
# |                             |  Client raises `no available  |       |
# |                             |      endpoints` exception     |       |
# |                             +-------------------------------+       |
# |                                                                     v
# |                                                       +--------------------------+
# |                                                       |      call Endpoint       |
# |                                                       |  (endpoint has its own   |
# |                                                       |         retries)         |
# |                                                       +--------------------------+
# |                                                                     :
# |                                                                     v
# |                                                       Yes /--------------------\
# +-----------------------------------------------------------| any Exception from |
#                                                             |   failed request?  |
#                                                             \--------------------/
#                                                                       | No
#                                                                       v
#                                                             +---------------------+
#                                                             |return the response  |
#                                                             +---------------------+

    HTTP_CALLS = (
        'get',
        'options',
        'post',
        'put',
        'head',
        'patch',
        'delete',
    )

    def __init__(self, lb, ep_list_update_tries=1, **ep_kwargs):
        """
        :param lb: instance of :class:`~ahoyhoy.lb.iloadbalancer.ILoadBalancer`
        :param ep_list_update_tries: how many times to try to update endpoints list in LB
        :param ep_kwargs: arguments to pass to an Endpoint ('retry_http_call_func', 'headers')
        """
        # abc.ABCMeta will be type for lb
        if type(lb) is abc.ABCMeta:
            raise TypeError("Load Balancer needs to be instantiated first.")
        self._lb = lb
        self._ep_list_update_tries = ep_list_update_tries
        self._ep_kwargs = ep_kwargs
        logger.debug("Create client with lb %s and ep_kwargs %s", self._lb, self._ep_kwargs)

    def _resolve(self):
        """
        LB will pick and return an Endpoint.
        If no Endpoints are available, update the LB list
        and raise the exception (so it can be then retried).
        """
        try:
            ep = self._lb.pick()
        except LbNoEndpointsException:
            logger.exception("There are no endpoints available, so update the list for more tries.")
            self._lb.update()
            raise

        logger.debug("Endpoint was picked: %s", ep)

        return ep

    def resolve(self):
        """
        Resolve an Endpoint. If `LbNoEndpointsException` was raised, it's possible
        to add more "tries", update Endpoints list and try to resolve it one more time.
        (see ._resolve)
        """
        ep = retry_call(self._resolve, exceptions=LbNoEndpointsException, tries=self._ep_list_update_tries)
        return ep

    @staticmethod
    def _augment_endpoint(ep, **kwargs):
        """
        Set additional parameters to endpoint.
        :param headers dict:
        :param retry_http_call_func partial: function which accepts http call func and its arguments
        """
        logger.debug("_augment_endpoint is called")

        headers = kwargs.pop('headers', None)
        retry_http_call_func = kwargs.pop('retry_http_call_func', None)

        if retry_http_call_func:
            logger.debug("Set retries: %s", retry_http_call_func)
            ep.set_retry(retry_http_call_func)

        if headers:
            logger.debug("Set headers: %s", headers)
            ep.set_headers(headers)

        return ep

    def _call_endpoint(self, ep, http_method, *args, **kwargs):
        _ep = self._augment_endpoint(ep, **self._ep_kwargs)
        logger.debug("Call an Endpoint: %s", _ep)

        try:
            response = getattr(_ep, http_method)(*args, **kwargs)
            logger.debug("Received the response from the Endpoint.")
        except RequestException as e:
            logger.exception(e)
            raise
        except Exception as e:
            logger.exception("Got unexpected exception: %s", str(e))
            raise
        return response

    def _resolve_and_call_endpoint(self, http_method, *args, **kwargs):
        try:
            ep = self.resolve()
        except LbNoEndpointsException:
            raise ClientNoEndpointsException(
                "No available endpoints are found and maximum retries amount for updating an endpoints list exceeded.")

        result = self._call_endpoint(ep, http_method, *args, **kwargs)
        return result

    def _dispatch(self, *args, **kwargs):
        """
        Delegates calls to the Endpoint through the `retry_call` function.
        At this stage retries are used to resolve a new Endpoint, if all of the
        previous ones failed.
        This function will retry unlimited amount of times until `LbNoEndpointsException`
        is finally raised. This will raise final `ClientNoEndpointsException`.
        """
        result = retry_call(self._resolve_and_call_endpoint, fargs=args, fkwargs=kwargs, exceptions=RequestException)

        return result

    def __getattr__(self, name):
        """
        Other methods of endpoint can't be called through the client,
        just because it can be different endpoint already.

        TODO: delegate all other actions (like client.headers.update(..)) to the client.
        """

        if name in self.HTTP_CALLS:
            def wrapper(*args, **kwargs):
                logger.debug("Got an HTTP call %s with arguments: %s, %s", name, args, kwargs)
                http_method = name
                return self._dispatch(http_method, *args, **kwargs)
            return wrapper

        raise AttributeError("No such attribute: '{}'. Only HTTP methods can be called for now.".format(name))


def SimpleClient(session=None, retry_http_call=None):
    """
    Shortcut

    >>> from ahoyhoy.client.client import SimpleClient
    >>> client = SimpleClient().get('http://google.com')

    """
    from ahoyhoy.endpoints import SimpleHttpEndpoint
    return SimpleHttpEndpoint(session=session, retry=retry_http_call)
