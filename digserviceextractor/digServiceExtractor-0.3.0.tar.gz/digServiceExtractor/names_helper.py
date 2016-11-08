# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-10-05 16:01:52
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-10-07 14:00:32

from digDictionaryExtractor.populate_trie import populate_trie
from digDictionaryExtractor.dictionary_extractor import DictionaryExtractor

from names import names
default_names_trie = populate_trie(iter(names))


def get_service_extractor(names_trie=default_names_trie):
    return DictionaryExtractor()\
        .set_trie(names_trie)\
        .set_pre_filter(lambda x: True)\
        .set_pre_process(lambda x: x.lower())\
        .set_metadata({'extractor': 'dig_service_dictionary_extractor'})\
        .set_renamed_input_fields('tokens')\
        .set_ngrams(3)
