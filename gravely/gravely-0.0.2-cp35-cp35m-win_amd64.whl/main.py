# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
Main module for gravely,
a gravity simulator written to taste modern Python packaging practices.
"""

import argparse
import sys

from . import diagnostics
from . import simulation
from . import tests


def main(config_filename=None):
    """Process command line arguments, execute appropriate subcommand."""
    description = "gravely, a gravity simulator. Copyright (c) LCODE team."
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(help='subcommand to execute')
    parser.add_argument('--config', default=config_filename,
                        help='configuration file')

    parser_run = subparsers.add_parser('run', help='run a simulation')
    parser_run.set_defaults(func=subcommand_run)

    parser_test = subparsers.add_parser('test', help='run tests')
    parser_test.add_argument('nosetests_args', nargs=argparse.REMAINDER)
    parser_test.set_defaults(func=subcommand_test)

    parser_animate = subparsers.add_parser('animate',
                                           help='draw an animated graph')
    parser_animate.set_defaults(func=subcommand_animate)

    args, extra = parser.parse_known_args()
    if 'func' not in args:
        parser.print_usage()
        sys.exit(1)
    args.func(args, extra)


def subcommand_run(args, extra):
    """Process subcommand 'run' - run a simulation."""
    assert not extra  # TODO: log a warning
    simulation.run(args.config)


def subcommand_test(args, extra):
    """Process subcommand 'test' - run tests."""
    tests.run(args.nosetests_args + extra)


def subcommand_animate(args, extra):
    """Process subcommand 'animate' - draw an animated graph."""
    assert not extra  # TODO: log a warning
    diagnostics.animate(args.config)


if __name__ == '__main__':  # pragma: no cover
    main()
