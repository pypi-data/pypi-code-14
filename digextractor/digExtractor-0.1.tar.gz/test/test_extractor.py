import unittest
import pygtrie as trie
from digExtractor.extractor import extract

class TestExtractor(unittest.TestCase):

    def test_extractor(self):
        doc = { 'a': 'hello', 'b': 'world'}
        curried_extract = extract(extractor = lambda x:  x['c'])
        updated_doc = curried_extract(doc, ['a', 'b'], ['c', 'd'], 'e')
        self.assertEqual(updated_doc['e'], 'hello')
        self.assertEqual(updated_doc['a'], 'hello')
        self.assertEqual(updated_doc['b'], 'world')

if __name__ == '__main__':
    unittest.main()