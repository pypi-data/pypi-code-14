import collections

from markio.utils import markdown


class MarkdownString(collections.UserString):
    """
    A regular markdown string that has a .html() attribute that converts it to
    HTML.
    """

    def html(self):
        """
        Return a HTML representation of string.
        """

        return markdown(str(self))
