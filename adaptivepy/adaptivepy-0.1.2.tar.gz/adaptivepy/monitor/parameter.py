from enum import Enum


class Parameter:
    @classmethod
    def possible_values(cls):
        """
        :return: Set of the possible values for this parameter
        :rtype: set[obj]
        """
        raise NotImplementedError()


class DiscreteParameter(Parameter, Enum):
    """
    Class for a discrete parameter based on an enum and declarable in the same
    way.
    """
    @classmethod
    def possible_values(cls):
        return set(cls)

    @classmethod
    def get_range(cls, start, stop):
        """
        :type start: int
        :type stop: int
        :return: Range of the current parameter
        """
        return set(filter(lambda x: start <= x.value <= stop, cls))
