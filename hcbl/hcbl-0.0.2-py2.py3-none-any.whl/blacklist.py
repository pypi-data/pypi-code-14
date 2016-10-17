#!/usr/bin/env python
# coding=utf-8

from wu_manber import WuManber
from Hachi_filter import HachiFilter, file2list

class Blacklist(HachiFilter):
    """
    A plugin for Hachi to block spam words.
    """
    def __init__(self, fp=None):
        self.wm = None
        if fp == None:
            self.filepath = './data/blacklist.csv'
        else:
            self.filepath = fp
        self.load_model()

    def load_model(self):
        self.wm = WuManber()
        self.wm.InitPattern(file2list(self.filepath))

    def predict(self, msg, level=0):
        blacklist_result = self.wm.Search(msg)
        # print blacklist_result
        if blacklist_result[0] != {}:
            return True
        return False

    def reset_param(self, filepath):
        self.filepath = filepath
        self.load_model()
