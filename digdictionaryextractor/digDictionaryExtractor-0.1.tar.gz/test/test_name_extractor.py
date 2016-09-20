import os
import sys
import codecs

import unittest

import json
import pygtrie as trie
from digDictionaryExtractor.populate_trie import populate_trie
from digDictionaryExtractor.name_extractor import get_name_dictionary_extractor

class TestNameExtractor(unittest.TestCase):

    def load_file(self):
    	names_file = os.path.join(os.path.dirname(__file__), "names.json")
    	names = json.load(codecs.open(names_file, 'r', 'utf-8'))
    	return names

    def test_name_extractor(self):
    	names = self.load_file()
        t = populate_trie(map(lambda x: x.lower(), names))
        self.assertTrue(isinstance(t.get('barbara'), basestring))
        self.assertFalse(isinstance(t.get('bar'), basestring))
        
        doc = {"foo": ['bar', 'Barbara']}
    	name_dictionary_extract = get_name_dictionary_extractor(t)
    	updated_doc = name_dictionary_extract(doc, 'names', ['foo'])
    	self.assertEquals(updated_doc['names'], frozenset(['barbara']))


if __name__ == '__main__':
    unittest.main()