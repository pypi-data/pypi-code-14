import unittest

from digExtractor.extractor_processor import ExtractorProcessor
from digPhoneExtractor.phone_extractor import PhoneExtractor


class TestPhoneExtractorMethods(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_phone_extractor(self):
        doc = {'content': 'Sexy new girl in town searching for a great date wiff u Naughty fresh girl here searching 4 a great date wiff you Sweet new girl in town seeking for a good date with u for80 2sixseven one9zerofor 90hr incall or out call',
               'url': 'http://liveescortreviews.com/ad/philadelphia/602-228-4192/1/310054', 'b': 'world'}

        extractor = PhoneExtractor().set_metadata({'extractor': 'phone'})
        ep = ExtractorProcessor().set_input_fields(['url', 'content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'],
                         {'obfuscation': 'False', 'telephone': '6022284192'})
        self.assertEqual(result[1]['value'],
                         {'obfuscation': 'True', 'telephone': '4802671904'})


if __name__ == '__main__':
    unittest.main()
