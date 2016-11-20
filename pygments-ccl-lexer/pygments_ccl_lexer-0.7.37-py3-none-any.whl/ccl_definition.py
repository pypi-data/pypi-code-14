from pygments.token import Keyword, Name, Operator, Text, Comment, Number, String, Punctuation, Token

from .functions import FUNCTIONS, DATATYPES, KEYWORDS, PSEUDO_TYPES, NAMESPACE, OPERATOR_WORDS

TOKEN_ASSIGNMENTS = {
    'keywords': Keyword,
    'datatypes': Keyword.Types,
    'operator_words': Operator.Word,
    'functions': Token.Name,
    'namespace': Keyword.Namespace,
    'pseudo_types': Keyword.Pseudo
}

_keywords = KEYWORDS
_functions = FUNCTIONS
_datatypes = DATATYPES
_operator_words = OPERATOR_WORDS
_namespace = NAMESPACE
_pseudo_types = PSEUDO_TYPES


def create_dictionary(t):
    ccl_tokens = {}
    for k, v in t:
        if "__" not in k:
            if k[0] == '_':
                ccl_tokens[k[1:]] = [word.replace(' ', '\s') for word in v]
    return ccl_tokens

tokens = locals().items()
CCL_TOKENS = create_dictionary(tokens)
