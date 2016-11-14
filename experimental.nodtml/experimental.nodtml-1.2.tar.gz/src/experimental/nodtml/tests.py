# -*- coding: utf-8 -*-
from DocumentTemplate.DT_HTML import HTML
from DocumentTemplate.DT_String import String
from unittest import TestCase


class NoDtlmlTestCase(TestCase):

    def test_string_call(self):
        self.assertEqual(String(u'foobar')._orig__call__(), u'foobar')
        self.assertEqual(String(u'foobar')(), u'')

    def test_string_str(self):
        self.assertEqual(String(u'foobar')._orig__str__(), u'foobar')
        self.assertEqual(String(u'foobar')(), u'')

    def test_html_quotedHTML(self):
        self.assertEqual(HTML(u'foobar')._orig_quotedHTML(), u'foobar')
        self.assertEqual(HTML(u'foobar').quotedHTML(), u'')

    def test_html_str(self):
        self.assertEqual(HTML(u'foobar')._orig__str__(), u'foobar')
        self.assertEqual(HTML(u'foobar').__str__(), u'')
