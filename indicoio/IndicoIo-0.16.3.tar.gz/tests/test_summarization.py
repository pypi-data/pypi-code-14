import os, unittest

from indicoio import config
from indicoio import summarization

TEXT_DATA = open(os.path.join(os.path.dirname(__file__), "data", "long_text.txt"), 'rb').read()

class SummarizationTest(unittest.TestCase):
    def setUp(self):
        self.api_key = config.api_key

        if not self.api_key:
            raise SkipTest

    def test_summarization(self):
        response = summarization(TEXT_DATA, top_n=5)
        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 5)
