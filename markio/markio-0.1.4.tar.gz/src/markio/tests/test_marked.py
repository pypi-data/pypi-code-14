import pytest

from markio.marked import parse_marked


@pytest.fixture
def src():
    return """Title
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
"""


@pytest.fixture()
def src_hash_titles():
    return """# title

    meta

short description

## sub1

sub text.

## sub2

sub text.
"""


def test_parse_valid_document(src):
    marked = parse_marked(src)
    assert marked.title == 'Title'
    assert 'meta1: value' in marked.meta
    assert 'meta2: value' in marked.meta
    assert marked.short_description.startswith('Short description paragraph.')
    assert marked.short_description.endswith(';-)')
    assert len(marked.sections) == 2
    assert marked.sections[0][0] == ('Subsection 1')
    assert marked.sections[1][0] == ('Subsection 2')


def test_valid_document_round_trip(src):
    marked = parse_marked(src)
    assert marked.source() == src


def test_source_with_hash_titles(src_hash_titles):
    marked = parse_marked(src_hash_titles)
    assert marked.title == 'title'
    assert marked.meta == 'meta'
    assert marked.short_description == 'short description'
    assert marked.sections[0] == ('sub1', 'sub text.')
    assert marked.sections[1] == ('sub2', 'sub text.')
    assert len(marked.sections) == 2
