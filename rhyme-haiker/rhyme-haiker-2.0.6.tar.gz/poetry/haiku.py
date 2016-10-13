# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import INFO

import poetry
from poetry.haiker.haiker import Haiker
from poetry.utils.data_reader import DataReader
from poetry.data_constructor.words_data import WordsData

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


class Haiku(object):

    """
    Example usage:

    >>> from poetry.haiku import Haiku
    >>> Haiku.compose()
    """

    OUTPUT_DIR = poetry.__path__[0] + '/output/'
    WORDS_FIVE_FILE_NAME = 'words_five.pickle'
    WORDS_SEVEN_FILE_NAME = 'words_seven.pickle'

    @classmethod
    def compose(cls):
        logger.info("Compose")

        WordsData.words_five_list = DataReader.read_pickled_file(cls.OUTPUT_DIR + cls.WORDS_FIVE_FILE_NAME)
        WordsData.words_seven_list = DataReader.read_pickled_file(cls.OUTPUT_DIR + cls.WORDS_SEVEN_FILE_NAME)

        haiker = Haiker()
        haiku = haiker.compose()

        logger.info(haiku)
        return haiku
