import os
import sys
import codecs

import unittest

import json
from digExtractor.extractor_processor import ExtractorProcessor
from digSocialMediaIdExtractor import socialmedia_id_extractor

class TestSocialMediaExtractor(unittest.TestCase):

    def test_socialmedia_id_extractor(self):
        doc = {"tokens":[{"extractor":"crf_tokenizer","result":
        [{"value":["adair","location",":","escorts","missouri","escorts","kansas",
        "city","escorts","adair","my","information","follow","me","on","twitter","@","DiamondSquirt","location",":","kansas","city","escorts","type",":"]}],
        "name":"tokens_high_recall",
        "source":"readability[?name='readability_high_recall'].(result[*][value])"},
        {"extractor":"crf_tokenizer","result":
        [{"value":["information","location",":","kansas","city","escorts","type"
        ,":","escort","agency","agency"]}],"name":"tokens_low_recall",
        "source":"readability[?name='readability_low_recall'].(result[*][value])"}]}

        #print doc["tokens"][0]["result"][0]["value"]
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        #print updated_doc

        self.assertEquals(updated_doc['social_media_ids'][0]['result']['value'], {'twitter': 'diamondsquirt', 'instagram': None})

    def test_missing_tokens(self):
        doc = {"tokens":[{"extractor":"crf_tokenizer","result":
        [{"value":[]}],
        "name":"tokens_high_recall",
        "source":"readability[?name='readability_high_recall'].(result[*][value])"},
        {"extractor":"crf_tokenizer","result":
        [{"value":[]}],"name":"tokens_low_recall",
        "source":"readability[?name='readability_low_recall'].(result[*][value])"}]}
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        #print updated_doc

        self.assertEquals(updated_doc, doc) 

    def test_empty_tokens(self):
        doc = {}
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor()
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        #print updated_doc

        self.assertEquals(updated_doc, {})       

if __name__ == '__main__':
    unittest.main()
