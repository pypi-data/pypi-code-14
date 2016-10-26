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
    ❏DChars❏ : dchars/languages/bod/symbols.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.utilities.name2symbols import Name2Symbols

#...............................................................................
# symbols used by Tibetan.
#
# CAVEAT ! If you modify these dictionaries, don't forget to modify their
# corresponding transliteration's dictionaries !
#
#...............................................................................
SYMB_CONSONANTS = Name2Symbols(
    {   'K'            : (chr(0x0F40),),
        'KH'           : (chr(0x0F41),),
        'G'            : (chr(0x0F42),),
        'GH'           : (chr(0x0F43),),
        'NG'           : (chr(0x0F44),),
        'C'            : (chr(0x0F45),),
        'CH'           : (chr(0x0F46),),
        'J'            : (chr(0x0F47),),
        'NY'           : (chr(0x0F49),),
        'TT'           : (chr(0x0F4A),),
        'TTH'          : (chr(0x0F4B),),
        'DD'           : (chr(0x0F4C),),
        'DDH'          : (chr(0x0F4D),),
        'NN'           : (chr(0x0F4E),),
        'T'            : (chr(0x0F4F),),
        'TH'           : (chr(0x0F50),),
        'D'            : (chr(0x0F51),),
        'DH'           : (chr(0x0F52),),
        'N'            : (chr(0x0F53),),
        'P'            : (chr(0x0F54),),
        'PH'           : (chr(0x0F55),),
        'B'            : (chr(0x0F56),),
        'BH'           : (chr(0x0F57),),
        'M'            : (chr(0x0F58),),
        'TS'           : (chr(0x0F59),),
        'TSH'          : (chr(0x0F5A),),
        'DZ'           : (chr(0x0F5B),),
        'DZH'          : (chr(0x0F5C),),
        'W'            : (chr(0x0F5D),),
        'ZH'           : (chr(0x0F5E),),
        'Z'            : (chr(0x0F5F),),
        '-'            : (chr(0x0F60),),
        'Y'            : (chr(0x0F61),),
        'R'            : (chr(0x0F62),),
        'L'            : (chr(0x0F63),),
        'SH'           : (chr(0x0F64),),
        'SS'           : (chr(0x0F65),),
        'S'            : (chr(0x0F66),),
        'H'            : (chr(0x0F67),),
        'KSS'          : (chr(0x0F69),),
        'FIXED-FORM R' : (chr(0x0F6A),),

        'KK'           : (chr(0x0F6B),),
        'RR'           : (chr(0x0F6C),),

        # pseudo-consonant :
        'A'             : (chr(0x0F68),),

        # Tibetan transliteration of Chinese sound 'F' :
        'TIB. TRANS. OF CHIN. SOUND F' : (chr(0x0F55)+chr(0x0F39),),
        'TIB. TRANS. OF CHIN. SOUND V' : (chr(0x0F56)+chr(0x0F39),),
    })

SYMB_SUBJOINED_CONSONANTS = Name2Symbols(
    {
        'K'            : (chr(0x0F90),),
        'KH'           : (chr(0x0F91),),
        'G'            : (chr(0x0F92),),
        'GH'           : (chr(0x0F93),),
        'NG'           : (chr(0x0F94),),
        'C'            : (chr(0x0F95),),
        'CH'           : (chr(0x0F96),),
        'J'            : (chr(0x0F97),),
        'NY'           : (chr(0x0F99),),
        'TT'           : (chr(0x0F9A),),
        'TTH'          : (chr(0x0F9B),),
        'DD'           : (chr(0x0F9C),),
        'DDH'          : (chr(0x0F9D),),
        'NN'           : (chr(0x0F9E),),
        'T'            : (chr(0x0F9F),),
        'TH'           : (chr(0x0FA0),),
        'D'            : (chr(0x0FA1),),
        'DH'           : (chr(0x0FA2),),
        'N'            : (chr(0x0FA3),),
        'P'            : (chr(0x0FA4),),
        'PH'           : (chr(0x0FA5),),
        'B'            : (chr(0x0FA6),),
        'BH'           : (chr(0x0FA7),),
        'M'            : (chr(0x0FA8),),
        'TS'           : (chr(0x0FA9),),
        'TSH'          : (chr(0x0FAA),),
        'DZ'           : (chr(0x0FAB),),
        'DZH'          : (chr(0x0FAC),),
        'W'            : (chr(0x0FAD),),
        'ZH'           : (chr(0x0FAE),),
        'Z'            : (chr(0x0FAF),),
        '-'            : (chr(0x0FB0),),
        'Y'            : (chr(0x0FB1),),
        'R'            : (chr(0x0FB2),),
        'L'            : (chr(0x0FB3),),
        'SH'           : (chr(0x0FB4),),
        'SS'           : (chr(0x0FB5),),
        'S'            : (chr(0x0FB6),),
        'H'            : (chr(0x0FB7),),
        'KSS'          : (chr(0x0FB9),),

        # pseudo-consonant :
        'A'             : (chr(0x0FB8),),
    })

SYMB_FIXEDFORM_SUBJOINED_CONSONANTS = Name2Symbols(
    {
        'W'            : (chr(0x0FBA),),
        'Y'            : (chr(0x0FBB),),
        'R'            : (chr(0x0FBC),),
    })

# Caveat : SYMB_VOWELS and SYMB_INDEPENDENT_VOWELS must have the same keys.
FAKE_A__SYMBOL = "FAKE_A"       # CAVEAT : can't be set to an empty string !
SYMB_VOWELS = Name2Symbols(
    {
      # we need to define 'A' as a dependent vowel even if no symbol exists in
      # devanagari. Such a string will be deleted by DCharacterBOD.get_sourcestr_representation()
      'A'                               : (FAKE_A__SYMBOL,),

      # normal letters :
      'AA'                              : (chr(0x0F71),),
      'I'                               : (chr(0x0F72),),
      'II'                              : (chr(0x0F73),),
      'U'                               : (chr(0x0F74),),
      'UU'                              : (chr(0x0F75),),
      'VOCALIC R'                       : (chr(0x0F76),),
      'VOCALIC RR'                      : (chr(0x0F77),),
      'VOCALIC L'                       : (chr(0x0F78),),
      'VOCALIC LL'                      : (chr(0x0F79),),
      'E'                               : (chr(0x0F7A),),
      'AI'                              : (chr(0x0F7B),),
      'O'                               : (chr(0x0F7C),),
      'AU'                              : (chr(0x0F7D),),

      'REVERSED I'                      : (chr(0x0F80),),
      'REVERSED II'                     : (chr(0x0F81),),
    })

SYMB_OTHER_SYMBOLS = Name2Symbols(
    {
      'SYLLABLE OM'                  : (chr(0x0F00),),

      # astrological signs (1/2) :
      'LOGOTYPE SIGN CHAD RTAGS'     : (chr(0x0F15),),
      'LOGOTYPE SIGN LHAG RTAGS'     : (chr(0x0F16),),
      'ASTROLOGICAL SIGN SGRA GCAN-CHAR RTAGS' : (chr(0x0F17),),
      'ASTROLOGICAL SIGN -KHYUD PA'  : (chr(0x0F18),),
      'ASTROLOGICAL SIGN SDONG TSHUGS' : (chr(0x0F19),),
      'SIGN RDEL DKAR GCIG'          : (chr(0x0F1A),),
      'SIGN RDEL DKAR GNYIS'         : (chr(0x0F1B),),
      'SIGN RDEL DKAR GSUM'          : (chr(0x0F1C),),
      'SIGN RDEL NAG GCIG'           : (chr(0x0F1D),),
      'SIGN RDEL NAG GNYIS'          : (chr(0x0F1E),),
      'SIGN RDEL DKAR RDEL NAG'      : (chr(0x0F1F),),

      # astrological signs (2/2) :
      'SIGN YAR TSHES'               : (chr(0x0F3E),),
      'SIGN MAR TSHES'               : (chr(0x0F3F),),

      # digits :
      'DIGIT ZERO'                   : (chr(0x0F20),),
      'DIGIT ONE'                    : (chr(0x0F21),),
      'DIGIT TWO'                    : (chr(0x0F22),),
      'DIGIT THREE'                  : (chr(0x0F23),),
      'DIGIT FOUR'                   : (chr(0x0F24),),
      'DIGIT FIVE'                   : (chr(0x0F25),),
      'DIGIT SIX'                    : (chr(0x0F26),),
      'DIGIT SEVEN'                  : (chr(0x0F27),),
      'DIGIT HEIGHT'                 : (chr(0x0F28),),
      'DIGIT NINE'                   : (chr(0x0F29),),
      'DIGIT HALF ZERO'              : (chr(0x0F2A),),
      'DIGIT HALF ONE'               : (chr(0x0F2B),),
      'DIGIT HALF TWO'               : (chr(0x0F2C),),
      'DIGIT HALF THREE'             : (chr(0x0F2D),),
      'DIGIT HALF FOUR'              : (chr(0x0F2E),),
      'DIGIT HALF FIVE'              : (chr(0x0F2F),),
      'DIGIT HALF SIX'               : (chr(0x0F30),),
      'DIGIT HALF SEVEN'             : (chr(0x0F31),),
      'DIGIT HALF HEIGHT'            : (chr(0x0F32),),
      'DIGIT HALF NINE'              : (chr(0x0F33),),

      # Symbols :
      'SYMBOL DRIL BU'                  : (chr(0x0FC4),),
      'SYMBOL RDO RJE'                  : (chr(0x0FC5),),
      'SYMBOL PADMA GDAN'               : (chr(0x0FC6),),
      'SYMBOL RDO RJE RGYA GRAM'        : (chr(0x0FC7),),
      'SYMBOL PHUR PA'                  : (chr(0x0FC8),),
      'SYMBOL NOR BU'                   : (chr(0x0FC9),),
      'SYMBOL NOR BU NYIS -KHYIL'       : (chr(0x0FCA),),
      'SYMBOL NOR BU GSUM -KHYIL'       : (chr(0x0FCB),),
      'SYMBOL NOR BU BZHI -KHYIL'       : (chr(0x0FCC),),

      # Astrological signs :
      'SIGN RDEL NAG RDEL DKAR'         : (chr(0x0FCE),),
      'SIGN RDEL NAG GSUM'              : (chr(0x0FCF),),

      # Religious symbols :
      'RIGHT-FACING SVASTI SIGN'                : (chr(0x0FD5),),
      'LEFT-FACING SVASTI SIGN'                 : (chr(0x0FD6),),
      'RIGHT-FACING SVASTI SIGN WITH DOTS'      : (chr(0x0FD7),),
      'LEFT-FACING SVASTI SIGN WITH DOTS'       : (chr(0x0FD8),),

      # Annotation marks :
      'MARK LEADING MCHAN RTAGS'        : (chr(0x0FD9),),
      'MARK TRAILING MCHAN RTAGS'       : (chr(0x0FDA),),

      # cantillation signs :
      'CANTILLATION SIGN HEAVY BEAT'    : (chr(0x0FC0),),
      'CANTILLATION SIGN LIGHT BEAT'    : (chr(0x0FC1),),
      'CANTILLATION SIGN CANG TE-U'     : (chr(0x0FC2),),
      'CANTILLATION SIGN SBUB -CHAL'    : (chr(0x0FC3),),
    })

SYMB_PUNCTUATION = Name2Symbols(
    {
      # Head marks :
      'MARK GTER YIG MGO TRUNCATED A': (chr(0x0F01),),
      'MARK GTER YIG MGO -UM RNAM BCAD MA' : (chr(0x0F02),),
      'MARK GTER YIG MGO -UM GTER TSHEG MA' : (chr(0x0F03),),
      'MARK INITIAL YIG MGO MDUN MA' : (chr(0x0F04),),
      'MARK CLOSING YIG MGO SGAB MA' : (chr(0x0F05),),
      'MARK CARET YIG MGO PHUR SHAD MA' : (chr(0x0F06),),
      'MARK YIG MGO TSHEG SHAD MA'   : (chr(0x0F07),),

      # Marks and signs :
      'MARK SBRUL SHAD'                 : (chr(0x0F08),),
      'MARK BSKUR YIG MGO'              : (chr(0x0F09),),
      'MARK BKA- SHOG YIG MGO'          : (chr(0x0F0A),),
      'MARK INTERSYLLABIC TSHEG'        : (chr(0x0F0B),),
      'MARK DELIMITER TSHEG BSTAR'      : (chr(0x0F0C),),
      'MARK SHAD'                       : (chr(0x0F0D),),
      'MARK NYIS SHAD'                  : (chr(0x0F0E),),
      'MARK TSHEG SHAD'                 : (chr(0x0F0F),),
      'MARK NYIS TSHEG SHAD'            : (chr(0x0F10),),
      'MARK RIN CHEN SPUNGS SHAD'       : (chr(0x0F11),),
      'MARK RGYA GRAM SHAD'             : (chr(0x0F12),),
      'MARK CARET -DZUD RTAGS ME LONG CAN' : (chr(0x0F13),),
      'MARK GTER TSHEG'                 : (chr(0x0F14),),

      # Marks and signs :
      'MARK BSDUS RTAGS'                : (chr(0x0F34),),
      'MARK NGAS BZUNG NYI ZLA'         : (chr(0x0F35),),
      'MARK CARET -DZUD RTAGS BZHI MIG CAN'     : (chr(0x0F36),),
      'MARK NGAS BZUNG SGOR RTAGS'      : (chr(0x0F37),),
      'MARK CHE MGO'                    : (chr(0x0F38),),
      'MARK TSA -PHRU'                  : (chr(0x0F39),),

      # Paired punctuation :
      'MARK GUG RTAGS GYON'             : (chr(0x0F3A),),
      'MARK GUG RTAGS GYAS'             : (chr(0x0F3B),),
      'MARK ANG KHANG GYON'             : (chr(0x0F3C),),
      'MARK ANG KHANG GYAS'             : (chr(0x0F3D),),

      # Marks and signs :
      'SIGN NYI ZLA NAA DA'             : (chr(0x0F82),),

      'SIGN LCI RTAGS'                  : (chr(0x0F86),),
      'SIGN YANG RTAGS'                 : (chr(0x0F87),),

      # Transliteration head letters :
      'SIGN GRU CAN RGYINGS'            : (chr(0x0F8A),),
      'SIGN GRU MED RGYINGS'            : (chr(0x0F8B),),
      'SIGN INVERTED MCHU CAN'          : (chr(0x0F8C),),

      # Transliteration subjoined signs :
      'SUBJOINED SIGN LCE TSA CAN'      : (chr(0x0F8D),),
      'SUBJOINED SIGN MCHU CAN'         : (chr(0x0F8E),),
      'SUBJOINED SIGN INVERTED MCHU CAN': (chr(0x0F8F),),

      # Signs :
      'KU RU KHA'                       : (chr(0x0FBE),),
      'KU RU KHA BZHI MIG CAN'          : (chr(0x0FBF),),

      # Marks :
      'MARK BSKA- SHOG GI MGO RGYAN'    : (chr(0x0FD0),),
      'MARK MNYAM YIG GI MGO RGYAN'     : (chr(0x0FD1),),
      'MARK NYIS TSHEG'                 : (chr(0x0FD2),),

      # Head marks :
      'MARK INITIAL BRDA RNYING YIG MGO MDUN MA' : (chr(0x0FD3),),
      'MARK CLOSING BRDA RNYING YIG MGO SGAB MA' : (chr(0x0FD4),),

      # = Sanskrit avagraha (अवग्रह) = ऽ
      'MARK PALUTA'                     : (chr(0x0F85),),

      # others :
      ' '                                       : (" ",),
      '\n'                                      : ('\n',),
      '\r'                                      : ('\r',),
      '\t'                                      : ('\t',),

    })

SYMB_DIACRITICS = Name2Symbols(
    {
      # = Sanskrit visarga :
      'SIGN RNAM BCAD'                  : (chr(0x0F7F),),

      # = srog med = Sanskrit virama
      'MARK HALANTA'                    : (chr(0x0F84),),

      # = Sanskrit anusvara
      'SIGN RJES SU NGA RO'             : (chr(0x0F7E),),

      # = Sanskrit candrabindu
      'SIGN NYI ZLA NAA DA'             : (chr(0x0F82),),
      'SIGN SNA LDAN'                   : (chr(0x0F83),),
    })
# we define these constant(s) in order to avoir multiple calls to
# SYMB_DIACRITICS.get_default_symbol :
SYMB_DIACRITICS__RNAM_BCAD = SYMB_DIACRITICS.get_default_symbol('SIGN RNAM BCAD')
SYMB_DIACRITICS__HALANTA = SYMB_DIACRITICS.get_default_symbol('MARK HALANTA')

#...............................................................................
# we calculate these tuples which are often used in order to speed up the code :
#...............................................................................
SYMB_DIACRITICS__ANUSV_CANDR = (
        SYMB_DIACRITICS.get_default_symbol('SIGN RJES SU NGA RO'),
        SYMB_DIACRITICS.get_default_symbol('SIGN NYI ZLA NAA DA'),
        SYMB_DIACRITICS.get_default_symbol('SIGN SNA LDAN'),
    )

#...............................................................................
# list of symbols used in Tibetan words derived from Sanskrit :
#...............................................................................
TIBETANSANSKRIT_SYMB_CONSONANTS = (
        'GH',
        'DH',
        'BH',
        'DZH',
        'TT',
        'TTH',
        'DD',
        'DDH',
        'NN',
        'SS',
        'KSS',
        'FIXED-FORM R',
    )

TIBETANSANSKRIT_SYMB_FIXSUBJCO = (
        'W',
        'Y',
        'R',
    )

TIBETANSANSKRIT_SYMB_VOWELS = (
      'AA',
      'II',
      'UU',
      "AI",
      "AU",
      'VOCALIC R',
      'VOCALIC RR',
      'VOCALIC L',
      'VOCALIC LL',
      'REVERSED I',
      'REVERSED II',
    )

TIBETANSANSKRIT_SYMB_DIACRITICS = (
        # @@BOD-INTERNALSTRUCTURE-007
        # 'SIGN RNAM BCAD',
        # # "gtiH" and not "gatiH", so rnam bcad isn't an evidence of a Sanskrit word

        'MARK HALANTA',

        # @@BOD-INTERNALSTRUCTURE-008
        # 'SIGN RJES SU NGA RO',
        # ཁསཾ = "khaMs" and not "khasaM", so rjes su nga ro isn't an evidence of a Sanskrit word

        'SIGN NYI ZLA NAA DA',
        'SIGN SNA LDAN',
    )

TIBETANSANSKRIT_SYMB_PUNCTUATION = (
        'MARK PALUTA',
    )

# corresponding Unicode symbols :
TIBETANSANSKRIT_UNICODE_SYMBOLS = \
  list(map(SYMB_CONSONANTS.get_default_symbol,
           TIBETANSANSKRIT_SYMB_CONSONANTS)) + \
  list(map(SYMB_FIXEDFORM_SUBJOINED_CONSONANTS.get_default_symbol,
           TIBETANSANSKRIT_SYMB_FIXSUBJCO)) + \
  list(map(SYMB_VOWELS.get_default_symbol,
           TIBETANSANSKRIT_SYMB_VOWELS)) + \
  list(map(SYMB_DIACRITICS.get_default_symbol,
           TIBETANSANSKRIT_SYMB_DIACRITICS)) + \
  list(map(SYMB_PUNCTUATION.get_default_symbol,
           TIBETANSANSKRIT_SYMB_PUNCTUATION))

################################################################################
# SPACING SYMBOLS :
################################################################################
TSHEG_SYMBOL = SYMB_PUNCTUATION.get_default_symbol('MARK INTERSYLLABIC TSHEG')
SPACE_SYMBOL = SYMB_PUNCTUATION.get_default_symbol(' ')

# ################################################################################
# # symbols used by Tibetan words derived from Sanskrit :
# ################################################################################
# TIBETANSANSKRIT_TRANSLITERATED_SYMBOLS = \
#   list(TIBETANSANSKRIT_SYMB_CONSONANTS) + \
#   list(SYMB_FIXEDFORM_SUBJOINED_CONSONANTS) + \
#   list(TIBETANSANSKRIT_SYMB_CONSONANTS) + \
#   list(TIBETANSANSKRIT_SYMB_PUNCTUATION)


