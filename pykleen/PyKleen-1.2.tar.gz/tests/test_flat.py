# -*- coding: utf-8 -*-
import datetime as dt
from contextlib import contextmanager
from decimal import Decimal

from pytest import raises

import pykleen as p


@contextmanager
def should_raise(message):
    with raises(p.Error) as err:
        yield
    assert str(err.value) == message, str(err.value)


@contextmanager
def should_raise_errors(errors):
    with raises(p.Errors) as err:
        yield
    assert err.value.errors == errors, err.value.errors


def test_size():
    test_1 = p.size()
    assert test_1([1, 5, 7]) == [1, 5, 7]
    assert test_1([4] * 44) == [4] * 44
    assert test_1('A simple string.') == 'A simple string.'

    test_2 = p.size(min_len=2, max_len=8)
    assert test_2([1, 5, 7]) == [1, 5, 7]
    assert test_2({1, 5, 7}) == {1, 5, 7}
    assert test_2((1, 5, 7,)) == (1, 5, 7,)
    assert test_2('String.') == 'String.'

    with should_raise('Too short.'):
        assert test_2([1])
    with should_raise('Too long.'):
        assert test_2([1] * 10)

    with should_raise('Too short.'):
        p.size(min_len=5)([1, 5, 7])
    with should_raise('Too long.'):
        p.size(max_len=5)([1, 5, 7, 6, 7, 8, 9])

    with should_raise('Too short.'):
        p.size(min_len=5)('Test')
    with should_raise('Too long.'):
        p.size(max_len=5)('Test string.')

    for value in [False, None, iter([1, 2, 4])]:
        with should_raise('Invalid type %s.' % type(value).__name__):
            p.size()(value)


def test_string():
    test_1 = p.string()
    assert test_1('String') == 'String'
    assert test_1('String' * 44) == 'String' * 44
    assert test_1(b'Bytes') == 'Bytes'
    assert test_1('Motörhead') == 'Motörhead'
    assert test_1(b'Mot\xc3\xb6rhead') == 'Motörhead'
    assert test_1(5667) == '5667'

    test_2 = p.string(min_len=5, max_len=150)
    assert test_2('String.') == 'String.'
    assert test_2('A somewhat longer string.') == 'A somewhat longer string.'
    assert test_2('   With spaces   ') == 'With spaces'

    with should_raise('Too short.'):
        test_2('')
    with should_raise('Too short.'):
        test_2('              ')
    with should_raise('Too long.'):
        test_2('A string' * 50)

    test_3 = p.string(strip=False)
    assert test_3('   With spaces   ') == '   With spaces   '


def test_string_clean():
    test_1 = p.string()
    assert test_1('String <script>') == 'String'
    assert test_1('String <script>Test</script>') == 'String Test'

    test_2 = p.string(allowed_tags=['strong', 'em'])
    assert test_2('Em <em>String</em>') == 'Em <em>String</em>'
    assert test_2('Bold <b>String</b>') == 'Bold String'

    test_3 = p.string(allowed_tags=['strong', 'em'],
                      allowed_attributes={'em': ['name']})
    assert test_3('Em <em name="x">it</em>') == 'Em <em name="x">it</em>'
    assert test_3('Em <em class="y">String</em>') == 'Em <em>String</em>'

    test_4 = p.string(strip_tags=False)
    assert test_4('<script>X</script>') == '<script>X</script>'


def test_regex():
    test_1 = p.regex(r'^[0-9]{4}[A-Z]{2}$')
    assert test_1('1234XY') == '1234XY'
    assert test_1(b'1234XY') == '1234XY'
    assert test_1('1234XY<script></script>') == '1234XY'

    with should_raise('Does not match.'):
        test_1('aaaa')

    test_2 = p.regex(r'^[0-9]{4}[A-Z]{2}$',
                     p.All([p.string(), p.To(lambda v: v.upper())]))

    assert test_2('1234XY') == '1234XY'
    assert test_2('4321xy') == '4321XY'


def test_numeric():
    test_1 = p.numeric()
    assert test_1('44') == 44
    assert test_1('44.55') == 45
    assert test_1('-32') == -32
    assert test_1('3E+5') == 300000

    with should_raise('Invalid number.'):
        assert test_1('inf')

    for value in ['Blah', 'nan', 'inf', '-inf']:
        with should_raise('Invalid number.'):
            assert test_1(value)

    test_2 = p.numeric(3)
    assert test_2('44.7889') == Decimal('44.789')
    assert test_2('75.1') == Decimal('75.100')
    assert test_2('22.123,075.112') == Decimal('22123075.112')

    test_3 = p.numeric(at_least=44, at_most=99)
    assert test_3('44.7889') == Decimal('45'), test_3('44.7889')
    assert test_3('75.1') == Decimal('75'), test_3('75.1')


def test_boolean():
    test_1 = p.boolean()
    assert test_1('yes') is True
    assert test_1('y') is True
    assert test_1('no') is False
    assert test_1(-1) is False
    assert test_1(1) is True
    assert test_1(True) is True
    assert test_1(False) is False
    assert test_1(None) is False
    assert test_1('nan') is False

    test_2 = p.boolean(is_true_when=['ja', 'j'])
    assert test_2('ja') is True
    assert test_2('j') is True
    assert test_2('nee') is False
    assert test_2('n') is False
    assert test_2(True) is False

    test_3 = p.boolean(is_false_when=['nee', 'n'])
    assert test_3('yes') is True
    assert test_3('y') is True
    assert test_3('nee') is False
    assert test_3('n') is False
    assert test_3(True) is True
    assert test_3(False) is True

    test_4 = p.boolean(is_true_when=['ja', 'j'], is_false_when=['nee', 'n'])
    assert test_4('ja') is True
    assert test_4('j') is True
    assert test_4('nee') is False
    assert test_4('n') is False

    with should_raise('Invalid boolean.'):
        test_4('yes')


def test_datetime():
    test_1 = p.datetime()
    assert test_1('2000-1-1 11:34') == dt.datetime(2000, 1, 1, 11, 34)
    assert test_1('2000-9-16 15:39:11') == dt.datetime(2000, 9, 16, 15, 39, 11)
    assert test_1('16-9-2000 3:45') == dt.datetime(2000, 9, 16, 3, 45)

    with should_raise('Invalid datetime.'):
        test_1('2000-19-19')

    with should_raise('Invalid datetime.'):
        test_1('16-9-2000 26:21')

    test_2 = p.datetime(['%Y-%m-%d %H:%M', '%m-%d-%Y %H:%M'])
    assert test_2('2000-1-1 21:45') == dt.datetime(2000, 1, 1, 21, 45)
    assert test_2('2000-9-16 22:19') == dt.datetime(2000, 9, 16, 22, 19)
    assert test_2('9-16-2000 11:33') == dt.datetime(2000, 9, 16, 11, 33)

    with should_raise('Invalid datetime.'):
        test_1('2000-19-19')

    with should_raise('Invalid datetime.'):
        test_1('16-9-2000 26:21')


def test_date():
    test_1 = p.date()
    assert test_1('2000-1-1') == dt.date(2000, 1, 1)
    assert test_1('2000-9-16') == dt.date(2000, 9, 16)
    assert test_1('16-9-2000') == dt.date(2000, 9, 16)

    with should_raise('Invalid date.'):
        test_1('2000-19-19')

    test_2 = p.date(['%Y-%m-%d', '%m-%d-%Y'])
    assert test_2('2000-1-1') == dt.date(2000, 1, 1)
    assert test_2('2000-9-16') == dt.date(2000, 9, 16)
    assert test_2('9-16-2000') == dt.date(2000, 9, 16)

    with should_raise('Invalid date.'):
        test_2('19-6-2000')


def test_minutes():
    test_1 = p.minutes()
    assert test_1('10:00') == 600
    assert test_1('10.30') == 630
    assert test_1('163:30') == 9810
    assert test_1('1030') == 630
    assert test_1('930') == 570
    assert test_1('45') == 45
    assert test_1('') == 0

    with should_raise('Invalid format.'):
        test_1('a20')

    with should_raise('Invalid format.'):
        test_1('20-10')


def test_one_of():
    test_1 = p.one_of([True, False, None])
    assert test_1(True) is True
    assert test_1(None) is None

    with should_raise('Invalid value.'):
        test_1('aaaa')

    test_2 = p.one_of([1, 6, 8], p.numeric())
    assert test_2('6') == 6
    assert test_2(8) == 8

    with should_raise('Invalid number.'):
        test_2('aaaa')


def test_set_of():
    test_1 = p.set_of([5, 7, 9])
    assert test_1([5]) == [5]
    assert test_1([5, 7, 9]) == [5, 7, 9]
    assert test_1(5) == [5]

    with should_raise('Invalid value(s) aaaa.'):
        test_1('aaaa')

    test_2 = p.set_of([1, 6, 8], p.numeric())
    assert test_2([6, 8]) == [6, 8]
    assert test_2(['6', '8']) == [6, 8]
    assert test_2('6') == [6]
    assert test_2('6,8') == [6, 8]

    with should_raise('Invalid value(s) 2, 7.'):
        test_2('2,6,7')

    class Custom(object):
        def __init__(self, name):
            self.name = name

        def __eq__(self, other):
            return self.name == other.name

    test_3 = p.set_of([Custom('x'), Custom('y')])
    test_3([Custom('x')]) == [Custom('x')]

    with should_raise('Invalid type Custom.'):
        test_2(Custom('One'))


def test_list_of():
    test_1 = p.list_of(p.numeric())
    test_1(['1', '5', '44.8']) == [1, 5, 45]
    test_1('4,7,99') == [4, 7, 99]
    test_1([1, '55', 99.4, '6']) == [1, 55, 99, 6]

    with should_raise_errors({
        1: 'Invalid number.',
        3: 'Invalid number.',
    }):
        test_1([5, 'a', 76, 'cc'])
