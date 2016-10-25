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
    ❏DChars❏ : dchars/languages/jpn/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
from dchars.languages.jpn.symbols import DEFAULTSYMB__DAKUTEN, \
                                         DEFAULTSYMB__HANDAKUTEN, \
                                         HIRAGANA_TO_SMALL_HIRAGANA, \
                                         HIRAGANA_TO_KATAKANA, \
                                         HIRAGANA_ORDER, \
                                         KATAKANA_TO_SMALL_KATAKANA

import unicodedata
import copy

# known transliterations :
import dchars.languages.jpn.transliterations.shepburn.shepburn as shepburntrans

################################################################################
class DCharacterJPN(DCharacterMotherClass):
    """
        class DCharacterJPN
    """

    # transliteration's functions :
    trans__get_transliteration = {
          "shepburn" : shepburntrans.dchar__get_translit_str,
          }

    trans__init_from_transliteration = {
          "shepburn" : shepburntrans.dchar__init_from_translit_str,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DCharacterJPN.__eq__

                aliud   :       DCharacterJPN object
        """
        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.chartype == aliud.chartype) and \
               (self.diacritic == aliud.diacritic) and \
               (self.smallsize == aliud.smallsize)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 chartype = None,
                 punctuation = False,
                 diacritic = None,
                 smallsize = False):
        """
                DCharacterJPN.__init__

                .. code-block:: none

                    unknown_char        : bool
                    base_char           : None or a string
                                            o "あ", "い", ... (one hiragana, NOT A KATAKANA)

                                            o "東", "名" (one kanji)

                    chartype            : None (=unknown character) or a string
                                            "hiragana" / "katakana" / "kanji" / "choonpu" / "other"

                                              about "ー" (the chōonpu 長音符 symbol)
                                              confer http://en.wikipedia.org/wiki/Ch%C5%8Donpu

                    punctuation         : bool
                    diacritic           : None / "dakuten" / "handakuten"
                    smallsize           : bool
        """
        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.chartype = chartype
        self.diacritic = diacritic
        self.smallsize = smallsize

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterJPN.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "chartype="+repr(self.chartype) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "diacritic="+repr(self.diacritic) + "; " + \
               "smallsize="+repr(self.smallsize)

    #///////////////////////////////////////////////////////////////////////////
    def clearAccentuation(self):
        """
                DCharacterJPN.clearAccentuation
        """
        self.diacritic = None

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterJPN.clone
        """
        return DCharacterJPN( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              chartype = self.chartype,
                              punctuation = self.punctuation,
                              diacritic = self.diacritic,
                              smallsize = self.smallsize )

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterJPN.get_sourcestr_representation

                RETURN VALUE : a (str) string.
        """

        #.......................................................................
        # unknown char ? Nothing to do :
        #.......................................................................
        if self.unknown_char:
            if self.dstring_object.options["anonymize the unknown characters"] == 'yes':
                return UNKNOWN_CHAR_SYMBOL
            else:
                return self.base_char

        #.......................................................................
        # ok, the function can analyse <self> :
        #.......................................................................
        res = []

        if self.punctuation:
            res.append( self.base_char )

        else:

            if self.chartype == 'hiragana':

                if not self.smallsize:
                    res.append( self.base_char )
                else:
                    res.append( HIRAGANA_TO_SMALL_HIRAGANA[ self.base_char ] )

            elif self.chartype == 'katakana':

                if not self.smallsize:
                    res.append( HIRAGANA_TO_KATAKANA[self.base_char] )
                else:
                    res.append( KATAKANA_TO_SMALL_KATAKANA[ HIRAGANA_TO_KATAKANA[self.base_char] ] )

            elif self.chartype == 'kanji':
                res.append( self.base_char )

            elif self.chartype == 'choonpu':
                res.append( self.base_char )

            elif self.chartype == 'other':
                res.append( self.base_char )

        if self.diacritic == 'dakuten':
            res.append( DEFAULTSYMB__DAKUTEN )

        elif self.diacritic == 'handakuten':
            res.append( DEFAULTSYMB__HANDAKUTEN )

        res = "".join(res)

        res = unicodedata.normalize('NFC', res)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self, transliteration_method, options):
        """
                DCharacterJPN.get_transliteration

                method  : string
        """
        return DCharacterJPN.trans__get_transliteration[transliteration_method](
            dstring_object = self.dstring_object,
            dchar = self,
            options = options)

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DCharacterJPN.get_usefull_combinations

                Yield, one dchar at a time,  all the usefull combinations of characters,
                i.e. only the 'interesting' characters (not punctuation if it's too simple
                by example).

                NB : this function has nothing to do with linguistic or a strict
                     approach of the language. This function allows only to get the
                     most common and/or usefull characters of the writing system.

                NB : function required by the dchars-fe project.
        """

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
            for chartype in ('hiragana', 'katakana', 'choonpu'):
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
                            self.__init__( dstring_object = self.dstring_object,
                                           base_char = base_char,
                                           chartype = chartype,
                                           punctuation = False,
                                           diacritic = diacritic,
                                           smallsize = smallsize )

                            yield copy.copy(self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterJPN.init_from_transliteration

                src     :       string
                transliteration_method  : string

                Return <self>.
        """
        self.reset()
        return DCharacterJPN.trans__init_from_transliteration[transliteration_method](dchar = self,
                                                                                      src = src)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterJPN.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.chartype = None
        self.diacritic = None
        self.smallsize = False

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterJPN.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.diacritic = None
        self.smallsize = False

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DCharacterJPN.sortingvalue

                Return a SortingValue object

                NB : this function has almost no interest; you must use DStringJPN.sortingvalue()
                     to compare two strings. Use this function if you just want to compare
                     two characters.
        """
        res = SortingValue()

        if self.dstring_object.options["sorting method"] == "default":

            if self.unknown_char:
                # unknown char :
                res.append(1)
                res.append( ord(self.base_char) )
                return res

            # known char :
            res.append(0)

            # base_char :
            res.append( HIRAGANA_ORDER[self.base_char] )

            # small size ?
            res.append( {True:0,
                         False:1}[self.smallsize] )

            # hiragana < katakana :
            if self.chartype == 'hiragana':
                res.append(0)
            elif self.chartype == 'katakana':
                res.append(1)
            else:
                res.append(2)

        else:
            raise DCharsError( context = "DCharacterJPN.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res
