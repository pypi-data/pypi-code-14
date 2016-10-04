import sys
import time
import os
import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from digExtractor.extractor import Extractor
from digExtractor.extractor_processor import ExtractorProcessor
from digReviewIDExtractor.review_id_extractor import ReviewIDExtractor

class TestReviewIDExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_review_id_extractor(self):
        doc = {'content': 'Hey guys! I\'m Heidi!!! I am a bubbly, busty, blonde massage therapist and only provide the most sensual therapeutic experience! I love what I do and so will YOU!!! I am always learning new techniqes and helping other feel relaxed. Just send Me an email and lets meet!!!  I am reviewed! #263289 \nheidishandsheal@gmail.com', 'b': 'world'}

        extractor = ReviewIDExtractor().set_metadata({'extractor': 'review_id'})
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('extracted').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['extracted']['value'], [{'identifier': '263289', 'site': 'others'}])

    

if __name__ == '__main__':
    unittest.main()



