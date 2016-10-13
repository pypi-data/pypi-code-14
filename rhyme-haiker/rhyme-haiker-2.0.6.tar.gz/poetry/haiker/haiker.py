# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import WARNING
import random

from poetry.data_constructor.words_data import WordsData
from poetry.rhymer.rhymer import Rhymer

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(WARNING)
logger.setLevel(WARNING)
logger.addHandler(handler)


class Haiker:

    def compose(self):
        """
        俳句を詠む．
        """
        first_loop_limit = 10
        first_current_loop = 0
        while True:
            if first_current_loop == first_loop_limit:
                return "***** だめでした *****"

            rhyming_num = random.choice([1, 2, 3])
            logger.debug('韻: {}'.format(rhyming_num))

            # get 5
            try:
                first_sentence = self._get_n_char_sentence(5)
            except IndexError:
                first_current_loop += 1
                continue
            first_words = WordsData.get_words(first_sentence)
            logger.debug("5: {}".format(first_words))
            # get 7
            try:
                second_sentence = self._get_n_char_sentence(7)
            except IndexError:
                first_current_loop += 1
                continue
            second_words = WordsData.get_words(second_sentence)
            second_last_vowel = WordsData.get_n_char_vowel(second_sentence, rhyming_num)
            logger.debug("7: {}".format(second_words))
            logger.debug(second_last_vowel)
            # get 5 and rhyming
            second_loop_limit = 500
            second_current_loop = 0
            while True:
                second_current_loop += 1
                if second_current_loop == second_loop_limit:
                    break

                try:
                    third_sentence = self._get_n_char_sentence(5)
                except IndexError:
                    logger.debug('*** pop from empty list ***')
                    logger.info('*** やりなおし ***')
                    second_current_loop += 1
                    break
                third_last_vowel = WordsData.get_n_char_vowel(third_sentence, rhyming_num)
                if Rhymer.is_rhymed(second_last_vowel, third_last_vowel):
                    third_words = WordsData.get_words(third_sentence)
                    haiku = ' '.join([first_words, second_words, third_words])
                    logger.debug("5*: {}".format(third_words))
                    logger.debug(third_last_vowel)
                    return haiku
            first_current_loop += 1
            if first_current_loop == first_loop_limit:
                return "***** だめでした *****"

    def _get_n_char_sentence(self, n):
        """
        n 文字の文章を取得
        """
        if n == 5:
            random.shuffle(WordsData.words_five_list)
            try:
                return WordsData.words_five_list.pop()
            except IndexError:
                raise
        elif n == 7:
            random.shuffle(WordsData.words_seven_list)
            try:
                return WordsData.words_seven_list.pop()
            except IndexError:
                raise
        else:
            logger.info('*** Invalid number: {} ***'.format(n))
            raise ValueError
