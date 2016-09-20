import os
import sys
import codecs

import unittest

import json
import pygtrie as trie
from digReadabilityExtractor.readability_extractor import get_readability_extractor

class TestReadabilityExtractor(unittest.TestCase):

    def load_file(self, name):
        file = os.path.join(os.path.dirname(__file__), name)
        text = codecs.open(file, 'r', 'utf-8').read().replace('\n','')
        return text

    def test_readability_extractor(self):
        dig_html = self.load_file("dig.html")
        dig_text = self.load_file("dig.txt")
        doc = {"foo": dig_html}
    	readability_extract = get_readability_extractor()
    	updated_doc = readability_extract(doc, 'extracted', ['foo'])
    	self.assertEquals(updated_doc['extracted'], dig_text)


if __name__ == '__main__':
    unittest.main()