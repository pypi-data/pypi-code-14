import unittest
import pygtrie as trie
import re
from digExtractor.extractor import extract
from digRegexExtractor.regex_extractor import regex_extractor
from digRegexExtractor.regex_extractor import get_regex_extractor
from digRegexExtractor.name_regex_extractor import get_name_regex_extractor

class TestNameRegexExtractor(unittest.TestCase):

    def test_extractor(self):
        doc = { 'a': 'my name is foo', 'b': 'world'}
        curried_extract = get_regex_extractor(re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE))
        updated_doc = curried_extract(doc, 'e', ['a'])
        self.assertEqual(updated_doc['e'], ['foo'])


    def test_name_extractor(self):
        doc = { 'a': 'my name is foo', 'b': 'world'}
        updated_doc = get_name_regex_extractor()(doc, 'e', ['a'])
        self.assertEqual(updated_doc['e'], ['foo'])

if __name__ == '__main__':
    unittest.main()