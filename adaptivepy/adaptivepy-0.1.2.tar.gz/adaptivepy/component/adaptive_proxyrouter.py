from adaptivepy.component.adaptive import Adaptive
from adaptivepy.component.proxyrouter import ExternalProxyRouter, ProxyRouter, \
    InternalProxyRouter

from adaptivepy.component.adaptation_space import aggregate_adaptation_space

PARAMETER_VALUE_PROVIDER = "parameter_value_provider"


class AdaptiveProxyRouter(Adaptive, ProxyRouter):
    """
    Abstract class for a proxy router with external control based on an
    adaptation space
    """

    @classmethod
    def adaptation_space(cls):
        return aggregate_adaptation_space(cls.candidates())

    def __init__(self, parameter_value_provider=None):
        super().__init__(parameter_value_provider=parameter_value_provider)

    def arguments_provider(self):
        return {
            PARAMETER_VALUE_PROVIDER: self.parameter_value_provider()
        }

    def updated_monitored_value(self, parameter, old_value, new_value):
        """
        Updates regardless of the parameter value (force recomputation)
        It is encouraged that this method is reimplemented to filter out any
        state changes which have no impact on routing
        """
        self.route(self.choose_route())


class AdaptiveExternalProxyRouter(ExternalProxyRouter, AdaptiveProxyRouter):
    pass


class AdaptiveInternalProxyRouter(InternalProxyRouter, AdaptiveProxyRouter):
    pass

