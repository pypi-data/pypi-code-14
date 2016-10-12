# -*- coding: utf-8 -*-

from poetry.rhymer.rhymer import Rhymer
import unittest


class TestRhymer(unittest.TestCase):

    def test_is_rhymed(self):
        first_pron = "アイウエオ"
        second_pron = "アイウエオ"

        self.assertTrue(
            Rhymer.is_rhymed(
                first_pron,
                second_pron
            )
        )

    def test_evaluate(self):
        rhymer = Rhymer()

        first_pron = "アイウエオ"
        second_pron = "アイウエオ"

        self.assertEqual(
            rhymer.evaluate(
                first_pron,
                second_pron
            ),
            5
        )

        first_pron = "アイウエオ"
        second_pron = "カキクケオ"

        self.assertEqual(
            rhymer.evaluate(
                first_pron,
                second_pron
            ),
            1
        )


if __name__ == '__main__':
    unittest.main()
