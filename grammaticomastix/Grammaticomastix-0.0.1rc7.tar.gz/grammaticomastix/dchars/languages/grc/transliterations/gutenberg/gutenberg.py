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
    ❏DChars❏ : dchars/languages/grc/transliterations/gutenberg/gutenberg.py

    Transliteration defined on http://www.pgdp.net/wiki/Greek
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
AVAILABLE_DIRECTIONS = (+1,)

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
# LOWER_CASE[base_char] = transliterated character
LOWER_CASE = {"α"     : "a",
              "β"     : "b",
              'γ'     : "g",
              'δ'     : "d",
              'ε'     : "e",
              'ζ'     : "z",
              'η'     : "ê",
              'θ'     : "th",
              'ι'     : "i",
              'κ'     : "k",
              'λ'     : "l",
              'μ'     : "m",
              'ν'     : "n",
              'ξ'     : "x",
              'ο'     : "o",
              'π'     : "p",
              'ρ'     : "r",
              'σ'     : "s",
              'τ'     : "t",
              # see infra for more details
              # -> confer the option [grc.gutenberg]transliteration for upsilon
              'υ'     : "y",
              'φ'     : "ph",
              'χ'     : "ch",
              'ψ'     : "ps",
              'ω'     : "ô",

              'ϝ'     : "f",
              'ϗ'     : '&',
              'ϡ'     : '<sampi>',
              'ϛ'     : '<stigma>',
              'ϙ'     : 'q',
              }

# UPPER_CASE[base_char] = transliterated character
UPPER_CASE = {"α"     : "A",
              "β"     : "B",
              'γ'     : "G",
              'δ'     : "D",
              'ε'     : "E",
              'ζ'     : "Z",
              'η'     : "Ê",
              'θ'     : "Th",
              'ι'     : "I",
              'κ'     : "K",
              'λ'     : "L",
              'μ'     : "M",
              'ν'     : "N",
              'ξ'     : "X",
              'ο'     : "O",
              'π'     : "P",
              'ρ'     : "R",
              'σ'     : "S",
              'τ'     : "T",
              'υ'     : "U",
              'φ'     : "Ph",
              'χ'     : "Ch",
              'ψ'     : "PS",
              'ω'     : "Ô",

              'ϝ'     : "F",
              'ϗ'     : '&',
              'ϡ'     : '<SAMPI>',
              'ϛ'     : '<STIGMA>',
              'ϙ'     : 'Q',
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

# PUNCTUATION[base_char] = transliterated character
PUNCTUATION = {'-'       : '-',
               ')'       : ')',
               '('       : '(',
               '['       : '[',
               ']'       : ']',
               '{'       : '{',
               '}'       : '}',
               ' '       : ' ',
               '.'       : '.',
               ','       : ',',
               ';'       : '?',
               '!'       : '!',
               '·'       : ';',
               '"'       : '"',
               "'"       : "'",
               "—"       : "_",
               ":"       : ":",
               '\n'      : '\n',
               '\r'      : '\r',
               '\t'      : '\t',
               "‘"       : '<2018>',
               "’"       : '<2019>',
               "᾽"       : '<1FBD>',
              }

LOWER_CASE_INVERSED = invertdict(LOWER_CASE, accept_duplicated_values=True)
LOWER_CASE_INVERSED['b'] = 'β'
LOWER_CASE_INVERSED['s'] = 'σ'
UPPER_CASE_INVERSED = invertdict(UPPER_CASE)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)

# see http://www.pgdp.net/wiki/Transliterating_Greek/Marking_Accents
DIACRITICS =  {
                       "βαρεῖα"         : "\\",
                       "ὀξεῖα"          : "/",
                       "περισπωμένη"    : "^",

                       "μακρόν"         : "_",
                       "βραχύ"          : "-",

                       "ψιλὸν"          : ")",
                       "δασὺ"           : "h",

                       "ὑπογεγραμμένη"  : "|",
                       "διαλυτικά"      : "\"",
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

PATTERN_TXT = "((?P<trans_pneuma>({0}))?" \
              "(?P<trans_tonos>({1}))?" \
              "(?P<base_char>({2}))" \
              "(?P<trans_hypogegrammene>({3}))?" \
              "(?P<trans_dialutika>({4}))?" \
              "(?P<trans_mekos>({5}))?)".format("|".join(prepare_list_to_strformat(PNEUMA)),
                                                "|".join(prepare_list_to_strformat(TONOS)),
                                                "|".join(prepare_list_to_strformat(LETTERS)),
                                                "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                                                "|".join(prepare_list_to_strformat(DIALUTIKA)),
                                                "|".join(prepare_list_to_strformat(MEKOS)),
                                              )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "(({0})?" \
               "({1})?" \
               "({2})" \
               "({3})?" \
               "({4})?" \
               "({5})?)".format("|".join(prepare_list_to_strformat(PNEUMA)),
                                "|".join(prepare_list_to_strformat(TONOS)),
                                "|".join(prepare_list_to_strformat(LETTERS)),
                                "|".join(prepare_list_to_strformat(HYPOGEGRAMMENE)),
                                "|".join(prepare_list_to_strformat(DIALUTIKA)),
                                "|".join(prepare_list_to_strformat(MEKOS)),
                               )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')

PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, dchar):
    """
        function dchar__get_translit_str()

        dchar : DCharacterGRC object

        Return a transliterared string corresponding to <char>.
    """
    res = []

    if dchar.unknown_char:
        if dstring_object.options["anonymize the unknown characters"] == 'yes':
            return UNKNOWN_CHAR_SYMBOL
        else:
            return dchar.base_char

    #
    # from http://www.pgdp.net/wiki/Greek
    #
    # ῥ = rh, not hr
    if dchar.pneuma is not None and dchar.base_char != "ρ":
        res.append( DIACRITICS[dchar.pneuma] )

    if dchar.tonos is not None:
        res.append( DIACRITICS[dchar.tonos] )

    if dchar.dialutika == True:
        res.append( DIACRITICS['διαλυτικά'] )

    if dchar.base_char is not None:

        if dchar.punctuation:
            res.append( PUNCTUATION[dchar.base_char] )

        elif dchar.base_char in OTHER_SYMBOLS:
            res.append( OTHER_SYMBOLS[dchar.base_char] )
        else:
            if dchar.capital_letter == False:
                res.append( LOWER_CASE[dchar.base_char] )
            else:
                res.append( UPPER_CASE[dchar.base_char] )

    #
    # from http://www.pgdp.net/wiki/Greek
    #
    # ῥ = rh, not hr
    if dchar.pneuma is not None and dchar.base_char == "ρ":
        res.append( DIACRITICS[dchar.pneuma] )

    if dchar.hypogegrammene == True:
        res.append( DIACRITICS['ὑπογεγραμμένη'] )

    if dchar.mekos is not None:
        res.append( DIACRITICS[dchar.mekos] )

    str_res = "".join( res )

    if not dchar.unknown_char and not dchar.punctuation:

        if dstring_object.options["gutenberg:ignore accents"] == 'yes':
            str_res = str_res.replace("/", "")
            str_res = str_res.replace("\\", "")
            str_res = str_res.replace("^", "")

        if dstring_object.options["gutenberg:ignore smooth breathing"] == 'yes':
            str_res = str_res.replace(")", "")

        if dstring_object.options["gutenberg:ignore iota subscript"] == 'yes':
            str_res = str_res.replace("|", "")

        if dstring_object.options["gutenberg:ignore diaeresis"] == 'yes':
            str_res = str_res.replace("\"", "")

        if dstring_object.options["gutenberg:ignore makron and brakhu"] == 'yes':
            str_res = str_res.replace("-", "")
            str_res = str_res.replace("_", "")

    return str_res

#///////////////////////////////////////////////////////////////////////////////
def dstring__trans__get_trans(dstring_object):
    """
        function dstring__trans__get_trans

        Return a (unicode) string corresponding to the <dstring_object>.
    """

    res = []

    # we shift the position of the "rough breathing" in diphthongs from the
    # second to the first place AT THE BEGINNING OF A WORD (ex : οὐλομένην =
    # )oulo-, not o)ulo- ) . If inside a word, we delete the rough breathing
    # (e.g. καὑπὸ = kaupo not khaupo)
    ppreceding_dchar = None
    preceding_dchar = None
    for index_dchar, dchar in enumerate(dstring_object):

        if index_dchar >= 1:

            if preceding_dchar.base_char in ('α', 'ε', 'η', 'ο') and \
               dchar.base_char in ('υ', 'ι') and \
               not dchar.dialutika and \
               preceding_dchar.pneuma is None and \
               dchar.pneuma is not None:

                # at the beginning of a word :
                if ppreceding_dchar is None or \
                   ppreceding_dchar.unknown_char or ppreceding_dchar.punctuation:

                    preceding_dchar.pneuma = dchar.pneuma
                    dchar.pneuma = None

                else:
                    # inside a word:
                    dchar.pneuma = None

        ppreceding_dchar = preceding_dchar
        preceding_dchar = dchar

    for dchar in dstring_object:
        res.append( dchar__get_translit_str(dstring_object = dstring_object,
                                            dchar = dchar))

    str_res = "".join( res )

    #
    # from http://www.pgdp.net/wiki/Greek
    #
    # The letter γ (gamma) is usually transliterated as g, but n is used instead when it
    # occurs before certain letters:
    #
    #           Greek 	Transliteration
    #           γγ 	ng
    #           γκ 	nk
    #           γξ 	nx
    #           γχ 	nch
    str_res = str_res.replace("gg", "ng")
    str_res = str_res.replace("gk", "nk")
    str_res = str_res.replace("gx", "nx")
    str_res = str_res.replace("gch", "nch")

    #
    # from http://www.pgdp.net/wiki/Greek
    #
    # Double rho in the middle of a word always has rough breathing on the
    # second rho, so διαρροια should be transliterated as diarrhoia. Do this
    # even if the breathing mark is omitted in the printed text.
    str_res = str_res.replace("rr", "rrh")

    #
    # from http://www.pgdp.net/wiki/Greek
    #
    # If a word begins with a capitalized vowel, the accents and breathing
    # marks are often printed to the left of the letter, rather than above it.
    # If it has rough breathing, make the vowel lower case and capitalize
    # the H: hÊraklês becomes Hêraklês.
    str_res = str_res.replace("hA", "Ha")
    str_res = str_res.replace("hE", "He")
    str_res = str_res.replace("hÊ", "Hê")
    str_res = str_res.replace("hI", "Hi")
    str_res = str_res.replace("hO", "Ho")
    str_res = str_res.replace("hU", "Hu")
    str_res = str_res.replace("hÔ", "Hô")

    # alternative transliteration of upsilon :
    if dstring_object.options["gutenberg:transliteration for upsilon"] == "u":
        str_res = str_res.replace("y", "u")
        str_res = str_res.replace("Y", "U")

    elif dstring_object.options["gutenberg:transliteration for upsilon"] == "u or y":
        str_res = str_res.replace("ay", "au")
        str_res = str_res.replace("ey", "eu")
        str_res = str_res.replace("êy", "êu")
        str_res = str_res.replace("oy", "ou")
        str_res = str_res.replace("Ay", "Au")
        str_res = str_res.replace("Ey", "Eu")
        str_res = str_res.replace("Êy", "Êu")
        str_res = str_res.replace("Oy", "Ou")

    # No "hh" ?
    if dstring_object.options["gutenberg:hh becomes h"] == "yes":
        str_res = str_res.replace("hh", "h")

    return str_res
