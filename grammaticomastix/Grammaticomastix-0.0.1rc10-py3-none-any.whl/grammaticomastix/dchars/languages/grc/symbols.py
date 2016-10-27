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
    ❏DChars❏ : dchars/languages/grc/symbols.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.utilities.name2symbols import Name2Symbols

#...............................................................................
# symbols used by the Ancient Greek :
#
# CAVEAT ! If you modify these dictionaries, don't forget to modify their
# corresponding transliteration's dictionaries !
#
#...............................................................................
SYMB_LOWER_CASE = Name2Symbols(
    { 'α'       : ('α',),
      'β'       : ('β',),
      # 'ϐ' is not a base_char but its presence is required here.
      'ϐ'       : ('ϐ',),
      'γ'       : ('γ',),
      'δ'       : ('δ',),
      'ε'       : ('ε',),
      'ζ'       : ('ζ',),
      'η'       : ('η',),
      'θ'       : ('θ','ϑ'),
      'ι'       : ('ι',),
      'κ'       : ('κ','ϰ'), #0x03B0, 0x03F0
      'λ'       : ('λ',),
      'μ'       : ('μ',),
      'ν'       : ('ν',),
      'ξ'       : ('ξ',),
      'ο'       : ('ο',),
      'π'       : ('π','ϖ'), # 0x03C0, 0x03D6
      'ρ'       : ('ρ','ϱ'), # 0x03C1, 0x03F1
      'σ'       : ('σ','ϲ',), # 0x03C3, 0x03F2,
      # 'ς' is not a base_char but its presence is required here.
      'ς'       : ('ς',),
      'τ'       : ('τ',),
      'υ'       : ('υ',),
      'φ'       : ('φ',),
      'χ'       : ('χ',),
      'ψ'       : ('ψ',),
      'ω'       : ('ω',),
      'ϝ'       : ('ϝ',),
      'ϗ'       : ('ϗ'), # 0x03CF = GREEK KAI SYMBOL
      'ϡ'       : ('ϡ'), # 0x03E0 = GREEK SMALL LETTER SAMPI
      'ϛ'       : ('ϛ'), # 0x03DB = GREEK SMALL LETTER STIGMA
      'ϙ'       : ('ϙ', 'ϟ'), # 0x03D9, 0x03DF (KOPPA)
      })

SYMB_UPPER_CASE = Name2Symbols(
    { 'α'       : ('Α',),
      'β'       : ('Β',),
      'γ'       : ('Γ',),
      'δ'       : ('Δ',),
      'ε'       : ('Ε',),
      'ζ'       : ('Ζ',),
      'η'       : ('Η',),
      'θ'       : ('Θ',),
      'ι'       : ('Ι',),
      'κ'       : ('Κ',),
      'λ'       : ('Λ',),
      'μ'       : ('Μ',),
      'ν'       : ('Ν',),
      'ξ'       : ('Ξ',),
      'ο'       : ('Ο',),
      'π'       : ('Π',),
      'ρ'       : ('Ρ',),
      'σ'       : ('Σ',),
      'τ'       : ('Τ',),
      'υ'       : ('Υ','ϒ'), # 0x03A5, 0x03D2
      'φ'       : ('Φ',),
      'χ'       : ('Χ',),
      'ψ'       : ('Ψ',),
      'ω'       : ('Ω',),
      'ϝ'       : ('Ϝ','F'),    #0x3DC, 0x46
      'ϗ'       : ('Ϗ'), # 0x03CF = GREEK CAPITAL KAI SYMBOL
      'ϡ'       : ('Ϡ'), # 0x03E0 = GREEK LETTER SAMPI
      'ϛ'       : ('Ϛ'), # 0x03DA = GREEK LETTER STIGMA
      'ϙ'       : ('Ϙ'), # 0x03D8 (KOPPA)
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
    {'-'        : ('-',),
     ')'        : (')',),
     '('        : ('(',),
     '['        : ('[',),
     ']'        : (']',),
     '{'        : ('{',),
     '}'        : ('}',),
     ' '        : (' ',),
     '.'        : ('.',),
     ','        : (',',),
     ';'        : (';',),
     '!'        : ('!',),
     '·'        : ('·',),
     '"'        : ('"','‘',"’",),
     "'"        : ("'","᾽"),
     "—"        : ("_",),
     ":"        : (":"),
     '\n'       : ('\n',),
     '\r'       : ('\r',),
     '\t'       : ('\t',),
    })

SYMB_DIACRITICS = Name2Symbols(
    {"τόνος.βαρεῖα"          : ( chr(0x300),),        # ὰ
     "τόνος.ὀξεῖα"           : ( chr(0x301), chr(0x030D)),  # ά, α̍
     "μῆκος.μακρόν"          : ( chr(0x304),),        # ᾱ
     "μῆκος.βραχύ"           : ( chr(0x306),),        # ᾰ
     "τόνος.περισπωμένη"     : ( chr(0x342),),        # ᾶ
     "πνεῦμα.ψιλὸν"          : ( chr(0x313),),        # ἀ
     "πνεῦμα.δασὺ"           : ( chr(0x314),),        # ἁ
     "ὑπογεγραμμένη"         : ( chr(0x345),),        # ᾳ
     "διαλυτικά"             : ( chr(0x308),),        # ϋ
     })
# we define these constants in order to avoir multiple calls to SYMB_DIACRITICS.get_default_symbol :
DEFAULTSYMB__PNEUMAPSILON = SYMB_DIACRITICS.get_default_symbol('πνεῦμα.ψιλὸν')
DEFAULTSYMB__PNEUMADASU = SYMB_DIACRITICS.get_default_symbol('πνεῦμα.δασὺ')
DEFAULTSYMB__TONOSOXEIA = SYMB_DIACRITICS.get_default_symbol('τόνος.ὀξεῖα')
DEFAULTSYMB__TONOSBAREIA = SYMB_DIACRITICS.get_default_symbol('τόνος.βαρεῖα')
DEFAULTSYMB__TONOSPERISPOMENE = SYMB_DIACRITICS.get_default_symbol('τόνος.περισπωμένη')
DEFAULTSYMB__MEKOSBRAXU = SYMB_DIACRITICS.get_default_symbol('μῆκος.βραχύ')
DEFAULTSYMB__MEKOSMAKRON = SYMB_DIACRITICS.get_default_symbol('μῆκος.μακρόν')
DEFAULTSYMB__HUPOGEGRAMMENE = SYMB_DIACRITICS.get_default_symbol('ὑπογεγραμμένη')
DEFAULTSYMB__DIALYTIKA = SYMB_DIACRITICS.get_default_symbol('διαλυτικά')

#...............................................................................
# we calculate these tuples which are often used in order to speed up the code :
#...............................................................................
SYMB_DIACRITICS__TONOS = (SYMB_DIACRITICS['τόνος.βαρεῖα'] + \
                          SYMB_DIACRITICS['τόνος.ὀξεῖα'] + \
                          SYMB_DIACRITICS['τόνος.περισπωμένη'])

SYMB_DIACRITICS__MEKOS = (SYMB_DIACRITICS['μῆκος.μακρόν'] + \
                          SYMB_DIACRITICS['μῆκος.βραχύ'])

SYMB_DIACRITICS__PNEUMA = (SYMB_DIACRITICS['πνεῦμα.ψιλὸν'] + \
                           SYMB_DIACRITICS['πνεῦμα.δασὺ'])

