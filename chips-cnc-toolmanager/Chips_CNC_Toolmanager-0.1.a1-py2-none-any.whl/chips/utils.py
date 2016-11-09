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

from PyQt4.QtGui import QTextEdit



def plaintext_from_richtext(field):
    """an alternative to camelot.view.utils.text_from_richtext that returns the content of a richtext field als plaintext instead as a list of lines using QTextEdit."""
    if field:
        te = QTextEdit()
        te.setHtml(field)
        plaintext=te.toPlainText()
        return unicode(plaintext)
    else:
        return None

    return plaintext


###CNC machining calculator functions
def calculate_F(S, CPT, flutes):
    """Calculate feedrate from Spindlespeed S, Chipload in mm, number of flutes"""
    F = S * CPT * flutes
    return F

def calculate_Fp(F, Fp_percent,  F_Z_max):
    """calculate plunge feedrate from F and plungefeedrate in percent, but limit to F_Z_max"""
    Fp = (F /100) * Fp_percent
    #limit Fp to machines capabilities
    if Fp > F_Z_max:
        Fp = F_Z_max
    return Fp
