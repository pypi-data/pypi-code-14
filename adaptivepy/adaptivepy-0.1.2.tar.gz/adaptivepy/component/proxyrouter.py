from adaptivepy.component.proxy import Proxy


class TargetNotACandidateException(Exception):
    pass


class ProxyRouter:
    """
    Controls a proxy to be routed to a concrete implementation among candidates
    """

    def proxy(self):
        """
        :rtype: Proxy
        """
        raise NotImplementedError()

    def route(self, target):
        """
        :param target: Target candidate to route to
        :type target: cls
        :return: The instance being routed to
        """
        raise NotImplementedError()

    def arguments_provider(self):
        """
        Provides arguments used in factory methods of candidates
        :rtype: dict[str, Any]
        """
        raise NotImplementedError()

    def choose_route(self):
        """
        Determine which candidates is to be routed to
        :rtype: cls
        """
        raise NotImplementedError()

    @classmethod
    def candidates(cls, arguments_provider=None):
        """
        Provides candidates for the proxy to be routed to along with
        factory methods to create them.
        Constructor arguments can be given as a dictionary.

        :param arguments_provider: Provider for arguments of candidates
        :rtype: dict[cls, () -> Adaptive]
        """
        raise NotImplementedError()


class BaseProxyRouter(ProxyRouter):
    """
    Abstract class implementing basic features of a proxy router
    """

    def __init__(self):
        super().__init__()
        self._candidate_cache = {}
        """:type: dict[cls, object]"""

    def route(self, target):
        candidates = self.candidates(
            arguments_provider=self.arguments_provider())

        if target not in candidates:
            raise TargetNotACandidateException(
                "The target '{}' is not a routing candidate.".format(target)
            )

        if type(self.proxy().delegate()) is target:
            instance = self.proxy().delegate()
        else:
            if target in self._candidate_cache:
                instance = self._candidate_cache[target]
            else:
                # Not in cache, instanciate new instance
                instance = self._candidate_cache[target] = candidates[target]()
            assert type(instance) is target
            self.proxy().update_delegate(instance)

        return instance


class InternalProxyRouter(Proxy, BaseProxyRouter):
    """
    Proxy which changes its delegate based on internal adaptation control
    """

    def __init__(self):
        super().__init__(None)

    def proxy(self):
        return self


class ExternalProxyRouter(BaseProxyRouter):
    """
    Controls a proxy externally to route it to a concrete implementation among
    candidates
    """
    def __init__(self):
        super().__init__()
        self._proxy = Proxy(None)

    def proxy(self):
        return self._proxy


class RuntimeExternalProxyRouter(ExternalProxyRouter):
    """
    Router for which candidates and routing strategy are defined at runtime
    """
    def __init__(self, candidates, routing_strategy):
        """
        :param candidates: dict[cls, () -> Adaptive]
        :param routing_strategy: (Iterable[cls]) -> cls
        """
        super().__init__()
        self._candidates = candidates
        self._choose_route_strategy = routing_strategy

    def arguments_provider(self):
        return {}

    def candidates(self, **kwargs):
        # TODO: Verify the non-matching signature has no side-effects
        return self._candidates

    def choose_route(self):
        return self._choose_route_strategy(self.candidates().keys())
