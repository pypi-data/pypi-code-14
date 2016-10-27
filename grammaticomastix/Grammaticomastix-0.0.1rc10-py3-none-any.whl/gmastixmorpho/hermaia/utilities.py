#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Hermaia Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Hermaia.
#    Hermaia is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Hermaia is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Hermaia.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏Hermaia❏ : utilities.py

    Some usefull functions required by the Hermaia project.

    See the project's main page at https//github.com/suizokukan/hermaia
    ____________________________________________________________________________

    functions defined in this file :

    ● get_current_timestamp(self)
    ● textdiff_distance(str_a, str_b)
    ____________________________________________________________________________

    coding standards:
    ˮ ▶ class docstring : normal classes
    ˮ
    ˮ For each class, give the following informations :
    ˮ class attribute(s), instance attribute(s), method(s)
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ ▶ class docstring : namedtuple classes
    ˮ
    ˮ For each class, give only the instance attribute(s).
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ
    ˮ ▶ __init__()
    ˮ
    ˮ The arguments of an __init__() method have to be written one
    ˮ argument by line. If a __init__() method is called inside
    ˮ a __init__() method, the arguments have also to be be written
    ˮ one argument by line.
    ˮ
"""
import time
from difflib import SequenceMatcher

#///////////////////////////////////////////////////////////////////////////////
def get_current_timestamp():
    """
        get_current_timestamp()
        ________________________________________________________________________

        This function returns the (int)current time stamp.
        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE : the expected integer
    """
    return int(time.time())

#///////////////////////////////////////////////////////////////////////////....
def textdiff_distance(str_a, str_b):
    """
        textdiff_distance()
        ________________________________________________________________________

        This function returns the textdiff distance between the two
        strings <str_a, str_b>.

            E.g. textdiff_distance("a", "a") = 1
                 textdiff_distance("ab", "ac") = 0.3333
                 textdiff_distance("cheval", "chevaux") = 0.25
        ________________________________________________________________________

        PARAMETERS :

        ▪ str_a     : (str)
        ▪ str_b     : (str)

        RETURNED VALUE : a float greater than 0, smaller or equal to 1.
    """
    distance = SequenceMatcher(a=str_a, b=str_b).get_opcodes()
    accuracy = 1

    for expression in distance:
        if expression[0] != "equal":
            accuracy += (expression[2]-expression[1])+(expression[4]-expression[3])

    return float(1/accuracy)
