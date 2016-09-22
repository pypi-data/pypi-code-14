#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
File Name: test_cli.py
Author: shalk 
Mail: shalk@qq.com
Created Time: 2016-09-18 10:58:05
Description:  测试cli模块
"""

from updatesystem import cli
import unittest

class TestCliMethods(unittest.TestCase):
    """TestCliMethods
    测试 cli模块的方法
    """
    @classmethod
    def setUpClass(cls):
        cls.parser = cli.get_parser()

    def get_args(self,args):
        self.args_dict = cli.get_args_config(self.parser,args)


    def test_parser_without_option(self):
        args_input = []
        with self.assertRaises(SystemExit)as cm:
            cli.get_args_config(self.parser,args_input)
            self.assertEqual(cm.exception.code,2)

    def test_parser_with_check_option(self):
        args_input = [ "check" ,  ]
        self.get_args(args_input)
        self.assertTrue(self.args_dict['check'])
        self.assertEqual(self.args_dict['check_time'],"after")

        args_input = [ "check" , "--before" ]
        self.get_args(args_input)
        self.assertTrue(self.args_dict['check'])
        self.assertEqual(self.args_dict['check_time'],"before")
        

        args_input = [ "check" , "--after" ]
        self.get_args(args_input)
        self.assertTrue(self.args_dict['check'])
        self.assertEqual(self.args_dict['check_time'],"after")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCliMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
