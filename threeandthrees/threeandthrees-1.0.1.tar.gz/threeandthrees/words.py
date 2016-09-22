from collections import defaultdict, OrderedDict
import random
from colorama import init, Fore
import os
import re

init(autoreset=True)

safe_pattern = re.compile('^[a-z]{9}$')


def extract_words():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/american-english.txt', 'r') as f:
        raw_data = f.read().split('\n')
        data = list(filter(is_clean, raw_data))
        return data


def is_clean(word):
    return re.search(safe_pattern, word) is not None


def extract_cores(wordlist):
    coremap = defaultdict(list)
    for word in wordlist:
        coremap[word[3:6]].append(word)
    return coremap


all_words = extract_words()
coremap = extract_cores(all_words)


class Wordmonger(object):

    def __init__(self, all_words, coremap):
        self.words = all_words
        self.coremap = coremap
        self.challenge = OrderedDict()

    def answer_count(self, candidate):
        value = self.coremap.get(candidate, None)
        if value is None:
            return 0
        else:
            return len(value)

    def answers(self, candidate):
        return self.coremap.get(candidate, None)

    def generate(self):
        key = random.choice(list(self.coremap.keys()))
        return key
        # return self.coremap[key]

    def check(self, arg):
        return arg in self.coremap[arg[3:6]]

    def show_challenge(self):
        for idx, (key, value) in enumerate(self.challenge.iteritems(), 1):
            if value is not None:
                print(
                    "{idx}:\t {color}{word}".format(
                        **{
                            'idx': idx, 'word': value, 'color': Fore.GREEN
                        }
                    )
                )
            else:
                print(
                    "{idx}:\t ___{core}___".format(
                        **{'idx': idx, 'core': key}
                    )
                )

    def formulate_challenge(self, n=10):
        self.challenge = OrderedDict()
        while n > 0:
            new_core = random.choice(list(self.coremap.keys()))
            if new_core not in list(self.challenge.keys()):
                self.challenge[new_core] = None
                n -= 1

    def claim(self, answer):
        key = answer[3:6]
        if (
            answer in self.coremap[key]
            and key in list(self.challenge.keys())
        ):
            self.challenge[key] = answer
            return True
        else:
            return False


monger = Wordmonger(all_words, coremap)
