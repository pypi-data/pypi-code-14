#! /usr/bin/env python

import unittest
from decimal import Decimal
from dimana.units import Units
from dimana.value import Value
from dimana.tests.util import ParseTestClass


class UnitsUniquenessTests (unittest.TestCase):
    def test_value_type_construction(self):
        u1 = Units({})
        u2 = Units({})
        self.assertIs(u1, u2)

        u1 = Units({'meter': 1})
        u2 = Units({'meter': 1})
        self.assertIs(u1, u2)

        u1 = Units({'meter': 1, 'sec': -2})
        u2 = Units({'meter': 1, 'sec': -2})
        self.assertIs(u1, u2)

    def test_scalar(self):
        self.assertIs(Units.scalar, Units({}))


class UnitsValueConstructorTests (unittest.TestCase):
    def test_from_string(self):
        inputs = [
            '0',
            '1',
            '1.00',
            '+17e3',
            '-42.07000',
        ]

        unitses = [
            Units.scalar,
            Units.parse('GROM'),
        ]

        for units in unitses:
            for i in inputs:
                self.assertEqual(
                    units.from_string(i),
                    Value(Decimal(i), units),
                )


class UnitsArithmeticOperationsTests (unittest.TestCase):
    def setUp(self):
        self.m = Units({'meter': 1})
        self.s = Units({'sec': 1})

        # All equivalences are tested for each case here:
        self.eqcases = [Units.scalar, self.m, self.m * self.s, self.m / self.s]

    def test__add__(self):
        self.assertIs(self.m, self.m + self.m)

    def test__add__Mismatch(self):
        self.assertRaises(Units.Mismatch, lambda: self.m + self.s)

    def test__add__TypeError(self):
        self.assertRaises(TypeError, lambda: self.m + 'banana')

    def test__inv__(self):
        self.assertIs(self.m, -self.m)

    def test__mul__(self):
        self.assertIs(
            Units({'meter': 1, 'sec': 1}),
            self.m * self.s,
        )

    def test__mul__TypeError(self):
        self.assertRaises(TypeError, self.m.__mul__, 42)

    def test__div__(self):
        self.assertIs(
            Units({'meter': 1, 'sec': -1}),
            self.m / self.s,
        )

    def test__div__TypeError(self):
        self.assertRaises(TypeError, self.m.__div__, 42)

    def test__pow__(self):
        self.assertIs(
            Units({'meter': 3}),
            self.m ** 3,
        )

    def test__sub__is__add__(self):
        self.assertEqual(Units.__sub__, Units.__add__)

    def test__truediv__is__div__(self):
        self.assertEqual(Units.__truediv__, Units.__div__)

    # Equivalences:
    def test_scalar_cancellation_equivalence(self):
        for u in self.eqcases:
            self.assertIs(Units.scalar, u / u)

    def test_scalar_0_power(self):
        for u in self.eqcases:
            self.assertIs(Units.scalar, u ** 0)

    def test_mul_pow_equivalence(self):
        for u in self.eqcases:
            self.assertIs(u * u, u ** 2)

    def test_div_inverse_mul_equivalence(self):
        for u in self.eqcases:
            for k in self.eqcases:
                self.assertIs(u / k, u * (k ** -1))


@ParseTestClass
class UnitsParseAndStrTests (unittest.TestCase):

    targetclass = Units

    def assertParsedValueMatches(self, a, b):
        self.assertIs(a, b)

    m = Units({'meter': 1})
    s = Units({'sec': 1})
    kg = Units({'kg': 1})

    cases = [
        (Units.scalar,
         '1',
         ['foo^0',
          'x/x']),

        (s**(-2),
         '1 / sec^2',
         ['1/sec^2',
          'sec^-2',
          '1/(sec*sec)',
          '1/ ( sec  * sec )']),

        (m,
         'meter',
         []),

        (s,
         'sec',
         []),

        (m*s,
         'meter * sec',
         ['meter*sec',
          '1/(meter^-1*sec^-1)']),

        (m/s,
         'meter / sec',
         ['sec*meter / sec^2']),

        (m**2 * s,
         'meter^2 * sec',
         ['meter*sec*meter']),

        (m / s**2,
         'meter / sec^2',
         []),

        (m**2 / s**2,
         'meter^2 / sec^2',
         []),

        (kg**2 * m / s**2,
         'kg^2 * meter / sec^2',
         []),

        (s**2 / (kg*m),
         'sec^2 / (kg * meter)',
         []),

        (s**1.5,
         'sec^1.5',
         []),
    ]

    errorcases = [
        # These should trigger the top-level regex mismatch:
        '',
        '%',  # Doesn't match character classes.
        '1foo',  # Doesn't match initial character class.
        ' meter',  # No initial whitespace.
        'meter ',  # No trailing whitespace.

        # This should trigger error on unpacking of term parts:
        'a^b^c',

        # This should trigger error on int parsing of power:
        'a^b',

        # This should trigger error on unit name parsing of term:
        'a ^2',
    ]
