import unittest

from hgicommon.helpers import create_random_string

_PREFIX = "123"
_POSTFIX = "456"


class TestCreateRandomString(unittest.TestCase):
    """
    Tests for `create_random_string`.
    """
    def test_no_prefix_or_postfix(self):
        string = create_random_string()
        self.assertGreater(len(string), 0)
        self.assertIsInstance(string, str)

    def test_prefix(self):
        string = create_random_string(prefix=_PREFIX)
        self.assertTrue(string.startswith(_PREFIX))

    def test_postfix(self):
        string = create_random_string(postfix=_POSTFIX)
        self.assertTrue(string.endswith(_POSTFIX))

    def test_prefix_and_postfix(self):
        string = create_random_string(prefix=_PREFIX, postfix=_POSTFIX)
        self.assertTrue(string.startswith(_PREFIX))
        self.assertTrue(string.endswith(_POSTFIX))


if __name__ == '__main__':
    unittest.main()
