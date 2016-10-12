import unittest
from unittest.mock import Mock, patch
from collections import namedtuple, defaultdict
from datetime import date

from collectionz import GroupBy, CounterBy


Order = namedtuple('Order', 'date, email, product')
orders = [
    Order(date(2013, 3, 4), 'carl@mail.com', 'Computer'),
    Order(date(2014, 2, 20), 'mary@mail.com', 'Lamp'),
    Order(date(2016, 7, 1), 'eggs@mail.com', 'Desk'),
    Order(date(2016, 2, 12), 'mary@mail.com', 'TV'),
]


class TestGroupBy(unittest.TestCase):

    @patch('collectionz.GroupBy._build_add_to_group')
    def test_groupby_init(self, build_add_to_group_mock):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        build_add_to_group_mock.return_value = add_to_group
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(grouped._group[False]._group[0], orders[0])

    def test_build_add_to_group(self):
        group_by_mock = Mock()
        add_to_group = GroupBy._build_add_to_group(
            group_by_mock, lambda o: o.date.year > 2013)
        groups = add_to_group(defaultdict(list), orders[0])
        self.assertIn(orders[0], groups[False])

    def test_build_add_to_group_not_hashable(self):
        def a_grouper(o):
            return {}
        with self.assertRaises(Exception) as manager:
            group_by_mock = Mock()
            add_to_group = GroupBy._build_add_to_group(
                group_by_mock, a_grouper)
            add_to_group(defaultdict(list), orders[0])
        msg = 'Value returned by function "a_grouper" is not hashable'
        self.assertEqual(str(manager.exception), msg)

    @patch('collectionz.GroupBy._build_add_to_group')
    def test_get_item(self, build_add_to_group_mock):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        build_add_to_group_mock.return_value = add_to_group
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(grouped[False][0], orders[0])

    @patch('collectionz.GroupBy._build_add_to_group')
    def test_iter(self, build_add_to_group_mock):
        def add_to_group(group, obj):
            return {
                True: orders[1:],
                False: [orders[0]],
            }
        build_add_to_group_mock.return_value = add_to_group
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(sorted(list(grouped)), [False, True])

    def test_add_object(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        order = Order(date(2012, 9, 1), 'kate@mail.com', 'Toy')
        grouped.add(order)
        self.assertEqual(grouped[False][1], order)

    def test_len(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        self.assertEqual(len(grouped), len(orders))

    def test_eq(self):
        groupers = [lambda o: o.date.year > 2013]
        grouped1 = GroupBy(orders, groupers)
        grouped2 = GroupBy(orders[1:] + [orders[0]], groupers)
        self.assertEqual(grouped1, grouped2)

    def test_process(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        grouped.process(len)
        self.assertEqual(grouped[True], 3)

    def test_process_with(self):
        grouped = GroupBy(orders, [
            lambda o: o.date.year > 2013,
            lambda o: o.email,
        ])

        def with_fun(items, group, subgroup):
            return group, subgroup, tuple(items)
        res = {(i, j, tuple(k)) for i, j, k in grouped.process_with(with_fun)}
        expected = {
            (True, 'eggs@mail.com', (orders[2],)),
            (True, 'mary@mail.com', (orders[1], orders[3])),
            (False, 'carl@mail.com', (orders[0],)),
        }
        self.assertEqual(res, expected)

    def test_repr(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        grouped_repr = '{{False: {0}, True: {1}}}'.format(
            [orders[0]], orders[1:])
        self.assertEqual(repr(grouped), grouped_repr)

    def test_str(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        grouped_str = '{{False: {0}, True: {1}}}'.format(
            [orders[0]], orders[1:])
        self.assertEqual(str(grouped), grouped_str)

    def test_add_grouper(self):
        grouped = GroupBy(orders, [lambda o: o.date.year > 2013])
        grouper = lambda order: order.date.year
        grouped.add_grouper(grouper)
        self.assertEqual(grouped[True][2016][0], orders[2])


class TestCounterBy(unittest.TestCase):
    def test_init(self):
        """
        Create a 'CounterBy' object with 'orders' and assert it has two
        orders with email 'mary@mail.com'.
        """
        counter_by = CounterBy(orders, lambda o: o.email)
        self.assertEqual(counter_by['mary@mail.com'], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
