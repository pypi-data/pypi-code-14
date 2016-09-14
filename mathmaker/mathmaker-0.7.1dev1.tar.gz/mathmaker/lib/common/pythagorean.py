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

from mathmaker.lib import error

ALL_TRIPLES_5_100 = [
    [3, 4, 5],
    [6, 8, 10],
    [5, 12, 13],
    [9, 12, 15],
    [8, 15, 17],
    [12, 16, 20],
    [7, 24, 25],
    [15, 20, 25],
    [10, 24, 26],
    [20, 21, 29],
    [18, 24, 30],
    [16, 30, 34],
    [21, 28, 35],
    [12, 35, 37],
    [15, 36, 39],
    [24, 32, 40],
    [9, 40, 41],
    [27, 36, 45],
    [14, 48, 50],
    [24, 45, 51],
    [20, 48, 52],
    [28, 45, 53],
    [33, 44, 55],
    [40, 42, 58],
    [36, 48, 60],
    [11, 60, 61],
    [16, 63, 65],
    [25, 60, 65],
    [33, 56, 65],
    [39, 52, 65],
    [32, 60, 68],
    [42, 56, 70],
    [48, 55, 73],
    [24, 70, 74],
    [21, 72, 75],
    [45, 60, 75],
    [30, 72, 78],
    [48, 64, 80],
    [18, 80, 82],
    [13, 84, 85],
    [36, 77, 85],
    [40, 75, 85],
    [51, 68, 85],
    [60, 63, 87],
    [39, 80, 89],
    [54, 72, 90],
    [35, 84, 91],
    [57, 76, 95],
    [65, 72, 97],
    [28, 96, 100]]

TRIPLES_101_200_WO_TEN_MULTIPLES = [
    [20, 99, 101],
    [48, 90, 102],
    [40, 96, 104],
    [63, 84, 105],
    [56, 90, 106],
    [60, 91, 109],
    [66, 88, 110],
    [36, 105, 111],
    [15, 112, 113],
    [69, 92, 115],
    [80, 84, 116],
    [45, 108, 117],
    [56, 105, 119],
    [72, 96, 120],
    [22, 120, 122],
    [27, 120, 123],
    [35, 120, 125],
    [44, 117, 125],
    [75, 100, 125],
    [32, 126, 130],
    [66, 112, 130],
    [78, 104, 130],
    [81, 108, 135],
    [64, 120, 136],
    [88, 105, 137],
    [84, 112, 140],
    [55, 132, 143],
    [17, 144, 145],
    [24, 143, 145],
    [87, 116, 145],
    [100, 105, 145],
    [96, 110, 146],
    [48, 140, 148],
    [51, 140, 149],
    [42, 144, 150],
    [72, 135, 153],
    [93, 124, 155],
    [60, 144, 156],
    [85, 132, 157],
    [84, 135, 159],
    [96, 128, 160],
    [36, 160, 164],
    [99, 132, 165],
    [65, 156, 169],
    [119, 120, 169],
    [26, 168, 170],
    [72, 154, 170],
    [102, 136, 170],
    [52, 165, 173],
    [120, 126, 174],
    [49, 168, 175],
    [105, 140, 175],
    [78, 160, 178],
    [108, 144, 180],
    [19, 180, 181],
    [70, 168, 182],
    [33, 180, 183],
    [57, 176, 185],
    [60, 175, 185],
    [104, 153, 185],
    [111, 148, 185],
    [88, 165, 187],
    [114, 152, 190],
    [95, 168, 193],
    [130, 144, 194],
    [48, 189, 195],
    [75, 180, 195],
    [99, 168, 195],
    [117, 156, 195],
    [28, 195, 197],
    [56, 192, 200],
]

ALL_TRIPLES_5_200 = [
    [3, 4, 5],
    [6, 8, 10],
    [5, 12, 13],
    [9, 12, 15],
    [8, 15, 17],
    [12, 16, 20],
    [7, 24, 25],
    [15, 20, 25],
    [10, 24, 26],
    [20, 21, 29],
    [18, 24, 30],
    [16, 30, 34],
    [21, 28, 35],
    [12, 35, 37],
    [15, 36, 39],
    [24, 32, 40],
    [9, 40, 41],
    [27, 36, 45],
    [14, 48, 50],
    [30, 40, 50],
    [24, 45, 51],
    [20, 48, 52],
    [28, 45, 53],
    [33, 44, 55],
    [40, 42, 58],
    [36, 48, 60],
    [11, 60, 61],
    [16, 63, 65],
    [25, 60, 65],
    [33, 56, 65],
    [39, 52, 65],
    [32, 60, 68],
    [42, 56, 70],
    [48, 55, 73],
    [24, 70, 74],
    [21, 72, 75],
    [45, 60, 75],
    [30, 72, 78],
    [48, 64, 80],
    [18, 80, 82],
    [13, 84, 85],
    [36, 77, 85],
    [40, 75, 85],
    [51, 68, 85],
    [60, 63, 87],
    [39, 80, 89],
    [54, 72, 90],
    [35, 84, 91],
    [57, 76, 95],
    [65, 72, 97],
    [28, 96, 100],
    [60, 80, 100],
    [20, 99, 101],
    [48, 90, 102],
    [40, 96, 104],
    [63, 84, 105],
    [56, 90, 106],
    [60, 91, 109],
    [66, 88, 110],
    [36, 105, 111],
    [15, 112, 113],
    [69, 92, 115],
    [80, 84, 116],
    [45, 108, 117],
    [56, 105, 119],
    [72, 96, 120],
    [22, 120, 122],
    [27, 120, 123],
    [35, 120, 125],
    [44, 117, 125],
    [75, 100, 125],
    [32, 126, 130],
    [50, 120, 130],
    [66, 112, 130],
    [78, 104, 130],
    [81, 108, 135],
    [64, 120, 136],
    [88, 105, 137],
    [84, 112, 140],
    [55, 132, 143],
    [17, 144, 145],
    [24, 143, 145],
    [87, 116, 145],
    [100, 105, 145],
    [96, 110, 146],
    [48, 140, 148],
    [51, 140, 149],
    [42, 144, 150],
    [90, 120, 150],
    [72, 135, 153],
    [93, 124, 155],
    [60, 144, 156],
    [85, 132, 157],
    [84, 135, 159],
    [96, 128, 160],
    [36, 160, 164],
    [99, 132, 165],
    [65, 156, 169],
    [119, 120, 169],
    [26, 168, 170],
    [72, 154, 170],
    [80, 150, 170],
    [102, 136, 170],
    [52, 165, 173],
    [120, 126, 174],
    [49, 168, 175],
    [105, 140, 175],
    [78, 160, 178],
    [108, 144, 180],
    [19, 180, 181],
    [70, 168, 182],
    [33, 180, 183],
    [57, 176, 185],
    [60, 175, 185],
    [104, 153, 185],
    [111, 148, 185],
    [88, 165, 187],
    [114, 152, 190],
    [95, 168, 193],
    [130, 144, 194],
    [48, 189, 195],
    [75, 180, 195],
    [99, 168, 195],
    [117, 156, 195],
    [28, 195, 197],
    [56, 192, 200],
    [120, 160, 200]
]


# --------------------------------------------------------------------------
##
#   @brief Will return all [first_leg, second_leg] matching a given hypotenuse
def get_legs_matching_given_hypotenuse(side_length):
    if not type(side_length) == int:
        raise error.WrongArgument(str(side_length), "int")

    result = []

    for elt in ALL_TRIPLES_5_200:
        if elt[2] == side_length:
            result += [elt[0], elt[1]]

    return result


# --------------------------------------------------------------------------
##
#   @brief Will return all leg values matching a given one
def get_legs_matching_given_leg(side_length):
    if not type(side_length) == int:
        raise error.WrongArgument(str(side_length), "int")

    result = []

    for elt in ALL_TRIPLES_5_200:
        if elt[0] == side_length:
            result += [elt[1]]

        elif elt[1] == side_length:
            result += [elt[0]]

    return result
