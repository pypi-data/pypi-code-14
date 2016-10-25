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
    ❏DChars❏ : dchars/languages/hbo/transliterations/basic/basic.py
"""

from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.dicttools import invertdict
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.languages.hbo import symbols
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

# LETTERS["ALEF"] = ( without daghesh-mapiq, with daghesh-mapiq )
#
# I can't use double letters, e.g. "zz" for zayin + daghesh since the
# transliterated string "zzz" would stand for "zayin; zayin + daghesh"
# OR FOR "zayin + daghesh; zayin".
#
LETTERS = { 'ALEF'              : ("ʾ", "ʾ"),
            'BET'               : ("ḇ", "b"),
            'GIMEL'             : ("ḡ", "g"),
            'DALET'             : ("ḏ", "d"),
            'HE'                : ("h", "H"),
            'VAV'               : ("w", "W"),
            'ZAYIN'             : ("z", "Z"),
            'HET'               : ("ḥ", "Ḥ"),
            'TET'               : ("ṭ", "Ṭ"),
            'YOD'               : ("y", "Y"),
            'KAF'               : ("ḵ", "k"),
            'FINAL KAF'         : ("ḵ", "k"),
            'LAMED'             : ("l", "L"),
            'MEM'               : ("m", "M"),
            'FINAL MEM'         : ("m", "M"),
            'NUN'               : ("n", "N"),
            'FINAL NUN'         : ("n", "N"),
            'SAMEKH'            : ("s", "S"),
            'AYIN'              : ("ʿ", "ʿ",),
            'PE'                : ("p̄", "p"),
            'FINAL PE'          : ("p̄", "p"),
            'TSADI'             : ("ṣ", "Ṣ"),
            'FINAL TSADI'       : ("ṣ", "Ṣ"),
            'QOF'               : ("q", "Q"),
            'RESH'              : ("r", "R"),
            'SHIN'              : ("š", "Š"),
            'TAV'               : ("ṯ", "t"),
          }

LETTERS_INVERSED = {
            "ʾ"                 : "א",
            "ḇ"                 : "ב",
            "b"                 : "בּ",
            "ḡ"                 : "ג",
            "g"                 : "גּ",
            "ḏ"                 : "ד",
            "d"                 : "דּ",
            "h"                 : "ה",
            "H"                 : "הּ",
            "w"                 : "ו",
            "W"                 : "וּ",
            "z"                 : "ז",
            "Z"                 : "זּ",
            "ḥ"                 : "ח",
            "ṭ"                 : "ט",
            "Ṭ"                 : "טּ",
            "y"                 : "י",
            "Y"                 : "יּ",
            "ḵ"                 : "כ",
            "k"                 : "כּ",
            "l"                 : "ל",
            "L"                 : "לּ",
            "m"                 : "מ",
            "M"                 : "מּ",
            "n"                 : "נ",
            "N"                 : "נּ",
            "s"                 : "ס",
            "s+s"               : "סּ",
            "ʿ"                 : "ע",
            "p̄"                 : "פ",
            "p"                 : "פּ",
            "ṣ"                 : "צ",
            "Ṣ"                 : "צּ",
            "q"                 : "ק",
            "Q"                 : "קּ",
            "r"                 : "ר",
            "S"                 : "ש",
            "S+S"               : "שּ",
            "š"                 : "שׁ",
            "Š"                 : "שּׁ",
            "ś"                 : "שׂ",
            "Ś"                 : "שּׂ",
            "ṯ"                 : "ת",
            "t"                 : "תּ",
            }

#LETTERS_INVERSED2["בּ"] = ( daghesh_mapiq=True, shin_sin_dot, original_character="ב" )
LETTERS_INVERSED2 = {
            "א" : ( False, None, "א", ),
            "ב" :  ( False, None, "ב", ),
            "בּ" : ( True, None, "ב", ),
            "ג" : ( False, None, "ג", ),
            "גּ" : ( True, None, "ג", ),
            "ד" : ( False, None, "ד", ),
            "דּ" : ( True, None, "ד", ),
            "ה" : ( False, None, "ה", ),
            "הּ" : ( True, None, "ה", ),
            "ו" : ( False, None, "ו", ),
            "וּ" : ( True, None, "ו", ),
            "ז" : ( False, None, "ז", ),
            "זּ" : ( True, None, "ז", ),
            "ח" : ( False, None, "ח", ),
            "ט" : ( False, None, "ט", ),
            "טּ" : ( True, None, "ט", ),
            "י" : ( False, None, "י", ),
            "יּ" : ( True, None, "י", ),
            "כ" : ( False, None, "כ", ),
            "כּ" : ( True, None, "כ", ),
            "ל" : ( False, None, "ל", ),
            "לּ" : ( True, None, "ל", ),
            "מ" : ( False, None, "מ", ),
            "מּ" : ( True, None, "מ", ),
            "נ" : ( False, None, "נ", ),
            "נּ" : ( True, None, "נ", ),
            "ס" : ( False, None, "ס", ),
            "סּ" : ( True, None, "ס", ),
            "ע" : ( False, None, "ע", ),
            "פ" : ( False, None, "פ", ),
            "פּ" : ( True, None, "פ", ),
            "צ" : ( False, None, "צ", ),
            "צּ" : ( True, None, "צ", ),
            "ק" : ( False, None, "ק", ),
            "קּ" : ( True, None, "ק", ),
            "ר" : ( False, None, "ר", ),
            "ש" : ( False, None, "ש", ),
            "שּ" : ( True, None, "ש", ),
            "שׁ" : ( False, "HEBREW POINT SHIN DOT", "ש", ),
            "שּׁ" : ( True, "HEBREW POINT SHIN DOT", "ש", ),
            "שׂ" : ( False, "HEBREW POINT SIN DOT", "ש", ),
            "שּׂ" : ( True, "HEBREW POINT SIN DOT", "ש", ),
            "ת" : ( False, None, "ת", ),
            "תּ" : ( True, None, "ת", ),
            }

# dictionary used to get the transliteration string for
# a SHIN letter : SHIN_DOT[shin_sin_dot][daghesh_mapiq] = transliteration string
SHIN_DOT = {
                None                    : {
                                                False : "S",
                                                True : "S+S",
                                          },
                "HEBREW POINT SHIN DOT" : {
                                                False : "š",
                                                True : "Š",
                                          },
                "HEBREW POINT SIN DOT"  : {
                                                False : "ś",
                                                True : "Ś",
                                          }
           }

# OTHER_SYMBOLS[base_char] = transliterated character
OTHER_SYMBOLS = {
     '0'        : '0',
     '1'        : '1',
     '2'        : '2',
     '3'        : '3',
     '4'        : '4',
     '5'        : '5',
     '6'        : '6',
     '7'        : '7',
     '8'        : '8',
     '9'        : '9',
    }
OTHER_SYMBOLS_INVERSED = invertdict( OTHER_SYMBOLS )

# PUNCTUATION[base_char] = transliterated character
#
# ABOUT 'weird characters' : some characters are defined in this table only in order to pass tests.
PUNCTUATION = {
     ')'        : ')',
     '('        : '(',
     '['        : '[',
     ']'        : ']',
     '{'        : '{',
     '}'        : '}',
     ' '        : ' ',
     '\n'       : '\n',
     '\r'       : '\r',
     '\t'       : '\t',

     chr(0x05C0)        : "/",                  # א׀ # "HEBREW PUNCTUATION PASEQ"
     "/"                : "/+/",                # (weird character : see above)
     chr(0x05C3)        : ":",                  # א׃ # "HEBREW PUNCTUATION SOF PASUQ"
     ":"                : ":²",                 # (weird character : see abole)
     chr(0x05BE)        : "=",                  # א־ # "HEBREW PUNCTUATION MAQAF"
     "="                : "=²",                 # (weird character : see above)
     chr(0x05C6)        : "<nun hafukha>",      # ׆ # "HEBREW PUNCTUATION NUN HAFUKHA"

     chr(0x200E)        : chr(0x200E),  # "LEFT-TO-RIGHT MARK"
     chr(0x200F)        : chr(0x200F),  # "RIGHT-TO-RIGHT MARK"
    }
PUNCTUATION_INVERSED = invertdict( PUNCTUATION )

VOWELS = {
     "HEBREW POINT SHEVA"               : "ə",
     "HEBREW POINT HATAF SEGOL"         : "ĕ",
     "HEBREW POINT HATAF PATAH"         : "ă",
     "HEBREW POINT HATAF QAMATS"        : "ŏ",
     "HEBREW POINT HIRIQ"               : "i",
     "HEBREW POINT TSERE"               : "ē",
     "HEBREW POINT SEGOL"               : "e",
     "HEBREW POINT PATAH"               : "a",
     "HEBREW POINT QAMATS"              : "ā",
     "HEBREW POINT HOLAM"               : "ō",
     "HEBREW POINT HOLAM HASER FOR VAV" : "ō_vav",
     "HEBREW POINT QUBUTS"              : "u",
     "HEBREW POINT QAMATS QATAN"        : "o",
     }
VOWELS_INVERSED = invertdict(VOWELS)

POINTS = {
     "HEBREW POINT METEG"               : "|",
     "HEBREW POINT RAFE"                : "-",
     }

SPECIALPOINTS = {
     "HEBREW MARK UPPER DOT"            : "#HEBREW MARK UPPER DOT#",
     "HEBREW MARK LOWER DOT"            : "#HEBREW MARK LOWER DOT#",
     }
SPECIALPOINTS_INVERSED = invertdict( SPECIALPOINTS )

# E.g. CANTILATIONMARKS["HEBREW ACCENT ZAQEF GADOL"] = <HEBREW ACCENT ZAQEF GADOL>
CANTILATIONMARKS = { cmark:"<"+cmark+">" for cmark in symbols.SYMB_CANTILLATION_MARKS.keys() }
CANTILATIONMARKS_INVERSED = invertdict( CANTILATIONMARKS )

################################################################################
# transliteration's patterns :
# PATTERN  is used to cut one complex characters into its elements.
# PATTERN2 is used to cut several complex characters into a list of complex characters.
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.

T_BASECHARS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(LETTERS_INVERSED.keys())) + \
                regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )
T_VOWELS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(VOWELS_INVERSED.keys())))
T_METHEGH = isort_a_lstrings_bylen_nodup(
                 [re.escape(POINTS["HEBREW POINT METEG"]),] )
T_RAPHE = isort_a_lstrings_bylen_nodup(
                 [re.escape(POINTS["HEBREW POINT RAFE"]),] )
T_SPECIALPOINTS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(SPECIALPOINTS_INVERSED.keys())) )
T_CMARKS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(CANTILATIONMARKS_INVERSED.keys())) )

PATTERN_TXT = "((?P<base_char>({0}))" \
              "(?P<trans_vowel>({1}))?" \
              "(?P<trans_methegh>({2}))?" \
              "(?P<trans_raphe>({3}))?" \
              "(?P<trans_specialpoint>({4}))?" \
              "(?P<trans_cmark>({5})+)?)".format(
                  "|".join(prepare_list_to_strformat(T_BASECHARS)),
                  "|".join(prepare_list_to_strformat(T_VOWELS)),
                  "|".join(prepare_list_to_strformat(T_METHEGH)),
                  "|".join(prepare_list_to_strformat(T_RAPHE)),
                  "|".join(prepare_list_to_strformat(T_SPECIALPOINTS)),
                  "|".join(prepare_list_to_strformat(T_CMARKS)),
                )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "(({0})" \
               "({1})?" \
               "({2})?" \
               "({3})?" \
               "({4})?" \
               "({5})*" \
               ")".format("|".join(prepare_list_to_strformat(T_BASECHARS)),
                          "|".join(prepare_list_to_strformat(T_VOWELS)),
                          "|".join(prepare_list_to_strformat(T_METHEGH)),
                          "|".join(prepare_list_to_strformat(T_RAPHE)),
                          "|".join(prepare_list_to_strformat(T_SPECIALPOINTS)),
                          "|".join(prepare_list_to_strformat(T_CMARKS)),
                              )
# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')

PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, dchar):
    """
        function dchar__get_translit_str()

        dchar : DCharacterHBO object

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

        elif dchar.base_char in OTHER_SYMBOLS:
            res.append( OTHER_SYMBOLS[dchar.base_char] )

        else:
            if dchar.base_char == 'ש':
                res.append( SHIN_DOT[dchar.shin_sin_dot][dchar.daghesh_mapiq] )
            else:
                if not dchar.daghesh_mapiq:
                    # without daghesh-mapiq :
                    res.append(
                        LETTERS[symbols.SYMB_LETTERS.defaultsymbol2name[dchar.base_char]][0] )
                else:
                    # with daghesh-mapiq :
                    res.append(
                        LETTERS[symbols.SYMB_LETTERS.defaultsymbol2name[dchar.base_char]][1] )

        if dchar.vowel is not None:
            res.append( VOWELS[dchar.vowel] )

        if dchar.methegh:
            res.append( POINTS["HEBREW POINT METEG"] )

        if dchar.raphe:
            res.append( POINTS["HEBREW POINT RAFE"] )

        if dchar.specialpoint is not None:
            res.append( SPECIALPOINTS[dchar.specialpoint] )

        if dchar.cantillation_mark is not None:
            for cmark in dchar.cantillation_mark:
                res.append( CANTILATIONMARKS[cmark] )

    return "".join( res )

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function dchar__init_from_translit_str()

        dchar   :       DCharacterHBO object
        src     :       string

        Initialize and return <dchar>.

    """
    element = re.match(PATTERN, src)

    if element is None:
        dchar.unknown_char = True
        dchar.base_char = dchar.base_char

    else:
        dchar.unknown_char = False

        trans_basechar = element.group('base_char')
        if trans_basechar is None:
            dchar.base_char = None
        else:
            if trans_basechar in PUNCTUATION_INVERSED:
                dchar.punctuation = True
                dchar.base_char = PUNCTUATION_INVERSED[trans_basechar]

            elif trans_basechar in OTHER_SYMBOLS:
                dchar.punctuation = False
                dchar.base_char = OTHER_SYMBOLS_INVERSED[trans_basechar]

            else:
                dchar.punctuation = False

                (daghesh_mapiq,
                 shin_sin_dot,
                 sourcechar) = LETTERS_INVERSED2[LETTERS_INVERSED[trans_basechar]]

                dchar.base_char = sourcechar
                dchar.shin_sin_dot = shin_sin_dot
                dchar.daghesh_mapiq = daghesh_mapiq

        trans_vowel = element.group('trans_vowel')
        if trans_vowel is None:
            dchar.vowel = None
        else:
            dchar.vowel = VOWELS_INVERSED[trans_vowel]

        dchar.methegh = element.group('trans_methegh') is not None

        dchar.raphe = element.group('trans_raphe') is not None

        trans_spoint = element.group('trans_specialpoint')
        if trans_spoint is None:
            dchar.specialpoint = None
        else:
            dchar.specialpoint = SPECIALPOINTS_INVERSED[trans_spoint]

        trans_cmark = element.group('trans_cmark')
        if trans_cmark is None:
            dchar.cantillation_mark = None
        else:
            # trans_cmark.split = <NAME1><NAME2>
            dchar.cantillation_mark = []
            for name_cmark in trans_cmark.split(">"):
                if name_cmark != '':
                    dchar.cantillation_mark.append( CANTILATIONMARKS_INVERSED[name_cmark+">"] )

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring, dcharactertype, src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterHBO
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
                                                                                         "basic")
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
