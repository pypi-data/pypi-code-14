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
    ❏DChars❏ : dchars/languages/ang/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.languages.ang.symbols import DEFAULTSYMB__STRESS_MINUS1, \
                                         DEFAULTSYMB__STRESS1, \
                                         DEFAULTSYMB__STRESS2, \
                                         DEFAULTSYMB__MAKRON, \
                                         DEFAULTSYMB__UPPERDOT, \
                                         SYMB_LOWER_CASE, \
                                         SYMB_UPPER_CASE, \
                                         SORTING_ORDER
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

import itertools
import copy
import unicodedata

# known transliterations :
import dchars.languages.ang.transliterations.basic.basic as basictrans

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
################################################################################
COMPLETE_NORMALIZE_NFC = (

                # á̄ -> ā́
                ( chr(0x00E1) + chr(0x0304), chr(0x0101) + chr(0x0301) ),
                ## æ + makron -> ǣ
                #( chr(0x00E6) + chr(0x0304), chr(0x01E3) ),
                # é̄ -> ḗ
                ( chr(0x00E9) + chr(0x0304), chr(0x1E17) ),
                # í̄ -> ī́
                ( chr(0x00ED) + chr(0x0304), chr(0x012B) + chr(0x0301) ),
                # ó́ -> ṓ
                ( chr(0x00F3) + chr(0x0304), chr(0x1E53) ),
                # ú̄ -> ū́
                ( chr(0x00FA) + chr(0x0304), chr(0x016B) + chr(0x0301) ),
                # ý̄ -> ȳ́
                ( chr(0x00FD) + chr(0x0304), chr(0x0233) + chr(0x0301) ),

               )

################################################################################
class DCharacterANG(DCharacterMotherClass):
    """
        class DCharacterANG
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
                DCharacterANG.__eq__

                aliud   :       DCharacterANG object
        """
        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.capital_letter == aliud.capital_letter) and \
               (self.makron == aliud.makron) and \
               (self.stress == aliud.stress) and \
               (self.upperdot == aliud.upperdot)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 punctuation = False,
                 capital_letter = False,
                 makron = False,
                 stress = 0,
                 upperdot = False):
        """
                DCharacterANG.__init__

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                makron                          : bool
                stress                          : -1 (stress not taken in account) 0 (no stress),
                                                  1 (half-stressed) or 2
                upperdot                        : bool
        """
        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.capital_letter = capital_letter
        self.makron = makron
        self.stress = stress
        self.upperdot = upperdot

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterANG.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "capital_letter="+repr(self.capital_letter) + "; " + \
               "makron="+repr(self.makron) + "; " + \
               "stress="+repr(self.stress) + "; " + \
               "upperdot="+repr(self.upperdot)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterANG.clone

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                makron                          : bool
                stress                          : -1 (stress not taken in account) 0 (no stress),
                                                  1 (half-stressed) or 2
                upperdot                        : bool
        """
        return DCharacterANG( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              punctuation = self.punctuation,
                              capital_letter = self.capital_letter,
                              makron = self.makron,
                              stress = self.stress,
                              upperdot = self.upperdot )

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterANG.get_usefull_combinations

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
        base_characters  = ( 'a', 'æ', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
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
                               stress = 0,
                               makron = False,
                               upperdot = False)

                yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_char :
                                           base_characters,

                                           # capital_letter
                                           (False, True),

                                           # makron
                                           ( False, True,),

                                           # stress
                                           (-1, 0, 1, 2),

                                           # upperdot
                                           (False, True),
                                           ))

        for base_char, capital_letter, makron, stress, upperdot in combinations:

            add_this_dchar = True

            if base_char not in ('a', 'æ', 'e', 'i', 'o', 'u'):
                if makron is True or \
                   stress != 0 or \
                   upperdot == True:

                    add_this_dchar = False

            if add_this_dchar:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               punctuation = False,
                               capital_letter = capital_letter,
                               makron = makron,
                               stress = stress,
                               upperdot = upperdot)

                yield copy.copy(self)


    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self,
                            dstring_object,
                            transliteration_method):
        """
                DCharacterANG.get_transliteration

                transliteration_method  :       str
        """
        return DCharacterANG.trans__get_transliteration[transliteration_method](
            dstring_object = dstring_object,
            dchar=self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterANG.init_from_transliteration

                src                     : string
                transliteration_method  :       str

                Return <self>.
        """
        self.reset()
        return DCharacterANG.trans__init_from_transliteration[transliteration_method](src = src,
                                                                                      dchar = self)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterANG.get_sourcestr_representation

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

        if self.stress == -1:
            res.append( DEFAULTSYMB__STRESS_MINUS1 )
        if self.stress == 1:
            res.append( DEFAULTSYMB__STRESS1 )
        elif self.stress == 2:
            res.append( DEFAULTSYMB__STRESS2 )

        if self.makron:
            res.append( DEFAULTSYMB__MAKRON )

        if self.upperdot:
            res.append( DEFAULTSYMB__UPPERDOT )

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
                DCharacterANG.sortingvalue

                Return an SortingValue object

                NB : this function has almost no interest; you must use DStringANG.sortingvalue()
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

            # makron :
            if not self.makron:
                res.append( 0 )
            else:
                res.append( 1 )

            # # upperdot :
            # if not res.upperdot:
            #     self.append( 0 )
            # else:
            #     self.append( 1 )

        else:
            raise DCharsError( context = "DCharacterANG.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterANG.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.capital_letter = False
        self.makron = False
        self.stress = 0
        self.upperdot = False

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterANG.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.capital_letter = True
        self.makron = False
        self.stress = 0
        self.upperdot = False
