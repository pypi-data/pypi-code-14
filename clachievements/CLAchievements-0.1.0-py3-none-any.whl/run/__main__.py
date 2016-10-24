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

"""Run binaries, unlocking achievements if relevant."""

from contextlib import ExitStack
import os
import subprocess
import sys

from clachievements.achievements import iter_achievements
from clachievements.db import DB
from clachievements.run import Command

def run(args):
    """Wrapp command given in argument to look for achievements"""
    database = DB()
    command = Command(args)
    with ExitStack() as stack:
        for achievement in iter_achievements():
            if achievement.match_bin(command.bin):
                if database.is_locked(achievement):
                    stack.enter_context(achievement(command, database))
        sys.exit(subprocess.call(args, env=os.environ))

def main():
    """Main function"""
    run(sys.argv[1:])

if __name__ == "__main__":
    main()
