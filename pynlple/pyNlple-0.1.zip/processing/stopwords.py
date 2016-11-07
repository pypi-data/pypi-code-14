# -*- coding: utf-8 -*-
import codecs
import os

from module import get_abs_path as path
from module import append_paths as append


class Stopwords(object):

    def __init__(self, case_sensitive):
        self.case_sensitive = case_sensitive
        self.stopwords = list()
        stopwords_folder_path = path('processing/stopwords')
        for file_ in os.listdir(stopwords_folder_path):
            if file_.endswith(".txt"):
                with codecs.open(append(stopwords_folder_path, file_), 'r', 'utf8') as text_file:
                    for line in text_file:
                        stripped_word = line.strip()
                        if not self.case_sensitive:
                            stripped_word = stripped_word.lower()
                        if len(stripped_word) > 0:
                            self.stopwords.append(stripped_word)
        super(Stopwords, self).__init__()

    def is_a_stopword(self, token):
        return token in self.stopwords

    def is_not_a_stopword(self, token):
        if self.case_sensitive:
            return token not in self.stopwords
        else:
            return token.lower() not in self.stopwords


class Stopwords(object):

    def __init__(self, case_sensitive):
        self.case_sensitive = case_sensitive
        self.stopwords = list()
        stopwords_folder_path = path('processing/stopwords')
        for file_ in os.listdir(stopwords_folder_path):
            if file_.endswith(".txt"):
                with codecs.open(append(stopwords_folder_path, file_), 'r', 'utf8') as text_file:
                    for line in text_file:
                        stripped_word = line.strip()
                        if not self.case_sensitive:
                            stripped_word = stripped_word.lower()
                        if len(stripped_word) > 0:
                            self.stopwords.append(stripped_word)
        super(Stopwords, self).__init__()

    def is_a_stopword(self, token):
        return token in self.stopwords

    def is_not_a_stopword(self, token):
        if self.case_sensitive:
            return token not in self.stopwords
        else:
            return token.lower() not in self.stopwords