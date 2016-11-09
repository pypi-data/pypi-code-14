#!/usr/bin/python
# -*- coding: utf-8 -*-

##This file is part of Chips - CNC tool test and management suite
##Copyright (C) 2016  Sebastian Stetter
##https://bitbucket.org/sebste/chips

##This program is free software; you can redistribute it and/or
##modify it under the terms of the GNU General Public License
##as published by the Free Software Foundation; either version 2
##of the License, or (at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

##This file provides some basic machining calculation functions

from __future__ import division
from math import pi

def S(mat_vcc,  tool_diameter):
    """calculation of spindle speed in RPM"""
    n = (mat_vcc * 1000) / (pi * tool_diameter)
    return round(n)

def F(CPT,  S,  flutes):
    """calculation of feed rate: requires CPT (feed per tooth in mm), S (spindle speed in RPM) and the number of flutes of the tool"""

    F = S * CPT * flutes
    return round(F)

def Fplunge(F, minFplunge=None, F_FP_ratio=None,  plunge_angle=None):
    """calculation of plunge feed rate, based on F (horizontal feedrate) and
    plunge angle (90deg being vertical, 1deg being almost horizontal. minFplunge is the minimum Fplunge that has to be returned
    """
    if plunge_angle == None and F_FP_ratio !=None:
        #ratio based calculation
        Fp = F * F_FP_ratio
        if minFplunge and minFplunge > Fp:
            return minFplunge
        else:
            return round(Fp)

    elif plunge_angle and plunge_angle > 0 < 90:
        #angle based calculation
        #the flatter the angle, the higher closer the feed rate can be to the regular feedrate
        factor = 1 / 90 * (90 - plunge_angle)
        Fp = F * factor

        if minFplunge and minFplunge > Fp:
            return minFplunge
        else:
            return round(Fp)
        if minFplunge and minFplunge > Fp:
            return minFplunge
        else:
            return round(Fp)

    else:
        return None


def VCC(S, tool_diameter):
    """calculation of cuting speed Vc, based on spindle speed and tool diameter"""
    Vcc = pi * tool_diameter * S / 1000
    return round(Vcc)


#makes not much sense because it depends on the machine and is mostly static
#def calculate_Ap(tool_diameter,  percent_of_dia):
#    """calculation of Ap"""
#    pass


def Ae(tool_diameter,  percent_of_dia):
    """calculation of Ae"""
    return round(tool_diameter / 100 * percent_of_dia , 4)
