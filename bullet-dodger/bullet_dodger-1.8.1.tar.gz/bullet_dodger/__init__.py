# -*- coding: utf-8 -*-
# Bullet dodger: a game where you must dodge bullets
# Copyright (C) 2016 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '1.8.1'

import argparse

from pygame import quit

from .main import start_screen

PROGRAM_DESCRIPTION = 'fun and challenging mouse game where you must dodge bullets'

def main():
    args = parse_args()
    if args.version:
        print(__version__)
    else:
        start_screen()
        quit()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('--version', action='store_true',
                        help='output version information and exit')
    return parser.parse_args()
