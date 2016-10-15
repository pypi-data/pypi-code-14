#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Singleton module
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""


class Singleton:
    """
    Implementation of singleton
    """
    _instance = None

    def __init__(self, single_class):
        """
        Singleton constructor
        """
        self._singleton = single_class

    def get_instance(self):
        """
        Get the instance of the singleton
        """
        if self._instance is None:
            self._instance = self._singleton()

        return self._instance

    def __call__(self):
        """
        Prevention function in case that get_instance is not used.
        """
        raise TypeError('Use get_instance() to get the instance of the singleton.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._singleton)
