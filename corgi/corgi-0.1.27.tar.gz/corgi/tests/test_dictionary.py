from unittest import TestCase

from corgi.dictionary import rename_keys


class TestDictionaryFunctions(TestCase):

    def test_rename_keys(self):
        self.assertEqual(
            rename_keys(
                {'one': 1, 'two': 2},
                {'one': '1', 'two': '2'}
            ),
            {'1': 1, '2': 2, }
        )
