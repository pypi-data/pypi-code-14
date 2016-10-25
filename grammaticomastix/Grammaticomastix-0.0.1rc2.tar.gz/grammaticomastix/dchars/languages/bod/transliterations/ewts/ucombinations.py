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
    ❏DChars❏ : dchars/languages/bod/transliterations/ewts/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.bod.dcharacter import DCharacterBOD
from dchars.languages.bod.transliterations.ewts.ewts import dstring__get_translit_str

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

    dstring = new_dstring( 'bod' )()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters  = ('K',
                        'KH',
                        'G',
                        'GH',
                        'NG',
                        'C',
                        'CH',
                        'J',
                        'NY',
                        'TT',
                        'TTH',
                        'DD',
                        'DDH',
                        'NN',
                        'T',
                        'TH',
                        'D',
                        'DH',
                        'N',
                        'P',
                        'PH',
                        'B',
                        'BH',
                        'M',
                        'TS',
                        'TSH',
                        'DZ',
                        'DZH',
                        'W',
                        'ZH',
                        'Z',
                        '-',
                        'Y',
                        'R',
                        'L',
                        'SH',
                        'SS',
                        'S',
                        'H',
                        'KSS',

                        'A',
                       )

    #-----------------------------------------------------------------------
    # (1/2) simple characters
    #-----------------------------------------------------------------------
    for base_char in base_characters:

        dchar = DCharacterBOD( dstring_object = dstring,
                                base_char = base_char,
                                subj_consonants = None,
                                rnam_bcad = False,
                                punctuation = False,
                                halanta = False,
                                anusvara_candrabindu = None,
                                vowel1 = None,
                                vowel2 = None )

        dstring.append(dchar)
        dstring.update_istructs()

        txt = dstring__get_translit_str(dstring = dstring)

        res.append( str(dchar) + "{" + txt + "} " )

    #-----------------------------------------------------------------------
    # (2/2) complex characters
    #-----------------------------------------------------------------------
    combinations = (itertools.product(
                                       # base_chars
                                       ('K',),

                                       # vowel
                                       (      None,
                                              'AA',
                                              'I',
                                              'II',
                                              'U',
                                              'UU',
                                              'VOCALIC R',
                                              'VOCALIC RR',
                                              'VOCALIC L',
                                              'VOCALIC LL',
                                              'E',
                                              'AI',
                                              'O',
                                              'AU',
                                       )))

    for base_char, vowel in combinations:

        dchar = DCharacterBOD( dstring_object = dstring,
                                base_char = base_char,
                                subj_consonants = None,
                                rnam_bcad = False,
                                punctuation = False,
                                halanta = False,
                                anusvara_candrabindu = None,
                                vowel1 = vowel,
                                vowel2 = None )

        dstring.append(dchar)
        dstring.update_istructs()

        txt = dstring__get_translit_str(dstring = dstring)

        res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
