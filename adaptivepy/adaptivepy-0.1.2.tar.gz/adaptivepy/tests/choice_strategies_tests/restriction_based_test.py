import unittest

from adaptivepy.component.definitions import AdaptationSpace
from adaptivepy.monitor.parameter import DiscreteParameter

from adaptivepy.choice_strategies.restriction_based import choose_most_restricted


class SomeParameter(DiscreteParameter):
    state0 = 0
    state1 = 1
    state2 = 2


class OtherParameter(DiscreteParameter):
    state0 = 0
    state1 = 1
    state2 = 2


@AdaptationSpace({SomeParameter: {SomeParameter.state0}})
class SomeParamOneRestrict:
    pass


@AdaptationSpace({SomeParameter: {SomeParameter.state0},
                  OtherParameter: {OtherParameter.state0}})
class TwoParamOneRestrict:
    pass


@AdaptationSpace({SomeParameter: SomeParameter.get_range(0, 1)})
class SomeParamTwoRestrict:
    pass


@AdaptationSpace({OtherParameter: OtherParameter.get_range(0, 1)})
class OtherParamTwoRestrict:
    pass


class NonAdaptive:
    pass


class RestrictionBasedTestCase(unittest.TestCase):
    def test_no_parameter(self):
        self.assertIsNone(choose_most_restricted([], []))
        self.assertIsNone(choose_most_restricted([SomeParamOneRestrict], []))
        self.assertIs(NonAdaptive,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamOneRestrict],
                                             []))

    def test_one_parameter(self):
        self.assertIs(NonAdaptive,
                      choose_most_restricted([NonAdaptive],
                                             [SomeParameter]))
        self.assertIs(SomeParamOneRestrict,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamOneRestrict],
                                             [SomeParameter]))
        self.assertIs(SomeParamOneRestrict,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamOneRestrict,
                                              SomeParamTwoRestrict],
                                             [SomeParameter]))

        self.assertIs(SomeParamTwoRestrict,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamTwoRestrict,
                                              OtherParamTwoRestrict],
                                             [SomeParameter]))

    def test_two_parameters(self):
        self.assertIs(NonAdaptive,
                      choose_most_restricted([NonAdaptive],
                                             [SomeParameter, OtherParameter]))
        self.assertIs(SomeParamOneRestrict,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamOneRestrict],
                                             [SomeParameter, OtherParameter]))
        self.assertIs(TwoParamOneRestrict,
                      choose_most_restricted([NonAdaptive,
                                              SomeParamOneRestrict,
                                              TwoParamOneRestrict],
                                             [SomeParameter, OtherParameter]))

        # Should be equal, expect any of them
        equal_restrict = [SomeParamTwoRestrict, OtherParamTwoRestrict]
        self.assertIn(choose_most_restricted(equal_restrict,
                                             [SomeParameter, OtherParameter]),
                      equal_restrict)


if __name__ == '__main__':
    unittest.main()
