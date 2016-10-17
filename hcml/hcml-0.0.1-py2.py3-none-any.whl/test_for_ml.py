#!/usr/bin/env python
# coding=utf-8

import unittest
from meaningless import Meaningless

class MeaninglessTestCase(unittest.TestCase):
    """
    test for Hachi meaningless
    """

    def test_predict(self):
        m = Meaningless()
        msg = u'短句子'
        self.assertEqual(m.predict(msg), False)
        msg = u'这里没有敏感词 这里没有敏感词 这里没有敏感词 这里没有敏感词'
        self.assertEqual(m.predict(msg), True)
        msg = u'这么长的句子都不加一个标点符号你确定真的好意思吗'
        self.assertEqual(m.predict(msg), True)


if __name__ == "__main__":
    unittest.main()
