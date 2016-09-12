"""
Abstract interface for a Provider

Providers are designed to provide a Load Balancer a list, however it's
obtained.
"""

import abc

from six import add_metaclass

@add_metaclass(abc.ABCMeta)
class IProvider():
    """
    A provider provides endpoints for a load balancer.
    """

    @abc.abstractmethod
    def get_list(self):
        """
        Return a new list of hosts.
        """
        pass  # pragma: no cover
