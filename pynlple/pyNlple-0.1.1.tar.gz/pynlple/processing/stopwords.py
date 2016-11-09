# -*- coding: utf-8 -*-
import io
import os

from pynlple.module import append_paths as append
from pynlple.module import get_abs_path as path


class Stopwords(object):

    def __init__(self, case_sensitive):
        self.case_sensitive = case_sensitive
        self.stopwords = list()
        stopwords_folder_path = path('processing/data/rus/pos')
        for file_ in os.listdir(stopwords_folder_path):
            if file_.endswith(".txt"):
                with io.open(append(stopwords_folder_path, file_), 'rt', encoding='utf8') as text_file:
                    for line in text_file:
                        stripped_word = line.strip()
                        if not self.case_sensitive:
                            stripped_word = stripped_word.lower()
                        if len(stripped_word) > 0:
                            self.stopwords.append(stripped_word)
        super().__init__()

    def is_a_stopword(self, token):
        return token in self.stopwords

    def is_not_a_stopword(self, token):
        if self.case_sensitive:
            return token not in self.stopwords
        else:
            return token.lower() not in self.stopwords
