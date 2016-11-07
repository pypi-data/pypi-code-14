"""
    test_feedopml
    ~~~~~~~~~~~~~

    :copyright: 2016 by Daniel Neuhäuser
    :license: BSD, see LICENSE.rst for details
"""
import os
from glob import glob

import pytest

import feedopml


PROJECT_DIR = os.path.dirname(__file__)
EXAMPLES_DIR = os.path.join(PROJECT_DIR, 'examples')


@pytest.fixture(params=glob(os.path.join(EXAMPLES_DIR, '*.opml')))
def example_path(request):
    return os.path.join(EXAMPLES_DIR, request.param)


def test_examples_parse(example_path):
    list(feedopml.parse(example_path))
