#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Stdout handler for obtaining stdout log output
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import platform
from IHandler import IHandler
import re

if platform.system() == 'Windows':
    from StdoutHandlerWindows import StdoutHandlerWindows as StdoutHandlerUsed
elif (platform.system() == 'Linux') or \
    bool(re.search('CYGWIN', platform.system())):
    #
    from StdoutHandlerLinux import StdoutHandlerLinux as StdoutHandlerUsed
else:
    raise Exception("Platform not recognised.")

class StdoutHandler(IHandler):
    """
    Stdout handler class for obtaining stdout log output.
    """

    def __init__(self):
        """
        """
        self.__handler = StdoutHandlerUsed()

    def open(self):
        """
        """
        self.__handler.open()

    def close(self):
        """
        """
        self.__handler.close()

    def append(self, log_line):
        """
        """
        self.__handler.append(log_line)
        #Could include raise the exception.

