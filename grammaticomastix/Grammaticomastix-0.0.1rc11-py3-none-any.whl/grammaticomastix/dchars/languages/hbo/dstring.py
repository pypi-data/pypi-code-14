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
    ❏DChars❏ : dchars/languages/hbo/dstring.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError
from dchars.dstring import DStringMotherClass
from dchars.languages.hbo.dcharacter import DCharacterHBO
from dchars.languages.hbo.symbols import SYMB_LETTERS, \
                                         SYMB_OTHER_SYMBOLS, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_POINTS, \
                                         SYMB_VOWELS, \
                                         SYMB_CANTILLATION_MARKS, \
                                         SYMB_DIACRITICS__VOWELS, \
                                         SYMB_DIACRITICS__SHIN_SIN_DOT, \
                                         SYMB_DIACRITICS__DAGHESH_MAPIQ, \
                                         SYMB_DIACRITICS__METHEGH, \
                                         SYMB_DIACRITICS__RAPHE, \
                                         SYMB_DIACRITICS__CANTILLATION_MARKS, \
                                         SYMB_DIACRITICS__SPECIALPOINTS, \
                                         SYMB_SPECIALPOINTS
import re
import unicodedata
from dchars.utilities.lstringtools import number_of_occurences
from dchars.utilities.sortingvalue import SortingValue

# known transliterations :
import dchars.languages.hbo.transliterations.basic.basic as basictrans
import dchars.languages.hbo.transliterations.basic.ucombinations as basictrans_ucombinations

################################################################################
class DStringHBO(DStringMotherClass):
    """
        class DStringHBO

        DO NOT CREATE A DStringHBO object directly but use instead the
        dchars.py::new_dstring function.
    """

    # regex pattern used to slice a source string :
    #
    # NB : we use the default_symbols__pattern() function, NOT the normal
    #      default_symbols() function since some characters have to be
    #      treated apart to work with a regex.
    pattern_basechar = "|".join( SYMB_LETTERS.default_symbols__pattern() + \
                                 SYMB_OTHER_SYMBOLS.default_symbols__pattern() + \
                                 SYMB_PUNCTUATION.default_symbols__pattern() )
    pattern_diacritics = "|".join( SYMB_VOWELS.default_symbols__pattern() + \
                                   SYMB_POINTS.default_symbols__pattern() + \
                                   SYMB_SPECIALPOINTS.default_symbols__pattern() + \
                                   SYMB_CANTILLATION_MARKS.default_symbols__pattern() )
    pattern = re.compile("((?P<basechar>{0})(?P<diacritics>({1})+)?)".format( pattern_basechar,
                                                                              pattern_diacritics ))

    # transliterations' methods : available direction(s) :
    trans__directions = {
          "basic"       : basictrans.AVAILABLE_DIRECTIONS,
        }

    # transliteration's functions :
    trans__init_from_transliteration = {
          "basic" : basictrans.dstring__init_from_translit_str,
          }

    trans__get_transl_ucombinations = {
        "basic"   : basictrans_ucombinations.get_usefull_combinations,
        }


    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, str_src = None):
        """
                DStringHBO.__init__

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
                DStringHBO.get_usefull_combinations

                Return a DString with all the usefull combinations of characters,
                i.e. only the 'interesting' characters (not punctuation if it's too simple
                by example). The DChars stored in the dstring will be unique, id est, two
                dchars will not have the same appearence (__str__())

                NB : this function has nothing to do with linguistic or a strict
                     approach of the language. This function allows only to get the
                     most common and/or usefull characters of the writing system.
        """
        self.clear()

        dchar = DCharacterHBO(self)
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
                DStringHBO.get_usefull_transl_combinations

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
        # -> "Instance of 'DStringHBO' has no 'transliteration_method' member"
        res = DStringHBO.trans__get_transl_ucombinations[self.transliteration_method]()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self):
        """
                DStringHBO.get_transliteration
        """
        res = []

        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringHBO' has no 'transliteration_method' member"
        for dchar in self:
            res.append( dchar.get_transliteration(self.transliteration_method) )

        return "".join( res )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, str_src):
        """
                DStringHBO.init_from_str

                Function called by __init__(), initialize <self>

                str_src : str

                HOW IT WORKS :
                * (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
                * (2) = normalized_src -> (default symbols required) :
                *     replace_by_the_default_symbols() -> normalized_src
                * (3) initialisation from the recognized characters.
                *     re.finditer(DStringHBO.pattern) give the symbols{base_char, diacritics}
                *     (3.1) contextual_form
                *     (3.2) shin_sin_dot
                *     (3.3) daghesh_mapiq
                *     (3.4) methegh
                *     (3.5) specialpoint
                *     (3.6) vowel
                *     (3.7) raphe
                *     (3.8) cantillation_mark
                *     (3.9) we add the new character
        """
        #.......................................................................
        # (1) str_src -> (decomposition) unicodedata.normalize('NFD',) = normalized_src
        #.......................................................................
        normalized_src = unicodedata.normalize('NFD', str_src)

        #.......................................................................
        # (2) = normalized_src -> (default symbols required) :
        #     replace_by_the_default_symbols() -> normalized_src
        #.......................................................................
        normalized_src = SYMB_LETTERS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_OTHER_SYMBOLS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_PUNCTUATION.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_VOWELS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_POINTS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_SPECIALPOINTS.replace_by_the_default_symbols(normalized_src)
        normalized_src = SYMB_CANTILLATION_MARKS.replace_by_the_default_symbols(normalized_src)

        #.......................................................................
        # (3) initialisation from the recognized characters.
        #     re.finditer(DStringHBO.pattern) give the symbols{basechar, diacritics}
        #.......................................................................
        indexes = []    # indexes of the substring well analyzed : ( start, end )
        for element in re.finditer(DStringHBO.pattern, normalized_src):

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # we add the unknown characters at the beginning and in the middle
            # of the string (see at the end of this function)
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            if indexes:
                # <indexes> isn't empty :
                # ... we add the unknown character(s) between the last character and
                # the current one :
                for index in range( max(indexes[-1])+1, element.start() ):
                    new_character = DCharacterHBO(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )
            else:
                # <indexes> is empty :
                # ... we add the unknown character(s) before the first index in <indexes> :
                for index in range( 0, element.start() ):
                    new_character = DCharacterHBO(dstring_object = self,
                                                  unknown_char = True,
                                                  base_char = normalized_src[index])

                    self.append( new_character )

            indexes.append( (element.start(), element.end()-1 ) )

            data = element.groupdict()
            base_char   = data['basechar']
            diacritics = data['diacritics']

            punctuation = base_char in SYMB_PUNCTUATION.symbol2name

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.1) contextual_form
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            if base_char == "ך":
                base_char = "כ"
                contextual_form = "final"
            elif base_char == "ם":
                base_char = "מ"
                contextual_form = "final"
            elif base_char == "ן":
                base_char = "נ"
                contextual_form = "final"
            elif base_char == "ף":
                base_char = "פ"
                contextual_form = "final"
            elif base_char == "ץ":
                base_char = "צ"
                contextual_form = "final"
            elif punctuation == False:
                contextual_form = "initial+medium+final"
            else:
                contextual_form = None



            shin_sin_dot = None
            daghesh_mapiq = False
            methegh = False
            specialpoint = None
            vowel = None
            raphe = False
            cantillation_mark = None

            if diacritics is not None:
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.2) shin_sin_dot
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                shin_sin_dot_nbr = number_of_occurences( source_string = diacritics,
                                                         symbols = SYMB_DIACRITICS__SHIN_SIN_DOT )

                if shin_sin_dot_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), shin_sin_dot defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                shin_sin_dot = None
                if SYMB_POINTS.are_these_symbols_in_a_string("HEBREW POINT SHIN DOT", diacritics):
                    shin_sin_dot = "HEBREW POINT SHIN DOT"
                elif SYMB_POINTS.are_these_symbols_in_a_string("HEBREW POINT SIN DOT", diacritics):
                    shin_sin_dot = "HEBREW POINT SIN DOT"

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.3) daghesh_mapiq
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                daghesh_mapiq_nbr = number_of_occurences( source_string = diacritics,
                                                          symbols = SYMB_DIACRITICS__DAGHESH_MAPIQ)

                if daghesh_mapiq_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), daghesh_mapiq defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                daghesh_mapiq = SYMB_POINTS.are_these_symbols_in_a_string(
                    "HEBREW POINT DAGESH OR MAPIQ",
                    diacritics)

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.4) methegh
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                methegh_nbr = number_of_occurences( source_string = diacritics,
                                                    symbols = SYMB_DIACRITICS__METHEGH)

                if methegh_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), methegh defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                methegh = SYMB_POINTS.are_these_symbols_in_a_string("HEBREW POINT METEG",
                                                                    diacritics)

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.5) specialpoint
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                specialpoint_nbr = number_of_occurences( source_string = diacritics,
                                                          symbols = SYMB_DIACRITICS__SPECIALPOINTS)

                if specialpoint_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), specialpoint defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                specialpoint = None
                for specialpoint_char in SYMB_DIACRITICS__SPECIALPOINTS:
                    specialpoint_name = SYMB_SPECIALPOINTS.defaultsymbol2name[specialpoint_char]
                    if SYMB_SPECIALPOINTS.are_these_symbols_in_a_string(name=specialpoint_name,
                                                                        string=diacritics):
                        specialpoint = specialpoint_name
                        break

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.6) vowel
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                vowel_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__VOWELS)

                if vowel_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), vowel defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                vowel = None
                for vowel_char in SYMB_DIACRITICS__VOWELS:
                    vowel_name = SYMB_VOWELS.defaultsymbol2name[vowel_char]
                    if SYMB_VOWELS.are_these_symbols_in_a_string(name=vowel_name,
                                                                 string=diacritics):
                        vowel = vowel_name
                        break

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.7) raphe
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                raphe_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__RAPHE)

                if raphe_nbr > 1:
                    err_msg = "In '{0}' (start={1}, end={2}), raphe defined several times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                raphe = SYMB_POINTS.are_these_symbols_in_a_string("HEBREW POINT RAFE", diacritics)

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # (3.8) cantillation_mark
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                cmark_nbr = number_of_occurences( source_string = diacritics,
                                                  symbols = SYMB_DIACRITICS__CANTILLATION_MARKS )

                if cmark_nbr > 2:
                    err_msg = "In '{0}' (start={1}, end={2}), " \
                              "cantillation marks defined more than two times."
                    raise DCharsError( context = "DStringHBO.init_from_str",
                                       message = err_msg.format(element.string,
                                                                element.start(),
                                                                element.end()),)

                cantillation_mark = []
                for cmark_char in SYMB_DIACRITICS__CANTILLATION_MARKS:
                    cmark_name = SYMB_CANTILLATION_MARKS.defaultsymbol2name[cmark_char]
                    if SYMB_CANTILLATION_MARKS.are_these_symbols_in_a_string(name=cmark_name,
                                                                             string=diacritics):
                        cantillation_mark.append( cmark_name )

                if cantillation_mark == []:
                    cantillation_mark = None

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # (3.9) we add the new character
            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            new_character = DCharacterHBO(dstring_object = self,
                                          unknown_char = False,
                                          base_char = base_char,
                                          contextual_form = contextual_form,
                                          punctuation = punctuation,
                                          shin_sin_dot = shin_sin_dot,
                                          daghesh_mapiq = daghesh_mapiq,
                                          methegh = methegh,
                                          specialpoint = specialpoint,
                                          vowel = vowel,
                                          raphe = raphe,
                                          cantillation_mark = cantillation_mark)

            self.append( new_character )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # we add the final unknown characters (see at the beginning of this
        # function)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if indexes:
            # <element> is the last one and <indexes> isn't empty :
            for index in range( max(indexes[-1])+1, len(normalized_src) ):
                new_character = DCharacterHBO(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

        else:
            # <indexes> is empty :
            for index in range( 0, len(normalized_src) ):
                new_character = DCharacterHBO(dstring_object = self,
                                              unknown_char = True,
                                              base_char = normalized_src[index])

                self.append( new_character )

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src):
        """
                DStringHBO.init_from_transliteration

                src     :       string

                Return <self>
        """
        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringHBO' has no 'transliteration_method' member"
        DStringHBO.trans__init_from_transliteration[self.transliteration_method](
                dstring = self,
                dcharactertype = DCharacterHBO,
                src = src)

        return self

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringHBO.sortingvalue

                Return a SortingValue object
        """
        res = SortingValue()

        # Pylint can't know that <self> has an 'options' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringHBO' has no 'options' member"
        if self.options["sorting method"] == "default":

            # base character :
            data = []
            for char in self:
                data.append( ({False:0,
                               True:1}[char.unknown_char],
                              char.base_char ))
            res.append(data)

            # shin_sin_dot :
            data = []
            for char in self:
                data.append( ({None                     : 0,
                               "HEBREW POINT SHIN DOT"  : 1,
                               "HEBREW POINT SIN DOT"   : 2,}[char.shin_sin_dot]
                             ))
            res.append(data)

            # vowel :
            data = []
            for char in self:
                data.append( ({None                             : 0,
                               "HEBREW POINT PATAH"             : 1,
                               "HEBREW POINT SEGOL"             : 2,
                               "HEBREW POINT HIRIQ"             : 3,
                               "HEBREW POINT QUBUTS"            : 4,
                               "HEBREW POINT QAMATS"            : 5,
                               "HEBREW POINT QAMATS QATAN"      : 6,
                               "HEBREW POINT TSERE"             : 7,
                               "HEBREW POINT HOLAM"             : 8,
                               "HEBREW POINT HOLAM HASER FOR VAV": 9,
                               "HEBREW POINT HATAF SEGOL"       : 10,
                               "HEBREW POINT HATAF PATAH"       : 11,
                               "HEBREW POINT HATAF QAMATS"      : 12,
                               "HEBREW POINT SHEVA"             : 13,}[char.vowel]
                             ))
            res.append(data)

            # daghesh_mapiq :
            data = []
            for char in self:
                data.append( ({False:0,
                               True:1}[char.daghesh_mapiq] ))
            res.append(data)

            # methegh :
            data = []
            for char in self:
                data.append( ({False:0,
                               True:1}[char.methegh] ))
            res.append(data)

            # raphe :
            data = []
            for char in self:
                data.append( ({False:0,
                               True:1}[char.raphe] ))
            res.append(data)

            # special point :
            data = []
            for char in self:
                data.append( ({None                             : 0,
                               "HEBREW MARK UPPER DOT"          : 1,
                               "HEBREW MARK LOWER DOT"          : 2,}[char.specialpoint]
                             ))
            res.append(data)

        else:
            # Pylint can't know that <self> has an 'options' member
            # created when <self> has been initialized by new_dstring() :
            # pylint: disable=E1101
            # -> "Instance of 'DStringHBO' has no 'options' member"
            err_msg = "unknown sorting method '{0}'."
            raise DCharsError( context = "DStringHBO.sortingvalue",
                               message = err_msg.format(self.options["sorting method"]) )

        return res
