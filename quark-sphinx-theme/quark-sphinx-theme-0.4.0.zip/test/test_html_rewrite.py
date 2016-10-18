# -*- coding: utf-8 -*-
# This file is part of quark-sphinx-theme.
# Copyright (c) 2016 Felix Krull <f_krull@gmx.de>
# Released under the terms of the BSD license; see LICENSE.

import os
import sys
import unittest

from quark_sphinx_theme.ext.html_rewrite import (
    create_translator_class, HTMLCompatMixin, BoxesMixin, LiteralBlocksMixin)
from sphinx.writers.html import HTMLTranslator
DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, DIR)
from util import SphinxBuildFixture, with_document, with_elements  # noqa


testdoc_html_rewrite = os.path.join(DIR, 'testdoc-html_rewrite')


class TestHTMLRewriteOutputTestCases(SphinxBuildFixture):
    source_dir = testdoc_html_rewrite

    @with_elements('test_pre_block', './/div[@class="highlight"]//pre//span')
    def test_pre_block(self, elems):
        for span in elems:
            self.assertTrue(span.text)

    @with_elements('test_footnote', './/table[@class="docutils footnote"]/..')
    def test_footnote(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'div')
            self.assertEqual(par.get('class'), '-x-quark-footnote-wrapper')
            self.assertTrue(par.get('id'))
            self.assertFalse(par.find('./table').get('id'))

    @with_elements('test_citation', './/table[@class="docutils citation"]/..')
    def test_citation(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'div')
            self.assertEqual(par.get('class'), '-x-quark-citation-wrapper')
            self.assertTrue(par.get('id'))
            self.assertFalse(par.find('./table').get('id'))

    @with_elements('test_admonition',
                   './/div[@class="admonition-test admonition"]/../../../..')
    def test_admonition(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'table')
            self.assertIn('-x-quark-admonition', par.get('class'))
            self.assertIn('-x-quark-box', par.get('class'))

    @with_elements('test_warning',
                   './/div[@class="admonition warning"]/../../../..')
    def test_warning(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'table')
            self.assertIn('-x-quark-admonition', par.get('class'))
            self.assertIn('-x-quark-warning', par.get('class'))
            self.assertIn('-x-quark-box', par.get('class'))

    @with_elements('test_topic', './/div[@class="topic"]/../../../..')
    def test_topic(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'table')
            self.assertIn('-x-quark-topic', par.get('class'))
            self.assertIn('-x-quark-box', par.get('class'))

    @with_elements('test_sidebar', './/div[@class="sidebar"]/../../../..')
    def test_sidebar(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'table')
            self.assertIn('-x-quark-sidebar', par.get('class'))
            self.assertIn('-x-quark-box', par.get('class'))

    @with_elements('test_literal_block',
                   './/div[@class="highlight"]/../../../../..')
    def test_literal_block(self, elems):
        for par in elems:
            self.assertEqual(par.tag, 'table')
            self.assertIn('-x-quark-literal-block', par.get('class'))


class TestHTMLRewriteOutput(TestHTMLRewriteOutputTestCases, unittest.TestCase):
    pass


class TestHTMLCompatOutput(TestHTMLRewriteOutputTestCases, unittest.TestCase):
    tags = ['test_html_compat_alias']


class TestHTMLRewriteFeatures(SphinxBuildFixture, unittest.TestCase):
    source_dir = testdoc_html_rewrite
    config = {
        'quark_html_features': '',
    }

    @with_elements('test_footnote', './/table[@class="docutils footnote"]/..')
    def test_footnote(self, elems):
        for par in elems:
            self.assertNotIn(par.get('class'), '-x-quark-footnote-wrapper')

    @with_elements('test_citation', './/table[@class="docutils citation"]/..')
    def test_citation(self, elems):
        for par in elems:
            self.assertNotIn(par.get('class'), '-x-quark-citation-wrapper')

    @with_elements('test_admonition',
                   './/div[@class="admonition-test admonition"]/../../../..')
    def test_admonition(self, elems):
        for par in elems:
            self.assertNotEqual(par.tag, 'table')
            self.assertNotIn('-x-quark-admonition', par.get('class'))

    @with_elements('test_topic', './/div[@class="topic"]/../../../..')
    def test_topic(self, elems):
        for par in elems:
            self.assertNotEqual(par.tag, 'table')
            self.assertNotIn('-x-quark-topic', par.get('class'))

    @with_elements('test_sidebar', './/div[@class="sidebar"]/../../../..')
    def test_sidebar(self, elems):
        for par in elems:
            self.assertNotEqual(par.tag, 'table')
            self.assertNotIn('-x-quark-sidebar', par.get('class'))

    @with_elements('test_literal_block',
                   './/div[@class="highlight"]/../../../../..')
    def test_literal_block(self, elems):
        for par in elems:
            self.assertNotEqual(par.tag, 'table')
            self.assertNotIn('-x-quark-literal-block', par.get('class'))


class TestCreateTranslatorClass(unittest.TestCase):
    CLS = HTMLTranslator

    def test_no_enabled_no_disabled(self):
        cls = create_translator_class(self.CLS, [], [])
        self.assertTrue(issubclass(cls, self.CLS))
        self.assertFalse(issubclass(cls, HTMLCompatMixin))
        self.assertFalse(issubclass(cls, BoxesMixin))
        self.assertFalse(issubclass(cls, LiteralBlocksMixin))

    def test_some_enabled_no_disabled(self):
        cls = create_translator_class(self.CLS, ['compat'], [])
        self.assertTrue(issubclass(cls, self.CLS))
        self.assertTrue(issubclass(cls, HTMLCompatMixin))
        self.assertFalse(issubclass(cls, BoxesMixin))
        self.assertFalse(issubclass(cls, LiteralBlocksMixin))

    def test_no_enabled_some_disabled(self):
        cls = create_translator_class(self.CLS, [], ['boxes', 'literal_blocks'])
        self.assertTrue(issubclass(cls, self.CLS))
        self.assertFalse(issubclass(cls, HTMLCompatMixin))
        self.assertFalse(issubclass(cls, BoxesMixin))
        self.assertFalse(issubclass(cls, LiteralBlocksMixin))

    def test_some_enabled_some_disabled(self):
        cls = create_translator_class(self.CLS, ['compat', 'boxes'],
                                      ['literal_blocks', 'compat'])
        self.assertTrue(issubclass(cls, self.CLS))
        self.assertFalse(issubclass(cls, HTMLCompatMixin))
        self.assertTrue(issubclass(cls, BoxesMixin))
        self.assertFalse(issubclass(cls, LiteralBlocksMixin))


if __name__ == '__main__':
    unittest.main()
