import unittest

# import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'],
                         'sebasccelis@hotmail.com')

    def test_email_extractor_with_context(self):
        doc = {'content': 'HOTMAIL:  sebasccelis@hotmail.com  OTHER: sebasccelis@gml ', 'b': 'world'}

        extractor = EmailExtractor().set_metadata({'extractor': 'email'})
        extractor.set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(result[0]['value'], 'sebasccelis@hotmail.com')
        self.assertEqual(result[0]['obfuscation'], False)
        self.assertEqual(result[0]['field'], 'text')
        self.assertEqual(result[0]['start'], 10)
        self.assertEqual(result[0]['end'], 33)
        self.assertEqual(result[1]['value'], 'sebasccelis@gmail.com')
        self.assertEqual(result[1]['obfuscation'], True)
        self.assertEqual(result[1]['field'], 'text')
        self.assertEqual(result[1]['start'], 42)
        self.assertEqual(result[1]['end'], 57)

    def test_removing_social_media_account(self):
        doc = {'content': 'facebook:  facebook@hotmail.com  twitter: twitter@gml others: sebasccelis@gmail.com', 'b': 'world'}
        extractor = EmailExtractor().set_metadata({'extractor': 'email'})
        extractor.set_include_context(True)
        ep = ExtractorProcessor().set_input_fields(['content'])\
                                 .set_output_field('extracted')\
                                 .set_extractor(extractor)
        updated_doc = ep.extract(doc)
        result = updated_doc['extracted'][0]['result']
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], 'sebasccelis@gmail.com')


if __name__ == '__main__':
    unittest.main()
