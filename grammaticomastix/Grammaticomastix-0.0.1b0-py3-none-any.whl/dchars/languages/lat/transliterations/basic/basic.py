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
    ❏DChars❏ : dchars/languages/lat/transliterations/basic/basic.py
"""

from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.dicttools import invertdict
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
import re

################################################################################
# List of the available directions for this transliteration method :
#
#  +1 (text->transliteration)
#  -1 (transliteration->text)
#
################################################################################
AVAILABLE_DIRECTIONS = (-1, +1)

################################################################################
# transliteration's equivalences :
################################################################################
TRANS_EQUIVALENCES = ()

################################################################################
# transliteration's symbols :
################################################################################

#
# * CAVEAT ! If you modify these dictionaries, don't forget to modify their
#            corresponding symbols' dictionaries in symbols.py !
#
# LOWER_CASE[base_char] = transliterated character
LOWER_CASE = {"a"     : "a",
              "b"     : "b",
              'c'     : "c",
              'd'     : "d",
              'e'     : "e",
              'f'     : "f",
              'g'     : "g",
              'h'     : "h",
              'i'     : "i",
              'j'     : "j",
              'k'     : "k",
              'l'     : "l",
              'm'     : "m",
              'n'     : "n",
              'o'     : "o",
              'p'     : "p",
              'q'     : "q",
              'r'     : "r",
              's'     : "s",
              't'     : "t",
              'u'     : "u",
              'v'     : "v",
              'w'     : "w",
              'x'     : "x",
              'y'     : "y",
              'z'     : "z",
              }

# UPPER_CASE[base_char] = transliterated character
UPPER_CASE = {"a"     : "A",
              "b"     : "B",
              'c'     : "C",
              'd'     : "D",
              'e'     : "E",
              'f'     : "F",
              'g'     : "G",
              'h'     : "H",
              'i'     : "I",
              'j'     : "J",
              'k'     : "K",
              'l'     : "L",
              'm'     : "M",
              'n'     : "N",
              'o'     : "O",
              'p'     : "P",
              'q'     : "Q",
              'r'     : "R",
              's'     : "S",
              't'     : "T",
              'u'     : "U",
              'v'     : "V",
              'w'     : "W",
              'x'     : "X",
              'y'     : "Y",
              'z'     : 'Z',
             }

# PUNCTUATION[base_char] = transliterated character
PUNCTUATION = { '-'       : '-',
                ')'       : ')',
                '('       : '(',
                '['       : '[',
                ']'       : ']',
                '{'       : '{',
                '}'       : '}',
                '0'       : '0',
                '1'       : '1',
                '2'       : '2',
                '3'       : '3',
                '4'       : '4',
                '5'       : '5',
                '6'       : '6',
                '7'       : '7',
                '8'       : '8',
                '9'       : '9',
                ' '       : ' ',
                '.'       : '.',
                ','       : ',',
                ';'       : ';',
                '!'       : '!',
                '?'       : '?',
                '"'       : '"',
                "'"       : "'",
                ":"       : ":",
                '\n'      : '\n',
                '\r'      : '\r',
                '\t'      : '\t',
                "‘"       : '<2018>',
                "’"       : '<2019>',
                "᾽"       : '<1FBD>',
              }

LOWER_CASE_INVERSED = invertdict(LOWER_CASE, accept_duplicated_values=True)
UPPER_CASE_INVERSED = invertdict(UPPER_CASE)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)

DIACRITICS =  {
                "stress"        : "/",
                "short"         : "*",
                "long"          : "_",
                "diaeresis"     : "+",
              }
DIACRITICS_INVERSED = invertdict(DIACRITICS)

################################################################################
# transliteration's patterns :
# PATTERN  is used to cut one complex characters into its elements.
# PATTERN2 is used to cut several complex characters into a list of complex characters.
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.
DIAERESIS = isort_a_lstrings_bylen_nodup(
                 [re.escape(DIACRITICS['diaeresis'])] )
LENGTH = isort_a_lstrings_bylen_nodup(
                 [re.escape(DIACRITICS['short']),
                 re.escape(DIACRITICS['long'])] )
STRESS = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['stress']),])
LETTERS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(LOWER_CASE_INVERSED.keys())) + \
                regexstring_list(tuple(UPPER_CASE_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )

PATTERN_TXT = "((?P<base_char>({0}))" \
              "(?P<trans_stress>({1}))?" \
              "(?P<trans_length>({2}))?" \
              "(?P<trans_diaeresis>({3}))?" \
              ")".format("|".join(prepare_list_to_strformat(LETTERS)),
                         "|".join(prepare_list_to_strformat(STRESS)),
                         "|".join(prepare_list_to_strformat(LENGTH)),
                         "|".join(prepare_list_to_strformat(DIAERESIS)),
                         )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "(({0})" \
                "({1})?" \
                "({2})?" \
                "({3})?" \
                ")".format("|".join(prepare_list_to_strformat(LETTERS)),
                           "|".join(prepare_list_to_strformat(STRESS)),
                           "|".join(prepare_list_to_strformat(LENGTH)),
                           "|".join(prepare_list_to_strformat(DIAERESIS)),
                          )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')

PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, dchar):
    """
        function dchar__get_translit_str()

        dchar : DCharacterLAT object

        Return a transliterared string corresponding to <char>.
    """
    res = []

    if dchar.unknown_char:
        if dstring_object.options["anonymize the unknown characters"] == 'yes':
            return UNKNOWN_CHAR_SYMBOL
        else:
            return dchar.base_char

    if dchar.base_char is not None:

        if dchar.punctuation:
            res.append( PUNCTUATION[dchar.base_char] )
        else:
            if not dchar.capital_letter:
                # lower case :
                res.append( LOWER_CASE[dchar.base_char] )
            else:
                # upper case :
                res.append( UPPER_CASE[dchar.base_char] )

    if dchar.stress:
        res.append( DIACRITICS['stress'] )

    if dchar.length is not None:
        res.append( DIACRITICS[dchar.length] )

    if dchar.diaeresis:
        res.append( DIACRITICS['diaeresis'] )

    return "".join( res )

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function init_from_transliteration()

        dchar   :       DCharacterLAT object
        src     :       string

        Initialize and return <dchar>.

    """
    element = re.match(PATTERN, src)

    if element is None:
        dchar.unknown_char = True

    else:
        dchar.unknown_char = False

        trans_length = element.group('trans_length')
        if trans_length is None:
            dchar.length = None
        else:
            dchar.length = DIACRITICS_INVERSED[trans_length]

        dchar.stress = element.group('trans_stress') is not None

        dchar.diaeresis = element.group('trans_diaeresis') is not None

        base_char = element.group('base_char')
        if base_char in LOWER_CASE_INVERSED:
            # lower case :
            dchar.base_char = LOWER_CASE_INVERSED[base_char]
            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in UPPER_CASE_INVERSED:
            # upper case :
            dchar.base_char = UPPER_CASE_INVERSED[base_char]
            dchar.capital_letter = True
            dchar.punctuation = False

        else:
            # other symbols :
            dchar.base_char = PUNCTUATION_INVERSED[base_char]
            dchar.capital_letter = False
            dchar.punctuation = True

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring, dcharactertype, src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterLAT
        src             :       string

        Initialize <dstring>.
    """
    for start, dest in TRANS_EQUIVALENCES:
        src = src.replace( start, dest )

    last_real_index = -1
    for element in re.finditer(PATTERN2, src):

        real_indexes = range(element.start(), element.end())

        # we add the unknown chars placed BEFORE OR WITHIN the recognized characters :
        # pylint: disable=W0612
        # Unused variable 'i'
        for i in range( last_real_index+1, min(real_indexes) ):
            new_dcharacter = dcharactertype(dstring_object=dstring)
            new_dcharacter.unknown_char = True
            dstring.append( new_dcharacter )

        # we add the character read by the regex :
        string = element.string[element.start():element.end()]
        new_character = dcharactertype(dstring_object=dstring).init_from_transliteration(string,
                                                                                         "basic")
        dstring.append(new_character)

        last_real_index = max(real_indexes)

    # we add the unknown chars placed AFTER the recognized characters :
    # pylint: disable=W0612
    # Unused variable 'i'
    for i in range( last_real_index+1, len(src) ):
        new_dcharacter = dcharactertype(dstring_object=dstring)
        new_dcharacter.unknown_char = True
        dstring.append( new_dcharacter )
