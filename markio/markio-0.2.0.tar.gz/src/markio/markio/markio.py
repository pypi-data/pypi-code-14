import decimal

import iospec
from boxed.core import indent
from markio.marked import Marked
from markio.marked.meta import Meta, meta_property
from markio.marked.section import Section, SectionList, section_property
from markio.markio.answer_key import AnswerKey
from markio.markio.placeholder import Placeholder
from markio.utils import unindent, to_decimal


def load_iospec_data(data):
    """
    Load IoSpec content from a section
    """

    data = unindent(data)
    ast = iospec.parse(data + '\n')
    return ast


def iospec_view(attr):
    source_attr = attr + '_source'
    cache_attr = '_' + attr + '_cache'
    getcache = lambda self: getattr(self, cache_attr)
    getsource = lambda self: getattr(self, source_attr)

    def fget(self):
        cache = getcache(self)
        source = getsource(self)
        if self._examples_cache is not None:
            src, data = cache
            if src == source:
                return data

        data = load_iospec_data(source)
        setattr(self, cache_attr, (source, data))
        return data

    def fset(self, value):
        if value is None:
            setattr(self, source_attr, '')
            setattr(self, cache_attr, ('', None))
        else:
            source = indent(value.source(), 4)
            setattr(self, cache_attr, (source, value))

    return property(fget, fset)


class Markio(Marked):
    """
    Base node for the Markio AST.
    """

    author = meta_property('author')
    slug = meta_property('slug')
    tags = meta_property('tags')
    timeout = meta_property('timeout')
    language = meta_property('language')
    i18n = meta_property('i18n')
    description = section_property('description', default='')
    examples_source = section_property('examples', default='')
    tests_source = section_property('tests', default='')
    examples = iospec_view('examples')
    tests = iospec_view('tests')

    _examples_cache = None
    _tests_cache = None

    def __init__(self, title=None,
                 author=None, slug=None, tags=None, timeout=1,
                 language=None, i18n=None,
                 short_description='',
                 description='', examples=None, tests=None,
                 sections=None,
                 meta=None,
                 parent=None):

        super().__init__(title=title, parent=parent,
                         short_description=short_description)

        self.answer_key = Section('Answer Key', '', key='answer_key')
        self.placeholder = SectionList(self)
        self.translations = {}
        self.extra_sections = SectionList(self)
        self._parent = parent

        # Meta information
        self.author = author
        self.slug = slug
        self.tags = list(tags or [])
        self.timeout = to_decimal(timeout)
        self.language = language
        self.i18n = i18n

        # Simple sections
        self.description = description
        self.examples = examples
        self.tests = tests

        # Composite sections
        self.answer_key = AnswerKey(self.sections)
        self.placeholder = Placeholder(self.sections)

        # Extra sections
        if sections:
            raise NotImplementedError
        if meta:
            raise NotImplementedError

    def load_meta(self, data):
        self.meta = meta = Meta(self, data)

        # Timeout must be a number
        timeout = meta.setdefault('timeout', None)
        if timeout is not None:
            timeout = decimal.Decimal(timeout)
            meta['timeout'] = to_decimal(timeout)

    def load_section(self, title, content, tags):
        name = title.casefold()

        try:
            loader = getattr(self, 'load_section_' + name.replace(' ', '_'))
        except AttributeError:
            pass
        else:
            return loader(title, content, tags)

        # Extra sections
        return self.load_extra_section(title, content, tags)

    def load_section_description(self, title, content, tags):
        forbid_tags(title, tags)
        return super().load_section(title, content, tags)

    def load_section_examples(self, title, content, tags):
        forbid_tags(title, tags)
        section = super().load_section(title, content, tags)
        if content:
            self._examples_cache = content, load_iospec_data(content)
        return section

    def load_section_tests(self, title, content, tags):
        forbid_tags(title, tags)
        section = super().load_section(title, content, tags)
        if content:
            self._tests_cache = content, load_iospec_data(content)
        return section

    def load_section_answer_key(self, title, content, tags):
        return super().load_section(title, content, tags)

    def load_section_placeholder(self, title, content, tags):
        return super().load_section(title, content, tags)

    def load_extra_section(self, title, content, tags):
        raise NotImplementedError('invalid section: %s' % title)


def forbid_tags(title, tags):
    if tags:
        raise ValueError('%r section cannot have tags' % title)
