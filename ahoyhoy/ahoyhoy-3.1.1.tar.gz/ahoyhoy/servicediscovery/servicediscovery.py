import logging
from ..http import SessionProxy


logger = logging.getLogger(__name__)


class ServiceDiscoveryAdapter(object):
    """
    Adapter intended to be used as a mixin along with a :class:`~ahoyhoy.http.proxy.SessionProxy`
    in order to calculate a `protocol://host:port` string to be added to
    the `path` for a complete url.
    """
    def __init__(self, host, *args, **kwargs):
        self._host = host
        self._protocol = self.calculate_protocol(self.port)
        self._pre = kwargs.pop('pre_callback', None)
        self._post = kwargs.pop('post_callback', None)
        self._exc = kwargs.pop('exception_callback', None)
        # pass anything left on to superclasses
        super(ServiceDiscoveryAdapter, self).__init__(*args, **kwargs)

    @property
    def host(self):
        """Returns the endpoint's host"""
        return self._host

    @property
    def address(self):
        """Returns the endpoint's address"""
        return self.host.address

    @property
    def port(self):
        """Returns the endpoint's port"""
        return self.host.port

    @property
    def protocol(self):
        return self._protocol

    @property
    def url(self):
        """Returns the 'protocol://host:port' url"""
        url = '{}://{}'.format(self.protocol, self.address)
        if self.port:
            url += ':{}'.format(self.port)
        return url

    def __eq__(self, other):
        """Only want to check protocol, host, port, and url contains all."""
        return self.host == other.host

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "{}:{}".format(self._host, self._port)

    def calculate_protocol(self, port):
        """
        Use port for calculating the protocol.

        :param port:
        """
        if port is '443':
            return 'https'
        else:  # default to http
            return 'http'

    def pre_callback(self, urlpath):
        """
        Calculate and return the url to be passed to the Requests Session,
        using self.url (calculated from self.[host|port|protocol]).
        """
        if self._pre is None:
            request_url = self.url + urlpath
            logger.info("Using resolved url: %s", request_url)
            return request_url

        return self._pre(self, urlpath)

    def post_callback(self, result):
        # needs to be over-ridden to pass the correct "self"
        if self._post is None:
            return result

        return self._post(self, result)

    def exception_callback(self, exc):
        # again, needs to be overridden to pass the correct "self"
        if self._exc is None:
            raise exc

        return self._exc(self, exc)


class ServiceDiscoveryHttpClient(ServiceDiscoveryAdapter, SessionProxy):
    """
    An object that transparently allows Service Discovery while preserving
    the same API as a Requests Session object, so typical Requests methods
    take server-relative paths rather than full URLs.

    For instance, here's how you can make a Http GET request using Requests's
    standard `get` method.

        >>> from ahoyhoy.servicediscovery import ServiceDiscoveryHttpClient
        >>> from ahoyhoy.utils import Host
        >>> host = Host('google.com', '80')
        >>> sdhc = ServiceDiscoveryHttpClient(host)
        >>> sdhc.get('/')
        <Response [200]>

    Note the fact that we're passing `get` a path, _not_ a URL.

    Why?

    When using a form of Service Discovery, host/port (and sometimes protocol)
    portions of the URL are resolved at runtime.  This class adapts the a Requests
    Session in order to support this runtime service resolution.
    """
    def __init__(self, *args, **kwargs):
        super(ServiceDiscoveryHttpClient, self).__init__(*args, **kwargs)
