import pytest
from sulfur.simplehtml5 import validate


def assert_ok(data, html_identity=True):
    ast = validate(data)
    if html_identity:
        html_render = ast.render().strip()
        data = data.strip()
        assert html_render == data


def test_validate_simple_doctype_document():
    assert_ok("<!DOCTYPE html>")


def test_validate_simple_document():
    assert_ok("<!DOCTYPE html><head></head><body></body>")


def test_validate_tag_with_attribute():
    assert_ok('<div id="foo"></div>')


def test_validate_tag_with_unquoted_attribute():
    assert_ok('<div id=foo></div>')


def test_validate_tag_with_boolean_attribute():
    assert_ok('<div is-a-tag></div>')


def test_validate_self_closing_tag():
    assert_ok('<p>foo<br></p>')
    assert_ok('<p>foo<br/></p>', False)

