# -*- coding: utf-8 -*-
from pynlple.module import abs_path
from pynlple.processing.dictionary import DictionaryLookUp, FileFolderTokenMapping, DictionaryBasedTagger
from pynlple.processing.text import ClassTokenFilter


class DictionaryStopwordsFilter(ClassTokenFilter):

    def __init__(self, stopwords_provider=None, preprocessing_func=None):
        if not stopwords_provider:
            self.__stopwords_provider = FileFolderTokenMapping(
                ['punctuation.txt', {'rus/pos': ['conjunctions.txt', 'particles.txt', 'prepositions.txt', 'pronouns.txt']}],
                data_folder=abs_path(__file__, 'data'),
                recursive=True)
        else:
            self.__stopwords_provider = stopwords_provider
        self.__dictionary = DictionaryLookUp(self.__stopwords_provider, preprocessing_method=preprocessing_func)
        self.__tagger = DictionaryBasedTagger(self.__dictionary)
        super().__init__(self.__tagger)
