from pygments.lexers.sql import PostgresLexer, language_callback
from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation
# from pygments.lexers._postgres_builtins import KEYWORDS, DATATYPES, \
# PSEUDO_TYPES, PLPGSQL_KEYWORDS
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


class CCL_Lexer(PostgresLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'(' + '|'.join([s.replace(" ", "\s+")
                              for s in DATATYPES + PSEUDO_TYPES])
             + r')\b', Name.Builtin),
            (r'(' + '|'.join(KEYWORDS) + r')\b', Keyword),
            (r'[+*/<>=~!@#%^&|`?-]+', Operator),
            (r'::', Operator),  # cast
            (r'\$\d+', Name.Variable),
            (r'([0-9]*\.[0-9]*|[0-9]+)(e[+-]?[0-9]+)?', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r"(E|U&)?'(''|[^'])*'", String.Single),
            (r'(U&)?"(""|[^"])*"', String.Name),  # quoted identifier
            (r'(?s)(\$[^\$]*\$)(.*?)(\1)', language_callback),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),

            # psql variable in SQL
            (r""":(['"]?)[a-z][a-z0-9_]*\b\1""", Name.Variable),

            (r'[;:()\[\]\{\},\.]', Punctuation),
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/\*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ],
    }
