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
    ❏DChars❏ : dchars/languages/bod/transliterations/bodsan_symbols.py
"""

from dchars.utilities.dicttools import invertdict

#
# * CAVEAT ! If you modify these dictionaries, don't forget to modify their
#            corresponding symbols' dictionaries in symbols.py !
#
# * CAVEAT ! No duplicate value allowed in these dictionaries !
#
CONSONANTS = {
                 'K'            : chr(0x0915),
                 'KH'           : chr(0x0916),
                 'G'            : chr(0x0917),
                 'GH'           : chr(0x0918),
                 'NG'           : chr(0x0919),
                 # 'C'            : ???
                 # 'CH'           : ???
                 # 'J'            : ???
                 # 'JH'           : ???
                 'NY'           : chr(0x091E),
                 'TT'           : chr(0x091F),
                 'TTH'          : chr(0x0920),
                 'DD'           : chr(0x0921),
                 'DDH'          : chr(0x0922),
                 'NN'           : chr(0x0923),
                 'T'            : chr(0x0924),
                 'TH'           : chr(0x0925),
                 'D'            : chr(0x0926),
                 'DH'           : chr(0x0927),
                 'N'            : chr(0x0928),
                 'P'            : chr(0x092A),
                 'PH'           : chr(0x092B),
                 'B'            : chr(0x092C),
                 'BH'           : chr(0x092D),
                 'M'            : chr(0x092E),
                 'TS'           : chr(0x091A),
                 'TSH'          : chr(0x091B),
                 'DZ'           : chr(0x091C),
                 'DZH'          : chr(0x091D),
                 'W'            : chr(0x0935),
                 # 'ZH'           : 'zh',
                 # 'Z'            : 'z',
                 # '-'            : "'",
                 'Y'            : chr(0x092F),
                 'R'            : chr(0x0930),
                 'L'            : chr(0x0932),
                 'SH'           : chr(0x0936),
                 'SS'           : chr(0x0937),
                 'S'            : chr(0x0938),
                 'H'            : chr(0x0939),
                 # 'KSS'          : (chr(0x0F69),),
                 # 'FIXED-FORM R' : (chr(0x0F6A),),

                 # 'KK'           : (chr(0x0F6B),),
                 # 'RR'           : (chr(0x0F6C),),

                 # pseudo-consonant :
                 'A'             : 'FAKE_CONSONANT_A',

                # # Tibetan transliteration of Chinese sound 'F' :
                # 'TIB. TRANS. OF CHIN. SOUND F' : (chr(0x0F55)+chr(0x0F39),),
                # 'TIB. TRANS. OF CHIN. SOUND V' : (chr(0x0F56)+chr(0x0F39),),
             }

# the name of the vowels (the keys of this dictionary) must be consistent
# with symbols.py::SYMB_(IN)DEPENDENT_VOWELS
DEPENDENT_VOWELS = {
                'A'                             : 'FAKE_A',
                'AA'                            : chr(0x093E),
                'I'                             : chr(0x093F),
                'II'                            : chr(0x0940),
                'U'                             : chr(0x0941),
                'UU'                            : chr(0x0942),
                'VOCALIC R'                     : chr(0x0943),
                'VOCALIC RR'                    : chr(0x0944),
                'VOCALIC L'                     : chr(0x0962),
                'VOCALIC LL'                    : chr(0x0963),
                'E'                             : chr(0x0947),
                'AI'                            : chr(0x0948),
                'O'                             : chr(0x094B),
                'AU'                            : chr(0x094C),

                # 'REVERSED I'                    : "-i",
                # 'REVERSED II'                   : "-I",
         }

INDEPENDENT_VOWELS = {
                'A'                             : chr(0x0905),
                'AA'                            : chr(0x0906),
                'I'                             : chr(0x0907),
                'II'                            : chr(0x0908),
                'U'                             : chr(0x0909),
                'UU'                            : chr(0x090A),
                'VOCALIC R'                     : chr(0x090B),
                'VOCALIC RR'                    : chr(0x0960),
                'VOCALIC L'                     : chr(0x090C),
                'VOCALIC LL'                    : chr(0x0961),
                'E'                             : chr(0x090F),
                'AI'                            : chr(0x0910),
                'O'                             : chr(0x0913),
                'AU'                            : chr(0x0914),

                # 'REVERSED I'                    : "-i",
                # 'REVERSED II'                   : "-I",
         }

OTHER_SYMBOLS = {
                'SYLLABLE OM'                  : chr(0x0950),

                'DIGIT ZERO'                   : chr(0x0966),
                'DIGIT ONE'                    : chr(0x0967),
                'DIGIT TWO'                    : chr(0x0968),
                'DIGIT THREE'                  : chr(0x0969),
                'DIGIT FOUR'                   : chr(0x096A),
                'DIGIT FIVE'                   : chr(0x096B),
                'DIGIT SIX'                    : chr(0x096C),
                'DIGIT SEVEN'                  : chr(0x096D),
                'DIGIT HEIGHT'                 : chr(0x096E),
                'DIGIT NINE'                   : chr(0x096F),
                # 'DIGIT HALF ZERO'              : "\\u0F2A",
                # 'DIGIT HALF ONE'               : "\\u0F2B",
                # 'DIGIT HALF TWO'               : "\\u0F2C",
                # 'DIGIT HALF THREE'             : "\\u0F2D",
                # 'DIGIT HALF FOUR'              : "\\u0F2F",
                # 'DIGIT HALF FIVE'              : "\\u0F30",
                # 'DIGIT HALF SIX'               : "\\u0F31",
                # 'DIGIT HALF SEVEN'             : "\\u0F32",
                # 'DIGIT HALF HEIGHT'            : "\\u0F33",
                # 'DIGIT HALF NINE'              : "\\u0F34",

                # = Sanskrit avagraha (अवग्रह) = ऽ
                'MARK PALUTA'                   : "ऽ",
    }

PUNCTUATION = {
                 'MARK INTERSYLLABIC TSHEG'     : " ",
                 'MARK SHAD'                    : chr(0x0964),  # = Sanskrit danda
              }

DIACRITICS = {
                 'SIGN RNAM BCAD'                       : chr(0x0903),

                 'MARK HALANTA'                         : chr(0x094D),

                 'SIGN RJES SU NGA RO'                  : chr(0x0902),
                 # 'SIGN NYI ZLA NAA DA'                  : '???',
                 'SIGN SNA LDAN'                        : chr(0x0901),
             }


CONSONANTS_INVERSED = invertdict(CONSONANTS)
DEPENDENT_VOWELS_INVERSED = invertdict(DEPENDENT_VOWELS)
INDEPENDENT_VOWELS_INVERSED = invertdict(INDEPENDENT_VOWELS)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)
DIACRITICS_INVERSED = invertdict(DIACRITICS)

