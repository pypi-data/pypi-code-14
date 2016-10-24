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

"""Reset progress."""

import argparse
import os
import sys

from clachievements.db import db_path

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="clachievements.reset",
        description=(
            "Reset progress."
            ),
        formatter_class=argparse.RawTextHelpFormatter,
        )

    return parser

def confirm():
    """Ask for confirmation from user."""
    for _ in range(3):
        try:
            answer = input("Any progress will be lost. Proceed? [yes/no] ")
        except (KeyboardInterrupt, EOFError):
            print()
            return False
        if answer == "yes":
            return True
        if answer == "no":
            return False
        print("Please answer 'yes' or 'no'.")
    return False

def reset():
    """Reset progress"""
    if confirm():
        path = db_path()
        if not os.path.exists(path):
            return 0
        try:
            os.remove(path)
        except OSError as error:
            print("Error while removing '{}': {}.".format(
                path,
                str(error),
                ))
            return 1
        return 0
    else:
        print("Aborted.")
        return 0

def main():
    """Main function"""

    commandline_parser().parse_args()
    sys.exit(reset())

if __name__ == "__main__":
    main()
