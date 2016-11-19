from pygments.lexers.sql import language_callback
from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation, Token
# from pygments.lexers._postgres_builtins import KEYWORDS, DATATYPES, \
# PSEUDO_TYPES, PLPGSQL_KEYWORDS
from pygments.lexer import RegexLexer
from ccl_definition import *


__all__ = ['CCL_Lexer']


CCL_KEYWORDS = ['select', 'from', 'where', 'with', 'order by']
CCL_OPERATOR_WORDS = ['in', 'between', 'and', 'or', 'distinct']
CCL_FUNCTIONS = [
    'substring',
    'piece',
    'cnvtint',
    'cnvtdatetime',
    'uar_get_code_display']
CCL_CONSTANTS = ['curdate']


def make_case_insensitive(words):
    _words = words
    # for word in words:
    # _words.append(word.lower())
    return _words


def add_words(words, type):
    regex = r'(' + '|'.join(words) + r')\b'
    return (regex, type)


class CCL_Lexer(RegexLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r';.*?\n', Comment.Single),
            # (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\$[a-zA-Z0-9_]*\b', Name),
            add_words(KEYWORDS, Keyword),
            add_words(DATATYPES, Keyword.Types),
            add_words(OPERATOR_WORDS, Operator.Word),
            add_words(NAMESPACE, Keyword.Namespace),

            (r'[+*/<>=~!@#%^&|`?-]', Operator),
            (r'[0-9]+', Number.Integer),
            # TODO: Backslash escapes?
            (r"'(''|[^'])*'", String.Single),
            # not a real string literal in ANSI SQL
            (r'"(""|[^"])*"', String.Symbol),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Text),
            (r'[;:()\[\],\.]', Punctuation),

        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/\*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ],
    }


print("B4".lower())
