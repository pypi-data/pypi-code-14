#!/usr/bin/env python
# coding=utf-8

from Hachi_filter import HachiFilter
import jieba

configs = {
    'punc_rate_down': 0.02,
    'punc_rate_up': 0.35,
    'repeat_at_most': 20,
    'repeat_char': 5,
    'repeat_times': 4,
    'English_Alphabet': './data/wordsEn.txt',
    'least_char': 20,
}

class Meaningless(HachiFilter):
    """
    the plugin for Hachi to detect meaningless sentences
    """
    def __init__(self, args={}):
        self.tokenizer = jieba
        self.config = configs
        if args != {}:
            self.reset_param(args)
        self.English_words = set()
        self.load_model()

    def load_model(self):
        with open(self.config['English_Alphabet'], 'r') as f:
            alphabet = f.xreadlines()
            self.English_words = set(word.strip().lower() for word in alphabet)

    def count_freq(self, message, cut=True):
        cnt = {}
        if cut:
            message = self.tokenizer.cut(message)
        for word in message:
            if word not in cnt.keys():
                cnt[word] = 1
            else:
                cnt[word] += 1
        return cnt

    def get_mode(self, x):
        """
        return the mode [frequence, numbers] of the list
        """
        y = dict((a, x.count(a)) for a in x)
        cnt = max(y.values())
        mode = [0, cnt]
        for k, v in y.items():
            if v == cnt:
                mode[0] = k
                break
        return mode

    def is_repeat(self, message):
        # message = message.decode('utf-8')
        x = self.count_freq(message, False)
        if max(x.values()) >= self.config['repeat_at_most']:
            return True
        mode = self.get_mode(x.values())
        if mode[1] >= self.config['repeat_char'] and mode[0] >= self.config['repeat_times']:
            return True
        return False

    def punc_rate(self, message):
        punc = 0
        words = self.count_freq(message)
        for w in words.keys():
            if u'\u4e00' <= w <= u'\u9fff':
                continue
            if 'a' <= w.lower() <= 'z' and w.lower() not in self.English_words:
                continue
            punc += 1
        return float(punc) / len(words)

    def predict(self, message):
        if len(message) < self.config['least_char']:
            return False
        if self.is_repeat(message):
            return True
        if not self.config['punc_rate_down'] < self.punc_rate(message) < self.config['punc_rate_up']:
            return True
        return False

    def reset_param(self, args):
        for item in args.keys():
            if item in self.config.keys():
                self.config[item] = args[item]
