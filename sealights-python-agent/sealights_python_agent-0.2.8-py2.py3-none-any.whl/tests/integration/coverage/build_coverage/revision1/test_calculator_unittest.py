import unittest

from python_agent.tests.integration.coverage.build_coverage.revision1.calculator import Calculator

calc = Calculator()


class TestClass(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(1, 1), 2)

    def test_sub(self):
        self.assertEqual(calc.sub(1, 1), 0)

    def test_mul(self):
        self.assertEqual(calc.mul(2, 3), 6)
