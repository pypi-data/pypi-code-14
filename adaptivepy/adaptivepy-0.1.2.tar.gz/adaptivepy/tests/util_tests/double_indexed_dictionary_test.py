import unittest

from adaptivepy.util.double_indexed_dictionary import DoubleIndexedDictionary


class DoubleIndexedDictionaryTestCase(unittest.TestCase):

    def setUp(self):
        self.some_dict = DoubleIndexedDictionary()
        self.key_list = "this is a key list".split(' ')

        self.other_dict = DoubleIndexedDictionary()
        for k, v in zip(self.key_list, range(len(self.key_list))):
            self.other_dict.add(k, v)

    def test_get(self):
        self.assertEqual(self.some_dict.get,
                         self.some_dict.get_value)
        self.assertNotEqual(self.some_dict.get,
                            self.some_dict.get_key)
        self.some_dict.add("key", 1)
        self.assertIs(self.some_dict["key"], 1)

    def test_add(self):
        def validate_getters(k, v):
            ret1 = self.some_dict.get_value(k)
            self.assertIs(ret1, v)
            ret2 = self.some_dict.get_key(v)
            self.assertIs(ret2, k)

        a, b = 1, 2
        self.some_dict.add(a, b)
        validate_getters(a, b)

        c, d = 3, 4
        self.some_dict[c] = d
        validate_getters(c, d)

        self.assertEqual(len(self.key_list), len(self.other_dict))
        self.assertIn("key", self.other_dict)
        self.assertIs(self.other_dict.get_value("key"), 3)
        self.assertIs(self.other_dict.get_key(4), self.key_list[4])

    def test_pop(self):
        with self.assertRaises(KeyError):
            self.some_dict.pop(None)
        with self.assertRaises(KeyError):
            self.other_dict.pop("")

        self.assertEqual(len(self.key_list), len(self.other_dict))
        val = self.other_dict.pop("is")
        self.assertEqual(val, 1)
        self.assertEqual(len(self.key_list) - 1, len(self.other_dict))

if __name__ == '__main__':
    unittest.main()
