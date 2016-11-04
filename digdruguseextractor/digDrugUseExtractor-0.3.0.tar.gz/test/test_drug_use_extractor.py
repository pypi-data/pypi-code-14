import unittest

from digExtractor.extractor_processor import ExtractorProcessor
from digDrugUseExtractor.drug_use_extractor import DrugUseExtractor


class TestDrugUseExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_drug_use_extractor(self):
        doc = {'content': 'she is on drugs a dope whores and a junkie who is on some heavy drugs and does drugs and an adict, smells bad', 'b': 'world'}

        extractor = DrugUseExtractor().set_metadata({'extractor': 'drug'})
        extractor_processor = ExtractorProcessor().set_input_fields(
            ['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted'][0]['result'][0]['value'],
                         ['dope whores', 'junkie', 'adict', 'on drugs',
                         'on some heavy drugs', 'does drugs'])

    def test_drug_use_extractor_with_context(self):
        doc = {'content': 'she is on drugs a dope whores and a junkie who is on some heavy drugs and does drugs and an adict, smells bad', 'b': 'world'}

        extractor = DrugUseExtractor().set_metadata({'extractor': 'drug'})
        extractor.set_include_context(True)
        extractor_processor = ExtractorProcessor().set_input_fields(
            ['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'dope whores')
        self.assertEqual(result[0]['context']['start'], 18)
        self.assertEqual(result[0]['context']['end'], 29)
        self.assertEqual(result[1]['value'], 'junkie')
        self.assertEqual(result[1]['context']['start'], 36)
        self.assertEqual(result[1]['context']['end'], 42)
        self.assertEqual(result[2]['value'], 'adict')
        self.assertEqual(result[2]['context']['start'], 92)
        self.assertEqual(result[2]['context']['end'], 97)
        self.assertEqual(result[3]['value'], 'on drugs')
        self.assertEqual(result[3]['context']['start'], 7)
        self.assertEqual(result[3]['context']['end'], 15)
        self.assertEqual(result[4]['value'], 'on some heavy drugs')
        self.assertEqual(result[4]['context']['start'], 50)
        self.assertEqual(result[4]['context']['end'], 69)
        self.assertEqual(result[5]['value'], 'does drugs')
        self.assertEqual(result[5]['context']['start'], 74)
        self.assertEqual(result[5]['context']['end'], 84)


if __name__ == '__main__':
    unittest.main()
