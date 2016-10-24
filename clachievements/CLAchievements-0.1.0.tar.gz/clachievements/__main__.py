#!/usr/bin/env python3

# Command Line Achievements
# Copyright 2016 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Main binary: dispatch subcommands to submodules."""

import argdispatch

import clachievements

def commandline_parser():
    """Return a command line parser."""

    parser = argdispatch.ArgumentParser(
        prog="clachievements",
        description=(
            "Various tools for Command Line Achievements."
            ),
        formatter_class=argdispatch.RawTextHelpFormatter,
        )

    parser.add_argument(
        '--version',
        help='Show version',
        action='version',
        version='%(prog)s ' + clachievements.VERSION
        )

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="List of available subcommands.",
        )
    subparsers.required = True
    subparsers.dest = "subcommand"
    subparsers.add_submodules("clachievements")

    return parser

def main():
    """Main function"""

    commandline_parser().parse_args()

if __name__ == "__main__":
    main()
