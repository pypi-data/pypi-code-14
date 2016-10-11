# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import DEBUG
import pickle

import poetry

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class DataExporter:

    OUTPUT_DIR = poetry.__path__[0] + '/../output/'
    WORDS_FIVE_FILE_NAME = "words_five.pickle"
    WORDS_SEVEN_FILE_NAME = "words_seven.pickle"

    def __init__(self, words_five_data, words_seven_data):
        self.words_five_data = words_five_data
        self.words_seven_data = words_seven_data

    def export_pickle(self):
        """
        Pickle で保存．
        """
        self._export(pickle.dumps(self.words_five_data),
                     pickle.dumps(self.words_seven_data))

    def _export(self, words_five_data, words_seven_data):
        with open(self.OUTPUT_DIR + DataExporter.WORDS_FIVE_FILE_NAME, mode='wb') as f:
            f.write(words_five_data)
        with open(self.OUTPUT_DIR + DataExporter.WORDS_SEVEN_FILE_NAME, mode='wb') as f:
            f.write(words_seven_data)
