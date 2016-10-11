# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class WordsData(list):

    VOWEL = 'vowel'
    WORD = 'word'
    EMPTY = ''

    """
    単語の情報を網羅したデータクラス．

    - words_N_list: N 文字からなる sentence のリスト
    - sentence: 文章のデータ構造
    """
    words_five_list = list()
    words_seven_list = list()

    @classmethod
    def get_n_char_vowel(cls, sentence, n):
        """
        文章の読みの末尾 n 文字を返す
        """
        vowel = cls._get_vowel(sentence)
        return vowel[-n:]

    @classmethod
    def _get_vowel(cls, sentence):
        """
        文章の読みを返す
        """
        vowel_list = [word[cls.VOWEL] for word in sentence]
        return ''.join(vowel_list)

    @classmethod
    def get_words(cls, sentence):
        """
        文章データから，文章の文字列のみを返す
        """
        word_list = [word[cls.WORD] for word in sentence]
        return ''.join(word_list)
