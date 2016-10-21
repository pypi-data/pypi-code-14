# -*- coding: utf-8 -*-
from metaset import MetaSet


def test_union():
    assert MetaSet(a={1}) | MetaSet(b={2}) == {'a': {1}, 'b': {2}}
    assert MetaSet(a={1}) | MetaSet(a={1, 2}, b={2}) == {'a': {1, 2}, 'b': {2}}
    assert MetaSet(a={1}) | MetaSet(a={1}, b=set()) == {'a': {1}, 'b': set()}
    assert MetaSet(a=set()) | MetaSet(b=set()) == {'a': set(), 'b': set()}
    assert MetaSet() | MetaSet(a=set()) == {'a': set()}


def test_difference():
    assert MetaSet(a={1}) - MetaSet(b={2}) == {'a': {1}}
    assert MetaSet(a={1}) - MetaSet(a={2}) == {'a': {1}}
    assert MetaSet(a={1}) - MetaSet(a={1}) == {'a': set()}
    assert MetaSet(a=set()) - MetaSet(a={1}) == {'a': set()}
    assert MetaSet(a=set()) - MetaSet(a=set()) == {'a': set()}
    assert MetaSet(a=set()) - MetaSet() == {'a': set()}


def test_intersection():
    assert MetaSet(a={1}) & MetaSet(a={1, 2}) == {'a': {1}}
    assert MetaSet(a={1}) & MetaSet(b={2}) == {}
    assert MetaSet(a={1}) & MetaSet(a=set(), b={2}) == {'a': set()}
    assert MetaSet(a={1}) & MetaSet(a={2}) == {'a': set()}
    assert MetaSet(a=set()) & MetaSet(a=set()) == {'a': set()}
    assert MetaSet(a=set()) & MetaSet() == {}


def test_symmetric_difference():
    assert MetaSet(a={1}) ^ MetaSet(b={2}) == {'a': {1}, 'b': {2}}
    assert MetaSet(a={1}) ^ MetaSet(a={1, 2}) == {'a': {2}}
    assert MetaSet(a={1}) ^ MetaSet(a={1}) == {'a': set()}
    assert MetaSet(a=set()) ^ MetaSet(a=set()) == {'a': set()}
    assert MetaSet(a=set()) ^ MetaSet() == {'a': set()}
