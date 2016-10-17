#!/usr/bin/env python
# coding=utf-8

import unittest

from contact import Contact

class ContactTestCase(unittest.TestCase):
    """
    test for Hachi_contact
    """

    def test_predict(self):
        ctt = Contact()
        msg = u'给你一个网址\
                https://123456789?tel=15512345678?wechat=weixin1234。\
                再来个邮箱什么的abc123[at]email.com，留个QQ:123456，\
                午起罢溜司儿。都开始用微信了weiwei_xinxin。找不到就打电话\
                400-800-8888'
        self.assertEqual(ctt.predict(msg), True)

if __name__ == '__main__':
    unittest.main()
