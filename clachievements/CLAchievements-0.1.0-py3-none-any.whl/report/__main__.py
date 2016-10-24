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

"""Display a progress summary."""

import argparse
import operator

from clachievements.achievements import iter_achievements
from clachievements.db import DB

UNLOCKED_LINE = "\033[92m✔\033[0m \033[1m{title}\033[0m: {description} (unlocked on {date})"
LOCKED_LINE = "\033[91m✘\033[0m \033[1m{title}\033[0m: {description}"

def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="clachievements.report",
        description=(
            "Display achievement progress."
            ),
        formatter_class=argparse.RawTextHelpFormatter,
        )

    return parser

def report():
    """Display achievement progress"""
    database = DB()
    locked = unlocked = 0
    for achievement in sorted(iter_achievements(), key=operator.attrgetter('title')):
        unlock_date = database.unlock_date(achievement)
        if unlock_date is None:
            line = LOCKED_LINE
            unlocked += 1
        else:
            line = UNLOCKED_LINE
            locked += 1
        print(line.format(
            title=achievement.title,
            description=achievement.description(),
            date=unlock_date,
            ))
    summary = "{}% completed".format((locked * 100) // (locked + unlocked))
    print("-"*len(summary))
    print(summary)


def main():
    """Main function"""

    commandline_parser().parse_args()
    report()

if __name__ == "__main__":
    main()
