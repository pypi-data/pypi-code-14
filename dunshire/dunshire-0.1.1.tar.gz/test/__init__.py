"""
The whole test suite.

This module compiles the doctests and unittests from the rest of the
codebase into one big TestSuite() and the runs it. It also provides a
function :func:`build_suite` that merely builds the suite; the result
can be used by setuptools.
"""

from unittest import TestLoader, TestSuite, TextTestRunner
from doctest import DocTestSuite, ELLIPSIS

from dunshire import cones
from dunshire import errors
from dunshire import matrices
from dunshire import games
from test import matrices_test
from test import randomgen
from test import symmetric_linear_game_test

def build_suite(doctests=True):
    """
    Build our test suite, separately from running it.

    Parameters
    ----------

    doctests : bool
        Do you want to build the doctests, too? During random testing,
        the answer may be "no."

    """
    suite = TestSuite()
    if doctests:
        suite.addTest(DocTestSuite(cones))
        suite.addTest(DocTestSuite(errors, optionflags=ELLIPSIS))
        suite.addTest(DocTestSuite(games, optionflags=ELLIPSIS))
        suite.addTest(DocTestSuite(matrices, optionflags=ELLIPSIS))
        suite.addTest(DocTestSuite(symmetric_linear_game_test))
        suite.addTest(DocTestSuite(randomgen, optionflags=ELLIPSIS))
    slg_tests = TestLoader().loadTestsFromModule(symmetric_linear_game_test)
    suite.addTest(slg_tests)
    mat_tests = TestLoader().loadTestsFromModule(matrices_test)
    suite.addTest(mat_tests)
    return suite

def run_suite(suite):
    """
    Run all of the unit and doctests for the :mod:`dunshire` and
    :mod:`test` packages.
    """
    runner = TextTestRunner(verbosity=1)
    return runner.run(suite)
