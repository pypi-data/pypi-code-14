import unittest
import re
from digExtractor.extractor_processor import ExtractorProcessor
from digRegexExtractor.regex_extractor import RegexExtractor


class TestNameRegexExtractor(unittest.TestCase):

    def test_name_extractor(self):
        doc = {'a': 'my name is foo', 'b': 'world'}
        name_regex = re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        e = RegexExtractor().set_regex(name_regex).set_metadata({'extractor': 'name_regex'})
        ep = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)
        self.assertEqual(updated_doc['e'][0]['result'][0]['value'], 'foo')

    def test_double_name_extractor(self):
        doc = {'a': 'my name is foo but my friends call me bar', 'b': 'world'}
        name_regex = re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        call_me_name_regex = re.compile('(?:call[\s]+me[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        e = RegexExtractor().set_regex([name_regex, call_me_name_regex]).set_metadata({'extractor': 'name_regex'})
        ep = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)
        self.assertEqual(updated_doc['e'][0]['result'][0]['value'], 'foo')
        self.assertEqual(updated_doc['e'][0]['result'][1]['value'], 'bar')

    def test_duplicate_name_extractor(self):
        doc = {'a': 'my name is foo my name is foo', 'b': 'world'}
        name_regex = re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        e = RegexExtractor().set_regex(name_regex).set_metadata({'extractor': 'name_regex'})
        ep = ExtractorProcessor().set_input_fields('a').set_output_field('e').set_extractor(e)
        updated_doc = ep.extract(doc)
        self.assertEqual(updated_doc['e'][0]['result'][0]['value'], 'foo')
        self.assertEqual(len(updated_doc['e'][0]['result']), 1)

    def test_double_name_with_context_extractor(self):
        doc = {'a': 'my name is foo but my friends call me bar', 'b': 'world'}
        name_regex = re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        call_me_name_regex = re.compile('(?:call[\s]+me[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)
        e = RegexExtractor().set_regex([name_regex, call_me_name_regex])\
                            .set_metadata({'extractor': 'name_regex'})
        e.set_include_context(True)
        ep = ExtractorProcessor().set_input_fields('a')\
                                 .set_output_field('e')\
                                 .set_extractor(e)
        updated_doc = ep.extract(doc)
        self.assertEqual(updated_doc['e'][0]['result'][0]['value'], 'foo')
        self.assertEqual(updated_doc['e'][0]['result'][0]['context']['start'], 0)
        self.assertEqual(updated_doc['e'][0]['result'][0]['context']['end'], 14)
        self.assertEqual(updated_doc['e'][0]['result'][1]['value'], 'bar')
        self.assertEqual(updated_doc['e'][0]['result'][1]['context']['start'], 30)
        self.assertEqual(updated_doc['e'][0]['result'][1]['context']['end'], 41)


if __name__ == '__main__':
    unittest.main()
