import sys
import time
import os
import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digEmailExtractor.email_extractor import EmailExtractor

class TestEmailExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_email_extractor(self):
        doc = {'content': 'HOTMAIL:  sebasccelis@hotmail.com', 'b': 'world'}

        extractor = EmailExtractor().set_metadata({'extractor': 'email'})
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted']['value'], [{'email': 'sebasccelis@hotmail.com', 'obfuscation': 'False'}])

    

if __name__ == '__main__':
    unittest.main()



