"""Basic behaviour tests"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest
from jinja2_registry import Renderer, register_loader, register_filesystem_loader
from bs4 import BeautifulSoup

TESTING_DIR = os.path.realpath(os.path.dirname(__file__))


class TestBasic(unittest.TestCase):
    """Test basic behaviour of the Jinja2 Registry"""

    template_dirs = {
        'layouts':   'templates/layouts',
        'partials':  'templates/partials',
        'pages':     'templates/pages',
    }
    layout_templates = {key: os.path.sep.join((TESTING_DIR, value)) \
                        for key, value in iter(template_dirs.items())}

    def setUp(self):

        for namespace, path in iter(self.layout_templates.items()):
            register_filesystem_loader(namespace, path)

        class TestRenderer(Renderer):
            """Subclass of renderer with a different namespace"""
            namespace = 'test'
        self.TestRenderer = TestRenderer

    def test_complete_stack(self):
        """Test the basic behaviour of the registry"""

        renderer = Renderer('pages/title.html')
        result = renderer.render()

        bs = BeautifulSoup(result, 'html.parser')

        # Confirm structure
        structure = ','.join([tag.name for tag in bs.find('html').find_all()])
        expected = 'head,title,body,ul,li,a,li,a,div,p'
        self.assertEqual(structure, expected)

        # Confirm title from "title.html"
        self.assertEqual(bs.find('title').text, 'new_title')

        # Confirm content from "content.html"
        self.assertEqual(bs.find('p').text, 'some_content')

        # Confirm navigation from "nav.html"
        linktext = [a.text for a in bs.find_all('a')]
        self.assertIn('Content page', linktext)
        self.assertIn('New title page', linktext)


