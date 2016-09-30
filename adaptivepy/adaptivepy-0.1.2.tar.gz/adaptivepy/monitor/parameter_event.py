class MonitorAlreadyRegisteredException(ValueError):
    pass


class ImproperMonitorForParameterException(ValueError):
    pass


class ParameterValueSubscriber:
    """
    Allows to be updated by a parameter value provider of new monitored values
    """

    def updated_monitored_value(self, parameter, old_value, new_value):
        """
        :type parameter: Parameter to which the value belongs
        :param old_value: Latest value before update
        :param new_value: Updated value
        """
        raise NotImplementedError()


class ParameterValueProvider:
    """
    Provides a value for a parameter to MonitorEventSubscriber instances
    """

    def subscribe(self, subscriber, parameter):
        """
        Allows to subscribe for updates of a parameter
        :type subscriber: ParameterValueSubscriber
        :type parameter: Parameter
        """
        raise NotImplementedError()

    def unsubscribe(self, subscriber, parameter):
        """
        Allows to unsubscribe from updates of a parameter
        :type subscriber: ParameterValueSubscriber
        :type parameter: Parameter
        """
        raise NotImplementedError()

    def snapshot(self, parameters=None):
        """
        Provides a snapshot of the current system which can optionally be
        filtered with a set of parameters
        :param parameters: Parameters to acquire a snapshot value for, if None
                           the entire snapshot is provided
        :type parameters: Iterable[Parameter]
        """
        raise NotImplementedError()