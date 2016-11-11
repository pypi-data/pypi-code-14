# -*- coding: utf-8 -*-
import datetime as dt
from contextlib import contextmanager

from pytest import raises

import pykleen as p


@contextmanager
def should_raise_errors(errors):
    with raises(p.Errors) as err:
        yield
    assert err.value.errors == errors, err.value.errors


def test_one():
    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
    })

    assert schema({
        'name': 'Jan Jansen',
        'age': '44',
    }) == ({
        'name': 'Jan Jansen',
        'age': 44
    })

    with should_raise_errors({
        'name': 'Required.',
        'age': 'Invalid number.',
    }):
        schema({'age': 'aaa'})


def test_two():
    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
        p.Param('since', dt.date.today): p.date(),
        p.Param('scheme', 'purple'): p.one_of(['green', 'blue', 'purple'],
                                              p.string()),
    })

    since = dt.date.today() - dt.timedelta(days=5)

    assert schema({
        'name': 'Jan Jansen',
        'age': '44',
        'since': since,
        'scheme': 'blue',
    }) == ({
        'name': 'Jan Jansen',
        'age': 44,
        'since': since,
        'scheme': 'blue'
    })

    assert schema({
        'name': 'Jan Jansen',
        'age': '57',
    }) == ({
        'name': 'Jan Jansen', 'age': 57, 'since': dt.date.today(),
        'scheme': 'purple'
    })


def test_three():
    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
        'since': p.date(),
        'scheme': p.one_of(['green', 'blue', 'purple'], p.string()),
    }, nothing_is_required=True)

    assert schema({}) == ({
        'name': None,
        'age': None,
        'since': None,
        'scheme': None,
    })

    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
        'since': p.date(),
        'scheme': p.one_of(['green', 'blue', 'purple'], p.string()),
    }, fail_to_none=True)

    assert schema({
        'age': 'aaa',
        'scheme': 'blurp',
    }) == ({
        'name': None,
        'age': None,
        'since': None,
        'scheme': None,
    })


def test_four():
    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
        'address': p.Schema({
            'number': p.numeric(),
            'postal': p.string(min_len=4, max_len=8),
        }),
    })

    assert schema({
        'name': 'Jan Jansen',
        'age': '68',
        'address': {
            'number': '33',
            'postal': '57290AZ'
        }
    }) == ({
        'name': 'Jan Jansen',
        'age': 68,
        'address': {
            'number': 33,
            'postal': '57290AZ'
        }
    })

    with should_raise_errors({
        'age': 'Required.',
        'address': {
            'number': 'Required.',
            'postal': 'Too short.',
        }
    }):
        schema({
            'name': 'Jan Jansen',
            'address': {
                'postal': '57'
            }
        })


def test_five():
    schema = p.Schema({
        'name': p.string(min_len=1),
        'age': p.numeric(),
        'addresses': p.list_of(p.Schema({
            'number': p.numeric(),
            'postal': p.string(min_len=4, max_len=8),
        })),
    })

    assert schema({
        'name': 'Jan Jansen',
        'age': '68',
        'addresses': [{
            'number': '33',
            'postal': '57290AZ'
        }, {
            'number': '45',
            'postal': '39012XZ'
        }]
    }) == ({
        'name': 'Jan Jansen',
        'age': 68,
        'addresses': [{
            'number': 33,
            'postal': '57290AZ'
        }, {
            'number': 45,
            'postal': '39012XZ'
        }]
    })

    with should_raise_errors({
        'age': 'Required.',
        'addresses': {
            0: {
                'postal': 'Too short.',
            },
            1: {
                'number': 'Required.',
            }
        }
    }):
        schema({
            'name': 'Jan Jansen',
            'addresses': [{
                'number': '33',
                'postal': '31'
            }, {
                'postal': '39012XZ'
            }]
        })
