# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django
import pytest
from django.template import Context, Template as T

CTX = Context()

def test_templatetag():
    resp = T('{% load path2css %}{% path2css "/test/path/" %}').render(CTX).strip()
    assert resp == 'test test-path'

def test_templatetag_root_does_nothing():
    resp = T('{% load path2css %}{% path2css "//" %}').render(CTX).strip()
    assert resp == ''


def test_templatetag_with_prefix():
    resp = T('{% load path2css %}{% path2css "/test/" prefix="HELLO" %}').render(
        CTX,
    ).strip()
    assert resp == 'HELLO-test'


def test_templatetag_with_prefix_ending_with_separator():
    resp = T('{% load path2css %}{% path2css "/test/" prefix="HELLO_" %}').render(
        CTX,
    ).strip()
    assert resp == 'HELLO_test'


def test_templatetag_with_suffix():
    resp = T('{% load path2css %}{% path2css "/test/" suffix="BYE" %}').render(
        CTX,
    ).strip()
    assert resp == 'test-BYE'

def test_templatetag_with_suffix_ending_with_separator():
    resp = T('{% load path2css %}{% path2css "/test/" suffix="_BYE" %}').render(
        CTX,
    ).strip()
    assert resp == 'test_BYE'


@pytest.mark.xfail(condition=django.VERSION[0:2] < (1, 9),
                   reason="Django 1.8 doesn't have combination simple/assignment tags")
def test_templatetag_assignment():
    resp = T('''{% load path2css %}{% path2css "/test/" as GOOSE %}
    1{% for part in GOOSE %}---{{part}}---{% endfor %}2
    ''').render(
        CTX,
    ).strip()
    parts = [x for x in resp.split() if x]
    assert parts == ['1---test---2']
