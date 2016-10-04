#!/usr/bin/python3
# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
A module to make gravely tests runnable with, for example:
./gravely test
python3 -m gravely test
python3 -m path_to_gravely_source test
python3 -c 'import gravely.tests; gravely.tests.run()
path/to/gravely/source/gravely/tests/run.py
"""


def detect_tests_dir():
    import os
    try:
        import gravely.tests
        path = os.path.dirname(os.path.realpath(gravely.tests.__file__))
    except ImportError:
        path = __file__
    return os.path.dirname(os.path.realpath(path))


def run(nosetests_args=None):
    """Simulates running nosetests -w path/to/gravely."""
    import nose
    nosetests_args = nosetests_args or []
    tests_dir = detect_tests_dir()
    nose_config = nose.config.Config(includeExe=True, verbosity=2)
    nose_config.configureWhere(tests_dir)
    nose.main(config=nose_config, argv=(['nosetests'] + nosetests_args))


if __name__ == '__main__':
    run()
