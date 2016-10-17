# Copyright 2016 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os.path import join as pjoin
import io
import pkg_resources

from piglet import compilexml as cx
from piglet import intermediate as im
from piglet.compile import compile_to_source
from piglet.parse import parse_html
from piglet.position import Position as P
from piglet.template import Template
from piglet.test_loader import create_templates

from mock import Mock

EXTRACT_KEYWORDS = {'_', 'gettext', 'ngettext'}


def toim(s):
    return cx.compile_intermediate(parse_html(s)).children


def tosrc(s):
    return compile_to_source(cx.compile_intermediate(parse_html(s)))


class TestI18N:
    def test_it_compiles_i18n_message(self):
        n = toim('<div i18n:message="" i18n:comment="translate me">foo</div>')
        assert n == [
            im.TextNode(pos=P(1, 1), content='<div>'),
            im.TranslationNode(pos=P(1, 20),
                               message='',
                               comment='translate me',
                               children=[im.TextNode(pos=P(1, 50),
                                                     content='foo')]),
            im.TextNode(pos=P(1, 53), content='</div>'),
        ]
        assert n[1].get_msgstr() == 'foo'

    def test_it_compiles_i18n_message_with_custom_message(self):
        n = toim('<div i18n:message="bar">foo</div>')
        assert n == [
            im.TextNode(pos=P(1, 1), content='<div>'),
            im.TranslationNode(pos=P(1, 20),
                               message='bar',
                               comment=None,
                               children=[im.TextNode(pos=P(1, 25),
                                                     content='foo')]),
            im.TextNode(pos=P(1, 28), content='</div>'),
        ]
        assert n[1].get_msgstr() == 'bar'

    def test_it_substitutes_dynamic_placeholders(self):
        n = toim('<div i18n:message="">foo $x <py:if test="x">1</py:if></div>')
        assert n[1].get_msgstr() == 'foo ${x} ${dynamic.1}'

    def test_it_substitutes_named_placeholders(self):
        n = toim('<div i18n:message="">foo <b i18n:name="x">$x</b></div>')
        assert n[1].get_msgstr() == 'foo ${x}'

        n = toim('<div i18n:message="">foo <i18n:s name="x" expr="x"/></div>')
        assert n[1].get_msgstr() == 'foo ${x}'
        interpolation = n[1].children[1].children[0]
        assert isinstance(interpolation, im.InterpolateNode)
        assert interpolation.value == 'x'

    def test_it_processes_placeholder_values(self):
        t = Template('<div i18n:message="">foo <b i18n:name="x">$x</b></div>')
        assert t.render({'x': 'baa'}) == '<div>foo <b>baa</b></div>'

        t.translations_factory = lambda: Mock(
            gettext=Mock(return_value='${x} sheep'))

        assert t.render({'x': 'baa'}) == '<div><b>baa</b> sheep</div>'

        t.translations_factory = lambda: Mock(
            gettext=Mock(return_value='BINGO!'))
        assert t.render({'x': 'baa'}) == '<div>BINGO!</div>'

    def test_it_normalizes_whitespace(self):
        t = Template('<div i18n:message="">\nfoo \n \n bar </div>')
        assert t.render({}) == '<div>foo bar</div>'


class TestExtractor:

    def get_extractor(self, name='piglet'):
        for ep in pkg_resources.iter_entry_points('babel.extractors'):
            if ep.dist.project_name == 'piglet' and ep.name == name:
                return ep.load()
        assert False, "No setuptools entry point exposed"

    def test_it_extracts_from_i18n_directives(self):
        with create_templates([
            ('a', u'<a i18n:message="foo">bar</a>'),
            ('b', u'<a i18n:message="">bar</a>'),
            ('c', u'<a i18n:message="">x is ${x}</a>'),
            ('d', u'<a i18n:message="">y is <a i18n:name="why">${x}</a></a>'),
            ('e', u'<a i18n:message="">${ x }</a>'),
        ]) as d:
            file_messages = [('a', [(1, '_', 'foo', [])]),
                             ('b', [(1, '_', 'bar', [])]),
                             ('c', [(1, '_', 'x is ${x}', [])]),
                             ('d', [(1, '_', 'y is ${why}', [])]),
                             ('e', [(1, '_', '${x}', [])]),
                             ]
            e = self.get_extractor()
            for f, expected in file_messages:
                with io.open(pjoin(d, f), 'r', encoding='utf-8') as f:
                    assert list(e(f, EXTRACT_KEYWORDS, [], {})) == expected

    def test_it_extracts_from_i18n_attributes_on_py_directives(self):
        with create_templates([
            ('a', (u'<py:if test="1" i18n:message="">one</py:if>'
                   u'<py:else i18n:message="">two</py:else>')),
        ]) as d:
            file_messages = [('a', [(1, '_', 'one', []),
                                    (1, '_', 'two', [])]),
                             ]
            e = self.get_extractor()
            for f, expected in file_messages:
                with io.open(pjoin(d, f), 'r', encoding='utf-8') as f:
                    assert list(e(f, EXTRACT_KEYWORDS, [], {})) == expected

    def test_it_extracts_from_interpolations(self):

        with create_templates([
            ('a', u'<a title="${_(\'foo\')}"></a>'),
            ('b', u'${gettext("bar")}'),
            ('c', u'${ngettext("fish", "fishes", n)}'),
        ]) as d:
            file_messages = [('a', [(1, '_', 'foo', [])]),
                             ('b', [(1, 'gettext', 'bar', [])]),
                             ('c', [(1, 'ngettext', ('fish', 'fishes'), [])]),
                             ]
            e = self.get_extractor()
            for f, expected in file_messages:
                with io.open(pjoin(d, f), 'r', encoding='utf-8') as f:
                    assert list(e(f, EXTRACT_KEYWORDS, [], {})) == expected
