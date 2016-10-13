# -*- coding: utf-8 -*-

from logging import getLogger
from logging import StreamHandler
from logging import WARNING

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(WARNING)
logger.setLevel(WARNING)
logger.addHandler(handler)


class Rhymer:

    def __init__(self):
        self.point = 0

    @classmethod
    def is_rhymed(cls, first_pron, second_pron):
        """
        入力として読みを受け，
        末尾1字以上が一致していれば韻を踏んでいるとする．

        Args:
          first_pron: 一つ目の読み
          second_pron: 二つ目の読み
        """
        if first_pron == second_pron:
            return True
        else:
            return False

    def evaluate(self, first_pron, second_pron):
        """
        一致している字数をポイントとして評価する
        """
        self.point = 0

        for fp, sp in zip(first_pron[::-1], second_pron[::-1]):
            logger.debug("fp: " + fp + ", " + "sp: " + sp)
            if fp == sp:
                self.point += 1
            else:
                break
        return self.point
