"""
List provider

Provide a load balancer with a user-defined list
"""

from .iprovider import IProvider


class ListProvider(IProvider):
    """A simple list verison of the IProvider interface"""
    
    def __init__(self, *args):
        """
        Accepts a number of items to store as a list

        >>> from ahoyhoy.utils import Host
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> lp = ListProvider(Host('google1.com1', '80'), Host('google.com', '80'))
        >>> lp.get_list()
        (Host(address='google1.com1', port='80'), Host(address='google.com', port='80'))

        :param args: an iterable of items (hosts)
        """
        self._list = args

    def get_list(self):
        return self._list
