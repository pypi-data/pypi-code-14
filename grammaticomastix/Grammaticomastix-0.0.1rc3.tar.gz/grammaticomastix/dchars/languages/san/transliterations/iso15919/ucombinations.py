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
    ❏DChars❏ : dchars/languages/san/transliterations/iso15919/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.san.dcharacter import DCharacterSAN
from dchars.languages.san.transliterations.iso15919.iso15919 import dchar__get_translit_str

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

    SAN = new_dstring( 'san' )
    dstring = SAN()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters__vowels = (
                                  'A',
                                  'AA',
                                  'I',
                                  'II',
                                  'U',
                                  'UU',
                                  'VOCALIC R',
                                  'VOCALIC RR',
                                  'VOCALIC L',
                                  'VOCALIC LL',
                                  'SHORT E',
                                  'E',
                                  'SHORT O',
                                  'O',
                                  'AI',
                                  'AU',
                                )

    base_characters  = ( 'KA',
                         'KHA',
                         'GA',
                         'GHA',
                         'NGA',
                         'CA',
                         'CHA',
                         'JA',
                         'JHA',
                         'NYA',
                         'TTA',
                         'TTHA',
                         'DDA',
                         'DDHA',
                         'NNA',
                         'TA',
                         'THA',
                         'DA',
                         'DHA',
                         'NA',
                         'PA',
                         'PHA',
                         'BA',
                         'BHA',
                         'MA',
                         'YA',
                         'RA',
                         'LA',
                         'LLA',
                         'VA',
                         'SHA',
                         'SSA',
                         'SA',
                         'HA',
                         'DEVANAGARI SIGN VISARGA', )

    #-----------------------------------------------------------------------
    # (1/2) simple characters
    #-----------------------------------------------------------------------
    for base_char in base_characters__vowels:

        dchar = DCharacterSAN( dstring_object = dstring,
                               base_char = base_char,
                               accent = None,
                               punctuation = False,
                               nukta = False,
                               anusvara_candrabindu = None,
                               virama = False,
                               anudatta = False,
                               is_an_independent_vowel = True,
                               dependentvowel = None,
                               )

        txt = dchar__get_translit_str(dstring_object = dstring,
                                      prev_dchar = None,
                                      dchar = dchar)

        res.append( str(dchar) + "{" + txt + "} " )


    for base_char in base_characters:

        dchar = DCharacterSAN( dstring_object = dstring,
                       base_char = base_char,
                       accent = None,
                       punctuation = False,
                       nukta = False,
                       anusvara_candrabindu = None,
                       virama = False,
                       anudatta = False,
                       is_an_independent_vowel = False,
                       dependentvowel = None,
                     )

        txt = dchar__get_translit_str(dstring_object = dstring,
                                      prev_dchar = None,
                                      dchar = dchar)

        res.append( str(dchar) + "{" + txt + "} " )


    #-----------------------------------------------------------------------
    # (2/2) complex characters
    #-----------------------------------------------------------------------
    combinations = (itertools.product(
                                       # base_chars
                                       ('KA',),

                                       # anusvara_candrabindu
                                       #(None,
                                       # "DEVANAGARI SIGN ANUSVARA",
                                       # "DEVANAGARI SIGN INVERTED CANDRABINDU",
                                       # 'DEVANAGARI SIGN CANDRABINDU',
                                       # ),

                                       # virama
                                       #( False, True ),

                                       # anudatta
                                       #( False, True ),

                                       # dependentvowel
                                       (      None,
                                              'AA',
                                              'I',
                                              'II',
                                              'U',
                                              'UU',
                                              'VOCALIC R',
                                              'VOCALIC RR',
                                              #'CANDRA E',
                                              #'SHORT E',
                                              'E',
                                              'AI',
                                              #'CANDRA O',
                                              #'SHORT O',
                                              'O',
                                              'AU',
                                              'VOCALIC L',
                                              'VOCALIC LL',
                                       ),

                                       ))

    for base_char, dependentvowel in combinations:

        add_this_char = True

        if base_char == 'DEVANAGARI SIGN VISARGA':
            if dependentvowel is not None:
                add_this_char = False

        if add_this_char:
            dchar = DCharacterSAN( dstring_object = dstring,
                                   base_char = base_char,
                                   accent = None,
                                   punctuation = None,
                                   nukta = False,
                                   anusvara_candrabindu = None,
                                   virama = False,
                                   anudatta = False,
                                   is_an_independent_vowel = False,
                                   dependentvowel = dependentvowel,
                                   )

            txt = dchar__get_translit_str(dstring_object = dstring,
                                          prev_dchar = None,
                                          dchar = dchar)

            res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
