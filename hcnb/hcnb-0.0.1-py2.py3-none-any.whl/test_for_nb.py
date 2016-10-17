#!/usr/bin/env python
# coding=utf-8

import unittest
from bayes import NaiveBayes

class NaiveBayesTestCase(unittest.TestCase):
    """
    test for Hachi naive bayes
    """

    def test_predict(self):
        nb = NaiveBayes()
        msg = u'Lisp才是最好的语言'
        self.assertEqual(nb.predict(msg), True)
        msg = u'文本编辑器是啥子东西'
        self.assertEqual(nb.predict(msg), False)

if __name__ == "__main__":
    unittest.main()
