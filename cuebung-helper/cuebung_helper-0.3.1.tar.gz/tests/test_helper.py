#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests"""

import os
from io import BytesIO
import pytest
from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st

from cuebung_helper.helper import (_islistofstrings, _cmplistofstrings,
                                   _cleanresult, Boolean, Text,
                                   exchange_values)

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

settings.register_profile("ci", settings(max_examples=1000))
settings.register_profile("dev", settings(max_examples=10))
settings.register_profile("debug", settings(max_examples=10,
                                            verbosity=Verbosity.verbose))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))


@given(st.lists(st.text()))
def test_islistofstings(arg):
    """Test the function with the correct argument type"""
    assert _islistofstrings(arg)


NONETEXT = st.sampled_from([st.integers(), st.booleans(), st.floats()])


@given(st.lists(NONETEXT, min_size=1))
def test_not_islistofstings(arg):
    """Test the function with the incorrect argument type"""
    assert not _islistofstrings(arg)


@given(st.lists(NONETEXT, min_size=1))
def test_not_islistofstings2(arg):
    """Test the function with the incorrect argument type"""
    assert not _islistofstrings(tuple(arg))


@given(st.lists(st.text()))
def test_cmplistofstrings(arg):
    """Test the function with the correct argument type"""
    assert _cmplistofstrings(arg, arg)


@given(st.lists(st.text(), min_size=1))
def test_cmplistofstrings_diff_len(arg):
    """Test the function with two lists of not equal length"""
    assert not _cmplistofstrings(arg, arg[:-1])


@given(st.lists(st.text(), min_size=2),
       st.text())
def test_cmplistofstrings_diff_str(arg, swapword):
    """Test the function with two lists with different strings"""
    sndlst = arg[:]
    for i, word in enumerate(sndlst):
        if word != swapword:
            sndlst[i] = swapword
            break
    else:
        # if no entry in the list differs from swapword, force inequality
        # with a diffrent type of entry at the last place in the list
        sndlst[-1] = 42
    assert not _cmplistofstrings(arg, sndlst)


@given(st.lists(st.binary()))
def test_cleanresult(arg):
    """Test the function"""
    data = BytesIO(b'\n'.join(arg))
    out = _cleanresult(data)
    assert _islistofstrings(out)


@given(st.booleans())
def test_boolean(val):
    """Test the Boolean descriptor"""
    class UseBoolean:
        """Helper class"""
        val1 = Boolean(val)
        val2 = Boolean()

    use = UseBoolean()
    assert use.val1 == val
    assert not use.val2

    use.val1 = not val
    assert use.val1 != val
    use.val1 = val
    assert use.val1 == val

    # Test preset value
    assert not use.val2
    use.val2 = True
    assert use.val2
    use.val2 = False
    assert not use.val2

    with pytest.raises(ValueError):
        use.val2 = 1  # pylint: disable=R0204


@given(st.text(min_size=2))
def test_text(val):
    """Test the Text descriptor"""
    lval = int(len(val) / 2)
    sval1 = val[:lval]
    sval2 = val[lval:]

    class UseText:
        """Helper class"""
        val1 = Text(sval1)
        val2 = Text()

    use = UseText()
    assert use.val1 == sval1
    assert use.val2 is None

    use.val1 = sval2
    assert use.val1 == sval2
    use.val1 = sval1
    assert use.val1 == sval1

    # Test preset value
    assert use.val2 is None
    use.val2 = sval2
    assert use.val2 == sval2
    use.val2 = sval1
    assert use.val2 == sval1

    with pytest.raises(ValueError):
        use.val2 = 1


def test_mix_boolean_text():
    """Check if classes with mixed Descriptors preserve the default values"""

    class Mix():
        """Helper class"""
        val1 = Boolean()
        val2 = Text()
        val3 = Boolean()
        val4 = Text()

    use = Mix()
    assert not use.val1
    assert use.val2 is None
    assert not use.val3
    assert use.val4 is None
    assert isinstance(use.val1, bool)
    assert isinstance(use.val3, bool)
    use.val2 = "hallo"
    use.val4 = "du"
    assert isinstance(use.val2, str)
    assert isinstance(use.val4, str)


def test_boolean_without_class():
    """Test the getter"""
    val1 = Boolean()
    assert isinstance(val1, Boolean)


def test_exchange_values():
    """Test the exchanging of values via named pipes"""
    from random import randint
    valuelist = []
    with exchange_values(randint, (0, 50), valuelist):
        msg = os.open('message', os.O_RDONLY)
        cmd = os.open('command', os.O_WRONLY)
        innervalues = []
        for _ in range(10):
            os.write(cmd, b'N')
            val = os.read(msg, 10).decode()
            innervalues.append(int(val))
        os.close(msg)
        os.close(cmd)
    assert valuelist == innervalues
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
