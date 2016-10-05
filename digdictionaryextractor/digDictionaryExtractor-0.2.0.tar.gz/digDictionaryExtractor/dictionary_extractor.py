import json
import pygtrie
from pygtrie import CharTrie
from digExtractor.extractor import Extractor
from digDictionaryExtractor.populate_trie import populate_trie
from itertools import ifilter
import copy

class DictionaryExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = 'tokens'
        self.pre_process = lambda x:x
        self.pre_filter = lambda x:x
        self.post_filter = lambda x: isinstance(x,basestring)

    def get_trie(self):
        self.trie

    def set_trie(self, trie):
        if not (isinstance(trie, pygtrie.CharTrie)):
            raise ValueError("trie must be a CharTrie")
        self.trie = trie
        return self

    def set_pre_process(self, pre_process):
        self.pre_process = pre_process
        return self

    def set_pre_filter(self, pre_filter):
        self.pre_filter = pre_filter
        return self

    def set_post_filter(self, post_filter):
        self.post_filter = post_filter
        return self

    def extract(self, doc):
        try:
            extracts = list()
            tokens = doc['tokens']

            extracts.extend(ifilter(self.post_filter, 
                map(lambda x: self.trie.get(x), 
                    ifilter(self.pre_filter, 
                        map(self.pre_process, iter(tokens))))))
            return list(frozenset(extracts))

        except:
            return list()

    def get_metadata(self):
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        return self.renamed_input_fields;

