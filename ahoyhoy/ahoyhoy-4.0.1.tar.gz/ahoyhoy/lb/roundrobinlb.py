"""
Random Load Balancer

"""
from .iloadbalancer import ILoadBalancer


class RoundRobinLB(ILoadBalancer):
    """
    Implement round robin load balancing algorythm.
    """

    def __init__(self, provider, session=None):
        """
        >>> from ahoyhoy.utils import Host
        >>> from ahoyhoy.lb.providers import ListProvider
        >>> from ahoyhoy.lb import RoundRobinLB
        >>> rrlb = RoundRobinLB(ListProvider(Host('google1.com1', '80'), Host('google.com', '80')))
        >>> rrlb.pick()
        <Endpoint/.../Host(address='google1.com1', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>
        >>> rrlb.pick()
        <Endpoint/.../Host(address='google.com', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>
        >>> rrlb.pick()
        <Endpoint/.../Host(address='google1.com1', port='80')/<class 'ahoyhoy.circuit.circuit.ClosedState'>

        :param provider: :class:`~ahoyhoy.providers.iprovider.IProvider` instance
        """

        # TODO: This is python, and we can ducktype
        # Do I force people to adhere to an interface?
        # Unpythonic, but potentially clearer (in terms of code)
        #   to outside users
        super(RoundRobinLB, self).__init__(provider, session=session)
        self._counter = 0

    def _choose_next(self):
        """
        :return Endpoint or None
        """
        if not self._up:
            return None

        if self._counter >= len(self._up):
            self._counter = 0

        node = self._up[self._counter]
        self._counter += 1
        return self.get_or_create_endpoint(node)
