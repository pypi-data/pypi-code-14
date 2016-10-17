#!/usr/bin/env python
# coding=utf-8

import pickle
import os

def file2list(filename):
    if not isinstance(filename, str):
        raise TypeError
    listr = []
    with open(filename, 'r') as ff:
        for line in ff.readlines():
            listr.append(line.strip())
    return listr

class HachiFilter(object):
    """
    The basic class for Hachi filters.
    """
    def __init__(self, arg={}):
        self.arg = arg
        self.filter = object()
        self.load_model()

    def load_model(self):
        filepath = self.__name__ + '.pickle'
        if not os.path.exists(filepath):
            self.fit()
            with open(filepath, 'wb') as fw:
                pickle.dump(self.filter, fw)
                fw.close()
        else:
            with open(filepath, 'rb') as fr:
                self.filter = pickle.load(fr)
                fr.close()

    def load_data(self, filepath):
        data = file2list(filepath)
        return data

    def fit(self):
        data_path = './data.csv'
        if os.path.exists(data_path):
            self.filter.fit(load_data(data_path))

    def predict(self, message, level=0):
        return self.filter.predict(message)

    def reset_param(self, arg):
        self.arg = arg
