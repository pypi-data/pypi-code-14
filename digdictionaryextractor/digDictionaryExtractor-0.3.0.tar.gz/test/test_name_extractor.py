import os
import sys
import codecs

import unittest

import json
import pygtrie as trie
from digDictionaryExtractor.populate_trie import populate_trie
from digDictionaryExtractor.name_dictionary_extractor import get_name_dictionary_extractor
from digExtractor.extractor_processor import ExtractorProcessor


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
        e = get_name_dictionary_extractor(t)
        ep = ExtractorProcessor().set_input_fields(
            'foo').set_output_field('names').set_extractor(e)

        updated_doc = ep.extract(doc)
        self.assertEquals(updated_doc['names'][0]['result'][0]['value'], 'barbara')

    def test_ngrams_characters_name_extractor(self):
        names = self.load_file()
        t = populate_trie(map(lambda x: x.lower(), names))
        self.assertTrue(isinstance(t.get('barbara'), basestring))
        self.assertFalse(isinstance(t.get('bar'), basestring))

        doc = {"foo": ['b', 'a', 'r', ' ', 'B', 'a', 'r', 'b', 'a', 'r', 'a']}
        e = get_name_dictionary_extractor(t)
        e.set_ngrams(7)
        e.set_joiner('')
        ep = ExtractorProcessor().set_input_fields(
            'foo').set_output_field('names').set_extractor(e)

        updated_doc = ep.extract(doc)
        self.assertEquals(updated_doc['names'][0]['result'][0]['value'], 'ara')
        self.assertEquals(updated_doc['names'][0]['result'][1]['value'], 'barb')
        self.assertEquals(updated_doc['names'][0]['result'][2]['value'], 'barbara')

    def test_ngrams_words_name_extractor(self):
        names = self.load_file()
        t = populate_trie(map(lambda x: x.lower(), names))
        self.assertTrue(isinstance(t.get('barbara'), basestring))
        self.assertFalse(isinstance(t.get('bar'), basestring))

        doc = {"foo": ["at", "the", "market", "jean", "marie", "bought", "a", "loaf", "of", "bread"]}
        e = get_name_dictionary_extractor(t)
        e.set_ngrams(2)
        e.set_joiner(' ')
        ep = ExtractorProcessor().set_input_fields(
            'foo').set_output_field('names').set_extractor(e)

        updated_doc = ep.extract(doc)
        self.assertEquals(updated_doc['names'][0]['result'][0]['value'], 'jean')
        self.assertEquals(updated_doc['names'][0]['result'][1]['value'], 'marie')
        self.assertEquals(updated_doc['names'][0]['result'][2]['value'], 'jean marie')

    def test_ngrams_words_context_name_extractor(self):
        names = self.load_file()
        t = populate_trie(map(lambda x: x.lower(), names))
        self.assertTrue(isinstance(t.get('barbara'), basestring))
        self.assertFalse(isinstance(t.get('bar'), basestring))

        doc = {"foo": ["at", "the", "market", "jean", "marie", "bought", "a", "loaf", "of", "bread"]}
        e = get_name_dictionary_extractor(t)
        e.set_ngrams(2)
        e.set_joiner(' ')
        e.set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(
            'foo').set_output_field('names').set_extractor(e)

        updated_doc = ep.extract(doc)
        self.assertEquals(updated_doc['names'][0]['result'][0]['value'], 'jean')
        self.assertEquals(updated_doc['names'][0]['result'][0]['context']['start'], 3)
        self.assertEquals(updated_doc['names'][0]['result'][0]['context']['end'], 4)
        self.assertEquals(updated_doc['names'][0]['result'][1]['value'], 'marie')
        self.assertEquals(updated_doc['names'][0]['result'][1]['context']['start'], 4)
        self.assertEquals(updated_doc['names'][0]['result'][1]['context']['end'], 5)
        self.assertEquals(updated_doc['names'][0]['result'][2]['value'], 'jean marie')
        self.assertEquals(updated_doc['names'][0]['result'][2]['context']['start'], 3)
        self.assertEquals(updated_doc['names'][0]['result'][2]['context']['end'], 5)



if __name__ == '__main__':
    unittest.main()
