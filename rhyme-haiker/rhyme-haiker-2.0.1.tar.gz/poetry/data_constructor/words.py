# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Words(object):

    WORD = 'word'
    VOWEL = 'vowel'
    LENGTH = 'length'
    PART = 'part'
    words = None

    def __init__(self, word_dict):
        self.word = word_dict[self.WORD]
        self.vowel = word_dict[self.VOWEL]
        self.length = word_dict[self.LENGTH]
        self.part = word_dict[self.PART]

    # @classmethod
    # def tuple2words(cls, words_tuple):
    #     """
    #     文字列タプルから Words クラスタプルを作成．
    #     """
    #     if words_tuple is None:
    #         return words_tuple
    #     else:
    #         return (cls._dispatch(word) for word in words_tuple)

    # @classmethod
    # def _dispatch(cls, word):
    #     """
    #     Words クラスオブジェクトの場合，そのまま返す．
    #     そうでない場合，Words クラスオブジェクトを返す．
    #     """
    #     if isinstance(word, Words):
    #         return word
    #     else:
    #         return cls._search_dict(word)

    # def _search_dict(cls, word):
    #     """
    #     単語をもとに，対応する辞書を検索．
    #     """
    #     for word_dict in self.words:
    #         if word_dict.word == word:
    #             return word_dict
    #     return None
