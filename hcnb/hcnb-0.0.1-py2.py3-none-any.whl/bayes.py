#!/usr/bin/env python
# coding=utf-8

from Hachi_filter import HachiFilter, file2list
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import ndarray
import jieba
import os
import pickle

configs = {
    'threshold': 0.5,
    'classify_model': 'filter.pickle',
    'train_rate': 0.9,
    'spam_file': './data/spam.csv',
    'ham_file': './data/ham.csv',
    'words_file': './data/words.csv',
    'stopwords_file': './data/stopwords.csv',
    'userdict_file': './data/userdict.csv',
}

class NaiveBayes(HachiFilter):
    """
    Naive Bayes for Hachi to filt spam.
    """
    def __init__(self, args={}):
        self.clf = None
        self.config = configs
        if args != {}:
            self.reset_param(args)
        self.get_tfidf()
        self.load_model()

    def reset_param(self, args):
        for item in args.keys():
            if item in self.config.keys():
                self.config[item] = args[item]

    def get_tfidf(self):
        self.tokenizer = jieba
        self.tokenizer.load_userdict(self.config['userdict_file'])
        words = file2list(self.config['words_file'])
        stopwords = file2list(self.config['stopwords_file'])
        self.tv = TfidfVectorizer(stop_words=stopwords,
                                tokenizer=self.tokenizer.cut).fit(words)

    def load_model(self):
        model_path = self.config['classify_model']
        if not os.path.exists(model_path):
            self.train_model()
            with open(model_path, 'wb') as f:
                pickle.dump(self.clf, f)
                f.close()
        else:
            with open(model_path, 'rb') as f:
                self.clf = pickle.load(f)
                f.close()

    def train_model(self):
        ham_file = self.config['ham_file']
        spam_file = self.config['spam_file']
        ham = file2list(ham_file)
        spam = file2list(spam_file)
        y_train = len(ham) * [0] + len(spam) * [1]
        X_train = self.tv.transform(ham + spam)
        self.clf = MultinomialNB()
        self.clf.fit(X_train, y_train)

    def get_spam_rate(self, msg):
        y = self.clf.predict_proba(self.tv.transform([msg]))
        if isinstance(y, ndarray):
            y = y.tolist()
        return y[0][1]

    def predict(self, msg):
        y = self.get_spam_rate(msg)
        return True if y > self.config['threshold'] else False

    def show_analyse_result(self, rate):
        print('=' * 80)
        print('words:\t'),
        for item in rate:
            print(item[0] + '\t'),
        print('\nrate:\t'),
        for item in rate:
            print('%.3f\t' % item[1]),
        print('\n' + '=' * 80)

    def analyse(self, msg):
        words = list(self.tokenizer.cut(msg))
        spam_rate = [(w, self.get_spam_rate(w.encode('utf-8'))) for w in words]
        spam_rate.sort(cmp=lambda x,y: cmp(x[1],y[1]), reverse=True)
        self.show_analyse_result(spam_rate)
        return spam_rate
