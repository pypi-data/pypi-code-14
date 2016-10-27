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
    ❏DChars❏ : dchars/languages/jpn/dstring.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"

import re
import unicodedata

from dchars.errors.errors import DCharsError
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.dstring import DStringMotherClass
from dchars.languages.jpn.dcharacter import DCharacterJPN
from dchars.languages.jpn.symbols import SYMB_CHOONPU, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_DIACRITICS, \
                                         SYMB_HIRAGANA, \
                                         SYMB_SMALL_HIRAGANA, \
                                         SYMB_KATAKANA, \
                                         SYMB_SMALL_KATAKANA, \
                                         SYMB_KANJI, \
                                         KATAKANA_TO_HIRAGANA, \
                                         SMALL_HIRAGANA_TO_HIRAGANA, \
                                         SMALL_KATAKANA_TO_KATAKANA, \
                                         HIRAGANA_ORDER, \
                                         VOWEL_IN_HIRAGANA
from dchars.languages.jpn.symbols import SYMB_DIACRITICS__DAKUTEN, \
                                         SYMB_DIACRITICS__HANDAKUTEN

from dchars.utilities.lstringtools import number_of_occurences
from dchars.utilities.sortingvalue import SortingValue

# known transliterations :
import dchars.languages.jpn.transliterations.shepburn.shepburn as shepburntrans
import dchars.languages.jpn.transliterations.shepburn.ucombinations as shepburntrans_ucombinations

################################################################################
class DStringJPN(DStringMotherClass):
    """
        class DStringJPN

        DO NOT CREATE A DStringJPN object directly but use instead the
        dchars.py::new_dstring function.
    """

    # regex pattern used to slice a source string :
    #
    # NB : we use the default_symbols__pattern() function, NOT the normal
    #      default_symbols() function since some characters have to be
    #      treated apart to work with a regex.
    pattern_letters = "|".join( isort_a_lstrings_bylen_nodup(
                                SYMB_CHOONPU.default_symbols__pattern() + \
                                SYMB_HIRAGANA.default_symbols__pattern() + \
                                SYMB_SMALL_HIRAGANA.default_symbols__pattern() + \
                                SYMB_KATAKANA.default_symbols__pattern() + \
                                SYMB_SMALL_KATAKANA.default_symbols__pattern() +\
                                SYMB_KANJI.default_symbols__pattern() +\
                                SYMB_PUNCTUATION.default_symbols__pattern() ))
    pattern_diacritics = "|".join( isort_a_lstrings_bylen_nodup(
                                   SYMB_DIACRITICS.default_symbols__pattern() ))
    pattern = re.compile("((?P<letter>{0})(?P<diacritics>({1})+)?)".format( pattern_letters,
                                                                            pattern_diacritics ))

    # transliterations' methods : available direction(s) :
    trans__directions = {
          "shepburn"       : shepburntrans.AVAILABLE_DIRECTIONS,
        }

    # transliteration's functions :
    trans__init_from_transliteration = {
          "shepburn" : shepburntrans.dstring__init_from_translit_str,
          }

    trans__get_transliteration = {
          "shepburn"       : shepburntrans.dstring__trans__get_trans,
          }

    trans__get_transl_ucombinations = {
          "shepburn" : shepburntrans_ucombinations.get_usefull_combinations,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, str_src = None):
        """
                DStringJPN.__init__

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
    def get_sourcestr_representation(self):
        """
                DStringJPN.get_sourcestr_representation

                RETURN VALUE : a (str) string.
        """
        res = []

        for dchar in self:
            res.append( dchar.get_sourcestr_representation() )

        return "".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringJPN.get_usefull_combinations

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

        dchar = DCharacterJPN(self)
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
                DStringJPN.get_usefull_transl_combinations

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
        # -> "Instance of 'DStringJPN' has no 'transliteration_method' member"
        res = DStringJPN.trans__get_transl_ucombinations[self.transliteration_method]()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self):
        """
                DStringJPN.get_transliteration
        """

        # Pylint can't know that <self> has a 'trans__get_transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'trans__get_transliteration_method' member"
        res = DStringJPN.trans__get_transliteration[self.transliteration_method](self)
        return res

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, str_src):
        """
                DStringJPN.init_from_str

                Function called by __init__(), initialize <self> and return
                <indexes_of_unrecognized_chars>.

                str_src : str

                HOW IT WORKS :
                * (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
                * (2) = normalized_src -> (default symbols required) :
                *     replace_by_the_default_symbols() -> normalized_src
                * (3) initialisation from the recognized characters.
                *     re.finditer(DStringJPN.pattern) give the symbols{letter+diacritics}
                *     (3.1) base_char, chartype, smallsize
                *     (3.2) diacritic
                *     (3.3) we add the new character
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
        normalized_src = SYMB_CHOONPU.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_DIACRITICS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_HIRAGANA.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_SMALL_HIRAGANA.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_KATAKANA.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_SMALL_KATAKANA.replace_by_the_default_symbols(normalized_src)

        #.......................................................................
        # (3) initialisation from the recognized characters.
        #     re.finditer(DStringJPN.pattern) give the symbols{letter+diacritics}
        #.......................................................................
        indexes = []    # indexes of the substring well analyzed : ( start, end )
        for element in re.finditer(DStringJPN.pattern,
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
                    new_character = DCharacterJPN(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )

            else:
                # <indexes> is empty :
                # ... we add the unknown character(s) before the first index in <indexes> :
                for index in range( 0, element.start() ):
                    new_character = DCharacterJPN(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )

            indexes.append( (element.start(), element.end()-1 ) )

            data = element.groupdict()
            letter     = data['letter']
            diacritics = data['diacritics']

            punctuation = letter in SYMB_PUNCTUATION.symbol2name

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.1) base_char, chartype, smallsize
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

            if punctuation:
                # punctuation symbol :
                base_char = SYMB_PUNCTUATION.get_the_name_for_this_symbol(letter)
                smallsize = False
                chartype = "other"

            elif letter in SYMB_CHOONPU.symbol2name:
                # "ー" (the chōonpu 長音符 symbol)
                # confer http://en.wikipedia.org/wiki/Ch%C5%8Donpu
                base_char = SYMB_CHOONPU.get_the_name_for_this_symbol(letter)
                smallsize = False
                chartype = "choonpu"

            elif letter in SYMB_HIRAGANA.symbol2name:
                # hiragana :
                base_char = SYMB_HIRAGANA.get_the_name_for_this_symbol(letter)
                smallsize = False
                chartype = "hiragana"

            elif letter in SYMB_SMALL_HIRAGANA.symbol2name:
                # small hiragana :
                base_char = SYMB_HIRAGANA.get_the_name_for_this_symbol(\
                                                SMALL_HIRAGANA_TO_HIRAGANA[letter])
                smallsize = True
                chartype = "hiragana"

            elif letter in SYMB_KATAKANA.symbol2name:
                # katakana :
                base_char = SYMB_HIRAGANA.get_the_name_for_this_symbol(\
                        KATAKANA_TO_HIRAGANA[ SYMB_KATAKANA.get_the_name_for_this_symbol(letter) ])
                smallsize = False
                chartype = "katakana"

            elif letter in SYMB_SMALL_KATAKANA.symbol2name:
                # small katakana :
                base_char = SYMB_HIRAGANA.get_the_name_for_this_symbol(\
                                        KATAKANA_TO_HIRAGANA[SMALL_KATAKANA_TO_KATAKANA[letter]])
                smallsize = True
                chartype = "katakana"

            elif letter in SYMB_KANJI.symbol2name:
                # kanji :
                base_char = SYMB_KANJI.get_the_name_for_this_symbol(letter)
                smallsize = False
                chartype = "kanji"

            else:
                # other :
                base_char = letter
                smallsize = False
                chartype = "other"

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.2) diacritics
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            diacritic = None

            if diacritics is not None:

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.2.1) dakuten
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                dakuten_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__DAKUTEN )

                if dakuten_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), dakuten defined several times."
                    raise DCharsError( context = "DStringJPN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()))

                if SYMB_DIACRITICS.are_these_symbols_in_a_string('dakuten', diacritics):
                    diacritic = "dakuten"

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.2.2) handakuten
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                handakuten_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__HANDAKUTEN )

                if handakuten_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), handakuten defined several times."
                    raise DCharsError( context = "DStringJPN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()))

                if SYMB_DIACRITICS.are_these_symbols_in_a_string('handakuten', diacritics):
                    diacritic = "handakuten"


                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # dakuten + handakuten ? error
                if dakuten_nbr >= 1 and handakuten_nbr >= 1:
                    err_msg = "In '{0}' (start={1}, end={2}), dakuten and handakuten " \
                              "defined simultaneously"
                    raise DCharsError( context = "DStringJPN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()))


            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.3) we add the new character
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            new_character = DCharacterJPN(dstring_object = self,
                                          unknown_char = False,
                                          base_char = base_char,
                                          diacritic = diacritic,
                                          punctuation = punctuation,
                                          chartype=chartype,
                                          smallsize = smallsize)

            self.append( new_character )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # we add the final unknown characters (see at the beginning of this
        # function)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if indexes:
            # <element> is the last one and <indexes> isn't empty :
            for index in range( max(indexes[-1])+1, len(normalized_src) ):
                new_character = DCharacterJPN(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

        else:
            # <indexes> is empty :
            for index in range( 0, len(normalized_src) ):
                new_character = DCharacterJPN(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src):
        """
                DStringJPN.init_from_transliteration

                src     :       string

                Return <self>
        """

        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringJPN' has no 'transliteration_method' member"
        DStringJPN.trans__init_from_transliteration[self.transliteration_method](
                dstring = self,
                dcharactertype = DCharacterJPN,
                src = src)

        return self

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringJPN.sortingvalue

                sorting methods :
                o "default" : cf Kanji & Kana, Hadamitzky and Spahn, p. 22

                Return a SortingValue object
        """
        res = SortingValue()

        # Pylint can't know that <self> has an 'options' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringJPN' has no 'options' member"
        if self.options["sorting method"] == "default":

            # base character :
            data = []
            previous_char = None
            for index, char in enumerate(self):

                if char.unknown_char:
                    data.append( (1, ord(char.base_char)) )

                elif char.chartype == 'choonpu':
                    # we treat the choonpu symbol as if it was the last vowel
                    # cf Kanji & Kana, Hadamitzky and Spahn, p. 22

                    if index == 0:
                        # problem : no preceding vowel
                        data.append( (0, 0 ))
                    else:
                        vowel = VOWEL_IN_HIRAGANA[previous_char.base_char]
                        if vowel is not None:
                            # normal case : if char == 'か', vowel = 'あ'
                            data.append( (0, HIRAGANA_ORDER[vowel] ))
                        else:
                            # abnormal case : if char == 'ん', there's no vowel...
                            # so ... we take the order of ん.
                            data.append( (0, HIRAGANA_ORDER['ん'] ))

                elif char.chartype in ('hiragana', 'katakana'):
                    data.append( (0, HIRAGANA_ORDER[char.base_char] ))

                else:
                    # other cases : kanji or unknown symbol.
                    data.append( (0, ord(char.base_char) ))

                previous_char = char

            res.append(data)

            # small size :
            data = []
            for char in self:
                data.append( { False:0,
                               True:1, }[char.smallsize])
            res.append(data)

            # diacritic :
            data = []
            for char in self:
                data.append( { None:0,
                               "dakuten":1,
                               "handakuten":2 }[char.diacritic] )
            res.append(data)

            # hiragana < katakana:
            data = []
            for char in self:
                if char.chartype == 'hiragana':
                    data.append( 0 )
                elif char.chartype == 'choonpu':
                    # we treat the choonpu symbol as a katakana
                    # cf Kanji & Kana, Hadamitzky and Spahn, p. 22
                    data.append( 1 )
                elif char.chartype == 'katakana':
                    data.append( 1 )
                else:
                    data.append( 2 )

            res.append(data)

        else:
            # Pylint can't know that <self> has an 'options' member
            # created when <self> has been initialized by new_dstring() :
            # pylint: disable=E1101
            # -> "Instance of 'DStringJPN' has no 'options' member"
            err_msg = "unknown sorting method '{0}'."
            raise DCharsError( context = "DStringJPN.sortingvalue",
                               message = err_msg.format(self.options["sorting method"]) )

        return res
