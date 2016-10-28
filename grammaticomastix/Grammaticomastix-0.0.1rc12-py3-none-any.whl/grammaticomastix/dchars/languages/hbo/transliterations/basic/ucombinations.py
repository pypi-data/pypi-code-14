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
    ❏DChars❏ : dchars/languages/hbo/transliterations/basic/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.hbo.dcharacter import DCharacterHBO
from dchars.languages.hbo.transliterations.basic.basic import dchar__get_translit_str

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

    HBO = new_dstring( 'hbo' )
    dstring = HBO()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters = ( 'א',
                        'ב',
                        'ג',
                        'ד',
                        'ה',
                        'ו',
                        'ז',
                        'ח',
                        'ט',
                        'י',
                        'כ',
                        'ל',
                        'מ',
                        'נ',
                        'ס',
                        'ע',
                        'פ',
                        'צ',
                        'ק',
                        'ר',
                        'ש',
                        'ת' )

    #-----------------------------------------------------------------------
    # (1/2) simple characters
    #-----------------------------------------------------------------------
    for base_char in base_characters:
        for shin_sin_dot in (None,
                             "HEBREW POINT SHIN DOT",
                             "HEBREW POINT SIN DOT"):

            if base_char != 'SHIN':
                shin_sin_dot = None

            dchar = DCharacterHBO( dstring_object = dstring,
                                   base_char = base_char,
                                   contextual_form = None,
                                   shin_sin_dot = None,
                                   daghesh_mapiq = False,
                                   methegh = False,
                                   specialpoint = None,
                                   vowel = None,
                                   raphe = False,
                                   cantillation_mark = None )

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------

        #.......................................................................
        combinations = (itertools.product(
                                           # base_char :
                                           ( 'ב', ),

                                           # vowel :
                                           (None,
                                            "HEBREW POINT SHEVA",
                                            "HEBREW POINT HATAF SEGOL",
                                            "HEBREW POINT HATAF PATAH",
                                            "HEBREW POINT HATAF QAMATS",
                                            "HEBREW POINT HIRIQ",
                                            "HEBREW POINT TSERE",
                                            "HEBREW POINT SEGOL",
                                            "HEBREW POINT PATAH",
                                            "HEBREW POINT QAMATS",
                                            "HEBREW POINT HOLAM",
                                            "HEBREW POINT HOLAM HASER FOR VAV",
                                            "HEBREW POINT QUBUTS",
                                            "HEBREW POINT QAMATS QATAN"),
                                             ))

        for base_char, \
            vowel in combinations:

            dchar = DCharacterHBO( dstring_object = dstring,
                                    base_char = base_char,
                                    contextual_form = "initial+medium+final",
                                    shin_sin_dot = None,
                                    daghesh_mapiq = False,
                                    methegh = False,
                                    specialpoint = None,
                                    vowel = vowel,
                                    raphe = None,
                                    cantillation_mark = None, )

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

        #.......................................................................
        combinations = (itertools.product(
                                           # base_char :
                                           ( 'ש', ),

                                           # shin_sin_dot :
                                           (None, "HEBREW POINT SHIN DOT", "HEBREW POINT SIN DOT"),
                                          ))

        for base_char, shin_sin_dot, \
            in combinations:

            dchar = DCharacterHBO( dstring_object = dstring,
                                    base_char = base_char,
                                    contextual_form = "initial+medium+final",
                                    shin_sin_dot = shin_sin_dot,
                                    daghesh_mapiq = False,
                                    methegh = False,
                                    specialpoint = None,
                                    vowel = None,
                                    raphe = None,
                                    cantillation_mark = None, )

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
