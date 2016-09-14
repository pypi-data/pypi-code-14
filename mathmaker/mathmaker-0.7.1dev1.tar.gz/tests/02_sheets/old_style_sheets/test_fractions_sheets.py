# -*- coding: utf-8 -*-

# Mathmaker creates automatically maths exercises sheets
# with their answers
# Copyright 2006-2016 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker.

# Mathmaker is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from mathmaker.lib import shared
from mathmaker.lib.sheet import AVAILABLE


def test_simplification():
    """Checks if 'fraction-simplification' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['fraction-simplification'][0]()))


def test_product_and_quotient():
    """
    Checks if 'fractions-product-and-quotient' is generated without any error.
    """
    shared.machine.write_out(
        str(AVAILABLE['fractions-product-and-quotient'][0]()))


def test_sum():
    """Checks if 'fractions-sum' is generated without any error."""
    shared.machine.write_out(str(AVAILABLE['fractions-sum'][0]()))
