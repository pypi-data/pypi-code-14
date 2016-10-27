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
    ❏DChars❏ : dchars/languages/jpn/transliterations/shepburn/ucombinations.py
"""
from dchars.dchars import new_dstring
from dchars.languages.jpn.dcharacter import DCharacterJPN
from dchars.languages.jpn.transliterations.shepburn.shepburn import dchar__get_translit_str
from dchars.languages.jpn.symbols import HIRAGANA_TO_SMALL_HIRAGANA

#///////////////////////////////////////////////////////////////////////////
def get_usefull_combinations():
    """
            get_usefull_combinations()

            Return a (str)string with all the usefull combinations of characters,
            i.e. only the 'interesting' characters (not punctuation if it's too simple
            by example).

            NB : this function has nothing to do with linguistic or a strict
                 approach of the language. This function allows only to get the
                 most common and/or usefull characters of the writing system.

            NB : function required by the dchars-fe project.
    """
    res = []

    dstring = new_dstring( 'jpn' )()

    # base_char : we don't use the list stored in symbols.py
    # since we would lost the character's order.
    base_characters  = ( 'あ', 'い', 'う', 'え', 'お',
                         'か', 'き', 'く', 'け', 'こ',
                         'さ', 'し', 'す', 'せ', 'そ',
                         'た', 'ち', 'つ', 'て', 'と',
                         'な', 'に', 'ぬ', 'ね', 'の',
                         'は', 'ひ', 'ふ', 'へ', 'ほ',
                         'ま', 'み', 'む', 'め', 'も',
                         'や', 'ゆ', 'よ',
                         'ら', 'り', 'る', 'れ', 'ろ',
                         'わ', 'ゐ', 'ゑ', 'ゑ',
                         'を',
                         'ん',
                        )

    for base_char in base_characters:
        for chartype in ('hiragana', 'katakana'):
            for smallsize in (False, True):
                for diacritic in (None, "dakuten", "handakuten"):

                    add_this_char = True

                    if smallsize and base_char not in HIRAGANA_TO_SMALL_HIRAGANA:
                        add_this_char = False

                    if diacritic == 'dakuten' and \
                       base_char not in ('か', 'き', 'く', 'け', 'こ',
                                         'さ', 'し', 'す', 'せ', 'そ',
                                         'た', 'ち', 'つ', 'て', 'と',
                                         'は', 'ひ', 'ふ', 'へ', 'ほ',):
                        add_this_char = False

                    if diacritic == 'handakuten' and \
                       base_char not in ('は', 'ひ', 'ふ', 'へ', 'ほ',):
                        add_this_char = False

                    if add_this_char:

                        dchar = DCharacterJPN( dstring_object = dstring,
                                               unknown_char = False,
                                               base_char = base_char,
                                               punctuation = False,
                                               chartype = chartype,
                                               diacritic = diacritic,
                                               smallsize = smallsize )

                        txt = dchar__get_translit_str(dstring_object = dstring,
                                                      dchar = dchar)

                        res.append( str(dchar) + "{" + txt + "} " )

    return "".join(res)
