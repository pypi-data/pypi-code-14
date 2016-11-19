from pygments.lexers.sql import language_callback
from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation, Token
# from pygments.lexers._postgres_builtins import KEYWORDS, DATATYPES, \
# PSEUDO_TYPES, PLPGSQL_KEYWORDS
from pygments.lexer import RegexLexer
from ccl_definition import TOKEN_ASSIGNMENTS, CCL_TOKENS


__all__ = ['CCL_Lexer']


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

    root = [
        (r'\s+', Text),
        (r';.*?\n', Comment.Single),
        (r'/\*', Comment.Multiline, 'multiline-comments'),
        (r'\$[a-zA-Z0-9_]*\b', Name),
    ]

    for _type, words in CCL_TOKENS.items():
        root.append(add_words(words, TOKEN_ASSIGNMENTS[_type]))
    root += [
        (r'[+*/<>=~!@#%^&|`?-]', Operator),
        (r'[0-9]+', Number.Integer),
        # TODO: Backslash escapes?
        (r"'(''|[^'])*'", String.Single),
        # not a real string literal in ANSI SQL
        (r'"(""|[^"])*"', String.Symbol),
        (r'[a-zA-Z_][a-zA-Z0-9_]*', Text),
        (r'[;:()\[\],\.]', Punctuation),
    ]

    tokens = {
        'root': root,
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/\*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ],
    }


print("B4".lower())
