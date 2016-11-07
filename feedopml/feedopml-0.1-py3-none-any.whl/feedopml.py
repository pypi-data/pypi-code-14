"""
    feedopml
    ~~~~~~~~

    An OPML subscription list parser.

    :copyright: 2016 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import os

from lxml import etree


class FeedSubscription:
    """
    A feed subscription.
    """
    def __init__(self, type, text, xml_url,
                 description=None, html_url=None, language=None, title=None,
                 version=None):
        #: The type of feed, usually 'rss'.
        self.type = type

        #: The top-level `title` element from the feed or some user-defined
        #: value.
        self.text = text

        #: A HTTP URL to the feed.
        self.xml_url = xml_url


        # Optional attributes

        #: An optional description. Should correspond with the top-level
        #: description element from the feed.
        self.description = description

        #: An optional URL to the website corresponding to the feed. Should
        #: correspond with the top-level `link` element from the feed.
        self.html_url = None

        #: An optional language code. Should correspond with the top-level
        #: `language` element from the feed.
        self.language = None

        #: An optional title of the feed. Should correspond with the top-level
        #: `title` element from the feed.
        self.title = None

        #: An optional version of the feed format used.
        #:
        #: ===============  =============
        #: Value            Format
        #: ===============  =============
        #: 'RSS1'           RSS 1.0
        #: 'RSS'            RSS 0.91
        #:                  RSS 0.92
        #: 'RSS2'           RSS 2.0
        #: 'scriptingNews'  scriptingNews
        #: ===============  =============
        self.version = None


class ParserError(Exception):
    """
    Represents an error that occurred while parsing a subscription list.
    """


def parse(source, base_url=None):
    """
    Like :func:`parse_tree` but creates the tree using `lxml.etree.parse`.

    If parsing the XML fails, a :exc:`ParserError` is raised.
    """
    try:
        tree = etree.parse(source, base_url=base_url)
    except etree.Error as err:
        raise ParserError('invalid xml') from err

    return parse_tree(tree)


def parse_tree(tree):
    """
    Parses an `lxml.etree.ElementTree` representing an OPML subscription list
    and returns an iterable of :class:`FeedSubscription` objects.

    If parsing fails for some reason, a :exc:`ParserError` exception will be
    raised.
    """
    elements = tree.xpath('//outline[@type and @text and @xmlUrl]')
    return map(_parse_outline, elements)


def _parse_outline(element):
    if element.tag != 'outline':
        raise ParserError('expected outline tag, got {}'.format(element.tag))

    type = element.attrib['type']
    text = element.attrib['text']
    xml_url = element.attrib['xmlUrl']

    attributes = {
        name: element.attrib[xml_name]
        for name, xml_name in [
            ('description', 'description'),
            ('html_url', 'htmlUrl'),
            ('language', 'language'),
            ('title', 'title'),
            ('version', 'version')
        ]
        if xml_name in element.attrib
    }
    # TODO: Validate html_url and language.
    if 'version' in attributes:
        _validate_version(attributes['version'])

    return FeedSubscription(type, text, xml_url, **attributes)


def _validate_version(version):
    if version not in {'RSS', 'RSS1', 'RSS2', 'scriptingNews'}:
        raise ParserError('unexpected version value')
