#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests"""

import builtins
import os
from unittest.mock import patch
from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st

from cuebung_helper.emitter import emit, set_emit, reset_emit, MsgType
import cuebung_helper.emitter

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

settings.register_profile("ci", settings(max_examples=1000))
settings.register_profile("dev", settings(max_examples=10))
settings.register_profile("debug", settings(max_examples=10,
                                            verbosity=Verbosity.verbose))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))


def my_emit(msg):
    """Custom emit"""
    return msg

cuebung_helper.emitter.print = builtins.print


@given(st.text())
def test_emit(arg):
    """Test the function with the correct argument type"""
    msg = {'msg': arg}
    msg_result = msg.copy()
    msg_result['msgtype'] = MsgType.message
    with patch('cuebung_helper.emitter.print', autospec=True) as mock_print:
        emit(msg)
        mock_print.assert_called_with(msg_result)


@given(st.text())
def test_set_emit(arg):
    """Test set_emit"""
    reset_emit()
    set_emit(my_emit)
    msg = {'msg': arg}
    msg_result = msg.copy()
    msg_result['msgtype'] = MsgType.message
    assert emit(msg) == msg_result


# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
