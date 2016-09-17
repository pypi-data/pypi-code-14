# -*- coding: utf-8 -*-
import unittest


class CoerceTest(unittest.TestCase):
    def _get_target(self):
        from ..utils import coerce as target
        return target

    def test_first_value(self):
        from ..utils import NoSet

        func = self._get_target()
        first_value = 1
        second_value = NoSet
        default_value = None

        value = func(
            value1=first_value, value2=second_value,
            default=default_value)
        self.assertEqual(value, first_value)

    def test_second_value(self):
        from ..utils import NoSet

        func = self._get_target()
        first_value = NoSet
        second_value = 1
        default_value = None

        value = func(
            value1=first_value, value2=second_value,
            default=default_value)
        self.assertEqual(value, second_value)

    def test_default_value(self):
        from ..utils import NoSet

        func = self._get_target()
        first_value = NoSet
        second_value = NoSet
        default_value = 1

        value = func(
            value1=first_value, value2=second_value,
            default=default_value)
        self.assertEqual(value, default_value)

    def test_default_value_abridgement(self):
        from ..utils import NoSet

        func = self._get_target()
        first_value = NoSet
        second_value = NoSet

        value = func(value1=first_value, value2=second_value)
        self.assertEqual(value, None)
