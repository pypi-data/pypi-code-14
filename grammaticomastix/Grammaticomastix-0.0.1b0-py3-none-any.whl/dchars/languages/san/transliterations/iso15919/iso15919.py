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
    ❏DChars❏ : dchars/languages/san/transliterations/iso15919/iso15919.py
"""


from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.dicttools import invertdict
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
import re, unicodedata

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
#
#  used in dstring__init_from_translit_str.
#
################################################################################
TRANS_EQUIVALENCES = (
                        # r̥̄ [r+0304+0325]-> r̥̄ [r+0325+0304]
                        ( "r"+chr(0x0304)+chr(0x0325), "r"+chr(0x0325)+chr(0x0304)),

                        # l̥̄ [r+0304+0325]-> l̥̄ [l+0325+0304]
                        ( "l"+chr(0x0304)+chr(0x0325), "l"+chr(0x0325)+chr(0x0304)),

                        # anudatta + acute :
                        ( chr(0x0331)+chr(0x0301), chr(0x0301)+chr(0x0331) ),

                        # anudatta + acute :
                        ( chr(0x0331)+chr(0x0304), chr(0x0304)+chr(0x0331) ),
                     )

COMPACT_CHARACTERS = (
                    # 'ḥ' [h+0323] -> 'ḥ' (1E25)
                    ( "h"+chr(0x0323), chr(0x1E25) ),
                    # ṭ [t+0323] -> 'ṭ' (1E6D)
                    ( "t"+chr(0x0323), chr(0x1E6D) ),
                    # ḍ [d+0323] -> 'ḍ' (1E0D)
                    ( "d"+chr(0x0323), chr(0x1E0D) ),
                    # ḅ [b+0323] -> 'ḅ' (1E05)
                    ( "b"+chr(0x0323), chr(0x1E05) ),
                    # ṛ [r+0323] -> 'ṛ' (1E5B)
                    ( "r"+chr(0x0323), chr(0x1E5B) ),
                    # ḷ [l+0323] -> ḷ (1E37)
                    ( "l"+chr(0x0323), chr(0x1E37) ),
                    # ṣ [s+0323] -> ṣ (1E63)
                    ( "s"+chr(0x0323), chr(0x1E63) ),
                    # ś [s+0301] -> ś (015B)
                    ( "s"+chr(0x0301), chr(0x015B) ),
                    # ṇ [n+0323] -> ṇ (1E47)
                    ( "n"+chr(0x0323), chr(0x1E47) ),
                    # ṅ [n+0307] -> ṅ (1E45)
                    ( "n"+chr(0x0307), chr(0x1E45) ),
                    # ñ [n+0303] -> ñ (00F1)
                    ( "n"+chr(0x0303), chr(0x00F1) ),

                    # ŕ 0155 + 0325 -> ŕ̥ (r+0325+0301)
                    ( "ŕ̥", "ŕ̥"),
                    # ŕ 0155 + 0325 -> ŕ̥ (r+0325+0301)
                    ( "ŕ̥", "ŕ̥"),
                    # ĺ 013A + 0325 -> ĺ̥ (r+0325+0301)
                    ( "ĺ̥", "ĺ̥"),

                    # ġ [l+0307] -> ġ (0121)
                    ( "g"+chr(0x0307), chr(0x0121) ),
                    # ẏ [l+0307] -> ẏ (1E8F)
                    ( "y"+chr(0x0307), chr(0x1E8F) ),
                    # ṁ [m+0307] -> ṁ (1E41)
                    ( "m"+chr(0x0307), chr(0x1E41) ),

                    # vowel + makron :
                    ( "a"+chr(0x0304), chr(0x0101) ),
                    ( "e"+chr(0x0304), chr(0x0113) ),
                    ( "i"+chr(0x0304), chr(0x012B) ),
                    ( "o"+chr(0x0304), chr(0x014D) ),
                    ( "u"+chr(0x0304), chr(0x016B) ),

                    # vowel + acute + makron -> (vowel+makron) + acute
                    ( "a"+chr(0x0301)+chr(0x0304), chr(0x0101)+chr(0x0301) ),
                    ( "e"+chr(0x0301)+chr(0x0304), chr(0x0113)+chr(0x0301) ),
                    ( "i"+chr(0x0301)+chr(0x0304), chr(0x012B)+chr(0x0301) ),
                    ( "o"+chr(0x0301)+chr(0x0304), chr(0x014D)+chr(0x0301) ),
                    ( "u"+chr(0x0301)+chr(0x0304), chr(0x016B)+chr(0x0301) ),

                    # vowel + anudatta + makron + acute -> (vowel+makron) + acute + anudatta
                    ( "a"+chr(0x0331)+chr(0x0304)+chr(0x0301), chr(0x0101)+chr(0x0301)+chr(0x331) ),
                    ( "e"+chr(0x0331)+chr(0x0304)+chr(0x0301), chr(0x0113)+chr(0x0301)+chr(0x331) ),
                    ( "i"+chr(0x0331)+chr(0x0304)+chr(0x0301), chr(0x012B)+chr(0x0301)+chr(0x331) ),
                    ( "o"+chr(0x0331)+chr(0x0304)+chr(0x0301), chr(0x014D)+chr(0x0301)+chr(0x331) ),
                    ( "u"+chr(0x0331)+chr(0x0304)+chr(0x0301), chr(0x016B)+chr(0x0301)+chr(0x331) ),

                    # vowel + anudatta + acute + makron -> (vowel+makron) + acute + anudatta
                    ( "a"+chr(0x0331)+chr(0x0301)+chr(0x0304), chr(0x0101)+chr(0x0301)+chr(0x331) ),
                    ( "e"+chr(0x0331)+chr(0x0301)+chr(0x0304), chr(0x0113)+chr(0x0301)+chr(0x331) ),
                    ( "i"+chr(0x0331)+chr(0x0301)+chr(0x0304), chr(0x012B)+chr(0x0301)+chr(0x331) ),
                    ( "o"+chr(0x0331)+chr(0x0301)+chr(0x0304), chr(0x014D)+chr(0x0301)+chr(0x331) ),
                    ( "u"+chr(0x0331)+chr(0x0301)+chr(0x0304), chr(0x016B)+chr(0x0301)+chr(0x331) ),

                    # vowel + acute + anudatta + makron -> (vowel+makron) + acute + anudatta
                    ( "a"+chr(0x0301)+chr(0x0331)+chr(0x0304), chr(0x0101)+chr(0x0301)+chr(0x331) ),
                    ( "e"+chr(0x0301)+chr(0x0331)+chr(0x0304), chr(0x0113)+chr(0x0301)+chr(0x331) ),
                    ( "i"+chr(0x0301)+chr(0x0331)+chr(0x0304), chr(0x012B)+chr(0x0301)+chr(0x331) ),
                    ( "o"+chr(0x0301)+chr(0x0331)+chr(0x0304), chr(0x014D)+chr(0x0301)+chr(0x331) ),
                    ( "u"+chr(0x0301)+chr(0x0331)+chr(0x0304), chr(0x016B)+chr(0x0301)+chr(0x331) ),
                 )

UNCOMPACT_CHARACTERS = (
                        # vowel + acute accent :
                        ( chr(0x00E1), "a"+chr(0x0301) ),
                        ( chr(0x00E9), "e"+chr(0x0301) ),
                        ( chr(0x00ED), "i"+chr(0x0301) ),
                        ( chr(0x00F3), "o"+chr(0x0301) ),
                        ( chr(0x00FA), "u"+chr(0x0301) ),

                        # vowel + makron + acute accent :
                        # ḗ (0x1E17)
                        ( chr(0x1E17), chr(0x0113)+chr(0x0301) ),
                        # ṓ (0x1E53)
                        ( chr(0x1E53), chr(0x014D)+chr(0x0301) ),

                        # some consonants + anudatta have a compact unicode representation :
                        ( chr(0x1E07), "b"+chr(0x0331) ),
                        ( chr(0x1E0F), "d"+chr(0x0331) ),
                        ( chr(0x1E35), "k"+chr(0x0331) ),
                        ( chr(0x1E3B), "l"+chr(0x0331) ),
                        ( chr(0x1E49), "n"+chr(0x0331) ),
                        ( chr(0x1E5F), "r"+chr(0x0331) ),
                        ( chr(0x1E6F), "t"+chr(0x0331) ),
                        ( chr(0x1E95), "z"+chr(0x0331) ),
                        ( chr(0x1E96), "h"+chr(0x0331) ),
    )

################################################################################
# transliteration's symbols :
################################################################################

#
# * CAVEAT ! If you modify these dictionaries, don't forget to modify their
#            corresponding symbols' dictionaries in symbols.py !
#
# * CAVEAT ! No duplicate value allowed in these dictionaries !
#
CONSONANTS = {
                 'KA'            : 'k',
                 'KHA'           : 'kh',
                 'GA'            : 'g',
                 'GHA'           : 'gh',
                 'NGA'           : 'ṅ',
                 'CA'            : 'c',
                 'CHA'           : 'ch',
                 'JA'            : 'j',
                 'JHA'           : 'jh',
                 'NYA'           : 'ñ',
                 'TTA'           : 'ṭ',
                 'TTHA'          : 'ṭh',
                 'DDA'           : 'ḍ',
                 'DDHA'          : 'ḍh',
                 'NNA'           : 'ṇ',
                 'TA'            : 't',
                 'THA'           : 'th',
                 'DA'            : 'd',
                 'DHA'           : 'dh',
                 'NA'            : 'n',
                 'PA'            : 'p',
                 'PHA'           : 'ph',
                 'BA'            : 'b',
                 'BHA'           : 'bh',
                 'MA'            : 'm',
                 'YA'            : 'y',
                 'RA'            : 'r',
                 'LA'            : 'l',
                 # (http://en.wikipedia.org/wiki/ISO_15919) In ISO 15919,
                 # ḷ(1E37=006C 0323) = ळ.
                 # l̥(006C 0325) = ऌ /  ॢ
                 'LLA'           : 'ḷ',
                 'VA'            : 'v',
                 'SHA'           : 'ś',
                 'SSA'           : 'ṣ',
                 'SA'            : 's',
                 'HA'            : 'h',

                 'DEVANAGARI SIGN VISARGA'         : 'ḥ',
             }

# only for consonants with nukta described as TWO unicode characters (consonant + nukta)
CONSONANTS_WITH_NUKTA = {

                #...............................................................
                # consonants written with a nukta and
                # (1) existing as ONE unicode character (!= त़ is TA + nukta)
                # (2) respecting the rule : NFC( NFD( char ) ) = char
                #...............................................................
                'n+nukta'                      : 'ṉ',
                'ḷ+nukta'                      : 'ḻ',
                'r+nukta'                      : 'ṟ',

                #...............................................................
                # the following symbols exist as independent character in Unicode
                # (e.g. : j+nukta = ZA) but do not respect
                # the rule NFC(NFD(char)) == char
                #...............................................................
                'ka+nukta'             : 'q',
                'kha+nukta'            : 'ḵẖ', # ḵẖ (1E35=006B 200D; 1E96=0068 0331)
                'ga+nukta'             : 'ġ',
                'j+nukta'              : 'z',
                'ḍ+nukta'              : 'ṛ',
                'ḍh+nukta'             : 'ṛh',
                'ph+nukta'             : 'f',
                'y+nukta'              : 'ẏ',

                #...............................................................
                # the following symbols doesn't exist as independent characters
                # in Unicode :
                #...............................................................
                'va+nukta'             : 'w',
                'ha+nukta'             : 'h̤',
                'sa+nukta'             : 's̤',
                'ta+nukta'             : 't̤',
                 }


# id est, CONSONANTS_WITH_NUKTA_TO_CONSONANT['w'] = 'v' + nukta
CONSONANTS_WITH_NUKTA_TO_CONSONANT = {
                 'q'    : 'KA',
                 'ḵẖ'   : 'KHA',
                 'ġ'    : 'GA',
                 'z'    : 'JA',
                 'ṛ'    : 'DHA',
                 'ṛh'   : 'DDHA',
                 'f'    : 'PHA',
                 'ẏ'    : 'YA',

                 'w'    : 'VA',
                 'h̤'    : 'HA',
                 's̤'    : 'SA',
                 't̤'    : 'TA',
                 }

# the name of the vowels (the keys of this dictionary) must be consistent
# with symbols.py::SYMB_(IN)DEPENDENT_VOWELS
VOWELS = {
                'A'                             : 'a',
                'AA'                            : 'ā',
                'I'                             : 'i',
                'II'                            : 'ī',
                'U'                             : 'u',
                'UU'                            : 'ū',
                # consonant ṛ(1E5B=0072+0323) (ḍa + nukta) <> vowel r̥(0072+0325)
                'VOCALIC R'                     : 'r̥',
                # r̥̄ = r + 0325 + 0304, not r + 0304 + 0325
                'VOCALIC RR'                    : 'r̥̄',
                 # (http://en.wikipedia.org/wiki/ISO_15919) In ISO 15919,
                 # ḷ(1E37=006C 0323) = ळ.
                 # l̥(006C 0325) = ऌ /  ॢ
                'VOCALIC L'                     : 'l̥',
                # l̥̄= l + 0325 + 0304, not l + 0304 + 0325
                'VOCALIC LL'                    : 'l̥̄',
                'SHORT E'                       : 'e',
                'E'                             : 'ē',
                'AI'                            : 'ai',
                'SHORT O'                       : 'o',
                'O'                             : 'ō',
                'AU'                            : 'au',
                'CANDRA E'                      : 'ê',
                'CANDRA O'                      : 'ô',
         }

VOWELS_IN_HIATUS = {
                'A'                             : ':a',
                'AA'                            : ':ā',
                'I'                             : ':i',
                'II'                            : ':ī',
                'U'                             : ':u',
                'UU'                            : ':ū',
                'SHORT E'                       : ':e',
                'E'                             : ':ē',
                'AI'                            : ':ai',
                'SHORT O'                       : ':o',
                'O'                             : ':ō',
                'AU'                            : ':au',
                'VOCALIC R'                     : ':r̥',
                'VOCALIC RR'                    : ':r̥̄',
                'VOCALIC L'                     : ':l̥',
                'VOCALIC LL'                    : ':l̥̄',
         }

OTHER_SYMBOLS = {
              #.................................................................
              # not defined in ISO15919 (?) but usefull :
              #.................................................................
              'DEVANAGARI OM'                           : "<OM>",
              'DEVANAGARI DIGIT ZERO'                   : '0',
              'DEVANAGARI DIGIT ONE'                    : '1',
              'DEVANAGARI DIGIT TWO'                    : '2',
              'DEVANAGARI DIGIT THREE'                  : '3',
              'DEVANAGARI DIGIT FOUR'                   : '4',
              'DEVANAGARI DIGIT FIVE'                   : '5',
              'DEVANAGARI DIGIT SIX'                    : '6',
              'DEVANAGARI DIGIT SEVEN'                  : '7',
              'DEVANAGARI DIGIT HEIGHT'                 : '8',
              'DEVANAGARI DIGIT NINE'                   : '9',
    }

PUNCTUATION = {
              'DEVANAGARI SIGN AVAGRAHA'                : "’",

              #.................................................................
              # not defined in ISO15919 (?) but usefull :
              #.................................................................
              'DEVANAGARI DANDA'                        : '.',
              'DEVANAGARI DOUBLE DANDA'                 : '..',
              'DEVANAGARI ABBREVIATION SIGN'            : '°',
              'DEVANAGARI SIGN HIGH SPACING DOT'        : "<HIGH SPACING DOT>",
              ' '                                       : ' ',
              '.'                                       : '<.>',
              '\n'                                      : '\n',
              '\r'                                      : '\r',
              '\t'                                      : '\t',
              }

DIACRITICS = {
      'DEVANAGARI STRESS SIGN UDATTA'           : chr(0x0301),
      'DEVANAGARI STRESS SIGN ANUDATTA'         : chr(0x0331),

      'DEVANAGARI SIGN CANDRABINDU'             : 'm̐', # 006D 0310
      'DEVANAGARI SIGN ANUSVARA'                : 'ṁ', # 1E41
    }

CONSONANTS_INVERSED = invertdict(CONSONANTS)
CONSONANTS_WITH_NUKTA_INVERSED = invertdict(CONSONANTS_WITH_NUKTA)
CONSONANTS_WITH_NUKTA_TO_CONSONANT_INVERSED = invertdict(CONSONANTS_WITH_NUKTA_TO_CONSONANT)
VOWELS_INVERSED = invertdict(VOWELS)
VOWELS_IN_HIATUS_INVERSED = invertdict(VOWELS_IN_HIATUS)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)
DIACRITICS_INVERSED = invertdict(DIACRITICS)

################################################################################
# transliteration's patterns :
# PATTERN  is used to cut one complex characters into its elements.
# PATTERN2 is used to cut several complex characters into a list of complex characters.
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.

BASE_CHAR = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(CONSONANTS_INVERSED.keys())) + \
                regexstring_list(tuple(CONSONANTS_WITH_NUKTA_INVERSED.keys())) + \
                regexstring_list(tuple(VOWELS_INVERSED.keys())) + \
                regexstring_list(tuple(VOWELS_IN_HIATUS_INVERSED.keys())) + \
                regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )

ANUDATTA = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI STRESS SIGN ANUDATTA']),])

ACCENT   = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI STRESS SIGN UDATTA']),
                ])

ANUSVARA_CANDRABINDU = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI SIGN ANUSVARA']),
                 re.escape(DIACRITICS['DEVANAGARI SIGN CANDRABINDU']),
                 ])

PATTERN_TXT = "((?P<base_char>({0}))" \
              "(?P<accent>({1}))?" \
              "(?P<anudatta>({2}))?" \
              "(?P<anusvara_candrabindu>({3}))?)".format(
                            "|".join(prepare_list_to_strformat(BASE_CHAR)),
                            "|".join(prepare_list_to_strformat(ACCENT)),
                            "|".join(prepare_list_to_strformat(ANUDATTA)),
                            "|".join(prepare_list_to_strformat(ANUSVARA_CANDRABINDU)),
                            )

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "(({0})"  \
               "({1})?" \
               "({2})?" \
               "({3})?)".format(
                             "|".join(prepare_list_to_strformat(BASE_CHAR)),
                             "|".join(prepare_list_to_strformat(ACCENT)),
                             "|".join(prepare_list_to_strformat(ANUDATTA)),
                             "|".join(prepare_list_to_strformat(ANUSVARA_CANDRABINDU)),
                             )

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')
PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, prev_dchar, dchar):
    """
        function dchar__get_translit_str()

        prev_dchar, dchar : None or DCharacterSAN object

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
            # punctuation symbol :
            res.append( PUNCTUATION[dchar.base_char] )

        elif dchar.base_char in OTHER_SYMBOLS:
            # not a punctuation symbol nor a consonant or an independent vowel :
            res.append( OTHER_SYMBOLS[dchar.base_char] )

        elif not dchar.is_an_independent_vowel:
            # consonant :
            if not dchar.nukta:
                # pure devanagari consonant :
                res.append( CONSONANTS[dchar.base_char] )
            else:
                # consonant with nukta point :
                # dchar.base_char(KA) -> "q"
                letter = CONSONANTS_WITH_NUKTA_TO_CONSONANT_INVERSED[dchar.base_char]
                res.append( letter )

            # dependent vowel ?
            if dchar.dependentvowel is not None:
                res.append( VOWELS[dchar.dependentvowel] )

        else:
            # independent vowel :

            # hiatus ?
            if prev_dchar is None:
                # no hiatus : there's no preceding character.
                res.append( VOWELS[dchar.base_char] )

            elif not prev_dchar.is_an_independent_vowel and \
                 prev_dchar.dependentvowel is not None and \
                 prev_dchar.anusvara_candrabindu is None and \
                 not prev_dchar.virama:
                # yes, hiatus : a consonnant(prev_dchar) is followed by a vowel :
                res.append( VOWELS_IN_HIATUS[dchar.base_char] )

            elif prev_dchar.is_an_independent_vowel and \
                 prev_dchar.anusvara_candrabindu is None:
                 # yes, hiatus : a vowel(prev_dchar) is followed by a vowel :
                res.append( VOWELS_IN_HIATUS[dchar.base_char] )

            else:
                # no, no hiatus : no dependent vowel before the current character.
                res.append( VOWELS[dchar.base_char] )

    if dchar.accent is not None:
        res.append( DIACRITICS[dchar.accent] )

    if dchar.anudatta:
        res.append( DIACRITICS['DEVANAGARI STRESS SIGN ANUDATTA'] )

    if dchar.anusvara_candrabindu is not None:
        if dchar.anusvara_candrabindu == 'DEVANAGARI SIGN ANUSVARA':
            # anusvara :
            res.append( DIACRITICS[dchar.anusvara_candrabindu] )
        else:
            res.append( DIACRITICS[dchar.anusvara_candrabindu] )

    res = "".join( res )
    res = unicodedata.normalize('NFC', res)

    return res

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function init_from_transliteration()

        dchar   :       DCharacterSAN object
        src     :       string

        Initialize and return <dchar>.

    """
    element = re.match(PATTERN, src)

    if element is None:
        dchar.unknown_char = True
        dchar.base_char = dchar.base_char

    else:
        dchar.unknown_char = False

        dchar.anudatta = element.group('anudatta') is not None

        accent = element.group('accent')
        if accent is None:
            dchar.accent = None
        else:
            dchar.accent = DIACRITICS_INVERSED[accent]

        anusvara_candrabindu = element.group('anusvara_candrabindu')
        if anusvara_candrabindu is None:
            dchar.anusvara_candrabindu = None
        else:
            dchar.anusvara_candrabindu = DIACRITICS_INVERSED[anusvara_candrabindu]

        base_char = element.group('base_char')
        if base_char in PUNCTUATION_INVERSED:
            # punctuation symbol :
            dchar.punctuation = True
            dchar.base_char = PUNCTUATION_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

        elif base_char in OTHER_SYMBOLS_INVERSED:
            # not a punctuation symbol nor a consonant or an independent vowel :
            dchar.punctuation = False
            dchar.base_char = OTHER_SYMBOLS_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

        elif base_char in CONSONANTS_INVERSED:
            # pure devanagari consonant :
            dchar.punctuation = False
            dchar.base_char = CONSONANTS_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

            if dchar.base_char != "DEVANAGARI SIGN VISARGA":
                dchar.virama = True # by default, this consonant has no vowel.

        elif base_char in CONSONANTS_WITH_NUKTA_INVERSED:
            # consonant with nukta :
            dchar.punctuation = False
            dchar.base_char = CONSONANTS_WITH_NUKTA_TO_CONSONANT[base_char]
            dchar.nukta = True
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None
            dchar.virama = True # by default, this consonant has no vowel.

        else:
            # independent vowel ? If it's eventually a dependent vowel,
            # it will be analyzed in dstring__init_from_translit_str()
            dchar.punctuation = False
            dchar.is_an_independent_vowel = True
            dchar.dependentvowel = None
            dchar.nukta = False

            if base_char in VOWELS_INVERSED:
                dchar.base_char = VOWELS_INVERSED[base_char]
            else:
                dchar.base_char = VOWELS_IN_HIATUS_INVERSED[base_char]

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring,
                                    dcharactertype,
                                    src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterSAN
        src             :       string

        Initialize <dstring>.
    """
    #...........................................................................
    # transliteration's equivalences :
    #...........................................................................
    for start, dest in COMPACT_CHARACTERS:
        src = src.replace( start, dest )

    for start, dest in UNCOMPACT_CHARACTERS:
        src = src.replace( start, dest )

    for start, dest in TRANS_EQUIVALENCES:
        src = src.replace( start, dest )

    #...........................................................................
    # analyze of <src> :
    #...........................................................................
    last_real_index = -1
    for element in re.finditer( PATTERN2, src ):

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

        new_character = dcharactertype(dstring_object=dstring).init_from_transliteration(
            string,
            transliteration_method = "iso15919")

        if len(dstring)==0:
            dstring.append(new_character)

        else:
            prev_dchar = dstring[-1]

            # dependent vowel : we won't add another character to <dstring>
            # but we modify dstring[-1] :
            if not prev_dchar.is_an_independent_vowel and \
               not prev_dchar.punctuation and \
               prev_dchar.dependentvowel is None and \
               prev_dchar.anusvara_candrabindu is None and \
               new_character.is_an_independent_vowel:

                dstring[-1].dependentvowel = new_character.base_char
                dstring[-1].accent = new_character.accent
                dstring[-1].anusvara_candrabindu = new_character.anusvara_candrabindu
                dstring[-1].virama = new_character.virama
                dstring[-1].anudatta = new_character.anudatta

            # normal case :
            else:
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
