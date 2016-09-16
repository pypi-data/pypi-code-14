#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests"""

from collections import namedtuple
from io import BytesIO
import os
import pytest
from hypothesis import given, settings, Verbosity, example
import hypothesis.strategies as st

from cuebung_helper.emitter import set_emit, MsgType, reset_emit
from cuebung_helper.helper import _cmplistofstrings, _cleanresult, Config
from cuebung_helper.returnobject import (ReturnObject, PopenReturnObject,
                                         EmitMessages, ReferenceReturnObject)

__author__ = "Sebastian Stigler"
__copyright__ = "Sebastian Stigler"
__license__ = "mit"

settings.register_profile("ci", settings(max_examples=1000))
settings.register_profile("dev", settings(max_examples=10))
settings.register_profile("debug", settings(max_examples=10,
                                            verbosity=Verbosity.verbose))
settings.load_profile(os.getenv(u'HYPOTHESIS_PROFILE', 'default'))


@given(st.lists(st.text()),
       st.lists(st.text()),
       st.lists(st.text()),
       st.integers(min_value=0, max_value=255),
       st.booleans(),
       st.text())
def test_returnobject(stdout, stderr, error, returncode, timedout, msg):
    """ Test the object with legal data"""
    obj = ReturnObject(stdout, stderr, returncode, timedout, error)
    assert _cmplistofstrings(stdout, obj.stdout)
    assert _cmplistofstrings(stderr, obj.stderr)
    assert returncode == obj.returncode
    assert timedout == obj.timedout
    assert _cmplistofstrings(error, obj.error)

    txt = ("{c}(stdout={o}, stderr={e}, returncode={r}, timedout={t}, "
           "error={x})")
    filled_txt = txt.format(c='ReturnObject', o=stdout, e=stderr, r=returncode,
                            t=timedout, x=error)
    assert filled_txt == repr(obj)
    vgldict = {'msg': msg, 'stdout': stdout, 'stderr': stderr,
               'returncode': returncode, 'timedout': timedout, 'error': error}
    assert vgldict == obj.to_dict(msg)


@given(st.lists(st.integers(), min_size=1),
       st.integers(min_value=256))
def test_returnobject_illegal_input(tstlst, tstint):
    """ Test the object with illegal data"""
    with pytest.raises(ValueError):
        ReturnObject(stdout=tstlst)

    with pytest.raises(ValueError):
        ReturnObject(stderr=tstlst)

    with pytest.raises(ValueError):
        ReturnObject(returncode=tstint)

    with pytest.raises(ValueError):
        ReturnObject(returncode=-tstint + 255)

    with pytest.raises(ValueError):
        ReturnObject(returncode=tstlst)

    with pytest.raises(ValueError):
        ReturnObject(timedout=tstlst)

    with pytest.raises(ValueError):
        ReturnObject(error=tstlst)


@given(st.lists(st.text()),
       st.lists(st.text()),
       st.lists(st.text()),
       st.integers(min_value=0, max_value=255),
       st.booleans())
def test_returnobject_eq(stdout, stderr, error, returncode, timedout):
    """ Test equality and inequality"""
    obj = ReturnObject(stdout, stderr, returncode, timedout, error)
    vglobj = ReturnObject(stdout, stderr, returncode, timedout, error)
    assert obj == vglobj
    assert not obj != vglobj  # pylint: disable=C0113

    err_stdout = stdout[:]
    err_stdout.append("test")
    err_stderr = stderr[:]
    err_stderr.append("test")
    err_returncode = (returncode + 1) % 256
    err_timedout = not timedout
    err_error = error[:]
    err_error.append("test")
    assert obj != ReturnObject(err_stdout, stderr, returncode, timedout, error)
    assert obj != ReturnObject(stdout, err_stderr, returncode, timedout, error)
    assert obj != ReturnObject(stdout, stderr, err_returncode, timedout, error)
    assert obj != ReturnObject(stdout, stderr, returncode, err_timedout, error)
    assert obj != ReturnObject(stdout, stderr, returncode, timedout, err_error)
    with pytest.raises(TypeError):
        obj == 1  # pylint: disable=W0104


@given(st.lists(st.binary()),
       st.lists(st.binary()),
       st.integers(min_value=0, max_value=255),
       st.booleans())
def test_popenreturnobject_vgl(stdout, stderr, returncode, use_stdin):
    """ Test the object with legal data"""
    popen = namedtuple('Popen', 'stdout stderr returncode')
    b_stdout = b'\n'.join(stdout)
    b_stderr = b'\n'.join(stderr)
    result = popen(BytesIO(b_stdout), BytesIO(b_stderr), returncode)
    obj = PopenReturnObject.from_popen(result, cfg=Config(use_stdin, ' ', ' '))
    vglobj = ReturnObject(_cleanresult(BytesIO(b_stdout)),
                          _cleanresult(BytesIO(b_stderr)), returncode)
    assert vglobj == obj
    assert obj.cfg.use_stdin == use_stdin


@given(st.sampled_from([st.integers(), st.floats(), st.text()]),
       st.sampled_from([st.integers(), st.floats(), st.booleans()]))
def test_popenreturnobject_illegal(use_stdin, command):
    """Test the object with additional illegal input"""

    with pytest.raises(ValueError):
        PopenReturnObject(cfg=use_stdin)

    with pytest.raises(ValueError):
        PopenReturnObject(cfg=Config(use_stdin, 'NA', 'NA'))

    with pytest.raises(ValueError):
        PopenReturnObject(cfg=Config(True, command, 'NA'))

    with pytest.raises(ValueError):
        PopenReturnObject(cfg=Config(True, 'NA', command))


@given(st.text(),
       st.text(),
       st.integers(),
       st.booleans())
def test_emitmessages(stdin_txt, commandline_arg_txt, error_txt, use_stdin):
    """Test the emitmessage object"""
    emt = EmitMessages()

    with pytest.raises(ValueError):
        emt.command_templ = error_txt

    emt.use_stdin = use_stdin

    if emt.use_stdin:
        emt.command_templ = stdin_txt
        assert emt.command_templ == stdin_txt
    else:
        emt.command_templ = commandline_arg_txt
        assert emt.command_templ == commandline_arg_txt


def myemit(msg):
    """help function"""
    global RETURNVALUE  # pylint: disable=W0603
    RETURNVALUE = msg

RETURNVALUE = None


@given(st.sampled_from([st.text(), None]))
def test_rro_validate_basic(msg_extra):
    """Simple validation test"""
    obj = PopenReturnObject()
    reference = ReferenceReturnObject()

    set_emit(myemit)
    assert reference.validate(obj, msg_extra)
    reset_emit()

    assert RETURNVALUE['msgtype'] == MsgType.passed
    assert RETURNVALUE['msg'] == reference.txt.passed.general
    if msg_extra is not None:
        assert RETURNVALUE['msg_extra'] == msg_extra


def test_rro_validate_invalide_args():
    """Test for invalid object"""

    obj = ReturnObject()
    reference = ReferenceReturnObject()

    with pytest.raises(TypeError):
        reference.validate(obj)

    with pytest.raises(TypeError):
        reference.validate(None)


@given(st.binary(min_size=1),
       st.binary(min_size=1),
       st.binary(min_size=1),
       st.integers(min_value=1, max_value=255),
       st.booleans())
@example(b'\n', b'\x00', b'\x00', 1, False)
def test_rro_validate_not_eq(stdout, stderr, error, returncode, use_stdin):
    """ Test the object with differnt results"""
    popen = namedtuple('Popen', 'stdout stderr returncode')
    stdout += b'x'
    stderr += b'x'
    error += b'x'
    result = popen(BytesIO(stdout), BytesIO(stderr), returncode)
    cfg = Config(use_stdin, ' ', ' ')
    obj = PopenReturnObject.from_popen(result, error, cfg)
    obj._timedout = True  # pylint: disable=W0212

    reference = ReferenceReturnObject()

    set_emit(myemit)
    # timedout
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed_timedout
    reference.dont_check.timedout = True
    # returncode
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed_returncode
    reference.dont_check.returncode = True
    # output_linecount
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed_output_linecount
    reference.dont_check.output_linecount = True
    # stderr
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed_stderr
    reference.dont_check.stderr = True
    # stdout
    assert not reference.validate(obj)
    print(RETURNVALUE)
    assert RETURNVALUE['msgtype'] == MsgType.failed_stdout
    reference.dont_check.stdout = True
    # error
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed_error
    reference.dont_check.error = True
    # general
    assert not reference.validate(obj)
    assert RETURNVALUE['msgtype'] == MsgType.failed
    reset_emit()
# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
