import unittest
import pygtrie as trie
from digDictionaryExtractor.populate_trie import populate_trie

class TestPopulateTrie(unittest.TestCase):

    def test_populate_trie(self):
        values = ['abacus', 'abate', 'adder', 'brave']
        t = populate_trie(iter(values))
        self.assertTrue(isinstance(t.get('abate'), basestring))
        self.assertFalse(isinstance(t.get('debate'), basestring))

if __name__ == '__main__':
    unittest.main()