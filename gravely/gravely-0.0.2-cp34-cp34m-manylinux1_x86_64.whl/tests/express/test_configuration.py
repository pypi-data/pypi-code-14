# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

import os
import tempfile
from unittest import mock

import gravely.configuration


TEST_CONFIG_STRING = '''
from gravely.body import Body
from gravely.units import kg, km, sec
ton = 1000 * kg
bodies = [Body(1*ton, x=100*km, vx=100*km/sec)]
'''
DEFAULT_DT = 100


def test_config_from_path():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(TEST_CONFIG_STRING.encode())
    f.close()
    c = gravely.configuration.from_path(f.name)
    os.unlink(f.name)
    _check_config(c)


def test_config_from_string():
    c = gravely.configuration.from_string(TEST_CONFIG_STRING)
    _check_config(c)


def _check_config(c):
    assert c.bodies[0]['m'] == 1000 * 1000
    assert c.bodies[0]['v'] == [100 * 1000 * 100, 0, 0]
    assert c.dt == DEFAULT_DT  # from default config


def test_config_autodetect_str1():
    c = gravely.configuration.autodetect(TEST_CONFIG_STRING)
    _check_config(c)


def test_config_autodetect_str2():
    c = gravely.configuration.autodetect('b = 4; a = b')
    _check_autoconfig(c)


def test_config_autodetect_dict():
    c = gravely.configuration.autodetect({'a': 4})
    _check_autoconfig(c)


@mock.patch('gravely.configuration.from_path')
def test_config_autodetect_path(mock_from_path):
    gravely.configuration.autodetect('/home/test/test.cfg.py')
    mock_from_path.assert_called_with('/home/test/test.cfg.py')


def test_config_autodetect_rerun():
    c = gravely.configuration.autodetect({'a': 4})
    c = gravely.configuration.autodetect(c)
    _check_autoconfig(c)


def test_config_autodetect_None():
    c = gravely.configuration.autodetect(None)
    assert c.dt == DEFAULT_DT


def _check_autoconfig(c):
    assert c.a == 4
    assert c.dt == DEFAULT_DT
