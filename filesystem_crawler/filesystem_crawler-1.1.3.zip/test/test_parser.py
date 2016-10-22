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
from filesystem_crawler import parse_match_rules
from filesystem_crawler import parse_match_rules_from_file

class ParserTest(unittest.TestCase):

    def setUp(self):
        self.fileRulesName = 'match_rules'

        self.rawMatchRules = '''
            #test rules

            /*match*
            i/*doesnt*
        '''

        with open(self.fileRulesName, 'w') as f:
            f.write(self.rawMatchRules)

    def test_parse_match_rules(self):
        basedirPath = 'x:\\root'

        expectedRules = []
        expectedRules.append(MatchRule(r'x\:\\root\\[^\\]*match[^\\]*$'))
        expectedRules.append(MatchRule(r'x\:\\root\\[^\\]*doesnt[^\\]*$', polarity=False))


        actualRules, actualErrors = parse_match_rules(basedirPath, self.rawMatchRules)

        self.assertEqual(len(actualErrors), 0)

        self.assertEqual(len(expectedRules), len(actualRules))

        actualRulesPatterns = [str(p.pattern) for p in actualRules]

        for expectedRule in expectedRules:
            self.assertTrue(str(expectedRule.pattern) in actualRulesPatterns)

    def test_parse_match_rules(self):
        basedirPath = 'x:\\root'

        expectedRules = []
        expectedRules.append(MatchRule(r'x\:\\root\\[^\\]*match[^\\]*$'))
        expectedRules.append(MatchRule(r'x\:\\root\\[^\\]*doesnt[^\\]*$', polarity=False))


        actualRules, actualErrors = parse_match_rules_from_file(basedirPath, self.fileRulesName)

        self.assertEqual(len(actualErrors), 0)

        self.assertEqual(len(expectedRules), len(actualRules))

        actualRulesPatterns = [str(p.pattern) for p in actualRules]

        for expectedRule in expectedRules:
            self.assertTrue(str(expectedRule.pattern) in actualRulesPatterns)


