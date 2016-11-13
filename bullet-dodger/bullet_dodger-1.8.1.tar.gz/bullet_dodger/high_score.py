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

from .global_constants import HIGHEST_SCORE_PATH


def load_highest_score():
    with open(HIGHEST_SCORE_PATH, 'r') as highest_score_file:
        highest_score = int(highest_score_file.readlines()[0])
    return highest_score


def save_highest_score(highest_score):
    with open(HIGHEST_SCORE_PATH, 'w') as highest_score_file:
        highest_score_file.write(str(highest_score))
