import unittest
from digExtractor.extractor_processor import ExtractorProcessor
from digAgeRegexExtractor.age_regex_helper import get_age_regex_extractor


class TestAgeRegexExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_age_regex_extractor(self):
        doc = {'content': "32years old ,im 23",
               'b': 'world'}

        extractor = get_age_regex_extractor()
        extractor_processor = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)

        result1 = updated_doc['extracted'][0]['result'][0]
        result2 = updated_doc['extracted'][0]['result'][1]
        self.assertEqual(result1['value'], '32')
        self.assertEqual(result2['value'], '23')

    def test_age_regex_extractor_with_context(self):
        doc = {'content': "32years old ,im 23",
               'b': 'world'}

        extractor = get_age_regex_extractor()
        extractor.set_include_context(True)
        extractor_processor = ExtractorProcessor().set_input_fields(
            'content').set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)

        result1 = updated_doc['extracted'][0]['result'][0]
        result2 = updated_doc['extracted'][0]['result'][1]
        self.assertEqual(result1['value'], '32')
        self.assertEqual(result1['context']['start'], 0)
        self.assertEqual(result1['context']['end'], 11)
        self.assertEqual(result2['value'], '23')
        self.assertEqual(result2['context']['start'], 11)
        self.assertEqual(result2['context']['end'], 18)


if __name__ == '__main__':
    unittest.main()
