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
    ❏DChars❏ : dchars/languages/grc/transliterations/betacode/betacode.py
"""

from dchars.errors.errors import DCharsError
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
# * CAVEAT ! No duplicate value allowed in these dictionaries !
#
LOWER_CASE = {"α"     : "A",
              "β"     : "B",
              'γ'     : "G",
              'δ'     : "D",
              'ε'     : "E",
              'ζ'     : "Z",
              'η'     : "H",
              'θ'     : "Q",
              'ι'     : "I",
              'κ'     : "K",
              'λ'     : "L",
              'μ'     : "M",
              'ν'     : "N",
              'ξ'     : "C",
              'ο'     : "O",
              'π'     : "P",
              'ρ'     : "R",
              'σ'     : "S",
              'τ'     : "T",
              'υ'     : "U",
              'φ'     : "F",
              'χ'     : "X",
              'ψ'     : "Y",
              'ω'     : "W",
              'ϝ'     : '<f>',
              'ϗ'     : '&',
              'ϡ'     : '<sampi>',
              'ϛ'     : '<stigma>',
              'ϙ'     : '<koppa>',
              }

# UPPER_CASE[base_char] = transliterated character
UPPER_CASE = {"α"     : "A",
              "β"     : "B",
              'γ'     : "G",
              'δ'     : "D",
              'ε'     : "E",
              'ζ'     : "Z",
              'η'     : "H",
              'θ'     : "Q",
              'ι'     : "I",
              'κ'     : "K",
              'λ'     : "L",
              'μ'     : "M",
              'ν'     : "N",
              'ξ'     : "C",
              'ο'     : "O",
              'π'     : "P",
              'ρ'     : "R",
              'σ'     : "S",
              'τ'     : "T",
              'υ'     : "U",
              'φ'     : "F",
              'χ'     : "X",
              'ψ'     : "PS",
              'ω'     : "W",
              'ϝ'     : "<F>",
              'ϗ'     : '&',
              'ϡ'     : '<SAMPI>',
              'ϛ'     : '<STIGMA>',
              'ϙ'     : '<KOPPA>',
             }

# OTHER_SYMBOLS[base_char] = transliterated character
OTHER_SYMBOLS = {
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
         }

PUNCTUATION = {'-'       : '-', # http://en.wikipedia.org/wiki/Beta_code
               ')'       : ')',
               '('       : '(',
               '['       : '[',
               ']'       : ']',
               '{'       : '{',
               '}'       : '}',
               ' '       : ' ',
               '.'       : '.', # http://en.wikipedia.org/wiki/Beta_code
               ','       : ',', # http://en.wikipedia.org/wiki/Beta_code
               ';'       : ';', # http://en.wikipedia.org/wiki/Beta_code
               '!'       : '!',
               '·'       : ':', # http://en.wikipedia.org/wiki/Beta_code
               '"'       : '"',
               "’"       : "'", # http://en.wikipedia.org/wiki/Beta_code
               "'"       : "’", # no duplicates !
               "—"       : "_", # http://en.wikipedia.org/wiki/Beta_code
               ":"       : "::", # no duplicate : we have already '·' : ':'
               '\n'      : '\n',
               '\r'      : '\r',
               '\t'      : '\t',
               "‘"       : '<2018>',
               "᾽"       : '<1FBD>',
              }

LOWER_CASE_INVERSED = invertdict(LOWER_CASE, accept_duplicated_values=True)
LOWER_CASE_INVERSED['B'] = 'β'
LOWER_CASE_INVERSED['S'] = 'σ'
UPPER_CASE_INVERSED = invertdict(UPPER_CASE)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)

DIACRITICS =  {
                       "βαρεῖα"         : "\\",
                       "ὀξεῖα"          : "/",
                       "περισπωμένη"    : "=",

                       "μακρόν"         : "&",
                       "βραχύ"          : "'",

                       "ψιλὸν"          : ")",
                       "δασὺ"           : "(",

                       "ὑπογεγραμμένη"  : "|",
                       "διαλυτικά"      : "+",
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

PNEUMA = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['ψιλὸν']),
                 re.escape(DIACRITICS['δασὺ'])] )
TONOS = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['βαρεῖα']),
                 re.escape(DIACRITICS['ὀξεῖα']),
                 re.escape(DIACRITICS['περισπωμένη'])] )
LETTERS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(LOWER_CASE_INVERSED.keys())) + \
                regexstring_list(tuple(UPPER_CASE_INVERSED.keys())) + \
                regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )
HYPOGEGRAMMENE = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['ὑπογεγραμμένη']),] )
DIALUTIKA = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['διαλυτικά']),] )
MEKOS = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['μακρόν']),
                re.escape(DIACRITICS['βραχύ'])] )

# order defined in http://www.tlg.uci.edu/encoding/
#
# * On lowercase letters these are keyed in the order:
#   (1) letter, (2) breathing, (3) accent, (4) iota subscript. E.g. W(=|
#
# * On uppercase letters these are keyed in the order:
#   (1) asterisk, (2) breathing, (3) accent, (4) letter, (5) iota subscript. E.g. *(=W|
#
PATTERN_TXT__LOWERCASE =  "((?P<base_charLC>({0}))" \
                          "(?P<trans_pneumaLC>({1}))?" \
                          "(?P<trans_tonosLC>({2}))?" \
                          "(?P<trans_hypogegrammeneLC>({3}))?" \
                          "(?P<trans_dialutikaLC>({4}))?" \
                          "(?P<trans_mekosLC>({5}))?)".format(
                              "|".join(prepare_list_to_strformat(LETTERS)),
                              "|".join(prepare_list_to_strformat(PNEUMA)),
                              "|".join(prepare_list_to_strformat(TONOS)),
                              "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                              "|".join(prepare_list_to_strformat(DIALUTIKA)),
                              "|".join(prepare_list_to_strformat(MEKOS)),
                              )

PATTERN_TXT__UPPERCASE =  "(\\*(?P<trans_pneumaUC>({1}))?" \
                          "(?P<trans_tonosUC>({2}))?" \
                          "(?P<base_charUC>({0}))" \
                          "(?P<trans_hypogegrammeneUC>({3}))?" \
                          "(?P<trans_dialutikaUC>({4}))?" \
                          "(?P<trans_mekosUC>({5}))?)".format(
                              "|".join(prepare_list_to_strformat(LETTERS)),
                              "|".join(prepare_list_to_strformat(PNEUMA)),
                              "|".join(prepare_list_to_strformat(TONOS)),
                              "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                              "|".join(prepare_list_to_strformat(DIALUTIKA)),
                              "|".join(prepare_list_to_strformat(MEKOS)),
                              )

PATTERN_TXT = "(" + PATTERN_TXT__LOWERCASE + "|" + PATTERN_TXT__UPPERCASE + ")"
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')

PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2__LOWERCASE ="(({0})" \
                         "({1})?" \
                         "({2})?" \
                         "({3})?" \
                         "({4})?" \
                         "({5})?)".format("|".join(prepare_list_to_strformat(LETTERS)),
                                          "|".join(prepare_list_to_strformat(PNEUMA)),
                                          "|".join(prepare_list_to_strformat(TONOS)),
                                          "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                                          "|".join(prepare_list_to_strformat(DIALUTIKA)),
                                          "|".join(prepare_list_to_strformat(MEKOS)),
                                         )

PATTERN_TXT2__UPPERCASE ="(\\*({1})?" \
                         "({2})?" \
                         "({0})" \
                         "({3})?" \
                         "({4})?" \
                         "({5})?)".format("|".join(prepare_list_to_strformat(LETTERS)),
                                          "|".join(prepare_list_to_strformat(PNEUMA)),
                                          "|".join(prepare_list_to_strformat(TONOS)),
                                          "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                                          "|".join(prepare_list_to_strformat(DIALUTIKA)),
                                          "|".join(prepare_list_to_strformat(MEKOS)),
                                         )
PATTERN_TXT2 = "(" + PATTERN_TXT2__LOWERCASE + "|" + PATTERN_TXT2__UPPERCASE + ")"
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')

PATTERN2 = re.compile(PATTERN_TXT2)


#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, dchar):
    """
        function get_transliteration

        dchar   :       DCharacterGRC object

        Return a transliterared string corresponding to <char>.
    """

    res = []

    if dchar.unknown_char:
        if dstring_object.options["anonymize the unknown characters"] == 'yes':
            return UNKNOWN_CHAR_SYMBOL
        else:
            return dchar.base_char

    else:

        if dchar.punctuation:
            # punctuation :
            res.append( PUNCTUATION[dchar.base_char] )

        elif dchar.base_char in OTHER_SYMBOLS:
            res.append( OTHER_SYMBOLS[dchar.base_char] )

        else:

            if dchar.capital_letter:
                # upper case letter :
                res.append( '*' )

                if dchar.pneuma is not None:
                    res.append( DIACRITICS[dchar.pneuma] )

                if dchar.tonos is not None:
                    res.append( DIACRITICS[dchar.tonos] )

                res.append( UPPER_CASE[dchar.base_char] )

            else:
                # lower case letter :
                res.append( LOWER_CASE[dchar.base_char] )

                if dchar.pneuma is not None:
                    res.append( DIACRITICS[dchar.pneuma] )

                if dchar.tonos is not None:
                    res.append( DIACRITICS[dchar.tonos] )

            if dchar.hypogegrammene == True:
                res.append( DIACRITICS['ὑπογεγραμμένη'] )

            if dchar.dialutika == True:
                res.append( DIACRITICS['διαλυτικά'] )

            if dchar.mekos is not None:
                res.append( DIACRITICS[dchar.mekos] )

    return "".join( res )

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function init_from_transliteration()

        dchar   :       DCharacterGRC object
        src     :       string

        Initialize and return <char>.
    """
    element = re.match(PATTERN, src)

    trans_pneuma = None
    trans_mekos = None
    trans_tonos = None

    if element is None:
        dchar.unknown_char = True

    else:
        dchar.unknown_char = False

        #-----------------------------------------------------------------------
        # lower case letter, punctuation or another symbol :
        #-----------------------------------------------------------------------
        if element.group('base_charLC') is not None:

            dchar.capital_letter = False
            base_char = element.group('base_charLC')

            if base_char in PUNCTUATION_INVERSED:
                dchar.punctuation = True
            elif base_char in OTHER_SYMBOLS_INVERSED:
                dchar.punctuation = False
            else:
                dchar.punctuation = False

                trans_pneuma = element.group('trans_pneumaLC')
                trans_tonos = element.group('trans_tonosLC')
                dchar.hypogegrammene = element.group('trans_hypogegrammeneLC') is not None
                dchar.dialutika = element.group('trans_dialutikaLC') is not None
                trans_mekos = element.group('trans_mekosLC')

        #-----------------------------------------------------------------------
        # upper case letter
        #-----------------------------------------------------------------------
        elif element.group('base_charUC') is not None:

            dchar.capital_letter = True
            base_char = element.group('base_charUC')

            dchar.punctuation = False

            trans_pneuma = element.group('trans_pneumaUC')
            trans_tonos = element.group('trans_tonosUC')
            base_char = element.group('base_charUC')
            dchar.hypogegrammene = element.group('trans_hypogegrammeneUC') is not None
            dchar.dialutika = element.group('trans_dialutikaUC') is not None
            trans_mekos = element.group('trans_mekosUC')

        #-----------------------------------------------------------------------
        # problem : unknown possibility
        #-----------------------------------------------------------------------
        else:
            raise DCharsError(
                context = 'betacode.py::init_from_transliteration',
                message = "DCharacterGRC.init_from_transliteration__betacode; src="+str(src))

        if dchar.punctuation:
            dchar.base_char = PUNCTUATION_INVERSED[base_char]
        else:

            if trans_pneuma is None:
                dchar.pneuma = None
            else:
                dchar.pneuma = DIACRITICS_INVERSED[trans_pneuma]

            if trans_tonos is None:
                dchar.tonos = None
            else:
                dchar.tonos = DIACRITICS_INVERSED[trans_tonos]

            if trans_mekos is None:
                dchar.mekos = None
            else:
                dchar.mekos = DIACRITICS_INVERSED[trans_mekos]

            if base_char in OTHER_SYMBOLS_INVERSED:
                dchar.base_char = OTHER_SYMBOLS_INVERSED[base_char]
            elif not dchar.capital_letter:
                dchar.base_char = LOWER_CASE_INVERSED[base_char]
            else:
                dchar.base_char = UPPER_CASE_INVERSED[base_char]

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring, dcharactertype, src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterGRC
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
            new_dcharacter.base_char = src[i]
            dstring.append( new_dcharacter )

        # we add the character read by the regex :
        string = element.string[element.start():element.end()]
        new_character = dcharactertype(dstring_object=dstring).init_from_transliteration(string,
                                                                   "betacode")
        dstring.append(new_character)

        last_real_index = max(real_indexes)

    # we add the unknown chars placed AFTER the recognized characters :
    # pylint: disable=W0612
    # Unused variable 'i'
    for i in range( last_real_index+1, len(src) ):
        new_dcharacter = dcharactertype(dstring_object=dstring)
        new_dcharacter.unknown_char = True
        new_dcharacter.base_char = src[i]
        dstring.append( new_dcharacter )

#///////////////////////////////////////////////////////////////////////////////
def dstring__trans__get_trans(dstring_object):
    """
        function dstring__trans__get_trans

        Return a (unicode) string corresponding to the <dstring_object>.
    """

    res = []

    for dchar in dstring_object:
        res.append( dchar__get_translit_str(dstring_object = dstring_object,
                                            dchar = dchar))

    return "".join( res )
