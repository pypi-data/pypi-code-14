#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_smyte_pylib
----------------------------------

Tests for `smyte_pylib` module.
"""

import pytest
from mock import patch


from smyte_pylib.pacer import Pacer


def test_limit():
    'Ensure that every 5th test is true if limit=5'
    pacer = Pacer(5, 60)
    for attempt in range(100):
        assert pacer.test() == (attempt % 5 == 0)

@patch('time.time')
def test_time(mock_time):
    'Ensure pacing by time works as expected'
    mock_time.return_value = 0
    pacer = Pacer(1000, 1.0)

    assert pacer.test()
    assert not pacer.test()
    mock_time.return_value = 0.5
    assert not pacer.test()
    mock_time.return_value = 0.7
    assert not pacer.test()
    mock_time.return_value = 1.3
    assert pacer.test()
    mock_time.return_value = 2.7
    assert pacer.test()
    mock_time.return_value = 3.6
    assert not pacer.test()
    mock_time.return_value = 3.699
    assert not pacer.test()
    mock_time.return_value = 3.701
    assert pacer.test()
    mock_time.return_value = 4.7
    assert not pacer.test()
    mock_time.return_value = 4.702
    assert pacer.test()
    mock_time.return_value = 5.703
    assert pacer.test()
