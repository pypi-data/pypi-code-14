#!/usr/bin/python3
"""
MatrixParser tests
"""
__author__ = 'heliosantos99@gmail.com (Helio Santos)'

import unittest
import os

from .context import filesystem_crawler
from filesystem_crawler import FilesystemCrawler
from filesystem_crawler import MatchRule

class FilesystemCrawlerTest(unittest.TestCase):

    def test_match_root_files(self):
        basedirPath = 'root'
        
        matchrules = []
        matchrules.append(MatchRule(r'root\\[^\\]*match[^\\]*$'))
        matchrules.append(MatchRule(r'root\\[^\\]*doesnt[^\\]*$', polarity=False))

        crawler = FilesystemCrawler(matchrules)
        matchedPaths = crawler.search(basedirPath, True)
        self.assertEqual(len(matchedPaths), 1)
        self.assertEqual(matchedPaths[0][0], 'root\\match.txt')

    def test_match_all_levels(self):
        basedirPath = 'root'
        
        matchrules = []
        matchrules.append(MatchRule(r'root\\.*match[^\\]*$'))
        matchrules.append(MatchRule(r'root\\.*doesnt[^\\]*$', polarity=False))

        crawler = FilesystemCrawler(matchrules)
        matchedPaths = crawler.search(basedirPath, True)
        self.assertEqual(len(matchedPaths), 6)
        for matchedPath in matchedPaths:
            self.assertTrue('\\match.txt' in matchedPath[0])


    def test_match_files_with_content(self):
        basedirPath = 'root'
        
        matchrules = []
        matchrules.append(MatchRule(r'root\\[^\\]*$', contentPattern='matching text'))

        crawler = FilesystemCrawler(matchrules)
        matchedPaths = crawler.search(basedirPath, True)

        self.assertEqual(len(matchedPaths), 1)
        self.assertEqual(matchedPaths[0][0], 'root\\valid content.txt')


    def test_match_root_files(self):
        basedirPath = 'root'
        
        matchrules = []
        matchrules.append(MatchRule(r'root\\[^\\]*match[^\\]*$'))
        matchrules.append(MatchRule(r'root\\[^\\]*doesnt[^\\]*$', polarity=False))

        matchedCallbacks = []
        def matchCallback(match):
            matchedCallbacks.append(match[0])
        crawler = FilesystemCrawler(matchrules, matchCallback=matchCallback)
        matchedPaths = crawler.search(basedirPath, True)
        self.assertEqual(len(matchedPaths), len(matchedCallbacks))
        self.assertEqual(matchedCallbacks[0], 'root\\match.txt')
