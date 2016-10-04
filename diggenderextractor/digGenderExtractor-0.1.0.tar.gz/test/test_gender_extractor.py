import sys
import time
import os
import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digGenderExtractor.gender_extractor import GenderExtractor

class TestGenderExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_price_extractor(self):
        doc = {'content': 'female ts male gender', 'b': 'world'}

        extractor = GenderExtractor().set_metadata({'extractor': 'gender'})
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted']['value'], 'transgender')

    

if __name__ == '__main__':
    unittest.main()



