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

import os

from .paths import get_config_dir

# Resolution
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_ALLOY_ORANGE = (196, 121, 67)
RED = (255, 0, 0)
YELLOW = (255, 255, 12)

# Highest score file
HIGHEST_SCORE_PATH = os.path.join(get_config_dir(), 'highest_score')
if not os.path.exists(HIGHEST_SCORE_PATH):
    with open(HIGHEST_SCORE_PATH, 'w') as highest_score_file:
        highest_score_file.write('0')
