# -*- coding: utf-8 -*-
"""
    pygments.lexers.bohrium
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for Bohrium.
"""

import re

from pygments.lexer import RegexLexer
from pygments.token import *

class BohriumLexer(RegexLexer):
    name = 'Bohrium'
    aliases = ['bohrium']
    filenames = ['*.bh']
    flags = re.IGNORECASE

    tokens = {
        'root': [
            (r'\n|\s+', Text),

            (r'#(.*)', Comment.Single),
            (r'\.+', Comment.Special),

            (r'\d+', Number.Integer),

            (r'[\[\](){};,/?:\\]', Punctuation),

            (r'a\d+=?\[', Name.Variable),
            (r'a\d+=?\b', Name.Variable),

            (r'BH_.*?\b', Keyword.Operator)
        ]
    }
