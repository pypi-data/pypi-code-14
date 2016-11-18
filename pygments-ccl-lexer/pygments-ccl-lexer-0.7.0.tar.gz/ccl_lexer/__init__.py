from pygments.lexers.sql import PostgresLexer
from pygments.token import Keyword, Name, Operator

__all__ = ['CCL_Lexer']


CCL_KEYWORDS = ['select', 'from', 'where', 'with', 'order by']
CCL_OPERATOR_WORDS = ['in', 'between', 'and', 'or', 'distinct']
CCL_FUNCTIONS = ['substring', 'piece','cnvtint','cnvtdatetime', 'uar_get_code_display']
CCL_CONSTANTS = ['curdate']
class CCL_Lexer(PostgresLexer):
    name = 'CCL'
    aliases = ['ccl', 'prg']
    filenames = ['*.ccl']

    def get_tokens_unprocessed(self, text):
        extra_content = [
            (CCL_FUNCTIONS, Name.Function),
            (CCL_KEYWORDS, Keyword),
            (CCL_OPERATOR_WORDS, Operator.Word),
            (CCL_CONSTANTS, Name.Constant)
        ]

        for index, token, value in self.get_tokens_unprocessed(text):
            if token is Name:
                for i in extra_content:
                    if value in i[0]:
                        yield index, i[1], value
                        break;
                else:
                    yield index, token, value
            else:
                yield index, token, value

