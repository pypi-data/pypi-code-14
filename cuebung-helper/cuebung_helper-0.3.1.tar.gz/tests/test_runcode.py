#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests"""

import os
import pytest
from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st

from cuebung_helper import RunCode
from cuebung_helper.helper import Command

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

settings.register_profile("ci", settings(max_examples=1000))
settings.register_profile("dev", settings(max_examples=10))
settings.register_profile("debug", settings(max_examples=10,
                                            verbosity=Verbosity.verbose))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))

BASEPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts')


@given(st.lists(st.integers()),
       st.integers(min_value=0))
def test_runcode(args, timeout):
    """Basic test for RunCode"""
    cmd = os.path.join(BASEPATH, 'emptytest')
    formatlist = ['%d'] * len(args)
    if len(args) == 0:
        args = None
        vglargs = ()
        formatlist = None
        vglfmtlist = []
    else:
        args = tuple(args)
        vglargs = args
        vglfmtlist = formatlist
    txt = "{n}(cmd={c}, args={a}, formatlist={s}, timeout={t}, fifo={f})"
    filled = txt.format(n='RunCode', c=cmd, a=vglargs, s=vglfmtlist, t=timeout,
                        f='error')
    assert repr(RunCode(cmd, args, formatlist, timeout)) == filled


@given(st.integers(),
       st.lists(st.integers(), min_size=1),
       st.integers(max_value=-1))
def test_runcode_illegal_args(cmd, args, timeout):
    """Test the class with illegal paramertes"""
    with pytest.raises(ValueError):
        RunCode(cmd)

    with pytest.raises(ValueError):
        RunCode('')

    with pytest.raises(ValueError):
        RunCode(' ', args, ['%d'] * len(args))

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), "")

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), args)

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), ['Xd'] * len(args))

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), ['%d'] * (len(args) - 1))

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), ['%d'] * len(args), timeout)

    with pytest.raises(ValueError):
        RunCode(' ', tuple(args), ['%ü'] * len(args))

    with pytest.raises(TypeError):
        RunCode(' ', tuple(str(arg) for arg in args), ['%d'] * len(args))

    with pytest.raises(ValueError):
        RunCode(' ', fifo='')

    with pytest.raises(ValueError):
        RunCode(' ', fifo=cmd)

    with pytest.raises(ValueError):
        RunCode(Command(cmd, cmd))

    with pytest.raises(ValueError):
        RunCode(Command('xxx', ''))


@given(st.tuples(st.integers(), st.integers()))
def test_runcode_stdin(args):
    """Test the class in the use_stdin mode with valid entries"""
    cmd = os.path.join(BASEPATH, 'run_stdin.py')
    formatlist = ['%d'] * 2
    timeout = 1
    runcode = RunCode(cmd, args, formatlist, timeout)
    ret = runcode.run(use_stdin=True)
    assert not ret.timedout
    assert ret.returncode == 3
    assert ret.stderr == [str(args[1])]
    assert ret.stdout == [str(args[0])]


@given(st.tuples(st.integers(), st.integers()))
def test_runcode_commandline(args):
    """Test the class in the commandline argument mode with valid entries"""
    cmd = os.path.join(BASEPATH, 'run_commandline.py')
    formatlist = ['%d'] * 2
    timeout = 1
    runcode = RunCode(cmd, args, formatlist, timeout)
    ret = runcode.run(use_stdin=False)
    assert not ret.timedout
    assert ret.returncode == 4
    assert ret.stderr == [str(args[1])]
    assert ret.stdout == [str(args[0])]


@given(st.integers(min_value=2))
def test_runcode_timeout(timeout):
    """Test the timeout constraint"""
    cmd = 'sleep'
    args = (timeout, )
    formatlist = ['%d']
    runcode = RunCode(cmd, args, formatlist, timeout=0.1)
    ret = runcode.run()
    assert ret.timedout


@given(st.tuples(st.integers(), st.integers(), st.integers()))
def test_runcode_namedpipe(args):
    """Test the class in the use_stdin mode with valid entries"""
    cmd = os.path.join(BASEPATH, 'run_named_pipe.py')
    formatlist = ['%d'] * 3
    timeout = 1
    runcode = RunCode(cmd, args, formatlist, timeout, fifo='/tmp/namedpipe')
    ret = runcode.run(use_stdin=True)
    assert not ret.timedout
    assert ret.returncode == 3
    assert ret.stderr == [str(args[1])]
    assert ret.stdout == [str(args[0])]
    assert ret.error == [str(args[2])]
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
