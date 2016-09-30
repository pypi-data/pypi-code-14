import types


class HasAdaptationSpace:
    @classmethod
    def adaptation_space(cls):
        """
        :return: Dictionary of adaptation parameters and related adaptation
        space for the component_tests
        :rtype: dict[Parameter, set]
        """
        raise NotImplementedError()


class AdaptationSpace:
    """
    Class decorator to declare a class' adaptive space with syntactic sugar
    """
    def __init__(self, space):
        self.__space = space

    def adaptation_space(self):
        return self.__space

    def __call__(self, c):
        setattr(c, HasAdaptationSpace.adaptation_space.__name__,
                types.MethodType(AdaptationSpace.adaptation_space, self))
        return c


# TODO: Add support for adaptive states
# class AdaptiveState(Enum):
#     active = 0
#     passive = 1
#     quiescent = 2
#
#
# class HasAdaptiveState:
#     def state(self):
#         """
#         :rtype: AdaptiveState
#         """
#         raise NotImplementedError()
