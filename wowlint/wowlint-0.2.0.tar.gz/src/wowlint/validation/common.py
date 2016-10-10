# -*- coding: utf-8 -*-
from enchant.checker import SpellChecker
import enchant

from wowlint.validation.core import LinewiseLint, Severity


def unSmartQuote(sillyString):
    return sillyString.\
        replace(u"’", "'").\
        replace(u"‘", "'").\
        replace(u"“", '"').\
        replace(u"”", '"')


class SpellCheck(LinewiseLint):
    message = u"({block}:{line}) Word is incorrectly spelt: '{word}'"
    severity = Severity.WARNING

    def __init__(self, config={}):
        LinewiseLint.__init__(self, config=config)
        self.checker = SpellChecker(enchant.DictWithPWL(config.get('lang', 'en_GB'), 'custom.dict'))

    def validate_line(self, blockIndex, lineIndex, line):
        issues = []
        self.checker.set_text(unSmartQuote(line.text))
        for err in self.checker:
            issues.append(self.create_issue(blockIndex, lineIndex, word=err.word))
        return issues


class LineTooLong(LinewiseLint):
    message = "({block}:{line}) Line too long ({len} characters)"
    severity = Severity.WARNING

    def __init__(self, config={}):
        LinewiseLint.__init__(self, config=config)
        self.LINE_LENGTH_LIMIT = config.get('max_length', 200)

    def validate_line(self, blockIndex, lineIndex, line):
        lineLength = len(line.text)
        if lineLength > self.LINE_LENGTH_LIMIT:
            return [self.create_issue(blockIndex, lineIndex, len=lineLength)]


LINT_CLASSES = [
    LineTooLong,
    SpellCheck
]
