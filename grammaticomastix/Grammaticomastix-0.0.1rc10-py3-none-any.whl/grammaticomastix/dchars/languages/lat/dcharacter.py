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
    ❏DChars❏ : dchars/languages/lat/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.languages.lat.symbols import SYMB_DIACRITICS
from dchars.languages.lat.symbols import DEFAULTSYMB__STRESS, \
                                         DEFAULTSYMB__DIAERESIS, \
                                         SYMB_LOWER_CASE, \
                                         SYMB_UPPER_CASE
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

import itertools
import copy
import unicodedata

# known transliterations :
import dchars.languages.lat.transliterations.basic.basic as basictrans

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
################################################################################
COMPLETE_NORMALIZE_NFC = (
                # á̄ -> ā́
                ( chr(0x00E1) + chr(0x0304), chr(0x0101) + chr(0x0301) ),
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

                #  Ḯ -> Ḯ
                ( chr(0x00CF) + chr(0x0301), chr(0x1E2E) ),
                # ḯ -> ḯ
                ( chr(0x00EF) + chr(0x0301), chr(0x1E2F) ),
               )

################################################################################
class DCharacterLAT(DCharacterMotherClass):
    """
        class DCharacterLAT
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
                DCharacterLAT.__eq__

                aliud   :       DCharacterLAT object
        """
        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.capital_letter == aliud.capital_letter) and \
               (self.length == aliud.length) and \
               (self.stress == aliud.stress) and \
               (self.diaeresis == aliud.diaeresis)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 punctuation = False,
                 capital_letter = False,
                 length = None,
                 stress = False,
                 diaeresis = False):
        """
                DCharacterLAT.__init__

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                length                          : None or a string ("short", "long")
                stress                          : bool
                diaeresis                       : bool
        """
        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.capital_letter = capital_letter
        self.length = length
        self.stress = stress
        self.diaeresis = diaeresis

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterLAT.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "capital_letter="+repr(self.capital_letter) + "; " + \
               "length="+repr(self.length) + "; " + \
               "stress="+repr(self.stress) + "; " + \
               "diaeresis="+repr(self.diaeresis)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterLAT.clone

                unknown_char                    : bool
                base_char                       : None or a string
                punctuation                     : True, False
                capital_letter                  : True, False

                length                          : None or a string ("short", "long")
                stress                          : bool
                diaeresis                       : bool
        """
        return DCharacterLAT( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              punctuation = self.punctuation,
                              capital_letter = self.capital_letter,
                              length = self.length,
                              stress = self.stress,
                              diaeresis = self.diaeresis )

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterLAT.get_usefull_combinations

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
                             'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                             'y', 'z', )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters:
            for capital_letter in (False, True):
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               punctuation = False,
                               capital_letter = capital_letter,
                               stress = False,
                               length = None,
                               diaeresis = False)

                yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_char :
                                           base_characters,

                                           # capital_letter
                                           (False, True),

                                           # length
                                           ( None, "short", "long",),

                                           # stress
                                           (False, True),

                                           # diaeresis
                                           (False, True),
                                           ))

        for base_char, capital_letter, length, stress, diaeresis in combinations:

            add_this_dchar = True

            if base_char not in ('a', 'e', 'i', 'o', 'u'):
                if length is not None or \
                   stress == True or \
                   diaeresis == True:

                    add_this_dchar = False

            if add_this_dchar:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               punctuation = False,
                               capital_letter = capital_letter,
                               length = length,
                               stress = stress,
                               diaeresis = diaeresis)

                yield copy.copy(self)


    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self,
                            dstring_object,
                            transliteration_method):
        """
                DCharacterLAT.get_transliteration

                transliteration_method  :       str
        """
        return DCharacterLAT.trans__get_transliteration[transliteration_method](
            dstring_object = dstring_object,
            dchar=self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterLAT.init_from_transliteration

                src                     : string
                transliteration_method  :       str

                Return <self>.
        """
        self.reset()
        return DCharacterLAT.trans__init_from_transliteration[transliteration_method](src = src,
                                                                                      dchar = self)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterLAT.get_sourcestr_representation

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

        if self.stress:
            res.append( DEFAULTSYMB__STRESS )

        if self.length == 'short' or self.length == 'long':
            res.append( SYMB_DIACRITICS.get_default_symbol(self.length) )

        if self.diaeresis:
            res.append( DEFAULTSYMB__DIAERESIS )

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
                DCharacterLAT.sortingvalue

                Return an SortingValue object

                NB : this function has almost no interest; you must use DStringLAT.sortingvalue()
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
            res.append( ord(self.base_char) )

            # length :
            if self.length is None:
                res.append( 0 )
            elif self.length == "short":
                res.append( 0 )
            elif self.length == "long":
                res.append( 1 )
            else:
                raise DCharsError( context = "DCharacterLAT.sortingvalue",
                                   message = "unknown value for length ="+\
                                             str(self.length) )

            # # stress :
            # if not res.stress:
            #     self.append( 0 )
            # else:
            #     self.append( 1 )

            # # diaeresis :
            # if not res.diaeresis:
            #     self.append( 0 )
            # else:
            #     self.append( 1 )

        else:
            raise DCharsError( context = "DCharacterLAT.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterLAT.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.capital_letter = False
        self.length = None
        self.stress = None
        self.diaeresis = False

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterLAT.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.capital_letter = True
        self.length = None
        self.stress = None
        self.diaeresis = False
