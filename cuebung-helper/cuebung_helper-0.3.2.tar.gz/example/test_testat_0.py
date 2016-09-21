"""
    COPYRIGHT (C) 2016 by Sebastian Stigler

    NAME
        test_testat_0.py

    FIRST RELEASE
        2016-07-06  Sebastian Stigler  sebastian.stigler@hs-aalen.de

"""

import pytest
from cuebung_helper import RunCode, ReferenceReturnObject

PROGRAM_NAME = 'testat-0'
IGNORE_COMPILER_WARNINGS = False


def int_arith_avg(args):
    """Reference implementation"""
    a, b = args
    ret = int((a + b) / 2)
    reference = ReferenceReturnObject(["%d" % (ret)])

    return reference

TESTCASES = [(0, 0), (1, 0), (42, 21), (1, 1), (3, 9), (4, 2), (-1120, 1110),
             (-24, -51)]


@pytest.fixture(params=TESTCASES, ids=[repr(tst) for tst in TESTCASES])
def args(request):
    """Iterate over all testcases"""
    return request.param


def test_testat_0(filename, args):
    """Test the c code and compare to reference implementation"""
    result = RunCode(filename, args, ['%d'] * len(args)).run(use_stdin=True)
    reference = int_arith_avg(args)
    assert reference.validate(result)

# vim: ft=python ts=4 sta sw=4 et ai
# python: 3
