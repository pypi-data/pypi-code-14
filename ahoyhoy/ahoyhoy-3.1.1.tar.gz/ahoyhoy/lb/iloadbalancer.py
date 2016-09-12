"""
Abstract Load Balancer

"""

import abc

from six import add_metaclass


from .providers.iprovider import IProvider
from ..endpoints import Endpoint
from .exceptions import NoAvailableEndpointsLbException


@add_metaclass(abc.ABCMeta)
class ILoadBalancer(object):
    """
    Base class for load balancers.
    """

    def __init__(self, provider, session=None):
        """
        :param provider: any instance of :class:`~ahoyhoy.lb.providers.iprovider.IProvider`
        :param session: custom session
        """
        self._check_provider(provider)
        self._provider = provider
        self._session = session
        self._endpoints = {}  # all endpoints
        self._up = []  # create an empty `up` list
        self._down = []  # create an empty `down` list
        self.update()  # update the `up` list with the new hosts

    def _check_provider(self, provider):
        assert isinstance(provider, IProvider)

    @abc.abstractmethod
    def _choose_next(self):
        """
        Choose the next item from the list by given algorithm
        """
        pass  # pragma: no cover

    def pick(self):
        """
        Will only return nodes which have :class:`~ahoyhoy.circuit.OpenState`.
        """
        if not self._up:
            raise NoAvailableEndpointsLbException('No endpoints in closed state. Nothing to choose.')
        while self._up:
            ep = self._choose_next()
            if ep.available:
                return ep
            else:
                self._up.remove(ep.host)
                self._down.insert(0, ep.host)

        raise NoAvailableEndpointsLbException('No endpoints in closed state. Nothing to choose.')

    def update(self):
        """
        Update the hosts list with new hosts (if there are some).
        """
        new_hosts = list(self._provider.get_list())

        new_up_hosts = [h for h in new_hosts if h not in self._down]

        self._up = self._remove_duplicates_with_preserving_order(self._up + new_up_hosts)

    @staticmethod
    def _remove_duplicates_with_preserving_order(seq):
        # http://stackoverflow.com/a/480227/4492395
        seen = set()

        # Hoisting the lookup out of the loop, so it doesn't
        # have to lookup for the 'add' attribute each time.
        # Instead I have my seen.add method ready right away!!
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def get_or_create_endpoint(self, host):
        """
        Concrete method to create an Endpoint from a `Host` object

        :param host: `Host('host', 'port')` namedtuple
        """
        if host in self._endpoints:
            return self._endpoints[host]

        ep = Endpoint(host, session=self._session)
        self._endpoints[host] = ep
        return ep
