#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    DChars Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of DChars.
#    DChars is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DChars is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DChars.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏DChars❏ : dchars/languages/lat/transliterations/basic/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.fro.dcharacter import DCharacterFRO
from dchars.languages.fro.transliterations.basic.basic import dchar__get_translit_str

import itertools

#///////////////////////////////////////////////////////////////////////////
def get_usefull_combinations():
    """
            get_usefull_combinations()

            Return a (str)string with all the usefull combinations of characters,
            i.e. only the 'interesting' characters (not punctuation if it's too simple
            by example).

            NB : this function has nothing to do with linguistic or a strict
                 approach of the language. This function allows only to get the
                 most common and/or usefull characters of the writing system.

            NB : function required by the dchars-fe project.
    """
    res = []

    dstring = new_dstring( 'fro' )()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters  = ( 'a', 'æ', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                         'q', 'r', 's', 't', 'þ', 'ð', 'u', 'v',
                         'w', 'x', 'y', 'z', )

    #-----------------------------------------------------------------------
    # (1/2) simple characters
    #-----------------------------------------------------------------------
    for base_char in base_characters:
        for capital_letter in (False, True):

            dchar = DCharacterFRO( dstring_object = dstring,
                                   base_char = base_char,
                                   punctuation = False,
                                   capital_letter = capital_letter,
                                   cedilla = False,
                                   stress = 0)

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    #-----------------------------------------------------------------------
    # (2/2) complex characters
    #-----------------------------------------------------------------------
    combinations = (itertools.product(
                                       # base_char :
                                       ('a',),

                                       # capital_letter
                                       (False, True),

                                       # length
                                       ( None, "short", "long",),

                                       # stress
                                       (-1, 0, 1, 2),

                                       # cedilla
                                       (False, True),
                                       ))

    for base_char, capital_letter, length, stress in combinations:

        add_this_dchar = True

        if base_char not in ('a', 'e', 'i', 'o', 'u'):
            if stress != 0:
                add_this_dchar = False

        if base_char not in ('c',):
            if cedilla is True:
                add_this_dchar = False

        if add_this_dchar:
            dchar = DCharacterFRO( dstring_object = dstring,
                                   base_char = base_char,
                                   punctuation = False,
                                   capital_letter = capital_letter,
                                   stress = stress)

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
