import os
import json
import codecs
import unittest

from digExtractor.extractor_processor import ExtractorProcessor
from digDictionaryExtractor.populate_trie import populate_trie
from digCityExtractor.city_helper import\
    get_city_dictionary_extractor


class TestCityExtractorMethods(unittest.TestCase):

    def load_file(self, filename):
        names_file = os.path.join(os.path.dirname(__file__), filename)
        names = json.load(codecs.open(names_file, 'r', 'utf-8'))
        return names

    def test_city_extractor(self):
        doc = {'content': ["orlando", "Teacher", "to", "the", "New/Curious.", "Good-looking,", "Bi,", "Sense", "of", "Humor,", "Fun.", "Great", "Body.", "Educated,", "Honest,", "Sane.", "Healthy/DDF/Neg.", "AM,PM,", "24/7,", "Overnights,", "Multi-Days.", "Very", "Skilled:", "Massage", "or", "Vanilla", "or", "Kink", "or", "Wild.", "Discreet", "&", "Professional.", "Incalls", "&", "Outcalls:Abroad.", "VISIT", "MY", "WEBSITE", "FOR", "RATES,", "MORE", "HOT", "PICS,", "ALL", "MY", "REVIEWS,", "HIRING", "TIPS", "&", "MORE.", "", "", "", "", "", "his", "stats", "", "", "", "", "AGE:", "", "45", "", "Role:", "", "", "Versatile", "", "HEIGHT:", "", "5'11\"", "(180cm)", "", "WEIGHT:", "", "150", "-", "170", "lbs", "(68", "-", "77", "kg)", "", "Piercings:", "", "Not", "Specified", "", "", "", "RACE:", "", "White", "", "HAIR", "COLOR:", "", "Dark", "Brown", "", "EYE", "COLOR:", "", "Green", "", "Open", "To", "", "LTR", ":", "", "Yes", "", "Languages:", "", "English,", "Other", "", "", "", "BODY", "TYPE:", "", "Muscular/Buff", "", "BODY", "HAIR:", "", "Moderately", "hairy", "", "Tattoos:", "", "Not", "Specified", "", "Smoker:", "", "Not", "Specified", "", "", "", "", "", "", "", "reviews", "", "", "\r", "", "M4RN", "Reviews:", "", "8", "", "Most", "Recent", "M4RN", "Star", "Review:", "", "04/30/2016", "", "", "", "", "", "", "", "", "", "", "services", "provided", "", "", "", "Escort", "", "yes", "", "HOT", "Massage", "", "yes", "", "Massage", "", "yes", "", "Registered", "Therapi"]}
        cities = populate_trie(map(lambda x: x.lower(), self.load_file("cities.json")))
        stop_words = populate_trie(map(lambda x: x.lower(), self.load_file("stop_words.json")))

        extractor = get_city_dictionary_extractor(cities, stop_words)
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('cities').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['cities'][0]['result'][0]['value'], u'orlando') 

    def test_state_extractor(self):
        doc = {'content': ["", "ID#182730", "-", "florida", "LegendaryDave", "-", "Salt", "Lake", "-", "Gay", "Escorts", "&", "Gay", "Massage", "", "LegendaryDave", "2120.5", "Miles", "Away", "THE", "LEGENDARY", "DAVE-", "1ST", "TIME", "IN", "SALT", "LAKE", "CITY", "Over", "200", "Reviews!", "***Voted", "one", "of", "the", "Top", "50", "Escorts", "in", "the", "USA,", "for", "the", "last", "5", "years", "in", "a", "row***", "Secure,", "Masculine,", "Adventurous.", "Top/Vers", "Stud.", "Teacher", "to", "the", "New/Curious.", "Good-looking,", "Bi,", "Sense", "of", "Humor,", "Fun.", "Great", "Body.", "Educated,", "Honest,", "Sane.", "Healthy/DDF/Neg.", "AM,PM,", "24/7,", "Overnights,", "Multi-Days.", "Very", "Skilled:", "Massage", "or", "Vanilla", "or", "Kink", "or", "Wild.", "Discreet", "&", "Professional.", "Incalls", "&", "Outcalls:", "USA", "&", "Abroad.", "VISIT", "MY", "WEBSITE", "FOR", "RATES,", "MORE", "HOT", "PICS,", "ALL", "MY", "REVIEWS,", "HIRING", "TIPS", "&", "MORE.", "his", "stats", "AGE:", "45", "Role:", "Versatile", "HEIGHT:", "5'11\"", "(180cm)", "WEIGHT:", "150", "-", "170", "lbs", "(68", "-", "77", "kg)", "Piercings:", "Not", "Specified", "RACE:", "White", "HAIR", "COLOR:", "Dark", "Brown", "EYE", "COLOR:", "Green", "Open", "To", "LTR", ":", "Yes", "Languages:", "English,", "Other", "BODY", "TYPE:", "Muscular/Buff", "BODY", "HAIR:", "Moderately", "hairy", "Tattoos:", "Not", "Specified", "Smoker:", "Not", "Specified", "reviews", "\r", "M4RN", "Reviews:", "8", "Most", "Recent", "M4RN", "Star", "Review:", "04/30/2016", "", "services", "provided", "Escort", "yes", "HOT", "Massage", "yes", "Massage", "yes", "Registered", "Therapist", "yes", "In", "Calls", "yes", "Out", "Calls", "yes", "US", "Travel", "yes", "Int'l", "Travel", "yes", "Advertiser", "Since", "Dec", "'07", "contact", "info", "Phone:", "PREFERS", "PHONE", "CONTACT", "location", "2120.5", "Miles", "area:", "Salt", "Lake", "City", "/", "Ogden", "Local", "City:", "Salt", "Lake", "Postal", "Code:", "84101", "availability", "", "", "s", "m", "t", "w", "t", "f", "s", "7am-11am", "", "11am-3pm", "", "3pm-7pm", "", "7pm-11pm", "", "11pm-3am", "", "3am-7am", "", "", "Elite", "&", "Platinum", "Advertisers", "ELITE", "Toronto", "Barcelona", "San", "Francisco", "/", "Oakland", "Cleveland", "/", "Lorain", "/", "Elyria", "Los", "Angeles", "/", "West", "Hollywood", "Find", "LegendaryDave,", "Rent", "Men", "and", "Male", "Massage", "in", "Salt", "Lake", "", ""]}
        states = populate_trie(map(lambda x: x.lower(), self.load_file("states.json")))
        stop_words = populate_trie(map(lambda x: x.lower(), self.load_file("stop_words.json")))
        extractor = get_city_dictionary_extractor(states, stop_words)
        extractor_processor = ExtractorProcessor().set_input_fields(['content']).set_output_field('state').set_extractor(extractor)
        updated_doc = extractor_processor.extract(doc)
        self.assertEqual(updated_doc['state'][0]['result'][0]['value'], u'florida')


if __name__ == '__main__':
    unittest.main()
