#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests"""

import unittest.mock as mock
import pytest

from cuebung_helper import Make, PopenReturnObject, set_emit

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"


def myemit(msg):
    """help function"""
    global RETURNVALUE  # pylint: disable=W0603
    RETURNVALUE = msg

RETURNVALUE = None


@pytest.fixture(params=[False, True])
def ign_comp_warn(request):
    """Use signals for timing out or not."""
    return request.param


@pytest.fixture(params=['all', 'test'])
def func(request):
    """Use signals for timing out or not."""
    return request.param


@mock.patch('cuebung_helper.runcode.RunCode.run')
def test_make_clean(mock_runcode, ign_comp_warn):
    """Test Make class with clean methode"""
    res_ok = PopenReturnObject()
    res_to = PopenReturnObject(timedout=True)
    res_rc = PopenReturnObject(returncode=1)
    set_emit(myemit)

    make = Make(ignore_warnings=ign_comp_warn)

    mock_runcode.return_value = res_ok
    assert make.clean()
    assert mock_runcode.called

    mock_runcode.return_value = res_to
    assert not make.clean()
    assert RETURNVALUE['msg'] == Make.txt_clean_err

    mock_runcode.return_value = res_rc
    assert not make.clean()
    assert RETURNVALUE['msg'] == Make.txt_clean_err


@mock.patch('cuebung_helper.runcode.RunCode.run')
def test_make_all_test(mock_runcode, ign_comp_warn, func):
    """Test Make class with all/test methode"""
    res_ok = PopenReturnObject()
    res_to = PopenReturnObject(timedout=True)
    res_rc = PopenReturnObject(returncode=1)
    res_err = PopenReturnObject(stderr=['XYZ'])
    set_emit(myemit)

    make = Make(ignore_warnings=ign_comp_warn)

    mock_runcode.return_value = res_ok
    assert getattr(make, func)()
    assert RETURNVALUE['msg'] == Make.txt_ok

    mock_runcode.return_value = res_to
    assert not getattr(make, func)()
    assert RETURNVALUE['msg'] == Make.txt_timeout

    mock_runcode.return_value = res_rc
    assert not getattr(make, func)()
    assert RETURNVALUE['msg'] == Make.txt_errors

    mock_runcode.return_value = res_err
    assert ign_comp_warn == getattr(make, func)()
    assert RETURNVALUE['msg'] == Make.txt_warnings
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
