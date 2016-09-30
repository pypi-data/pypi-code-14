from adaptivepy.component.definitions import HasAdaptationSpace
from adaptivepy.monitor.parameter_event import ParameterValueSubscriber

from adaptivepy.monitor.monitor_event_manager import GLOBAL_MONITORS_EVENT_MANAGER


class Adaptive(HasAdaptationSpace, ParameterValueSubscriber):
    """
    Abstract class for an adaptive component with defined adaptation space
    """

    def __init__(self, parameter_value_provider=None):
        """
        :param parameter_value_provider: Provides values for parameters for the
                                         adaptation process
        """
        self._parameter_value_provider = \
            parameter_value_provider or GLOBAL_MONITORS_EVENT_MANAGER

    def parameter_value_provider(self):
        """
        :return: Monitoring group manager which provides necessary monitors
        :rtype: MonitorsProvider
        """
        return self._parameter_value_provider

    def _subscribe_to_all_parameters(self):
        for p in self.adaptation_space().keys():
            self.parameter_value_provider().subscribe(self, p)

    def _unsubscribe_from_all_parameters(self):
        for p in self.adaptation_space().keys():
            self.parameter_value_provider().unsubscribe(self, p)

    def _local_snapshot(self):
        """
        :rtype: dict[Parameter, Any]
        """
        return self.parameter_value_provider().snapshot(self.adaptation_space())
