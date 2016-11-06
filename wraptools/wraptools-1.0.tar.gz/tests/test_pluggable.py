import unittest

from wraptools import pluggable


def ignore_even(func):
    def wrapped(n):
        if n % 2 == 0:
            return "ERROR"
        return func(n)

    return wrapped


def echo(n):
    return n


class TestPluggable(unittest.TestCase):
    def test__wrap(self):
        target = pluggable.pluggable(ignore_even)(echo)
        self.assertEqual(target(1), 1)
        self.assertEqual(target(2), "ERROR")

        self.assertEqual(target.original_func(1), 1)
        self.assertEqual(target.original_func(2), 2)

        self.assertEqual(target.decorators, (ignore_even,))


class TestPurgePluggableDecorators(unittest.TestCase):
    def test__manually(self):
        target = pluggable.pluggable(ignore_even)(echo)

        try:
            pluggable.purge_pluggable_decorators.purge()
            self.assertEqual(target(1), 1)
            self.assertEqual(target(2), 2)
        finally:
            pluggable.purge_pluggable_decorators.wrap()

    def test__with(self):
        target = pluggable.pluggable(ignore_even)(echo)
        with pluggable.purge_pluggable_decorators():
            self.assertEqual(target(1), 1)
            self.assertEqual(target(2), 2)

    def test__decorator(self):
        target = pluggable.pluggable(ignore_even)(echo)

        @pluggable.purge_pluggable_decorators
        def test():
            self.assertEqual(target(1), 1)
            self.assertEqual(target(2), 2)

        test()
