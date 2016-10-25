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
#    (at your option) any anger version.
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
    ❏DChars❏ : dchars/languages/fro/symbols.py
"""
# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.utilities.name2symbols import Name2Symbols

#...............................................................................
# symbols used by Latin
#
# CAVEAT ! If you modify these dictionaries, don't forget to modify the
# corresponding transliteration's dictionaries !
#
#...............................................................................
SYMB_UPPER_CASE = Name2Symbols(
      {
      'a'          : ('A',),
      'b'          : ('B',),
      'c'          : ('C',),
      'ç'          : ('Ç',),
      'd'          : ('D',),
      'e'          : ('E',),
      'f'          : ('F',),
      'g'          : ('G',),
      'h'          : ('H',),
      'i'          : ('I',),
      'j'          : ('J',),
      'k'          : ('K',),
      'l'          : ('L',),
      'm'          : ('M',),
      'n'          : ('N',),
      'o'          : ('O',),
      'p'          : ('P',),
      'q'          : ('Q',),
      'r'          : ('R',),
      's'          : ('S',),
      't'          : ('T',),
      'þ'          : ('Þ',),
      'u'          : ('U',),
      'v'          : ('V',),
      'w'          : ('W',),
      'x'          : ('X',),
      'y'          : ('Y',),
      'z'          : ('Z',),
      })

SYMB_LOWER_CASE = Name2Symbols(
      {
      'a'          : ('a',),
      'b'          : ('b',),
      'c'          : ('c',),
      'ç'          : ('ç',),
      'd'          : ('d',),
      'e'          : ('e',),
      'f'          : ('f',),
      'g'          : ('g',),
      'h'          : ('h',),
      'i'          : ('i',),
      'j'          : ('j',),
      'k'          : ('k',),
      'l'          : ('l',),
      'm'          : ('m',),
      'n'          : ('n',),
      'o'          : ('o',),
      'p'          : ('p',),
      'q'          : ('q',),
      'r'          : ('r',),
      's'          : ('s',),
      't'          : ('t',),
      'þ'          : ('þ',),
      'u'          : ('u',),
      'v'          : ('v',),
      'w'          : ('w',),
      'x'          : ('x',),
      'y'          : ('y',),
      'z'          : ('z',),
      })

SYMB_PUNCTUATION = Name2Symbols(
    {'-'        : ("-", "—"),
     ')'        : (')',),
     '('        : ('(',),
     '['        : ('[',),
     ']'        : (']',),
     '{'        : ('{',),
     '}'        : ('}',),
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
     ' '        : (' ',),
     '.'        : ('.',),
     ','        : (',',),
     ';'        : (';',),
     '!'        : ('!',),
     '?'        : ('?',),
     '"'        : ('"','‘',"’",),
     "'"        : ("'","᾽"),
     ":"        : (":"),
     '\n'       : ('\n',),
     '\r'       : ('\r',),
     '\t'       : ('\t',),
    })

SYMB_DIACRITICS = Name2Symbols(
    {
     "stress1"    : ( chr(0x300), ),  # è
     "stress2"    : ( chr(0x301), ),  # é
     "stress12"   : ( chr(0x302), ),  # ê
     "stress3"    : ( chr(0x308), ),  # ï
     "cedilla"    : ( chr(0x327), ),  # ç
    })
# we define these constants in order to avoir multiple calls to SYMB_DIACRITICS.get_default_symbol :
DEFAULTSYMB__STRESS1 = SYMB_DIACRITICS.get_default_symbol("stress1")
DEFAULTSYMB__STRESS2 = SYMB_DIACRITICS.get_default_symbol("stress2")
DEFAULTSYMB__STRESS12 = SYMB_DIACRITICS.get_default_symbol("stress12")
DEFAULTSYMB__STRESS3  = SYMB_DIACRITICS.get_default_symbol("stress3")
DEFAULTSYMB__CEDILLA = SYMB_DIACRITICS.get_default_symbol("cedilla")

SORTING_ORDER = {
      'A'       : 10,
      'a'       : 10,

      'B'       : 30,
      'b'       : 30,

      'C'       : 40,
      'c'       : 40,
      'Ç'       : 40,
      'ç'       : 40,

      'D'       : 50,
      'd'       : 50,

      'E'       : 60,
      'e'       : 60,

      'F'       : 70,
      'f'       : 70,

      'G'       : 80,
      'g'       : 80,

      'H'       : 90,
      'h'       : 90,

      'I'       : 100,
      'i'       : 100,

      'J'       : 110,
      'j'       : 110,

      'K'       : 120,
      'k'       : 120,

      'L'       : 130,
      'l'       : 130,

      'M'       : 140,
      'm'       : 140,

      'N'       : 150,
      'n'       : 150,

      'O'       : 160,
      'o'       : 160,

      'P'       : 170,
      'p'       : 170,

      'Q'       : 180,
      'q'       : 180,

      'R'       : 190,
      'r'       : 190,

      'S'       : 200,
      's'       : 200,

      'T'       : 210,
      't'       : 210,

      'U'       : 230,
      'u'       : 230,

      'V'       : 240,
      'v'       : 240,

      'W'       : 250,
      'w'       : 250,

      'X'       : 260,
      'x'       : 260,

      'Y'       : 270,
      'y'       : 270,

      'Z'       : 280,
      'z'       : 280,
    }

#...............................................................................
# we calculate these tuple which is often used in order to speed up the code :
#...............................................................................
SYMB_DIACRITICS__STRESS1 = SYMB_DIACRITICS["stress1"]
SYMB_DIACRITICS__STRESS2 = SYMB_DIACRITICS["stress2"]
SYMB_DIACRITICS__STRESS12 = SYMB_DIACRITICS["stress12"]
SYMB_DIACRITICS__STRESS3 = SYMB_DIACRITICS["stress3"]
SYMB_DIACRITICS__CEDILLA = SYMB_DIACRITICS["cedilla"]
