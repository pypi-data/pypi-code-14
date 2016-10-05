import os
import sys
import codecs

import unittest

import json
from digReadabilityExtractor.readability_extractor import ReadabilityExtractor
from digExtractor.extractor_processor import ExtractorProcessor

class TestReadabilityExtractor(unittest.TestCase):

    def load_file(self, name):
        file = os.path.join(os.path.dirname(__file__), name)
        text = codecs.open(file, 'r', 'utf-8').read().replace('\n','')
        return text

    def test_readability_extractor(self):
        dig_html = self.load_file("dig.html")
        dig_text = self.load_file("dig.txt")
        doc = {"foo": dig_html}
    	e = ReadabilityExtractor()
        ep = ExtractorProcessor().set_input_fields('foo').set_output_field('extracted').set_extractor(e)
    	updated_doc = ep.extract(doc)
    	self.assertEquals(updated_doc['extracted'][0]['value'], dig_text)


if __name__ == '__main__':
    unittest.main()
