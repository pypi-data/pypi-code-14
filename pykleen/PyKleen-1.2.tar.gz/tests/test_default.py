# -*- coding: utf-8 -*-
from contextlib import contextmanager
from os import path

import check_manifest
from pytest import raises

import pykleen as p


@contextmanager
def should_raise(expected, message):
    with raises(expected) as err:
        yield
    assert str(err.value) == message, str(err.value)


def test_is_present():
    assert p


def test_manifest():
    dirname = path.dirname(__file__) + '/../'
    assert check_manifest.check_manifest(dirname) is True


def test_error():
    assert str(p.Error('Message here.')) == 'Message here.'


def test_errors():
    test_1 = p.Errors({
        'field': 'Not a number.',
        'other': 'Required.',
    })
    assert str(test_1) == '<Errors [field, other]>'
    assert test_1.errors == {
        'field': 'Not a number.',
        'other': 'Required.',
    }

    test_2 = p.Errors({
        'field': 'Not a number.',
        'other': 'Required.',
    }, 'Form validation failed.')
    assert str(test_2) == '<Errors [field, other] Form validation failed.>'
    assert test_2.errors == {
        'field': 'Not a number.',
        'other': 'Required.',
    }

    test_3 = p.Errors(message='Some general error.')
    assert str(test_3) == '<Errors [] Some general error.>'
    assert test_3.errors == {}


def test_one():
    one = p.One(lambda v: v is True)
    assert one(True) is True

    with should_raise(p.Error, 'Test failed.'):
        assert one(False)

    one = p.One(p.To(int))
    assert one('12') == 12

    with should_raise(p.Error, 'Conversion failed.'):
        one('aa')


def test_all():
    all = p.All([
        p.To(str),
        lambda v: len(v) < 10,
    ])
    assert all('More') == 'More'

    with should_raise(p.Error, 'Test failed.'):
        assert all('More than allowed.')

    all = p.All([
        p.To(int),
        lambda v: 0 < v < 10,
    ])
    assert all('5') == 5

    with should_raise(p.Error, 'Test failed.'):
        assert all('15')

    with should_raise(p.Error, 'Conversion failed.'):
        assert all('aa')


def test_or():
    test = p.Or([
        p.Yield(lambda v: v in [True, False], 'boolean'),
        p.Yield(lambda v: v in [None], 'none'),
        p.Yield(p.One(lambda v: isinstance(v, (str, bytes))), 'string'),
        p.Yield(p.One(lambda v: isinstance(v, int)), 'number'),
    ])

    assert test(True) == 'boolean'
    assert test(None) == 'none'
    assert test('blurp') == 'string'
    assert test(44) == 'number'

    with should_raise(p.Error, 'All tests failed.'):
        test(['some', 'words'])


def test_to():
    to = p.To(int)
    assert to('12') == 12

    with should_raise(p.Error, 'Conversion failed.'):
        assert to('aa')
