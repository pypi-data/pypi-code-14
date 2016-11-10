import json
try:
    from mock import patch, mock_open
except ImportError:
    from unittest.mock import patch, mock_open
import os
import sys
from unittest import TestCase
import yaml

from prose_wc import wc


class TestRun(TestCase):
    @patch.object(sys, 'exit')
    def test_it_works(self, mock_exit):
        old_argv = sys.argv
        sys.argv = ['test', '-h']
        with patch.object(sys, 'stderr'):
            wc.run()
        self.assertTrue(mock_exit.called)
        sys.argv = old_argv


class TestProseWC(TestCase):
    def setUp(self):
        base = os.path.dirname(__file__)
        full_base = os.path.dirname(os.path.abspath(__file__))
        self.plaintext = os.path.join(full_base, 'plaintext.test')
        self.jekyll = os.path.join(base, 'jekyll.test')

    @patch.object(sys, 'exit')
    def test_no_file(self, mock_exit):
        with patch.object(sys, 'stderr'):
            self.assertEqual(wc.prose_wc(wc.setup(['-h'])), 1)

    @patch.object(wc, 'update_file')
    def test_update(self, mock_update):
        wc.prose_wc(wc.setup(['-u', self.jekyll]))
        self.assertTrue(mock_update.called_once)

    @patch.object(wc, '_mockable_print')
    @patch.object(wc, 'default_dump')
    def test_output_default(self, mock_dump, mock_print):
        wc.prose_wc(wc.setup([self.plaintext]))
        self.assertTrue(mock_dump.called_once)
        self.assertTrue(mock_print.called_once)

    @patch.object(wc, '_mockable_print')
    @patch.object(wc, 'default_dump')
    def test_split_hyphens(self, mock_dump, mock_print):
        with patch.object(wc, 'INTERSTITIAL_PUNCTUATION') as mock_ip:
            wc.prose_wc(wc.setup(['-S', self.plaintext]))
        self.assertTrue(mock_ip.append.called_once)
        self.assertTrue(mock_dump.called_once)
        self.assertTrue(mock_print.called_once)

    @patch.object(wc, '_mockable_print')
    @patch.object(json, 'dumps')
    def test_output_json(self, mock_dump, mock_print):
        wc.prose_wc(wc.setup(['-f', 'json', self.plaintext]))
        self.assertTrue(mock_dump.called_once)
        self.assertTrue(mock_print.called_once)

    @patch.object(wc, '_mockable_print')
    @patch.object(yaml, 'safe_dump')
    def test_output_yaml(self, mock_dump, mock_print):
        wc.prose_wc(wc.setup(['-f', 'yaml', self.plaintext]))
        mock_dump.assert_called_once_with({
            'counts': {
                'file': self.plaintext,
                'type': 'md/txt',
                'words': 338,
                'paragraphs': 7,
                '_paragraphs': 'paragraphs',
                'characters_total': 1728,
                'characters_real': 1388
            }
        }, default_flow_style=False, indent=4)
        self.assertTrue(mock_print.called_once)


class TestWC(TestCase):
    def setUp(self):
        self.plaintext = """
        Everybody needs a friend. I thought today we would make a happy
        little stream that's just running through the woods here. Isn't that
        fantastic? You can just push a little tree out of your brush like
        that. Just let go - and fall like a little waterfall.
        """
        self.jekyll = """---
        layout: default
        title: Bob Ross, yo!
        ---

        Everybody needs a friend. I thought today we would make a happy
        little stream that's just running through the woods here. Isn't that
        fantastic? You can just push a little tree out of your brush like
        that. Just let go - and fall like a little waterfall."""

    def test_nonjekyll(self):
        result = wc.wc('non-jekyll', self.plaintext)
        self.assertEqual(result, {
            'counts': {
                'characters_real': 198,
                'characters_total': 244,
                'file': 'non-jekyll',
                'paragraphs': 1,
                'type': 'md/txt',
                'words': 46,
            }
        })

    def test_jekyll(self):
        result = wc.wc('jekyll', wc.strip_frontmatter(self.jekyll),
                       parsed=self.plaintext, is_jekyll=True)
        self.assertEqual(result, {
            'counts': {
                'characters_real': 198,
                'characters_total': 244,
                'file': 'jekyll',
                'paragraphs': 1,
                'type': 'jekyll',
                'words': 46,
            }
        })


class TestWCTextSpecificCases(TestCase):
    def test_hyphens(self):
        self.assertEqual(
            wc.wc('', 'a - b')['counts']['words'],
            2, 'hyphen and two spaces')
        self.assertEqual(
            wc.wc('', 'a- b')['counts']['words'],
            2, 'hyphen and one space')
        self.assertEqual(
            wc.wc('', 'a-b')['counts']['words'],
            1, 'hyphen and no spaces')

    def test_ellipses(self):
        self.assertEqual(
            wc.wc('', 'a . . . b')['counts']['words'],
            2, 'spaced ellipses and two spaces')
        self.assertEqual(
            wc.wc('', 'a. . .b')['counts']['words'],
            2, 'spaced ellipses and no spaces')
        self.assertEqual(
            wc.wc('', 'a ... b')['counts']['words'],
            2, 'unspaced ellipses and two spaces')
        self.assertEqual(
            wc.wc('', 'a... b')['counts']['words'],
            2, 'unspaced ellipses and one space')
        self.assertEqual(
            wc.wc('', 'a...b')['counts']['words'],
            2, 'unspaced ellipses and no spaces')

    def test_apostrophes(self):
        self.assertEqual(
            wc.wc('', "Madison's James")['counts']['words'],
            2, 'possessive apostrophe with s')
        self.assertEqual(
            wc.wc('', "James' Madison")['counts']['words'],
            2, 'possessive apostrophe with no s')


class TestUpdateFile(TestCase):
    def test_updates_frontmatter(self):
        content = """---
        layout: default
        title: Bob Ross, yo!
        ---

        Everybody needs a friend. I thought today we would make a happy
        little stream that's just running through the woods here. Isn't that
        fantastic? You can just push a little tree out of your brush like
        that. Just let go - and fall like a little waterfall."""
        result = {
            'counts': {
                'characters_real': 198,
                'characters_total': 244,
                'file': 'jekyll',
                'paragraphs': 1,
                'type': 'jekyll',
                'words': 47,
            }
        }
        with patch('prose_wc.wc.open', mock_open(), create=True) as \
                mocked_open:
            wc.update_file('jekyll', result, content, 4)
        file_handle = mocked_open.return_value
        file_handle.write.assert_called_with("""---
counts:
    characters_real: 198
    characters_total: 244
    file: jekyll
    paragraphs: 1
    type: jekyll
    words: 47
layout: default
title: Bob Ross, yo!
---

        Everybody needs a friend. I thought today we would make a happy
        little stream that\'s just running through the woods here. Isn\'t that
        fantastic? You can just push a little tree out of your brush like
        that. Just let go - and fall like a little waterfall.""")


class TestDefaultDump(TestCase):
    def test_dumps_results(self):
        result = {
            'counts': {
                'characters_real': 198,
                'characters_total': 244,
                'file': 'jekyll',
                'paragraphs': 1,
                'type': 'jekyll',
                'words': 47,
            }
        }
        self.assertEqual(wc.default_dump(result), 'jekyll (jekyll)\t'
                         '1 paragraph\t47 words\t198 characters (real)\t'
                         '244 characters (total)')
