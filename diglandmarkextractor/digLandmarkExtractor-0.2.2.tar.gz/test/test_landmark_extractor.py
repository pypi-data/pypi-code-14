import os
import sys
import codecs

import unittest

import json
from digLandmarkExtractor.dig_landmark_extractor import DigLandmarkExtractor
from digExtractor.extractor_processor import ExtractorProcessor
from landmark_extractor.extraction.Landmark import RuleSet
from digLandmarkExtractor.get_landmark_extractor_processors\
    import get_landmark_extractor_processors, get_landmark_extractor_processor_for_rule_set
from digExtractor.extractor_processor_chain import execute_processor_chain

class TestDigLandmarkExtractor(unittest.TestCase):

    def load_json_file(self, filename):
        rules_file = os.path.join(os.path.dirname(__file__), filename)
        rules = json.load(codecs.open(rules_file, 'r', 'utf-8'))
        return rules

    def load_file(self, filename):
        with open(os.path.join(os.path.dirname(__file__), filename), 'r') as myfile:
            data=myfile.read().replace('\n', '')
            return data

    def test_dig_landmark_extractor(self):
        rule = self.load_json_file("craigslist_rule.json")
        html = self.load_file("craigslist_ad.html")

        doc = {"foo": html}
        r = RuleSet(rule).rules[0]
        e = DigLandmarkExtractor()\
            .set_rule(r)\
            .set_metadata({"name": "landmark_extractor"})

        ep = ExtractorProcessor().set_input_fields(
            'foo').set_output_field(r.name).set_extractor(e)

        updated_doc = ep.extract(doc)
        self.assertEquals(updated_doc['posting_date'][0]['value'],
                          '2016-09-07 5:57pm')

    def test_many_dig_landmark_extractor(self):
        rules = self.load_json_file("craigslist_rules.json")
        html = self.load_file("craigslist_ad.html")

        doc = {"foo": html}

        eps = get_landmark_extractor_processors(RuleSet(rules), "foo")
        updated_doc = execute_processor_chain(doc, eps)
        self.assertEquals(updated_doc['posting_date-1'][0]['value'],
                          '2016-09-07 5:57pm')
        self.assertEquals(updated_doc['location-2'][0]['value'], 'Bend')

    def test_dig_landmark_extractor_rule_set(self):
        rules = self.load_json_file("craigslist_rules.json")
        html = self.load_file("craigslist_ad.html")

        doc = {"foo": html}

        ep = get_landmark_extractor_processor_for_rule_set(RuleSet(rules),
                                                           "foo")
        updated_doc = execute_processor_chain(doc, [ep])
        self.assertEquals(updated_doc['posting_date-1'][0]['value'],
                          '2016-09-07 5:57pm')
        self.assertEquals(updated_doc['location-2'][0]['value'], 'Bend')

    def test_dig_landmark_extractor_rule_set_renamed(self):
        rules = self.load_json_file("craigslist_rules.json")
        html = self.load_file("craigslist_ad.html")

        doc = {"foo": html}
        output_fields = {'posting_date-1': 'date', 'posting_date-2': 'date',
                         'location-1': 'location', 'location-2': 'location'}

        ep = get_landmark_extractor_processor_for_rule_set(RuleSet(rules),
                                                           "foo",
                                                           output_fields)
        updated_doc = execute_processor_chain(doc, [ep])
        self.assertEquals(updated_doc['date'][0]['value'],
                          '2016-09-07 5:57pm')
        self.assertEquals(updated_doc['date'][0]['original_output_field'],
                          'posting_date-1')
        self.assertEquals(len(updated_doc['date']), 1)
        self.assertEquals(updated_doc['location'][0]['value'], 'bend &gt;')
        self.assertEquals(updated_doc['location'][0]['original_output_field'],
                          'location-1')
        self.assertEquals(updated_doc['location'][1]['value'], 'Bend')
        self.assertEquals(updated_doc['location'][1]['original_output_field'],
                          'location-2')


if __name__ == '__main__':
    unittest.main()
