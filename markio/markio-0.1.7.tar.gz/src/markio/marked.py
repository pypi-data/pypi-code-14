import collections
import re
import sys

from markio.errors import MarkioSyntaxError
from markio.util import indent


def parse_marked(src, **kwargs):
    """
    Parse a Marked source code and return the parsed AST.

    Args:
        src (str or file):
            Marked source code.

    This function assumes the document has the following structure:

        Title
        =====

            # An indented YAML source with meta information
            meta1: value
            meta2: value

        Short description paragraph.

        Or maybe two paragraphs ;-)


        Subsection 1
        ------------

        Subsection data. We won't complain if you use invalid markdown source
        here.


        Subsection 2
        ------------

        You can use how many sections you like.

    The resulting :class:`Marked` object is a linear structure with ``title``,
    ``meta``, ``short_description``, and ``sections`` attributes. Sections is a
    sequence of (title, data) pairs.
    """

    parser = MarkedParser(src, **kwargs)
    return parser.parse()


class Marked(collections.Sequence):
    """
    Represents generic markio-like data.
    """

    def __init__(self, title, meta=None, short_description='', sections=None):
        self.title = title
        self.meta = meta
        self.short_description = short_description
        self.sections = list(sections or [])

    def __len__(self):
        return 4

    def __iter__(self):
        yield self.title
        yield self.meta
        yield self.short_description
        yield self.sections

    def __getitem__(self, idx):
        return list(self)[idx]

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)

    def source(self):
        """
        Renders generic markio source.
        """

        # Add title
        lines = [self.title, '=' * len(self.title), '']

        # Add meta
        if self.meta:
            lines.append(indent(self.meta, 4))
            lines.append('')

        # Add short description
        if self.short_description:
            lines.append(self.short_description)
            lines.append('')

        for title, data in self.sections:
            lines.extend(['', title, '-' * len(title), '', data, ''])

        return '\n'.join(lines)


class MarkedParser:
    """
    Generic parser for Markio-like documents.

    Prefer to use the :func:`parse` function instead of manually instantiating
    this class.
    """

    TITLE_RE = re.compile(r'^')
    WHITESPACE_RE = re.compile(r'^\s*')
    LINE_RE = re.compile(r'-*')

    def __init__(self, source):
        self.lineno = 0
        self.source = source
        self.stream = list(enumerate(self.source.splitlines(), 1))
        self.stream.reverse()
        self.parsed = Marked(title='')

    def __bool__(self):
        return bool(self.stream)

    def pop(self):
        """
        Pop next (lineno, line) on stream.

        Return None if no line is available.
        """

        try:
            pair = self.stream.pop()
            self.lineno = pair[0]
            return pair
        except ValueError:
            pass

    def push(self, *args):
        """
        Accept either .push(lineno, line) or .push(line).

        Insert line back to the stream.
        """

        if len(args) == 2:
            self.stream.append(args)
        else:
            line, = args
            self.stream.append((self.lineno, line))

    def skip_blank(self):
        """
        Skip all blank lines.
        """

        lineno, line = 0, ''
        while not line.strip():
            item = self.pop()
            if item is None:
                return
            lineno, line = item
        self.push(lineno, line)

    def read_indented(self):
        """
        Read all indented lines and return a pair of (level, content) with the
        string contents with indentation removed and the indentation level.
        """

        lines = []

        # Separate lines starting with spaces
        while self:
            lineno, line = self.pop()
            if (not line) or line[0] in ' \t':
                lines.append(line)
            else:
                self.push(lineno, line)
                break

        # Return empty content
        if not lines:
            return 0, ''

        # Remove trailing empty lines
        while lines:
            if not lines[-1].strip():
                lines.pop()
            else:
                break

        # Create content string and determine indentation level
        re = self.WHITESPACE_RE
        level = sys.maxsize
        get_level = lambda x: re.match(x).end()
        stripped = lambda line: line[level:] if line.strip() else ''
        level = min(get_level(line) for line in lines if line.strip())
        content = '\n'.join(map(stripped, lines))
        return level, content

    def read_before_title(self, prefix):
        """
        Consumes content until a title is reached.

        Return the content string.
        """

        data = []

        re = self.LINE_RE
        while self:
            lineno, line = self.pop()
            if line.startswith(prefix):
                self.push(lineno, line)
                break
            elif re.match(line).end() == len(line) != 0:
                title = data.pop()
                self.push(lineno, line)
                self.push(lineno - 1, title)
                break
            else:
                data.append(line)

        return '\n'.join(data)

    def read_title(self, chr, prefix):
        """
        Read title with the using the given underline character.
        """

        self.skip_blank()
        _, title = self.pop()

        # Check if title is in the heading hash tag form
        if title.startswith(prefix):
            return title[len(prefix):].strip()

        # No hash tags: search for a underline
        lineno, underline = self.pop()

        # Strip trailing spaces
        title = title.rstrip()
        underline = underline.rstrip()

        # Check underline length
        chars = set(underline)
        if len(chars) != 1 or chars != {chr}:
            raise MarkioSyntaxError(
                "line %s: title should have an underline formed of '%s' "
                "characters." % (lineno, chr)
            )
        if len(underline) != len(title):
            raise MarkioSyntaxError(
                'line %s: expect a underline of %s characters.' %
                (lineno, len(title))
            )
        return title.lstrip()

    def parse(self):
        """
        Return a MarkioGeneric object with project's parse tree.
        """

        self.parse_title()
        self.parse_meta()
        self.parse_short_description()
        self.parse_sections()
        return self.parsed

    def parse_title(self):
        self.parsed.title = self.read_title('=', '# ')

    def parse_meta(self):
        self.skip_blank()
        _, content = self.read_indented()
        self.parsed.meta = content

    def parse_short_description(self):
        self.parsed.short_description = self.read_before_title('## ').rstrip()

    def parse_sections(self):
        while self:
            self.parse_section()

    def parse_section(self):
        title = self.read_title('-', '## ')
        content = self.read_before_title('## ').rstrip()
        content = content.strip()
        self.parsed.sections.append((title, content))
