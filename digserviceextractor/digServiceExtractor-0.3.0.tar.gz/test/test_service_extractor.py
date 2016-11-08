import unittest

from digExtractor.extractor_processor import ExtractorProcessor
from digServiceExtractor.names_helper import get_service_extractor


class TestServiceExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_age_extractor(self):
        doc = {'content': ['FOV', 'HELLO', 'WORLD'], 'b': 'world'}

        extractor = get_service_extractor().set_metadata({'extractor': 'service'})
        extractor_processor = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'fov')

    def test_age_extractor_context(self):
        doc = {'content': ['FOV', 'HELLO', 'WORLD', 'hot', 'towel', 'treatment', 'other'], 'b': 'world'}

        extractor = get_service_extractor().set_metadata({'extractor': 'service'})
        extractor.set_include_context(True)
        extractor_processor = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'fov')
        self.assertEqual(result[0]['context']['start'], 0)
        self.assertEqual(result[0]['context']['end'], 1)
        self.assertEqual(result[1]['value'], 'hot towel treatment')
        self.assertEqual(result[1]['context']['start'], 3)
        self.assertEqual(result[1]['context']['end'], 6)


if __name__ == '__main__':
    unittest.main()
