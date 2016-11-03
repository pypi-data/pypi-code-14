# -*- coding: utf-8 -*-
"""Module for defining an extractor that accepts a list of tokens
and outputs tokens that exist in a user provided trie"""
import copy

from itertools import ifilter
from itertools import tee
from itertools import chain
from itertools import izip
from itertools import imap
from itertools import repeat
from pygtrie import CharTrie
from digExtractor.extractor import Extractor


class DictionaryExtractor(Extractor):

    def __init__(self):
        super(DictionaryExtractor, self).__init__()
        self.renamed_input_fields = 'tokens'
        self.pre_process = lambda x: x
        self.pre_filter = lambda x: x
        self.post_filter = lambda x: isinstance(x, basestring)
        self.trie = None
        self.metadata = {}
        self.ngrams = 1
        self.joiner = ' '

    def get_trie(self):
        return self.trie

    def set_trie(self, trie):
        if not isinstance(trie, CharTrie):
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

    def set_ngrams(self, ngrams):
        self.ngrams = ngrams
        return self

    def set_joiner(self, joiner):
        self.joiner = joiner
        return self

    def generate_ngrams_with_context_helper(self,
                                            ngrams_iterable,
                                            ngrams_length):
        return imap(lambda ngrams_with_index: (ngrams_with_index[1],
                                               ngrams_with_index[0],
                                               ngrams_with_index[0] +
                                               ngrams_length),
                    enumerate(ngrams_iterable))

    def generate_ngrams_with_context(self, tokens):
        chained_ngrams_iterable = self.generate_ngrams_with_context_helper(iter(tokens), 1)
        for n in range(2, self.ngrams + 1):
            ngrams_iterable = tee(tokens, n)
            for j in range(1, n):
                for k in range(j):
                    next(ngrams_iterable[j], None)
            ngrams_iterable_with_context = self.generate_ngrams_with_context_helper(izip(*ngrams_iterable), n)
            chained_ngrams_iterable = chain(chained_ngrams_iterable,
                                            ngrams_iterable_with_context)

        return chained_ngrams_iterable

    def generate_ngrams(self, tokens):
        chained_ngrams_iterable = iter(tokens)
        for n in range(2, self.ngrams + 1):
            ngrams_iterable = tee(iter(tokens), n)
            for j in range(1, n):
                for k in range(j):
                    next(ngrams_iterable[j], None)
            chained_ngrams_iterable = chain(chained_ngrams_iterable,
                                            izip(*ngrams_iterable))

        return chained_ngrams_iterable

    def combine_ngrams(self, ngrams):
        if isinstance(ngrams, basestring):
            return ngrams
        else:
            combined = self.joiner.join(ngrams)
            return combined

    def extract(self, doc):
        try:
            extracts = list()
            tokens = doc['tokens']

            if self.get_include_context():
                ngrams_iterable = self.generate_ngrams_with_context(tokens)
                extracts.extend(
                    map(lambda ngrams_context: self.wrap_value_with_context(ngrams_context[0], 'tokens', ngrams_context[1], ngrams_context[2]),
                        ifilter(lambda ngrams_context: self.post_filter(ngrams_context[0]),
                                map(lambda ngrams_context: (self.trie.get(ngrams_context[0]), ngrams_context[1], ngrams_context[2]),
                                            ifilter(lambda ngrams_context: self.pre_filter(ngrams_context[0]),
                                                    map(lambda ngrams_context: (self.pre_process(ngrams_context[0]), ngrams_context[1], ngrams_context[2]),
                                                        map(lambda ngrams_context: (self.combine_ngrams(ngrams_context[0]), ngrams_context[1], ngrams_context[2]), ngrams_iterable)))))))

            else:
                ngrams_iterable = self.generate_ngrams(tokens)

                extracts.extend(ifilter(self.post_filter,
                                        map(self.trie.get,
                                            ifilter(self.pre_filter,
                                                    map(self.pre_process,
                                                        map(self.combine_ngrams,
                                                            ngrams_iterable))))))
            return list(extracts)

        except Exception as inst:
            print "error operator"
            print type(inst)
            print inst
            return list()

    def get_metadata(self):
        """Returns a copy of the metadata that characterizes this extractor"""
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        """Overwrite the metadata that characterizes this extractor"""
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        """Return a scalar or ordered list of fields to rename to"""
        return self.renamed_input_fields
