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
    ❏DChars❏ : dchars/languages/san/dstring.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"

from dchars.errors.errors import DCharsError
from dchars.dstring import DStringMotherClass
from dchars.languages.san.symbols import SYMB_CONSONANTS, \
                                         SYMB_OTHER_SYMBOLS, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_INDEPENDENT_VOWELS, \
                                         SYMB_DEPENDENT_VOWELS, \
                                         SYMB_DIACRITICS

from dchars.languages.san.symbols import SYMB_DIACRITICS__ACCENTS, \
                                         SYMB_DIACRITICS__NUKTA, \
                                         SYMB_DIACRITICS__ANUSVARA_CANDRABINDU, \
                                         SYMB_DIACRITICS__VIRAMA, \
                                         SYMB_DIACRITICS__ANUDATTA
import re
import unicodedata
from dchars.utilities.lstringtools import number_of_occurences

from dchars.languages.san.dcharacter import DCharacterSAN

################################################################################
# known transliterations :
################################################################################
import dchars.languages.san.transliterations.itrans.itrans as trans_itrans
import dchars.languages.san.transliterations.itrans.ucombinations as trans_itrans_ucombinations

import dchars.languages.san.transliterations.iso15919.iso15919 as trans_iso15919
import dchars.languages.san.transliterations.iso15919.ucombinations as trans_iso15919_ucombinations

################################################################################
class DStringSAN(DStringMotherClass):
    """
        class DStringSAN
    """

    # regex pattern used to slice a source string :
    #
    # NB : we use the default_symbols__pattern() function, NOT the normal
    #      default_symbols() function since some characters have to be
    #      treated apart to work with a regex.
    pattern_basechar = "|".join( SYMB_CONSONANTS.default_symbols__pattern() + \
                                 SYMB_INDEPENDENT_VOWELS.default_symbols__pattern() + \
                                 SYMB_OTHER_SYMBOLS.default_symbols__pattern() + \
                                 SYMB_PUNCTUATION.default_symbols__pattern() )
    pattern_dependentvowel = "|".join( SYMB_DEPENDENT_VOWELS.default_symbols__pattern() )
    pattern_diacritics = "|".join( SYMB_DIACRITICS.default_symbols__pattern() )
    pattern_txt = "((?P<basechar>{0})((?P<dependentvowel>{1}))?(?P<diacritics>({2})+)?)"
    pattern = re.compile(pattern_txt.format( pattern_basechar,
                                             pattern_dependentvowel,
                                             pattern_diacritics ))

    # transliterations' methods : available direction(s) :
    trans__directions = {
          "itrans"      : trans_itrans.AVAILABLE_DIRECTIONS,
          "iso15919"    : trans_iso15919.AVAILABLE_DIRECTIONS,
        }

    # transliteration's functions :
    trans__init_from_transliteration = {
          "itrans"   : trans_itrans.dstring__init_from_translit_str,
          "iso15919" : trans_iso15919.dstring__init_from_translit_str,
          }

    trans__get_transl_ucombinations = {
          "itrans" : trans_itrans_ucombinations.get_usefull_combinations,
          "iso15919" : trans_iso15919_ucombinations.get_usefull_combinations,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, str_src = None):
        """
                DStringSAN.__init__

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
                DStringSAN.get_usefull_combinations

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

        dchar = DCharacterSAN(self)
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
                DStringSAN.get_usefull_transl_combinations

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
        # -> "Instance of 'DStringSAN' has no 'transliteration_method' member"
        res = DStringSAN.trans__get_transl_ucombinations[self.transliteration_method]()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self):
        """
                DStringSAN.get_transliteration
        """
        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringSAN' has no 'transliteration_method' member"

        res = []

        #.......................................................................
        # transliteration of each character in <self> :
        #.......................................................................
        for index, dchar in enumerate(self):

            # <prev_dchar> : None or a DStringSAN object.
            if index == 0:
                prev_dchar = None
            else:
                prev_dchar = self[index-1]

            res.append( dchar.get_transliteration(
                prev_dchar=prev_dchar,
                transliteration_method = self.transliteration_method) )

        res = "".join( res )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, str_src):
        """
                DStringSAN.init_from_str

                Function called by __init__(), initialize <self> and return
                <indexes_of_unrecognized_chars>.

                str_src : str

                HOW IT WORKS :
                * (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
                * (2) = normalized_src -> (itrans symbols required) :
                *     replace_by_the_default_symbols() -> normalized_src
                * (3) initialisation from the recognized characters.
                *     re.finditer(DStringSAN.pattern) give the symbols{base_char, diacritics}
                *     (3.1) virama
                *     (3.2) base_char, punctuation, dependentvowel, is_an_independent_vowel
                *     (3.3) accent
                *     (3.4) nukta
                *     (3.5) anusvara_candrabindu
                *     (3.6) anudatta
                *     (3.7) we add the new character
        """
        #.......................................................................
        # (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
        #.......................................................................
        normalized_src = unicodedata.normalize('NFD', str_src)

        #.......................................................................
        # (2) = normalized_src -> (itrans symbols required) :
        #     replace_by_the_default_symbols() -> normalized_src
        #.......................................................................
        normalized_src = SYMB_CONSONANTS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_INDEPENDENT_VOWELS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_DEPENDENT_VOWELS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_DIACRITICS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_PUNCTUATION.replace_by_the_default_symbols(normalized_src)

        #.......................................................................
        # (3) initialisation from the recognized characters.
        #     re.finditer(DStringSAN.pattern) give the symbols{basechar, diacritics}
        #.......................................................................
        indexes = []    # indexes of the substring well analyzed : ( start, end )
        for element in re.finditer(DStringSAN.pattern,
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
                    new_character = DCharacterSAN(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )
            else:
                # <indexes> is empty :
                # ... we add the unknown character(s) before the first index in <indexes> :
                for index in range( 0, element.start() ):
                    new_character = DCharacterSAN(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )

            indexes.append( (element.start(), element.end()-1 ) )

            data = element.groupdict()
            base_char   = data['basechar']
            dependentvowel = data['dependentvowel']
            diacritics = data['diacritics']

            # base_char as "क" becomes "KA"
            base_char__punctuation = SYMB_PUNCTUATION.get_the_name_for_this_symbol(base_char)
            base_char__other_symbols = SYMB_OTHER_SYMBOLS.get_the_name_for_this_symbol(base_char)
            base_char__consonant = SYMB_CONSONANTS.get_the_name_for_this_symbol(base_char)
            base_char__ivowel = SYMB_INDEPENDENT_VOWELS.get_the_name_for_this_symbol(base_char)
            base_char__dvowel = SYMB_DEPENDENT_VOWELS.get_the_name_for_this_symbol(dependentvowel)

            is_an_independent_vowel = False # <is_an_independent_vowel> is set here since,
                                            # if base_char is a punctuation symbol,
                                            # it will never be set again but it is needed by
                                            # the call to new_character = DCharacterSAN(...)

            virama = False
            if diacritics is not None:
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.1) virama
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                virama_nbr = number_of_occurences( source_string = diacritics,
                                                   symbols = SYMB_DIACRITICS__VIRAMA)

                if virama_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), 'virama' defined several times."
                    raise DCharsError( context = "DStringSAN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                virama = SYMB_DIACRITICS.are_these_symbols_in_a_string('DEVANAGARI SIGN VIRAMA',
                                                                       diacritics)

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.2) base_char, punctuation, dependentvowel, is_an_independent_vowel
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            if base_char__punctuation is not None:
                # punctuation symbol :
                punctuation = True
                base_char = base_char__punctuation

            elif base_char__other_symbols is not None:
                # "other symbol" : not punctuation nor consonant nor independent vowel :
                punctuation = False
                base_char = base_char__other_symbols

            else:
                punctuation = False

                if base_char__consonant is not None:
                    # consonant :
                    is_an_independent_vowel = False
                    base_char = base_char__consonant

                    # dependent vowel ?
                    if base_char != 'DEVANAGARI SIGN VISARGA' and \
                       not virama and dependentvowel is None:
                        # special case : for normal consonants (and visarga is a pseudo-consonant)
                        #                written without any vowel symbol, the dependent vowel
                        #                is 'A'. E.g. 'क' stands for 'ka', not for 'k'.
                        dependentvowel = "A"
                    else:
                        dependentvowel = base_char__dvowel

                else:
                    # independent vowel :
                    is_an_independent_vowel = True
                    dependentvowel = None
                    base_char = base_char__ivowel


            accent = None
            nukta = False
            anusvara_candrabindu = None
            anudatta = False
            if diacritics is not None:
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.3) accent
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                accent_nbr = number_of_occurences( source_string = diacritics,
                                                   symbols = SYMB_DIACRITICS__ACCENTS )

                if accent_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), 'accent' defined several times."
                    raise DCharsError( context = "DStringSAN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                accent = None
                for accent_char in SYMB_DIACRITICS__ACCENTS:
                    accent_name = SYMB_DIACRITICS.defaultsymbol2name[accent_char]
                    if SYMB_DIACRITICS.are_these_symbols_in_a_string(name=accent_name,
                                                                     string=diacritics):
                        accent = accent_name
                        break

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.4) nukta
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                nukta_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__NUKTA )

                if nukta_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), 'nukta' defined several times."
                    raise DCharsError( context = "DStringSAN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                nukta = SYMB_DIACRITICS.are_these_symbols_in_a_string('DEVANAGARI SIGN NUKTA',
                                                                      diacritics)

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.5) anusvara_candrabindu
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                anusvara_candrabindu_nbr = number_of_occurences(
                    source_string = diacritics,
                    symbols = SYMB_DIACRITICS__ANUSVARA_CANDRABINDU)

                if anusvara_candrabindu_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), " \
                              "'anusvara_candrabindu' defined several times."
                    raise DCharsError( context = "DStringSAN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                anusvara_candrabindu = None
                for anusvara_candrabindu_char in SYMB_DIACRITICS__ANUSVARA_CANDRABINDU:
                    anusvara_candrabindu_name = SYMB_DIACRITICS.defaultsymbol2name[
                        anusvara_candrabindu_char]
                    if SYMB_DIACRITICS.are_these_symbols_in_a_string(name=anusvara_candrabindu_name,
                                                                     string=diacritics):
                        anusvara_candrabindu = anusvara_candrabindu_name
                        break

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.6) anudatta
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                anudatta_nbr = number_of_occurences( source_string = diacritics,
                                                   symbols = SYMB_DIACRITICS__ANUDATTA)

                if anudatta_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), 'anudatta' defined several times."
                    raise DCharsError( context = "DStringSAN.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                anudatta = SYMB_DIACRITICS.are_these_symbols_in_a_string(
                    'DEVANAGARI STRESS SIGN ANUDATTA',
                    diacritics)

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.7) we add the new character
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            new_character = DCharacterSAN(dstring_object = self,
                                          unknown_char = False,
                                          base_char = base_char,
                                          accent = accent,
                                          punctuation = punctuation,
                                          nukta = nukta,
                                          anusvara_candrabindu = anusvara_candrabindu,
                                          virama = virama,
                                          anudatta = anudatta,
                                          is_an_independent_vowel = is_an_independent_vowel,
                                          dependentvowel = dependentvowel)
            self.append( new_character )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # we add the final unknown characters (see at the beginning of this
        # function)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if indexes:
            # <element> is the last one and <indexes> isn't empty :
            for index in range( max(indexes[-1])+1, len(normalized_src) ):
                new_character = DCharacterSAN(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

        else:
            # <indexes> is empty :
            for index in range( 0, len(normalized_src) ):
                new_character = DCharacterSAN(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src):
        """
                DStringSAN.init_from_transliteration

                src     :       string

                Return <self>
        """
        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringSAN' has no 'transliteration_method' member"

        DStringSAN.trans__init_from_transliteration[self.transliteration_method](
                dstring = self,
                dcharactertype = DCharacterSAN,
                src = src)

        return self

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringSAN.sortingvalue
        """
        _res = [ dchar.sortingvalue() for dchar in self ]

        # we don't treat the "visarga" (e.g. अः) as a stand-alone character but
        # as an attribute of the last character :
        res = []
        for index_svalue, svalue in enumerate(_res):
            if svalue == DCharacterSAN.sortingvalue_for_visarga:
                if index_svalue > 0:
                    res[-1][4] = 999
            else:
                res.append(svalue)

        return res
