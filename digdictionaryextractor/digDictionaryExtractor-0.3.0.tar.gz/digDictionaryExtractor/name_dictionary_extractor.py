# -*- coding: utf-8 -*-
"""Module for initializing default name dictionary extractor"""
import re

from digDictionaryExtractor.dictionary_extractor import DictionaryExtractor

# already lower cased
VALID_TOKEN_RE = re.compile('[a-z].*[a-z]')


def get_name_dictionary_extractor(name_trie):
    """Method for creating default name dictionary extractor"""

    return DictionaryExtractor()\
        .set_trie(name_trie)\
        .set_pre_filter(VALID_TOKEN_RE.match)\
        .set_pre_process(lambda x: x.lower())\
        .set_metadata({'extractor': 'dig_name_dictionary_extractor'})
