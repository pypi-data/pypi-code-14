# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import re

# Each regex must contain a named group "secret" that
# marks the substring to be censored.
DEFAULT_PATTERNS = (
    r'_KEY="(?P<secret>[^\s"]+)"',
    r'_KEY=(?P<secret>[^\s"]+)',

    r'_TOKEN=(?P<secret>[^\s"]+)',
    r'_TOKEN="(?P<secret>[^\s"]+)"',

    # HTTP authorization headers
    r'"authorization": "[^\s"]+? (?P<secret>[^\s"]+?)"',

    # URL passwords
    r'(?:[a-z0-9]+?:)?//[^\s:]+?:(?P<secret>[^@]+?)@',
)


class CensorSensitiveDataProcessor(object):
    """
    Attempt to prevent sensitive data from spilling into the logs by
    "censoring". The basic idea is that we have a couple of regular
    expressions that filter log messages containing passwords and API keys
    to replace them with asterisks.
    """
    def __init__(self, patterns=DEFAULT_PATTERNS, disabled=False):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.disabled = disabled

    def censor(self, secret, keep_chars=2, replacement_char='*'):
        """
        'foobar' -> 'fo****'
        """
        return (secret[:keep_chars] +
                replacement_char * (len(secret) - keep_chars))

    def sanitize_match(self, match):
        original = match.group()

        try:
            secret = match.group('secret')
            return original.replace(secret, self.censor(secret))
        except IndexError:
            return original

    def __call__(self, logger, method_name, log_str):
        if self.disabled:
            return log_str

        for regex in self.patterns:
            log_str = regex.sub(self.sanitize_match, log_str)
        return log_str
