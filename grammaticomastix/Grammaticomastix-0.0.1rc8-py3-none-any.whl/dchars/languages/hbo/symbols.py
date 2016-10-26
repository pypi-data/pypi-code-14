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
    ❏DChars❏ : dchars/languages/hbo/symbols.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"

from dchars.utilities.name2symbols import Name2Symbols

#...............................................................................
# symbols used by the Ancient Hebrew language.
#
# CAVEAT ! If you modify these dictionaries, don't forget to modify thei
# corresponding transliteration's dictionaries !
#
#...............................................................................
# NB : Even if I choosed letters' names derived from the unicode names
#      of these letters, I could use other names such as "alef", "א", and so on.
#
SYMB_LETTERS = Name2Symbols(
    { 'ALEF'              : ('א','ℵ'),
      'BET'               : ('ב','ℶ'),
      'GIMEL'             : ('ג','ℷ'),
      'DALET'             : ('ד','ℸ'),
      'HE'                : ('ה',),
      'VAV'               : ('ו',),
      'ZAYIN'             : ('ז',),
      'HET'               : ('ח',),
      'TET'               : ('ט',),
      'YOD'               : ('י',),
      'KAF'               : ('כ',),
      'FINAL KAF'         : ('ך',),
      'LAMED'             : ('ל',),
      'MEM'               : ('מ',),
      'FINAL MEM'         : ('ם',),
      'NUN'               : ('נ',),
      'FINAL NUN'         : ('ן',),
      'SAMEKH'            : ('ס',),
      'AYIN'              : ('ע',),
      'PE'                : ('פ',),
      'FINAL PE'          : ('ף',),
      'TSADI'             : ('צ',),
      'FINAL TSADI'       : ('ץ',),
      'QOF'               : ('ק'),
      'RESH'              : ('ר',),
      'SHIN'              : ('ש',),
      'TAV'               : ('ת',),
      })

SYMB_OTHER_SYMBOLS = Name2Symbols(
    {
     '0'        : ('0',),
     '1'        : ('1',),
     '2'        : ('2',),
     '3'        : ('3',),
     '4'        : ('4',),
     '5'        : ('5',),
     '6'        : ('6',),
     '7'        : ('7',),
     '8'        : ('8',),
     '9'        : ('9',),
    })

SYMB_PUNCTUATION = Name2Symbols(
    {')'        : (')',),
     '('        : ('(',),
     '['        : ('[',),
     ']'        : (']',),
     '{'        : ('{',),
     '}'        : ('}',),
     ' '        : (' ',),
     '\n'       : ('\n',),
     '\r'       : ('\r',),
     '\t'       : ('\t',),

     "HEBREW PUNCTUATION PASEQ"         : ( chr(0x05C0),),      # א׀
     "HEBREW PUNCTUATION SOF PASUQ"     : ( chr(0x05C3), ":"),  # א׃
     "HEBREW PUNCTUATION MAQAF"         : ( chr(0x05BE),),      # א־
     "HEBREW PUNCTUATION NUN HAFUKHA"   : ( chr(0x05C6),),      # ׆

     "LEFT-TO-RIGHT MARK"               : ( chr(0x200E),),
     "RIGHT-TO-LEFT MARK"               : ( chr(0x200F),),
    })

SYMB_VOWELS = Name2Symbols(
    {"HEBREW POINT SHEVA"               : ( chr(0x05B0),),      # אְ
     "HEBREW POINT HATAF SEGOL"         : ( chr(0x05B1),),      # אֱ
     "HEBREW POINT HATAF PATAH"         : ( chr(0x05B2),),      # אֲ
     "HEBREW POINT HATAF QAMATS"        : ( chr(0x05B3),),      # אֳ
     "HEBREW POINT HIRIQ"               : ( chr(0x05B4),),      # אִ
     "HEBREW POINT TSERE"               : ( chr(0x05B5),),      # אֵ
     "HEBREW POINT SEGOL"               : ( chr(0x05B6),),      # אֶ
     "HEBREW POINT PATAH"               : ( chr(0x05B7),),      # אַ
     "HEBREW POINT QAMATS"              : ( chr(0x05B8),),      # אָ
     "HEBREW POINT HOLAM"               : ( chr(0x05B9),),      # אֹ
     "HEBREW POINT HOLAM HASER FOR VAV" : ( chr(0x05BA),),      # אֺ, וֺ
     "HEBREW POINT QUBUTS"              : ( chr(0x05BB),),      # אֻ
     "HEBREW POINT QAMATS QATAN"        : ( chr(0x05C7),),      # אׇ
     })

SYMB_POINTS = Name2Symbols(
    {"HEBREW POINT DAGESH OR MAPIQ"     : ( chr(0x05BC),),      # אּ
     "HEBREW POINT METEG"               : ( chr(0x05BD),),      # אֽ
     "HEBREW POINT RAFE"                : ( chr(0x05BF),),      # אֿ
     "HEBREW POINT SHIN DOT"            : ( chr(0x05C1),),      # אׁ, שׁ
     "HEBREW POINT SIN DOT"             : ( chr(0x05C2),),      # אׂ, שׂ
     })

SYMB_SPECIALPOINTS = Name2Symbols(
    {
     "HEBREW MARK UPPER DOT"            : ( chr(0x05C4),),      # אׄ
     "HEBREW MARK LOWER DOT"            : ( chr(0x05C5),),      # אׅ
    })

# unicode names : do not change them since they are used for the transliteration !
SYMB_CANTILLATION_MARKS = Name2Symbols(
    {"HEBREW ACCENT ETNAHTA"            : ( chr(0x0591),),
     "HEBREW ACCENT SEGOL"              : ( chr(0x0592),),
     "HEBREW ACCENT SHALSHELET"         : ( chr(0x0593),),
     "HEBREW ACCENT ZAQEF QATAN"        : ( chr(0x0594),),
     "HEBREW ACCENT ZAQEF GADOL"        : ( chr(0x0595),),
     "HEBREW ACCENT TIPEHA"             : ( chr(0x0596),),
     "HEBREW ACCENT REVIA"              : ( chr(0x0597),),
     "HEBREW ACCENT ZARQA"              : ( chr(0x0598),),
     "HEBREW ACCENT PASHTA"             : ( chr(0x0599),),
     "HEBREW ACCENT YETIV"              : ( chr(0x059A),),
     "HEBREW ACCENT TEVIR"              : ( chr(0x059B),),
     "HEBREW ACCENT GERESH"             : ( chr(0x059C),),
     "HEBREW ACCENT GERESH MUQDAM"      : ( chr(0x059D),),
     "HEBREW ACCENT GERSHAYIM"          : ( chr(0x059E),),
     "HEBREW ACCENT QARNEY PARA"        : ( chr(0x059F),),
     "HEBREW ACCENT TELISHA GEDOLA"     : ( chr(0x05A0),),
     "HEBREW ACCENT PAZER"              : ( chr(0x05A1),),
     "HEBREW ACCENT ATNAH HAFUKH"       : ( chr(0x05A2),),
     "HEBREW ACCENT MUNAH"              : ( chr(0x05A3),),
     "HEBREW ACCENT MAHAPAKH"           : ( chr(0x05A4),),
     "HEBREW ACCENT MERKHA"             : ( chr(0x05A5),),
     "HEBREW ACCENT MERKHA KEFULA"      : ( chr(0x05A6),),
     "HEBREW ACCENT DARGA"              : ( chr(0x05A7),),
     "HEBREW ACCENT QADMA"              : ( chr(0x05A8),),
     "HEBREW ACCENT TELISHA QETANA"     : ( chr(0x05A9),),
     "HEBREW ACCENT YERAH BEN YOMO"     : ( chr(0x05AA),),
     "HEBREW ACCENT OLE"                : ( chr(0x05AB),),
     "HEBREW ACCENT ILUY"               : ( chr(0x05AC),),
     "HEBREW ACCENT DEHI"               : ( chr(0x05AD),),
     "HEBREW ACCENT ZINOR"              : ( chr(0x05AE),),
     "HEBREW MARK MASORA CIRCLE"        : ( chr(0x05AF),),
    })
# we define these constants in order to avoir multiple calls to SYMB_DIACRITICS.get_default_symbol :
DEFAULTSYMB__DAGHESHMAPIQ = SYMB_POINTS.get_default_symbol("HEBREW POINT DAGESH OR MAPIQ")
DEFAULTSYMB__METEG = SYMB_POINTS.get_default_symbol("HEBREW POINT METEG")
DEFAULTSYMB__RAFE = SYMB_POINTS.get_default_symbol("HEBREW POINT RAFE")

#...............................................................................
# we calculate these tuple which is often used in order to speed up the code :
#...............................................................................
SYMB_DIACRITICS = ( tuple(SYMB_VOWELS.keys()) + \
                    tuple(SYMB_POINTS.keys()) + \
                    tuple(SYMB_CANTILLATION_MARKS.keys()) )

SYMB_DIACRITICS__SHIN_SIN_DOT = (SYMB_POINTS["HEBREW POINT SHIN DOT"] + \
                                 SYMB_POINTS["HEBREW POINT SIN DOT"])
SYMB_DIACRITICS__DAGHESH_MAPIQ = (SYMB_POINTS["HEBREW POINT DAGESH OR MAPIQ"],)
SYMB_DIACRITICS__METHEGH = (SYMB_POINTS.get_default_symbol("HEBREW POINT METEG"),)

SYMB_DIACRITICS__SPECIALPOINTS = SYMB_SPECIALPOINTS.default_symbols()

SYMB_DIACRITICS__VOWELS = SYMB_VOWELS.default_symbols()

SYMB_DIACRITICS__RAPHE = (SYMB_POINTS.get_default_symbol("HEBREW POINT RAFE"),)

SYMB_DIACRITICS__CANTILLATION_MARKS = SYMB_CANTILLATION_MARKS.default_symbols()
