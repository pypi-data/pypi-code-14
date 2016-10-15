#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
from IHandler import IHandler

class TxtHandler(IHandler):
    """
    """

    def __init__(self, filename):
        """
        """
        self.__ori_filename = filename
        self.__filename = os.path.abspath(filename)
        self.__filedesc = file(self.__filename, 'w')

    def open(self):
        """
        """
        pass

    def close(self):
        """
        """
        self.__filedesc.close()

    def append(self, log_line):
        """
        """
        log_line_str = log_line.get_string().strip()
        self.__filedesc.write(log_line_str + "\n")
