import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor_processor import ExtractorProcessor
from digAddressExtractor.address_extractor import AddressExtractor

class TestAddressExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_address_extractor(self):
        doc = {'content': 'Very passable black 25 year young TS girl with the best of the best! 9193959158 hosting off Western Boulevard NCstate area I\'m waiting! 20-40 $pecial$', 'b': 'world'}

        extractor = AddressExtractor().set_metadata({'extractor': 'address'})
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)
        updated_doc = ep.extract(doc)

        result = updated_doc['extracted'][0]['result'][0]

        self.assertEqual(result['value'], 'hosting off western boulevard')

    def test_address_extractor_with_context(self):
        doc = {'content': 'Very passable black 25 year young TS girl with the best of the best! 9193959158 hosting off Western Boulevard NCstate area I\'m waiting! 20-40 $pecial$', 'b': 'world'}

        extractor = AddressExtractor().set_metadata({'extractor': 'address'})\
                                      .set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)

        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result'][0]
        self.assertEqual(result['value'], 'hosting off western boulevard')
        self.assertEqual(result['context']['start'], 69)
        self.assertEqual(result['context']['end'], 110)

    def test_multiple_address_extractor_with_context(self):
        doc = {'content': 'The LA area has many airports.  LAX is located at 1 World Way, Los Angeles, CA 90045.  The Bob Hope airport is at 2627 N Hollywood Way, Burbank, CA 91505.  Both are very busy.', 'b': 'world'}

        extractor = AddressExtractor().set_metadata({'extractor': 'address'})\
                                      .set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)

        updated_doc = ep.extract(doc)
        result1 = updated_doc['extracted'][0]['result'][0]
        self.assertEqual(result1['value'], '1 world way,')
        self.assertEqual(result1['context']['start'], 50)
        self.assertEqual(result1['context']['end'], 62)
        result2 = updated_doc['extracted'][0]['result'][1]
        self.assertEqual(result2['value'], '2627 n hollywood way,')
        self.assertEqual(result2['context']['start'], 114)
        self.assertEqual(result2['context']['end'], 135)


if __name__ == '__main__':
    unittest.main()
