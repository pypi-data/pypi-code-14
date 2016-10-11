# -*- coding: utf-8 -*-

import logging
import pickle

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class DataReader:

    @classmethod
    def read_file(cls, addr):
        """
        学習用データ読み込み
        """
        with open(addr) as f:
            return f.read()

    @classmethod
    def read_pickled_file(cls, addr):
        """
        pickle 化したデータの読み込み
        """
        with open(addr, 'rb') as f:
            return pickle.load(f)
