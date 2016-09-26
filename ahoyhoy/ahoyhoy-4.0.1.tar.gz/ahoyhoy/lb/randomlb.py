"""
Random Load Balancer

"""
from random import randint

from .iloadbalancer import ILoadBalancer


class RandomLB(ILoadBalancer):
    """
    Implements random algorithm for chosing a host from the list.
    """

    def __init__(self, provider, session=None, random_function=randint):
        """
        >>> from ahoyhoy.utils import Host
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.lb import RandomLB
        >>> rrlb = RandomLB(ListProvider(Host('google1.com1', '80'), Host('google.com', '80')))
        >>> rrlb.pick()
        <Endpoint/.../Host(address='google...', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>

        Custom random function:

        >>> def my_random(*args):
        ...    return 0
        >>> rrlb = RandomLB(
        ...     ListProvider(Host('google1.com1', '80'), Host('google.com', '80')),
        ...     random_function=my_random)
        >>> rrlb.pick()
        <Endpoint/.../Host(address='google1.com1', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>

        :param provider: :class:`~ahoyhoy.lb.providers.ListProvider` instance
        :param random_function: function which returns random number for the given range. By default: :attr:`random.randint`
        """
        super(RandomLB, self).__init__(provider, session=session)
        self.random_function = random_function

    def _choose_next(self):
        """
        :return Endpoint or None
        """
        listsize = len(self._up)

        if listsize <= 0:
            return None
        else:
            index = self.random_function(0, listsize-1)
            return self.get_or_create_endpoint(self._up[index])
