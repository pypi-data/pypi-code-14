# -*- coding: utf-8 -*-
from digDictionaryExtractor.dictionary_extractor import DictionaryExtractor


def get_city_dictionary_extractor(city_trie, stop_words=[]):
    """Method for creating default name dictionary extractor"""

    return DictionaryExtractor()\
        .set_trie(city_trie)\
        .set_pre_filter(lambda x: x not in stop_words)\
        .set_pre_process(lambda x: x.lower())\
        .set_metadata({'extractor': 'dig_city_dictionary_extractor'})\
        .set_ngrams(3)\
        .set_joiner(' ')
