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
    ❏DChars❏ : dchars/languages/bod/transliterations/ewts/ewts_symbols.py
"""

from dchars.utilities.dicttools import invertdict

#
# * CAVEAT ! If you modify these dictionaries, don't forget to modify their
#            corresponding symbols' dictionaries in symbols.py !
#
# * CAVEAT ! No duplicate value allowed in these dictionaries !
#
CONSONANTS = {
                 'K'            : 'k',
                 'KH'           : 'kh',
                 'G'            : 'g',
                 'GH'           : 'g+h',
                 'NG'           : 'ng',
                 'C'            : 'c',
                 'CH'           : 'ch',
                 'J'            : 'j',
                 'NY'           : 'ny',
                 'TT'           : 'T',
                 'TTH'          : 'Th',
                 'DD'           : 'D',
                 'DDH'          : 'D+h',
                 'NN'           : 'N',
                 'T'            : 't',
                 'TH'           : 'th',
                 'D'            : 'd',
                 'DH'           : 'd+h',
                 'N'            : 'n',
                 'P'            : 'p',
                 'PH'           : 'ph',
                 'B'            : 'b',
                 'BH'           : 'b+h',
                 'M'            : 'm',

                 'TS'           : 'ts',
                 'TSH'          : 'tsh',
                 'DZ'           : 'dz',
                 'DZH'          : 'dz+h',
                 'W'            : 'w',
                 'ZH'           : 'zh',
                 'Z'            : 'z',
                 '-'            : "'",
                 'Y'            : 'y',
                 'R'            : 'r',
                 'L'            : 'l',
                 'SH'           : 'sh',
                 'SS'           : 'Sh',
                 'S'            : 's',
                 'H'            : 'h',
                 'KSS'          : 'k+Sh',

                 'FIXED-FORM R' : 'R+',
                 # 'KK'           : (chr(0x0F6B),),
                 # 'RR'           : (chr(0x0F6C),),

                 'SIGN VISARGA'         : 'ḥ',

                 # pseudo-consonant :
                 'A'             : 'KAKE_A',

                 'TIB. TRANS. OF CHIN. SOUND F' : 'f',
                 'TIB. TRANS. OF CHIN. SOUND V' : 'v',
             }

FIXEDFORM_SUBJOINED_CONSONANTS = {
                'W'            : "+W",
                'Y'            : "+Y",
                'R'            : "+R",
             }

# the name of the vowels (the keys of this dictionary) must be consistent
# with symbols.py::SYMB_VOWELS
VOWELS = {
                'A'                             : 'a',
                'AA'                            : 'A',
                'I'                             : 'i',
                'II'                            : 'I',
                'U'                             : 'u',
                'UU'                            : 'U',
                'VOCALIC R'                     : 'r-i',
                'VOCALIC RR'                    : 'r-I',
                'VOCALIC L'                     : 'l-i',
                'VOCALIC LL'                    : 'l-I',
                'E'                             : 'e',
                'AI'                            : 'ai',
                'O'                             : 'o',
                'AU'                            : 'au',

                'REVERSED I'                    : "-i",
                'REVERSED II'                   : "-I",
         }

OTHER_SYMBOLS = {
                # from http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/3/
                'DIGIT ZERO'                   : "0",
                'DIGIT ONE'                    : "1",
                'DIGIT TWO'                    : "2",
                'DIGIT THREE'                  : "3",
                'DIGIT FOUR'                   : "4",
                'DIGIT FIVE'                   : "5",
                'DIGIT SIX'                    : "6",
                'DIGIT SEVEN'                  : "7",
                'DIGIT HEIGHT'                 : "8",
                'DIGIT NINE'                   : "9",
                'DIGIT HALF ZERO'              : "\\u0F2A",
                'DIGIT HALF ONE'               : "\\u0F2B",
                'DIGIT HALF TWO'               : "\\u0F2C",
                'DIGIT HALF THREE'             : "\\u0F2D",
                'DIGIT HALF FOUR'              : "\\u0F2F",
                'DIGIT HALF FIVE'              : "\\u0F30",
                'DIGIT HALF SIX'               : "\\u0F31",
                'DIGIT HALF SEVEN'             : "\\u0F32",
                'DIGIT HALF HEIGHT'            : "\\u0F33",
                'DIGIT HALF NINE'              : "\\u0F34",

                # from http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/4/
                'SYLLABLE OM'                  : "oM",
    }

PUNCTUATION = {  # from http://www.thlib.org/reference/transliteration/#!essay=/thl/ewts/5/
                 'MARK INTERSYLLABIC TSHEG'        : " ",
                 'MARK DELIMITER TSHEG BSTAR'      : "*",
                 'MARK SHAD'                       : "/",
                 'MARK NYIS SHAD'                  : "//",
                 'MARK TSHEG SHAD'                 : ";",
                 'MARK RIN CHEN SPUNGS SHAD'       : "|",
                 'MARK SBRUL SHAD'                 : "!",
                 'MARK GTER TSHEG'                 : ":",
                 'MARK NYIS TSHEG SHAD'            : "\\u0F10",
                 'MARK RGYA GRAM SHAD'             : "\\u0F12",
                 " "                                       : "_",
                 'MARK BSDUS RTAGS'                : "=",
                 'KU RU KHA'                       : "\\u0FBE",
                 'KU RU KHA BZHI MIG CAN'          : "\\u0FBF",
                 'MARK CARET -DZUD RTAGS BZHI MIG CAN'  : "\\u0F36",
                 'MARK CARET -DZUD RTAGS ME LONG CAN'   : "\\u0F13",
                 'MARK GTER YIG MGO TRUNCATED A'        : "\\u0F01",
                 'MARK GTER YIG MGO -UM RNAM BCAD MA'   : "\\u0F02",
                 'MARK GTER YIG MGO -UM GTER TSHEG MA'  : "\\u0F03",
                 'MARK INITIAL YIG MGO MDUN MA'         : "@",
                 'MARK CLOSING YIG MGO SGAB MA'         : "#",
                 'MARK CARET YIG MGO PHUR SHAD MA'      : "$",
                 'MARK YIG MGO TSHEG SHAD MA'           : "%",
                 'MARK BSKUR YIG MGO'                   : "\\u0F09",
                 'MARK BKA- SHOG YIG MGO'               : "\\u0F0A",
                 'MARK BSKA- SHOG GI MGO RGYAN'         : "\\u0FD0",
                 'MARK MNYAM YIG GI MGO RGYAN'          : "\\u0FD1",
                 'MARK GUG RTAGS GYON'                  : "<",
                 'MARK GUG RTAGS GYAS'                  : ">",
                 'MARK ANG KHANG GYON'                  : "(",
                 'MARK ANG KHANG GYAS'                  : ")",

                 # = Sanskrit avagraha (अवग्रह) = ऽ
                 'MARK PALUTA'                          : "&",
              }

DIACRITICS = {
                 # = Sanskrit visarga :
                 'SIGN RNAM BCAD'                       : 'H',

                 # = srog med = Sanskrit virama
                 'MARK HALANTA'                         : '?',

                 # = Sanskrit anusvara
                 'SIGN RJES SU NGA RO'                  : 'M',

                 # = Sanskrit candrabindu
                 'SIGN NYI ZLA NAA DA'                  : '~M`',
                 'SIGN SNA LDAN'                        : '~M',
             }

CONSONANTS_INVERSED = invertdict(CONSONANTS)
VOWELS_INVERSED = invertdict(VOWELS)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)
DIACRITICS_INVERSED = invertdict(DIACRITICS)

