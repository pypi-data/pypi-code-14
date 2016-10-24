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

"""Display code to create aliases."""

import argparse
import textwrap

import clachievements

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="clachievements.alias",
        description=(
            "Display the shell code defining the aliases to enable Command Line Achievements."
            ),
        formatter_class=argparse.RawTextHelpFormatter,
        )

    return parser

ALIAS_CODE = textwrap.dedent("""
    for name in {binaries}
    do
        which $name > /dev/null && alias $name="python3 -m clachievements run $name"
    done
    """).strip().format(binaries=" ".join(clachievements.BINARIES))

def alias():
    """Display code to define aliases."""
    print(ALIAS_CODE)

def main():
    """Main function"""

    commandline_parser().parse_args()
    alias()

if __name__ == "__main__":
    main()
