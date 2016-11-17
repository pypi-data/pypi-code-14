# -*- coding: utf-8 -*-
import copy
from digExtractor.extractor import Extractor


class UrlLocalityExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = ['tokens',
                                     'city_from_url',
                                     'state_from_url',
                                     'country_from_url',
                                     'url']
        self.cities = None
        self.states = None
        self.country_code_dict = {}
        self.countries = None
        self.stop_words = None

    def get_cities(self):
        return self.cities

    def set_cities(self, cities):
        self.cities = cities
        return self

    def get_states(self):
        return self.states

    def set_states(self, states):
        self.states = states
        return self

    def get_country_code_dict(self):
        return self.country_code_dict

    def set_country_code_to_country(self, country_code_to_country):
        if not isinstance(country_code_to_country, dict):
            raise ValueError("country_code_to_country must be a dict")
        self.country_code_dict = country_code_to_country
        return self

    def get_countries(self):
        return self.countries

    def set_countries(self, countries):
        self.countries = countries
        return self

    def get_stop_words(self):
        return self.stop_words

    def set_stop_words(self, stop_words):
        self.stop_words = stop_words
        return self
        
    def extract(self, doc):
        dict_out = {}

        if 'city_from_url' in doc:
            dict_out['cities'] = list(doc['city_from_url'])
        else:
            dict_out['cities'] = []

        if 'state_from_url' in doc:
            dict_out['states'] = list(doc['state_from_url'])
        else:
            dict_out['states'] = []

        if 'country_from_url' in doc:
            dict_out['countries'] = list(doc['country_from_url'])
        else:
            dict_out['countries'] = []

        tokens_doc = list(doc['tokens'])
        url = list(doc['url'])[0]

        # Get country codes from url
        ann_countries = []
        for token in tokens_doc:
            if token in self.country_code_dict:
                # Check if its actually a country code in the orig url
                pos = url.find('.' + token)
                if url[pos-3:pos] in ['.co', '.ac'] or url[pos-4:pos] in ['.org', '.com', '.edu', '.gov']:
                    ann_countries.append(self.country_code_dict[token])
        dict_out['countries'].extend(ann_countries)

        for token in tokens_doc:
            for i in range(0, len(token)):
                for j in range(i):
                    # Cities
                    value = token[j:i]
                    city = self.cities.get(value)
                    if city is not None and len(value) > 4 and value not in self.stop_words:
                        dict_out['cities'].append(value)
                    # States
                    state = self.states.get(value)
                    if state is not None and len(value) > 4 and value not in self.stop_words:
                        dict_out['states'].append(value)

                    # Countries
                    country = self.countries.get(value)
                    if country is not None and len(value) > 4 and value not in self.stop_words:
                        dict_out['countries'].append(value)

        return dict_out

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields
