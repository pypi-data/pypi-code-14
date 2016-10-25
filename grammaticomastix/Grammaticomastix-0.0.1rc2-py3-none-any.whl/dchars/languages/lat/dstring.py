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
    ❏DChars❏ : dchars/languages/lat/dstring.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"

import re
import unicodedata

from dchars.errors.errors import DCharsError
from dchars.dstring import DStringMotherClass
from dchars.languages.lat.dcharacter import DCharacterLAT
from dchars.languages.lat.symbols import SYMB_PUNCTUATION, \
                                         SYMB_UPPER_CASE, \
                                         SYMB_LOWER_CASE, \
                                         SYMB_DIACRITICS
from dchars.languages.lat.symbols import SYMB_DIACRITICS__LENGTH, \
                                         SYMB_DIACRITICS__STRESS, \
                                         SYMB_DIACRITICS__DIAERESIS

from dchars.utilities.lstringtools import number_of_occurences
from dchars.utilities.sortingvalue import SortingValue

# known transliterations :
import dchars.languages.lat.transliterations.basic.basic as basictrans
import dchars.languages.lat.transliterations.basic.ucombinations as basictrans_ucombinations

################################################################################
class DStringLAT(DStringMotherClass):
    """
        class DStringLAT

        DO NOT CREATE A DStringLAT object directly but use instead the
        dchars.py::new_dstring function.
    """

    # regex pattern used to slice a source string :
    #
    # NB : we use the default_symbols__pattern() function, NOT the normal
    #      default_symbols() function since some characters have to be
    #      treated apart to work with a regex.
    pattern_letters = "|".join( SYMB_LOWER_CASE.default_symbols__pattern() + \
                                SYMB_UPPER_CASE.default_symbols__pattern() + \
                                SYMB_PUNCTUATION.default_symbols__pattern() )
    pattern_diacritics = "|".join( SYMB_DIACRITICS.default_symbols__pattern() )
    pattern = re.compile("((?P<letter>{0})(?P<diacritics>({1})+)?)".format( pattern_letters,
                                                                            pattern_diacritics ))

    # transliterations' methods : available direction(s) :
    trans__directions = {
          "basic"       : basictrans.AVAILABLE_DIRECTIONS,
        }

    # transliteration's functions :
    trans__init_from_transliteration = {
          "basic" : basictrans.dstring__init_from_translit_str,
          }

    trans__get_transliteration = {
          "basic" : basictrans.dchar__init_from_translit_str,
          }

    trans__get_transl_ucombinations = {
          "basic" : basictrans_ucombinations.get_usefull_combinations,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, str_src = None):
        """
                DStringLAT.__init__

		        the three following attributes have been created by the call to
				dchars.py::new_dstring() :

                self.iso639_3_name             : (str)
                self.transliteration_method    : (str)
                self.options                   : (dict)
        """
        DStringMotherClass.__init__(self)

        if str_src is not None:
            self.init_from_str(str_src)

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringLAT.get_usefull_combinations

                Return a DString with all the usefull combinations of characters,
                i.e. only the 'interesting' characters (not punctuation if it's too simple
                by example). The DChars stored in the dstring will be unique, id est, two
                dchars will not have the same appearence (__str__())

                NB : this function has nothing to do with linguistic or a strict
                     approach of the language. This function allows only to get the
                     most common and/or usefull characters of the writing system.

                NB : function required by the dchars-fe project.
        """
        self.clear()

        dchar = DCharacterLAT(self)
        for dchar in dchar.get_usefull_combinations():

            already_present = False
            for dchar2 in self:
                if str(dchar) == str(dchar2):
                    already_present = True

            if not already_present:
                self.append( dchar )

        return self

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_transl_combinations(self):
        """
                DStringLAT.get_usefull_transl_combinations

                Return a (str)string with all the usefull combinations of TRANSLITTERATED
                characters, i.e. only the 'interesting' characters (not punctuation if
                 it's too simple by example).

                NB : this function has nothing to do with linguistic or a strict
                     approach of the language. This function allows only to get the
                     most common and/or usefull characters of the writing system.

                NB : function required by the dchars-fe project.
        """

        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringLAT' has no 'transliteration_method' member"
        res = DStringLAT.trans__get_transl_ucombinations[self.transliteration_method]()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self):
        """
                DStringLAT.get_transliteration

                We try to use the method defined in self.transliteration_method;
                if this attribute doesn't exist, the function use the default method.
        """

        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringLAT' has no 'transliteration_method' member"

        res = []

        for dchar in self:
            res.append( dchar.get_transliteration(
                dstring_object = self,
                transliteration_method = self.transliteration_method) )

        return "".join( res )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, str_src):
        """
                DStringLAT.init_from_str

                Function called by __init__(), initialize <self> and return
                <indexes_of_unrecognized_chars>.

                str_src : str

                HOW IT WORKS :
                * (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
                * (2) = normalized_src -> (default symbols required) :
                *     replace_by_the_default_symbols() -> normalized_src
                * (3) initialisation from the recognized characters.
                *     re.finditer(DStringLAT.pattern) give the symbols{letter+diacritics}
                *     (3.1) base_char
                *     (3.2) length
                *     (3.3) stress
                *     (3.4) diaeresis
                *     (3.5) we add the new character
        """
        #.......................................................................
        # (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
        #.......................................................................
        normalized_src = unicodedata.normalize('NFD', str_src)

        #.......................................................................
        # (2) = normalized_src -> (default symbols required) :
        #     replace_by_the_default_symbols() -> normalized_src
        #.......................................................................
        normalized_src = SYMB_PUNCTUATION.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_LOWER_CASE.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_UPPER_CASE.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_DIACRITICS.replace_by_the_default_symbols(normalized_src)

        #.......................................................................
        # (3) initialisation from the recognized characters.
        #     re.finditer(DStringLAT.pattern) give the symbols{letter+diacritics}
        #.......................................................................
        indexes = []    # indexes of the substring well analyzed : ( start, end )
        for element in re.finditer(DStringLAT.pattern,
                                   normalized_src):

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # we add the unknown characters at the beginning and in the middle
            # of the string (see at the end of this function)
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            if indexes:
                # <indexes> isn't empty :
                # ... we add the unknown character(s) between the last character and
                # the current one :
                for index in range( max(indexes[-1])+1, element.start() ):
                    new_character = DCharacterLAT(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )
            else:
                # <indexes> is empty :
                # ... we add the unknown character(s) before the first index in <indexes> :
                for index in range( 0, element.start() ):
                    new_character = DCharacterLAT(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )

            indexes.append( (element.start(), element.end()-1 ) )

            data = element.groupdict()
            letter     = data['letter']
            diacritics = data['diacritics']

            punctuation = letter in SYMB_PUNCTUATION.symbol2name
            capital_letter = letter in SYMB_UPPER_CASE.symbol2name

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.1) base_char
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            if punctuation:
                # punctuation symbol :
                base_char = SYMB_PUNCTUATION.get_the_name_for_this_symbol(letter)
            elif not capital_letter:
                # lower case :
                base_char = SYMB_LOWER_CASE.get_the_name_for_this_symbol(letter)
            else:
                # upper case :
                base_char = SYMB_UPPER_CASE.get_the_name_for_this_symbol(letter)

            length = None
            stress = False
            diaeresis = False
            if diacritics is not None:
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.2) length
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                length_nbr = number_of_occurences( source_string = diacritics,
                                                   symbols = SYMB_DIACRITICS__LENGTH )

                if length_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), length defined several times."
                    raise DCharsError( context = "DStringLAT.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                length = None

                if SYMB_DIACRITICS.are_these_symbols_in_a_string('short', diacritics):
                    length = "short"
                elif SYMB_DIACRITICS.are_these_symbols_in_a_string('long', diacritics):
                    length = "long"

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.3) stress
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                stress_nbr = number_of_occurences( source_string = diacritics,
                                                   symbols = SYMB_DIACRITICS__STRESS)

                if stress_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), stress defined several times."
                    raise DCharsError( context = "DStringLAT.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                stress = SYMB_DIACRITICS.are_these_symbols_in_a_string("stress", diacritics)

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.4) diaeresis
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                diaeresis_nbr = number_of_occurences( source_string = diacritics,
                                                      symbols = SYMB_DIACRITICS__DIAERESIS)

                if diaeresis_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), diaeresis defined several times."
                    raise DCharsError( context = "DStringLAT.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                diaeresis = SYMB_DIACRITICS.are_these_symbols_in_a_string("diaeresis", diacritics)

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.5) we add the new character
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            new_character = DCharacterLAT(dstring_object = self,
                                          unknown_char = False,
                                          base_char = base_char,
                                          punctuation = punctuation,
                                          capital_letter = capital_letter,
                                          length = length,
                                          stress = stress,
                                          diaeresis = diaeresis)

            self.append( new_character )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # we add the final unknown characters (see at the beginning of this
        # function)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if indexes:
            # <element> is the last one and <indexes> isn't empty :
            for index in range( max(indexes[-1])+1, len(normalized_src) ):
                new_character = DCharacterLAT(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )
        else:
            # <indexes> is empty :
            for index in range( 0, len(normalized_src) ):
                new_character = DCharacterLAT(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src):
        """
                DStringLAT.init_from_transliteration

                src     :       string

                Return <self>
        """
        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringLAT' has no 'transliteration_method' member"

        DStringLAT.trans__init_from_transliteration[self.transliteration_method](
                dstring = self,
                dcharactertype = DCharacterLAT,
                src = src)

        return self

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringLAT.sortingvalue

                Return a SortingValue object
        """
        res = SortingValue()

        # Pylint can't know that <self> has an 'options' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringLAT' has no 'options' member"
        if self.options["sorting method"] == "default":

            # base character :
            data = []
            for char in self:
                data.append( ({False:0,
                               True:1}[char.unknown_char],
                              ord(char.base_char) ))
            res.append(data)

            # length :
            data = []
            for char in self:
                data.append( { None      : 0,
                               "short"   : 1,
                               "long"    : 2, }[char.length])
            res.append(data)

        else:
            # Pylint can't know that <self> has an 'options' member
            # created when <self> has been initialized by new_dstring() :
            # pylint: disable=E1101
            # -> "Instance of 'DStringLAT' has no 'options' member"
            err_msg = "unknown sorting method '{0}'."
            raise DCharsError( context = "DStringLAT.sortingvalue",
                               message = err_msg.format(self.options["sorting method"]) )

        return res
