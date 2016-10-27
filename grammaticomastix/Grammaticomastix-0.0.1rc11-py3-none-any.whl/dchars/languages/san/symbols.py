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
    ❏DChars❏ : dchars/languages/san/symbols.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.utilities.name2symbols import Name2Symbols

#...............................................................................
# symbols used by Sanskrit.
#
# CAVEAT ! If you modify these dictionaries, don't forget to modify thei
# corresponding transliteration's dictionaries !
#
#...............................................................................
SYMB_CONSONANTS = Name2Symbols(
    {   'KA'            : (chr(0x0915),),
        'KHA'           : (chr(0x0916),),
        'GA'            : (chr(0x0917),),
        'GHA'           : (chr(0x0918),),
        'NGA'           : (chr(0x0919),),
        'CA'            : (chr(0x091A),),
        'CHA'           : (chr(0x091B),),
        'JA'            : (chr(0x091C),),
        'JHA'           : (chr(0x091D),),
        'NYA'           : (chr(0x091E),),
        'TTA'           : (chr(0x091F),),
        'TTHA'          : (chr(0x0920),),
        'DDA'           : (chr(0x0921),),
        'DDHA'          : (chr(0x0922),),
        'NNA'           : (chr(0x0923),),
        'TA'            : (chr(0x0924),),
        'THA'           : (chr(0x0925),),
        'DA'            : (chr(0x0926),),
        'DHA'           : (chr(0x0927),),
        'NA'            : (chr(0x0928),),
        # 0x0929 ('NNNA') is defined below as a character with nukta.
        'PA'            : (chr(0x092A),),
        'PHA'           : (chr(0x092B),),
        'BA'            : (chr(0x092C),),
        'BHA'           : (chr(0x092D),),
        'MA'            : (chr(0x092E),),
        'YA'            : (chr(0x092F),),
        'RA'            : (chr(0x0930),),
        # 0x0931 ('RRA') is defined below as a character with nukta.
        'LA'            : (chr(0x0932),),
        'LLA'           : (chr(0x0933),),
        # 0x0934 ('LLLA') is defined below as a character with nukta.
        'VA'            : (chr(0x0935),),
        'SHA'           : (chr(0x0936),),
        'SSA'           : (chr(0x0937),),
        'SA'            : (chr(0x0938),),
        'HA'            : (chr(0x0939),),

        # pseudo-consonant :
        'DEVANAGARI SIGN VISARGA'         : (chr(0x0903),),
    })

# Caveat : SYMB_DEPENDENT_VOWELS and SYMB_INDEPENDENT_VOWELS must have the same keys.
SYMB_INDEPENDENT_VOWELS = Name2Symbols(
    { 'SHORT A'                         : (chr(0x0904),),
      'A'                               : (chr(0x0905),),
      'AA'                              : (chr(0x0906),),
      'I'                               : (chr(0x0907),),
      'II'                              : (chr(0x0908),),
      'U'                               : (chr(0x0909),),
      'UU'                              : (chr(0x090A),),
      'VOCALIC R'                       : (chr(0x090B),),
      'VOCALIC RR'                      : (chr(0x0960),),
      'VOCALIC L'                       : (chr(0x090C),),
      'VOCALIC LL'                      : (chr(0x0961),),
      'SHORT E'                         : (chr(0x090E),),
      'E'                               : (chr(0x090F),),
      'SHORT O'                         : (chr(0x0912),),
      'O'                               : (chr(0x0913),),
      'AI'                              : (chr(0x0910),),
      'AU'                              : (chr(0x0914),),
    })

# Caveat : SYMB_DEPENDENT_VOWELS and SYMB_INDEPENDENT_VOWELS must have the same keys.
FAKE_A__SYMBOL = "FAKE_A"       # CAVEAT : can't be set to an empty string !
SYMB_DEPENDENT_VOWELS = Name2Symbols(
    {
      # we need to define 'A' as a dependent vowel even if no symbol exists in
      # devanagari. Such a string will be deleted by DCharacterSAN.get_sourcestr_representation()
      'A'                               : (FAKE_A__SYMBOL,),

      # normal letters :
      'AA'                              : (chr(0x093E),),
      'I'                               : (chr(0x093F),),
      'II'                              : (chr(0x0940),),
      'U'                               : (chr(0x0941),),
      'UU'                              : (chr(0x0942),),
      'VOCALIC R'                       : (chr(0x0943),),
      'VOCALIC RR'                      : (chr(0x0944),),
      'CANDRA E'                        : (chr(0x0945),),
      'SHORT E'                         : (chr(0x0946),),
      'E'                               : (chr(0x0947),),
      'AI'                              : (chr(0x0948),),
      'CANDRA O'                        : (chr(0x0949),),
      'SHORT O'                         : (chr(0x094A),),
      'O'                               : (chr(0x094B),),
      'AU'                              : (chr(0x094C),),
      'VOCALIC L'                       : (chr(0x0962),),
      'VOCALIC LL'                      : (chr(0x0963),),
    })

SYMB_OTHER_SYMBOLS = Name2Symbols(
    {
      'DEVANAGARI OM'                           : (chr(0x0950),),

      'DEVANAGARI DIGIT ZERO'                   : (chr(0x0966),),
      'DEVANAGARI DIGIT ONE'                    : (chr(0x0967),),
      'DEVANAGARI DIGIT TWO'                    : (chr(0x0968),),
      'DEVANAGARI DIGIT THREE'                  : (chr(0x0969),),
      'DEVANAGARI DIGIT FOUR'                   : (chr(0x096A),),
      'DEVANAGARI DIGIT FIVE'                   : (chr(0x096B),),
      'DEVANAGARI DIGIT SIX'                    : (chr(0x096C),),
      'DEVANAGARI DIGIT SEVEN'                  : (chr(0x096D),),
      'DEVANAGARI DIGIT HEIGHT'                 : (chr(0x096E),),
      'DEVANAGARI DIGIT NINE'                   : (chr(0x096F),),

      '0'                                       : ( "0", ),
      '1'                                       : ( "1", ),
      '2'                                       : ( "2", ),
      '3'                                       : ( "3", ),
      '4'                                       : ( "4", ),
      '5'                                       : ( "5", ),
      '6'                                       : ( "6", ),
      '7'                                       : ( "7", ),
      '8'                                       : ( "8", ),
      '9'                                       : ( "9", ),
    })

SYMB_PUNCTUATION = Name2Symbols(
    { 'DEVANAGARI DANDA'                        : (chr(0x0964),),
      'DEVANAGARI DOUBLE DANDA'                 : (chr(0x0965), chr(0x007C)),
      'DEVANAGARI ABBREVIATION SIGN'            : (chr(0x0970),),
      'DEVANAGARI SIGN HIGH SPACING DOT'        : (chr(0x0971),),
      'DEVANAGARI SIGN AVAGRAHA'                : (chr(0x093D),),
      ' '                                       : (" ",),
      '.'                                       : (".",),
      '\n'                                      : ('\n',),
      '\r'                                      : ('\r',),
      '\t'                                      : ('\t',),
      '('                                       : ( "(", ),
      ')'                                       : ( ")", ),
      '-'                                       : ( "-", ),
      '`'                                       : ( "`", ),
      "'"                                       : ( "'",),
      "?"                                       : ( "?",),
      "!"                                       : ( "!",),
    })

SYMB_DIACRITICS = Name2Symbols(
    { 'DEVANAGARI SIGN INVERTED CANDRABINDU'    : (chr(0x0900),),
      'DEVANAGARI SIGN CANDRABINDU'             : (chr(0x0901),),
      'DEVANAGARI SIGN ANUSVARA'                : (chr(0x0902),),
      'DEVANAGARI SIGN NUKTA'                   : (chr(0x093C),),
      'DEVANAGARI STRESS SIGN UDATTA'           : (chr(0x0951),),
      'DEVANAGARI STRESS SIGN ANUDATTA'         : (chr(0x0952),),
      'DEVANAGARI GRAVE ACCENT'                 : (chr(0x0953),chr(0x0300)),
      'DEVANAGARI ACUTE ACCENT'                 : (chr(0x0954),chr(0x0301)),
      'DEVANAGARI SIGN VIRAMA'                  : (chr(0x094D),),
    })
# we define these constants in order to avoir multiple calls to SYMB_DIACRITICS.get_default_symbol :
DEFAULTSYMB__VIRAMA = SYMB_DIACRITICS.get_default_symbol("DEVANAGARI SIGN VIRAMA")
DEFAULTSYMB__ANUDATTA = SYMB_DIACRITICS.get_default_symbol("DEVANAGARI STRESS SIGN ANUDATTA")
DEFAULTSYMB__NUKTA = SYMB_DIACRITICS.get_default_symbol("DEVANAGARI SIGN NUKTA")

#...............................................................................
# we calculate these tuples which are often used in order to speed up the code :
#...............................................................................
SYMB_DIACRITICS__ACCENTS = (
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI STRESS SIGN UDATTA'),
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI ACUTE ACCENT'),
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI GRAVE ACCENT'),
                            )

SYMB_DIACRITICS__NUKTA = (
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN NUKTA'),
                         )

SYMB_DIACRITICS__ANUSVARA_CANDRABINDU = (
                SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN ANUSVARA'),
                SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN CANDRABINDU'),
                SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN INVERTED CANDRABINDU'),
                              )

SYMB_DIACRITICS__VIRAMA = (
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN VIRAMA'),
                          )

SYMB_DIACRITICS__ANUSVARA = (
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI SIGN ANUSVARA'),
                          )

SYMB_DIACRITICS__ANUDATTA = (
                            SYMB_DIACRITICS.get_default_symbol('DEVANAGARI STRESS SIGN ANUDATTA'),
                          )
