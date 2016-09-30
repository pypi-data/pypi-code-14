import unittest

from adaptivepy.monitor.parameter import DiscreteParameter


class EmptyParameter(DiscreteParameter):
        pass


class SingleItemParameter(DiscreteParameter):
    state0 = 0


class MultiItemParameter(DiscreteParameter):
    state0 = 0
    state1 = 1
    state2 = 2

MultiItemParameterAllStates = frozenset({
    MultiItemParameter.state0,
    MultiItemParameter.state1,
    MultiItemParameter.state2
})


class DiscreteParameterTestCase(unittest.TestCase):

    def test_possible_values(self):
        self.assertFalse(EmptyParameter.possible_values())
        self.assertEqual(SingleItemParameter.possible_values(),
                         {SingleItemParameter.state0})
        self.assertEqual(MultiItemParameter.possible_values(),
                         MultiItemParameterAllStates)

    def test_get_range(self):
        self.assertFalse(EmptyParameter.get_range(0, 0))
        self.assertFalse(EmptyParameter.get_range(0, 1))
        self.assertFalse(EmptyParameter.get_range(1, 0))

        self.assertFalse(SingleItemParameter.get_range(1, 1))
        self.assertFalse(SingleItemParameter.get_range(1, 0))
        self.assertEqual(SingleItemParameter.get_range(0, 1),
                         {SingleItemParameter.state0})
        self.assertEqual(SingleItemParameter.get_range(0, 2),
                         {SingleItemParameter.state0})

        self.assertFalse(MultiItemParameter.get_range(3, 0))
        self.assertFalse(MultiItemParameter.get_range(2, 0))
        self.assertEqual(MultiItemParameter.get_range(0, 2),
                         MultiItemParameterAllStates)
        self.assertEqual(MultiItemParameter.get_range(0, 0),
                         {MultiItemParameter.state0})
        self.assertEqual(MultiItemParameter.get_range(1, 4),
                         {MultiItemParameter.state1,
                          MultiItemParameter.state2})
        self.assertEqual(MultiItemParameter.get_range(0, 1),
                         {MultiItemParameter.state0,
                          MultiItemParameter.state1})

if __name__ == '__main__':
    unittest.main()
