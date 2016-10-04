import sys
import time
import os
import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digPriceExtractor.price_extractor import PriceExtractor

class TestPriceExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_price_extractor(self):
        doc = {'content': 'Good morning I\'m doing incalls only gentleman I\'m quick 60 roses ?Hhr 80 roses ?Hour 120 roses unrushed and f.service provided nonnegotiable donations  614-563-3342', 'b': 'world'}

        extractor = PriceExtractor().set_metadata({'extractor': 'price'})
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted']['value'], {'price': [{'price': '60', 'price_unit': 'rose', 'time_unit': 'hhr'}, {'price': '80', 'price_unit': 'rose', 'time_unit': 'hour'}, {'price': '120', 'price_unit': 'rose', 'time_unit': ''}], 'price_per_hour': ['80', '120']})

    

if __name__ == '__main__':
    unittest.main()



