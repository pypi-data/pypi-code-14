
import unittest

from yaoguang.entity import Entity


class Test(unittest.TestCase):

    def testEntity(self):
        a = Entity({"int": 2})
        b = Entity({"int": 1, "string": "hello", "a": a})
        self.assertEqual(1, b["int"])
        self.assertEqual("hello", b["string"])
        self.assertEqual({"int": 3}, b["a"])
        self.assertEqual(3, b["a"]["int"])


if __name__ == '__main__':
    unittest.main()
