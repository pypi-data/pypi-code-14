#!/usr/bin/env python
# coding=utf-8

from cnprep import Extractor
from Hachi_filter import HachiFilter

class Contact(HachiFilter):
    """
    Detect contact information.
    """
    def __init__(self, args=[]):
        self.filter = Extractor(args=args, limit=6)

    def predict(self, message, level=0):
        contact = self.filter.extract(message)
        for item in contact.values():
            if item != []:
                return True
        return False
