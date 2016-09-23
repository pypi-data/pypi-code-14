import unittest
import pygtrie as trie
from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digExtractor.extractor_processor_chain import execute_processor_chain

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

    def test_single_renamed_field_missing_extractor(self):
        doc = { 'b': 'world'}
        e = SampleSingleRenamedFieldExtractor()
        ep = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)

        self.assertTrue('e' not in updated_doc)
        self.assertEqual(updated_doc['b'], 'world')

    def test_multiple_renamed_field_extractor(self):
        doc = { 'a': 'hello', 'b': 'world'}
        e = SampleMultipleRenamedFieldExtractor()
        ep = ExtractorProcessor().set_input_fields(['a','b']).set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)

        self.assertEqual(updated_doc['e']['value'], 'helloworld')
        self.assertEqual(updated_doc['a'], 'hello')
        self.assertEqual(updated_doc['b'], 'world')

    def test_multiple_renamed_field_with_multiple_values_extractor(self):
        doc = { 'a': 'hello', 'b': [{'c': 'world'}, {'c': 'brooklyn'}, {'c': 'new york'}]}
        e = SampleMultipleRenamedFieldExtractor()
        ep = ExtractorProcessor().set_input_fields(['a','b[*].c']).set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)

        self.assertEqual(updated_doc['e'][0]['value'], 'helloworld')
        self.assertEqual(updated_doc['e'][1]['value'], 'hellobrooklyn')
        self.assertEqual(updated_doc['e'][2]['value'], 'hellonew york')
        self.assertEqual(updated_doc['a'], 'hello')

    def test_chained_extractor(self):
        
        e1 = SampleSingleRenamedFieldExtractor()
        e2 = SampleMultipleRenamedFieldExtractor()
        e3 = SampleMultipleRenamedFieldExtractor()
        ep1 = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e1)
        ep2 = ExtractorProcessor().set_input_fields(['a','b']).set_output_field('e').set_extractor(e2)
        ep3 = ExtractorProcessor().set_input_fields(['a','b']).set_output_field('e').set_extractor(e2)
        ep4 = ExtractorProcessor().set_input_fields(['a','b']).set_output_field('f').set_extractor(e2)
        doc = { 'a': 'hello', 'b': 'world'}
        updated_doc = execute_processor_chain(doc, [ep1, ep2, ep3, ep4])
        
        self.assertEqual(updated_doc['e'][0]['value'], 'hello')
        self.assertEqual(updated_doc['e'][1]['value'], 'helloworld')
        self.assertEqual(updated_doc['e'][2]['value'], 'helloworld')
        self.assertEqual(updated_doc['f']['value'], 'helloworld')
        self.assertEqual(updated_doc['a'], 'hello')
        self.assertEqual(updated_doc['b'], 'world')


if __name__ == '__main__':
    unittest.main()