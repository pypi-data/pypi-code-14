import unittest

from adaptivepy.component.adaptation_space import filter_by_adaptation_space, \
    extend_adaptation_space, union_adaptation_space, aggregate_adaptation_space
from adaptivepy.component.definitions import AdaptationSpace

from adaptivepy.monitor.parameter import DiscreteParameter


class SomeParameter(DiscreteParameter):
    state0 = 0
    state1 = 1
    state2 = 2


class OtherParameter(DiscreteParameter):
    state0 = 0
    state1 = 1
    state2 = 2


@AdaptationSpace({SomeParameter: {SomeParameter.state0, SomeParameter.state2}})
class Component1:
    pass


@AdaptationSpace({SomeParameter: {SomeParameter.state1}})
class Component2:
    pass


@AdaptationSpace({OtherParameter: {OtherParameter.state0}})
class Component3:
    pass


@AdaptationSpace({SomeParameter: {SomeParameter.state1},
                  OtherParameter: {OtherParameter.state1}})
class Component4:
    pass


class NonAdaptiveComponent:
    pass


c1, c2, c3, c4 = Component1, Component2, Component3, Component4
cNA = NonAdaptiveComponent

components = [c1, c2, c3, c4, cNA]


class AdaptationSpaceTestCase(unittest.TestCase):

    def test_extend_adaptation_space(self):
        space = {}
        ret_space = extend_adaptation_space(space, SomeParameter, set())
        self.assertIs(ret_space, space)
        self.assertIn(SomeParameter, space)
        self.assertEqual(len(space), 1)
        self.assertFalse(space[SomeParameter])  # Empty

        extend_adaptation_space(space, SomeParameter, {
            SomeParameter.state0
        })
        self.assertIn(SomeParameter.state0, space[SomeParameter])
        self.assertEqual(len(space[SomeParameter]), 1)

        extend_adaptation_space(space, SomeParameter, {
            SomeParameter.state0,
            SomeParameter.state2
        })

        self.assertIn(SomeParameter.state2, space[SomeParameter])
        self.assertEqual(len(space[SomeParameter]), 2)

        extend_adaptation_space(space,
                                OtherParameter,
                                OtherParameter.possible_values())
        self.assertIn(OtherParameter, space)
        self.assertEqual(space[OtherParameter],
                         OtherParameter.possible_values())

    def test_union_adaptation_space(self):
        space1, space2 = {}, {}
        ret_space = union_adaptation_space(space1, space2)
        for s in (space1, space2, ret_space):
            self.assertFalse(s)

        space1 = {SomeParameter: {SomeParameter.state1}}
        space2 = {SomeParameter: {SomeParameter.state2}}
        ret_space = union_adaptation_space(space1, space2)
        self.assertEqual(ret_space, {
            SomeParameter: {SomeParameter.state1, SomeParameter.state2}
        })

        space2 = {OtherParameter: {OtherParameter.state0,
                                   OtherParameter.state2}}
        ret_space = union_adaptation_space(space1, space2)
        self.assertEqual(ret_space, {
            SomeParameter: {SomeParameter.state1, SomeParameter.state2},
            OtherParameter: {OtherParameter.state0, OtherParameter.state2}
        })

        ret_space = union_adaptation_space(
            {SomeParameter: SomeParameter.possible_values()},
            {OtherParameter: OtherParameter.possible_values()})
        self.assertEqual(ret_space, {
            SomeParameter: SomeParameter.possible_values(),
            OtherParameter: OtherParameter.possible_values()
        })

    def test_aggregate_adaptation_space(self):
        self.assertFalse(aggregate_adaptation_space([]))
        self.assertFalse(aggregate_adaptation_space([cNA]))
        self.assertEqual(aggregate_adaptation_space([c1, c2]), {
            SomeParameter: SomeParameter.possible_values()
        })
        self.assertEqual(aggregate_adaptation_space(components), {
            SomeParameter: SomeParameter.possible_values(),
            OtherParameter: OtherParameter.get_range(0, 1)
        })

    def test_filter_by_adaptation_space(self):
        self.assertEqual(filter_by_adaptation_space(components, {}), {cNA})
        self.assertFalse(filter_by_adaptation_space(components, {},
                                                    exclude_agnostic=True))

        state = {
            SomeParameter: SomeParameter.state0
        }

        filtered_components = filter_by_adaptation_space(components, state)
        self.assertEqual(filtered_components, {c1, cNA})
        filtered_components = filter_by_adaptation_space(components, state,
                                                         exclude_agnostic=True)
        self.assertEqual(filtered_components, {c1})

        state = {
            SomeParameter: SomeParameter.state1,
            OtherParameter: OtherParameter.state1
        }

        filtered_components = filter_by_adaptation_space(components, state)
        self.assertEqual(filtered_components, {c2, c4, cNA})

        filtered_components = filter_by_adaptation_space(components, state,
                                                         exclude_agnostic=True)
        self.assertEqual(filtered_components, {c2, c4})

        state = {
            OtherParameter: OtherParameter.state2
        }

        self.assertEqual(filter_by_adaptation_space(components, state), {cNA})
        self.assertFalse(filter_by_adaptation_space(components, {},
                                                    exclude_agnostic=True))

if __name__ == '__main__':
    unittest.main()
