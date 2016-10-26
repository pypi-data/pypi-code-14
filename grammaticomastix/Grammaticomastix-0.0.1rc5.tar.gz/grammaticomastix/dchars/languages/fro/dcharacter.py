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
    ❏DChars❏ : dchars/languages/fro/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.languages.fro.symbols import DEFAULTSYMB__STRESS1, \
                                         DEFAULTSYMB__STRESS2, \
                                         DEFAULTSYMB__STRESS12, \
                                         DEFAULTSYMB__STRESS3, \
                                         DEFAULTSYMB__CEDILLA, \
                                         SYMB_LOWER_CASE, \
                                         SYMB_UPPER_CASE, \
                                         SORTING_ORDER
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

import itertools
import copy
import unicodedata

# known transliterations :
import dchars.languages.fro.transliterations.basic.basic as basictrans

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
################################################################################
COMPLETE_NORMALIZE_NFC = (
#                ('ç', 'ç'),   # 0063 0327 -> 00E7
               )

################################################################################
class DCharacterFRO(DCharacterMotherClass):
    """
        class DCharacterFRO
    """

    # transliteration's functions :
    trans__get_transliteration = {
          "basic" : basictrans.dchar__get_translit_str,
          }

    trans__init_from_transliteration = {
          "basic" : basictrans.dchar__init_from_translit_str,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DCharacterFRO.__eq__

                aliud   :       DCharacterFRO object
        """
        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.capital_letter == aliud.capital_letter) and \
               (self.stress == aliud.stress)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 punctuation = False,
                 capital_letter = False,
                 cedilla = False,
                 stress = 0):
        """
                DCharacterFRO.__init__

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                cedilla                         : False
                stress                          : 1,2,3,4
        """
        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.capital_letter = capital_letter
        self.cedilla = cedilla
        self.stress = stress

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterFRO.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "capital_letter="+repr(self.capital_letter) + "; " + \
               "cedilla="+repr(self.cedilla) + "; " + \
               "stress="+repr(self.stress) + "; "

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterFRO.clone

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                cedilla                         : bool
                stress                          : (int)1,2,3,4
        """
        return DCharacterFRO( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              punctuation = self.punctuation,
                              capital_letter = self.capital_letter,
                              cedilla = self.cedilla,
                              stress = self.stress)

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterFRO.get_usefull_combinations

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
        base_characters  = ( 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                             'q', 'r', 's', 't', 'þ', 'ð', 'u', 'v',
                             'w', 'x', 'y', 'z', )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters:
            for capital_letter in (False, True):
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               punctuation = False,
                               capital_letter = capital_letter,
                               cedilla = False,
                               stress = 0)

                yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_char :
                                           base_characters,

                                           # capital_letter
                                           (False, True),

                                           # stress
                                           (-1, 0, 1, 2),

                                           # cedilla
                                           (False, True),

                                           ))

        for base_char, capital_letter, stress, cedilla in combinations:

            add_this_dchar = True

            if base_char not in ('a', 'æ', 'e', 'i', 'o', 'u'):
                if stress != 0:
                    add_this_dchar = False

            if base_char not in ('c'):
                if cedilla is True:
                    add_this_dchar = False

            if add_this_dchar:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               punctuation = False,
                               capital_letter = capital_letter,
                               cedilla = cedilla,
                               stress = stress)

                yield copy.copy(self)


    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self,
                            dstring_object,
                            transliteration_method):
        """
                DCharacterFRO.get_transliteration

                transliteration_method  :       str
        """
        return DCharacterFRO.trans__get_transliteration[transliteration_method](
            dstring_object = dstring_object,
            dchar=self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterFRO.init_from_transliteration

                src                     : string
                transliteration_method  :       str

                Return <self>.
        """
        self.reset()
        return DCharacterFRO.trans__init_from_transliteration[transliteration_method](src = src,
                                                                                      dchar = self)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterFRO.get_sourcestr_representation

                Return a string.
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

        if self.base_char is not None:
            if self.punctuation:
                # punctuation symbol :
                res.append( self.base_char )
            elif not self.capital_letter:
                # lower case :
                res.append( SYMB_LOWER_CASE.get_default_symbol(self.base_char) )
            else:
                # upper case :
                res.append( SYMB_UPPER_CASE.get_default_symbol(self.base_char) )

        if self.stress == 1:
            res.append( DEFAULTSYMB__STRESS1 )
        if self.stress == 2:
            res.append( DEFAULTSYMB__STRESS2 )
        elif self.stress == 3:
            res.append( DEFAULTSYMB__STRESS12 )
        elif self.stress == 4:
            res.append( DEFAULTSYMB__STRESS3 )

        if self.cedilla is True:
            res.append( DEFAULTSYMB__CEDILLA )

        res = "".join(res)

        # (1/2) composition with unicodedata.normalize :
        res = unicodedata.normalize('NFC', res)
        # (2/2) composition with COMPLETE_NORMALIZE_NFC :
        for src, dest in COMPLETE_NORMALIZE_NFC:
            res = res.replace(src, dest)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DCharacterFRO.sortingvalue

                Return an SortingValue object

                NB : this function has almost no interest; you must use DStringFRO.sortingvalue()
                     to compare two strings. Use this function if you just want to compare
                     two characters.
        """

        res = SortingValue()

        if self.dstring_object.options["sorting method"] == "default":

            if self.unknown_char:
                # unknown char :
                res.append(1)
                return res

            # known char :
            res.append(0)

            # # capital_letter :
            # if res.capital_letter:
            #     res.append( 0 )
            # else:
            #     res.append( 1 )

            # base_char :
            if self.base_char not in SORTING_ORDER:
                res.append( -1 )
            else:
                res.append( SORTING_ORDER[self.base_char] )

        else:
            raise DCharsError( context = "DCharacterFRO.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterFRO.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.capital_letter = False
        self.cedilla = False
        self.stress = 0

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterFRO.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.capital_letter = True
        self.cedilla = False
        self.stress = 0
