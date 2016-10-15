#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Document class used in PyLogAnalyser.py module to store the log lines and the handlers
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""


class Document(object):

    def __init__(self):
        """
        """
        self.__log_lines = list([])
        self.__handlers = list([])
        self.__handler_init = list([])
        pass

    def append(self, log_line):
        """
        """
        #handler-dependent
        handlers = self.__handlers
        for handler in handlers:
            handler.append(log_line)

    def open(self):
        """
        """
        #handler-dependent
        pass

    def close(self):
        """
        """
        #handler-dependent
        handlers = self.__handlers
        for handler in handlers:
            handler.close()

    def add_handler(self, handler):
        """
        """
        self.__handlers.append(handler)
        #Check that not appended twice?

    def delete_handler(self, hanlder):
        """
        """
        pass
