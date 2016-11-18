from pygments.lexers.sql import SqlLexer
from pygments.token import Keyword, Name

__all__ = ['CCL_Lexer']


CCL_KEYWORDS = ['select', 'from', 'where', 'with', 'order by']
CCL_BUILTINS = ['in', 'between', 'and', 'or', 'distinct']
class CCL_Lexer(SqlLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']

    def get_tokens_unprocessed(self, text):
        extra_content = [(CCL_KEYWORDS, Keyword),
                         (CCL_BUILTINS, Name.Builtin)]

        for index, token, value in SqlLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                for i in extra_content:
                    if value in i[0]:
                        yield index, i[1], value
                        break;
                else:
                    yield index, token, value
            else:
                yield index, token, value

