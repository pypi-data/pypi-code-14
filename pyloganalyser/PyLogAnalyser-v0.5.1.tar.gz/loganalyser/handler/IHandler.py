#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Interface for Handler definition
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""


class IHandler(object):
    """
    Interface class Handler.
    """
    def __init__(self):
        """
        """
        pass
    
    def open(self):
        """
        """
        pass
    
    def close(self):
        """
        """
        pass

    def append(self, log_line):
        """
        """
        pass
        #Could include raise the exception.

