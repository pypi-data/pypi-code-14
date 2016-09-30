import unittest

from adaptivepy.monitor.base_implementations import create_fixed_monitor, \
    create_random_monitor


class SomeClass:
    pass


class MonitorBaseImplementationsTestCase(unittest.TestCase):
    def test_fixed_monitor(self):
        m = create_fixed_monitor(None)
        self.assertIs(m.value(), None)
        self.assertEqual(m.possible_values(), {None})

        obj = SomeClass()
        m = create_fixed_monitor(obj)
        self.assertIs(m.value(), obj)
        self.assertEqual(m.possible_values(), {obj})

    def test_random_monitor(self):
        pos_val = {1, 2, 3}
        m = create_random_monitor(pos_val)
        self.assertIn(m.value(), pos_val)
        self.assertEqual(m.possible_values(), pos_val)
        pos_val.add(4)
        self.assertNotIn(4, m.possible_values())

if __name__ == '__main__':
    unittest.main()
