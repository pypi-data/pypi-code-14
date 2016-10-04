import sys
import time
import os
import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
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
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted']['value'], {'input': "Very passable black 25 year young TS girl with the best of the best! 9193959158 hosting off Western Boulevard NCstate area I'm waiting! 20-40 $pecial$", 'address': ['hosting off western boulevard']})

    

if __name__ == '__main__':
    unittest.main()



