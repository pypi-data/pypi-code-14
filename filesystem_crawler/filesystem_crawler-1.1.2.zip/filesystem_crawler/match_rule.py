#!/usr/bin/python3.3
"""
TODO
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

import re


class MatchRule:

    def __init__(self, pattern, polarity=True,
                 dirsOnly=False, filesOnly=False, contentPattern=None):
        self.pattern = re.compile(pattern)
        self.polarity = polarity
        self.dirsOnly = dirsOnly
        self.filesOnly = filesOnly
        self.contentPattern = re.compile(contentPattern) if contentPattern else None
        if dirsOnly and filesOnly:
            raise Exception("Cannot exclusively include directories and files"
                            " at the same time.")

    def isMatch(self, dirname, isFile):
        typeMatches = (not self.dirsOnly and (isFile or not self.filesOnly)
                       or self.dirsOnly and not isFile)
        dirMatches = self.pattern.match(dirname) is not None

        contentMatches = self.contentMatches(dirname) if self.contentPattern and isFile and dirMatches and typeMatches else False

        return dirMatches and typeMatches and (not self.contentPattern  or self.contentPattern and contentMatches), self.polarity

    def contentMatches(self, dirname):
        try:
            with open(dirname, 'r') as textfile:
                for line in textfile:
                    if self.contentPattern.search(line) is not None:
                        return True
        except:  # not a text file
            pass
        return False
