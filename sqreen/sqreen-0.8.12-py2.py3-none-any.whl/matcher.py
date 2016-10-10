# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Matcher module
"""

import re
from operator import eq
from functools import partial

from .utils import is_unicode


MATCHERS = {
    'anywhere': lambda pattern, value: pattern in value,
    'starts_with': lambda pattern, value: value.startswith(pattern),
    'ends_with': lambda pattern, value: value.endswith(pattern),
    'equals': eq
}


class Matcher(object):
    """ Fast regex-like matcher
    """

    def __init__(self, patterns):
        self.insensitives_string_patterns = []
        self.sensitives_string_patterns = []
        self.regex_patterns = []

        self._prepare(patterns)

    def _prepare(self, patterns):
        """ Prepare all the patterns
        """
        for pattern in patterns:

            pattern_type = pattern['type']
            value = pattern['value']
            case_sensitive = pattern.get('case_sensitive', False)

            if pattern_type == 'string':
                pattern_options = pattern.get('options')

                # Get the match function name, defaulting to anywhere
                if not pattern_options:
                    match_name = 'anywhere'
                else:
                    match_name = pattern_options[0]

                if match_name not in MATCHERS.keys():
                    raise ValueError('Unknown match function {}'.format(match_name))

                # Lower the value in case of case insensitive match or
                # for not lower case pattern, it would never match
                if case_sensitive is False:
                    value = value.lower()

                match = partial(MATCHERS[match_name], value)

                if case_sensitive is False:
                    self.insensitives_string_patterns.append(match)
                else:
                    self.sensitives_string_patterns.append(match)

            elif pattern_type == 'regexp':
                if case_sensitive:
                    flags = 0
                else:
                    flags = re.IGNORECASE

                if 'multiline' in pattern.get('options', []):
                    flags = re.MULTILINE | flags

                self.regex_patterns.append(re.compile(value, flags))
            else:
                raise ValueError('Unknown pattern type %s', pattern_type)

    def match(self, value):
        """ Check if string value match one of the string or regex pattern the fastest
        way possible. Accept python 2 str, unicode and python 3 bytes and str.
        """

        # Correct encoding if possible and needed
        if not is_unicode(value):
            value = value.decode('utf-8', errors='replace')

        # Match case sensitive values
        for string_match in self.sensitives_string_patterns:
            if string_match(value):
                return True

        insensitive_value = value.lower()

        # Match case insensitive values
        for string_match in self.insensitives_string_patterns:
            if string_match(insensitive_value):
                return True

        # Match regexes
        for pattern_regex in self.regex_patterns:
            if pattern_regex.search(value) is not None:
                return True

        return False
