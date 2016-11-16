#!/usr/bin/env python
"""
An implementation of __main__() that allows us to "run this module."
"""
from sys import argv

from test import build_suite, run_suite


def main(doctests, loop):
    """
    The main function for this module. It runs the tests.

    We take two command-line arguments. The first enables you to turn
    off the doctests, which are deterministic. The second tells us to
    repeat the test suite indefinitely rather than return the result of
    running it once. The flags usually occur together so that we don't
    waste time running the doctests in a loop.

    Parameters
    ----------

    doctests : bool
        Do you want to run the doctests?

    loop : bool
        Do you want to loop and rerun the tests indefinitely?

    """
    # Running the test suite clobbers it! And deepcopy() doesn't work
    # on a suite that contains doctests! ARRRGRRGRRGRHG!!!!!! You're all
    # idiots.
    result = run_suite(build_suite(doctests))

    if result.wasSuccessful() and not loop:
        return 0

    if loop:
        passed = 0
        while result.wasSuccessful():
            print('Passed: {:d}'.format(passed))
            passed += 1
            result = run_suite(build_suite(doctests))

    return 1


if __name__ == '__main__':
    exit(main(not "--no-doctests" in argv, '--loop' in argv))
