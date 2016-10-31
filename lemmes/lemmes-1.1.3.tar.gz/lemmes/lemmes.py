# -*- coding: UTF-8 -*-
import sys
import io
import config as cf
import logging
from backports import csv
from itertools import groupby
from os.path import isfile, join, isdir
from os import path, popen, makedirs
import shutil
from nltk.stem import SnowballStemmer
from pickle import dump, load
import difflib
import string
import re
from rules import RULES
from unidecode import unidecode


class Lemmatizer:
    @classmethod
    def __init__(self):
        self.STEMMER = SnowballStemmer('spanish')
        self.LANG = cf.LANG
        self.LOG = logging.getLogger(__name__)
        if not isfile(cf.FILE_LEMMAS_BIN):
            self.create_lemmas()
        self.LOG.info('uncompress dict: ' + repr(cf.FILE_LEMMAS_BIN))
        self.DICTIONARY = self.uncompress(cf.FILE_LEMMAS_BIN)

    @classmethod
    def stemmer(self, token):
        for r, v in RULES.iteritems():
            if r in token:
                token = v
                break
        return token, self.STEMMER.stem(token)

    @classmethod
    def lemmatize(self, token):
        if len(token):
            lemma = None
            self.LOG.info(token)
            token, stemmed = self.stemmer(token)
            lemmas = self.DICTIONARY.get(stemmed)
            self.LOG.info(token + ' lemmas: ' + repr(lemmas))
            if lemmas:
                if len(lemmas) == 1:
                    return lemmas.values()[0]
                elif (token in lemmas.keys()):
                    return lemmas.get(token)
                else:
                    l_words1 = set(lemmas)
                    l_words2 = set()
                    len_stemm = len(stemmed)-1
                    for t in range(len_stemm, len(token)):
                        n_stemm = token[:len_stemm]
                        self.LOG.info('aprox: ' + str(t) + ': ' + n_stemm)
                        for l in lemmas.keys():
                            if n_stemm in l:
                                w = lemmas.get(l)
                                if len(w) <= len(token) + 1:
                                    l_words2.add(w)
                                    self.LOG.info('aprox: ' + repr(w))
                        if len(l_words2):
                            l_words1 = l_words2
                            l_words2 = set()
                        len_stemm += 1
                        self.LOG.info('set: ' + repr(l_words1))
                    l_words1 = list(l_words1)
                    return l_words1[0] if len(l_words1) == 1 else l_words1
        return token

    @classmethod
    def create_lemmas(self):
        lemmas = []
        dictionary = {}
        with io.open(cf.FILE_LEMMAS_CSV, 'r', encoding='utf-8') as flemma:
            reader = csv.reader(flemma)
            for row in reader:
                if row[2] == '1':
                    lemmas.append((row[0], row[1]))
        lemmas.sort()
        for stemm, stemms in groupby(lemmas, lambda x: x[0]):
            stemm_list = {}
            for words in stemms:
                self.LOG.debug('Stemm: ' + stemm + ' | Word: ' + words[1])
                stemm_list.update({unidecode(words[1]): words[1]})
            dictionary.update({stemm: stemm_list})
        self.compress(dictionary, cf.FILE_LEMMAS_BIN)
        self.LOG.info('Done!: ' + cf.FILE_LEMMAS_BIN)

    @staticmethod
    def uncompress(filename):
        output = open(filename, 'rb')
        return load(output)

    @staticmethod
    def compress(obj, filename):
        output = open(filename, 'wb')
        dump(obj, output)
        output.close()
        return filename

    @staticmethod
    def is_unicode(text):
        return text if isinstance(text, unicode) else unicode(text, 'utf8')

    @classmethod
    def move_file(self):
        lemmas = []
        dictionary = {}
        shutil.copy('data/' + cf.SOURCE_LEMMAS_CSV, cf.FILE_LEMMAS_CSV)
