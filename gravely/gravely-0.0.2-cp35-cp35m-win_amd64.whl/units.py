# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""
A collection of constants to be used from configuration files.
Example:
from gravely.body import Body
from gravely.units import sec, hour
dt = 3 * sec
diagnostics_period = 1 * hour
"""

centimeter = cm = second = sec = gram = g = 1

minute = 60 * sec
hour = 60 * minute
day = 24 * hour
meter = m = 100 * cm
kilogram = kg = 1000 * gram
kilometer = km = 1000 * meter
