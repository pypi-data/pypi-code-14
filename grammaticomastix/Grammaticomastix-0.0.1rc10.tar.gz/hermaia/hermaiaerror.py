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
    ❏Hermaia❏ : hermaiaerror.py

    See the project's main page at https//github.com/suizokukan/hermaia
    ____________________________________________________________________________

    HermaiaError class
    _____________________________________________________________________________

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
import logger
LOGGER = logger.get_logger(__name__)  # you may add e.g. level=logger.INFO .

################################################################################
class HermaiaError(BaseException):
    """
        class HermaiaError
        ________________________________________________________________________

        This class allows to log the errors.
        ________________________________________________________________________

        no class attributes

        no instance attributes

        methods :
        ◐ __init__(self, context, message)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, context, message):
        """
            HermaiaError().__init__
            ____________________________________________________________________
            ____________________________________________________________________

            PARAMETERS :
            ▪ context   : (str) a string describing the context of the error,
                          e.g. a function name
            ▪ message   : (str) the error message

            no RETURNED VALUE
        """
        BaseException.__init__(self, "["+context+"] "+message)
        LOGGER.error("[{0}] {1}".format(context, message))
