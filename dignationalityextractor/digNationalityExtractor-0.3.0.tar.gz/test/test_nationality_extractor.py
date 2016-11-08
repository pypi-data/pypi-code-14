import unittest

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digNationalityExtractor.names_helper import get_nationality_extractor


class TestNationalityExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nationality_type_extractor(self):
        doc = {'content': ['American', 'Antiguans',
                           'Panamanian', 'Hello', 'World'], 'b': 'world'}

        extractor = get_nationality_extractor().set_metadata(
            {'extractor': 'nationality'})
        ep = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'american')
        self.assertEqual(result[1]['value'], 'antiguans')
        self.assertEqual(result[2]['value'], 'panamanian')

    def test_nationality_type_extractor_context(self):
        doc = {'content': ['American', 'Antiguans',
                           'Panamanian', 'Hello', 'World', 'East', 'Timorese', 'kittian', 'and', 'nevisian', 'End'], 'b': 'world'}

        extractor = get_nationality_extractor().set_metadata(
            {'extractor': 'nationality'}).set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'american')
        self.assertEqual(result[0]['context']['start'], 0)
        self.assertEqual(result[0]['context']['end'], 1)
        self.assertEqual(result[1]['value'], 'antiguans')
        self.assertEqual(result[1]['context']['start'], 1)
        self.assertEqual(result[1]['context']['end'], 2)
        self.assertEqual(result[2]['value'], 'panamanian')
        self.assertEqual(result[2]['context']['start'], 2)
        self.assertEqual(result[2]['context']['end'], 3)
        self.assertEqual(result[3]['value'], 'east timorese')
        self.assertEqual(result[3]['context']['start'], 5)
        self.assertEqual(result[3]['context']['end'], 7)
        self.assertEqual(result[4]['value'], 'kittian and nevisian')
        self.assertEqual(result[4]['context']['start'], 7)
        self.assertEqual(result[4]['context']['end'], 10)


if __name__ == '__main__':
    unittest.main()
