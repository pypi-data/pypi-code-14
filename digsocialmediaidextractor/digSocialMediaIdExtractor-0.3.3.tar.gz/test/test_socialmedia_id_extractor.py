import codecs
import unittest
import json

from digExtractor.extractor_processor import ExtractorProcessor
from digSocialMediaIdExtractor import socialmedia_id_extractor


class TestSocialMediaExtractor(unittest.TestCase):
    def __init__(self):
        self.en_words = json.load(codecs.open("english.json", 'r', 'utf-8'))
        self.fr_words = json.load(codecs.open("french.json", 'r', 'utf-8'))

    def test_socialmedia_id_extractor(self):
        doc = {"tokens":["adair","location",":","escorts","missouri","escorts","kansas",
        "city","escorts","adair","my","information","follow","me","on","twitter","@","DiamondSquirt","location",":","kansas","city","escorts","type",":"]}

        #print doc["tokens"][0]["result"][0]["value"]
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor(self.en_words, self.fr_words)
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        self.assertEquals(updated_doc['social_media_ids'][0]['result']['value'], {'twitter': 'diamondsquirt'})

    def test_missing_tokens(self):
        doc = {"tokens":[]}
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor(self.en_words, self.fr_words)
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        #print updated_doc

        self.assertEquals(updated_doc, doc) 

    def test_empty_tokens(self):
        doc = {}
        extractor = socialmedia_id_extractor.SocialMediaIdExtractor(self.en_words, self.fr_words)
        extractor_processor = ExtractorProcessor().set_input_fields('tokens').set_output_field('social_media_ids').set_extractor(extractor)

        updated_doc = extractor_processor.extract(doc)

        #print updated_doc

        self.assertEquals(updated_doc, {})       

if __name__ == '__main__':
    unittest.main()
