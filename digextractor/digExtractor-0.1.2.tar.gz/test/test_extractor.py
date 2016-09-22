import unittest
import pygtrie as trie
from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor

class SampleSingleRenamedFieldExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = 'c'

    def extract(self, doc):
        return doc['c']

    def get_metadata(self):
        metadata = dict()
        metadata['extractor'] = "sample"
        return metadata

    def get_renamed_input_fields(self):
        return self.renamed_input_fields;

class SampleMultipleRenamedFieldExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['c','d']

    def extract(self, doc):
        return doc['c'] + doc['d']

    def get_metadata(self):
        metadata = dict()
        metadata['extractor'] = "sample"
        return metadata

    def get_renamed_input_fields(self):
        return self.renamed_input_fields;

class TestExtractor(unittest.TestCase):

    def test_single_renamed_field_extractor(self):
        doc = { 'a': 'hello', 'b': 'world'}
        e = SampleSingleRenamedFieldExtractor()
        ep = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)

        self.assertEqual(updated_doc['e']['value'], 'hello')
        self.assertEqual(updated_doc['a'], 'hello')
        self.assertEqual(updated_doc['b'], 'world')

    def test_multiple_renamed_field_extractor(self):
        doc = { 'a': 'hello', 'b': 'world'}
        e = SampleMultipleRenamedFieldExtractor()
        ep = ExtractorProcessor().set_input_fields(['a','b']).set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)

        self.assertEqual(updated_doc['e']['value'], 'helloworld')
        self.assertEqual(updated_doc['a'], 'hello')
        self.assertEqual(updated_doc['b'], 'world')

if __name__ == '__main__':
    unittest.main()