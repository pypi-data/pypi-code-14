import re

from markio.constants import PROGRAMMING_LANGUAGES_CODES


def indent(lines, indent):
    """
    Indent content with the given content level or content string.
    """

    indent = ' ' * indent if isinstance(indent, int) else indent
    return '\n'.join(indent + line for line in lines.splitlines())


def normalize_i18n(x):
    """
    Normalize accepted lang codes to ISO format.

    Also check if language codes are valid.
    """

    if x is None:
        return None
    return x.replace('-', '_')


def normalize_computer_language(x):
    """Normalize accepted computer language strings."""

    x = x.lower()
    return PROGRAMMING_LANGUAGES_CODES.get(x, x)


country_code_re = re.compile(
    r'^\w*(?P<i18n>([a-zA-Z][a-zA-Z])((?:-|_)(:?[a-zA-Z][a-zA-Z]))?)\w*$')
parenthesis_re = re.compile(r'.*[(](.*)[)]\w*')