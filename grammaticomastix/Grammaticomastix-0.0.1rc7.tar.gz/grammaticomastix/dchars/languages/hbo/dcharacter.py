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
    ❏DChars❏ : dchars/languages/hbo/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
from dchars.languages.hbo.symbols import SYMB_POINTS, \
                                         SYMB_VOWELS, \
                                         SYMB_CANTILLATION_MARKS, \
                                         SYMB_SPECIALPOINTS, \
                                         DEFAULTSYMB__DAGHESHMAPIQ, \
                                         DEFAULTSYMB__METEG, \
                                         DEFAULTSYMB__RAFE
# known transliterations :
import dchars.languages.hbo.transliterations.basic.basic as basictrans

import copy
import itertools

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
# see http://www.unicode.org/charts/PDF/UFB00.pdf
#
################################################################################
COMPLETE_NORMALIZE_NFC = (

                # FB2A שׁ HEBREW LETTER SHIN WITH SHIN DOT
                ( chr(0x05E9)+chr(0x05C1), chr(0xFB2A) ),
                # FB2B שׂ HEBREW LETTER SHIN WITH SIN DOT
                ( chr(0x05E9)+chr(0x05C2), chr(0xFB2B) ),
                # FB2C שּׁ HEBREW LETTER SHIN WITH DAGESH AND SHIN DOT
                ( chr(0x0549)+chr(0x05C1), chr(0xFB2C) ),
                # FB2D שּׂ HEBREW LETTER SHIN WITH DAGESH AND SIN DOT
                ( chr(0x0549)+chr(0x05C2), chr(0xFB2D) ),

                # FB2E אַ HEBREW LETTER ALEF WITH PATAH
                ( chr(0x05D0)+chr(0x05B7), chr(0xFB2E) ),
                # FB2F אָ HEBREW LETTER ALEF WITH QAMATS
                ( chr(0x05D0)+chr(0x05B8), chr(0xFB2F) ),

                # consonants + daghesh/mapiq :
                ( chr(0x05D0)+chr(0x05BC), chr(0xFB30) ),
                ( chr(0x05D1)+chr(0x05BC), chr(0xFB31) ),
                ( chr(0x05D2)+chr(0x05BC), chr(0xFB32) ),
                ( chr(0x05D3)+chr(0x05BC), chr(0xFB33) ),
                ( chr(0x05D4)+chr(0x05BC), chr(0xFB34) ),
                ( chr(0x05D5)+chr(0x05BC), chr(0xFB35) ),
                ( chr(0x05D6)+chr(0x05BC), chr(0xFB36) ),
                ( chr(0x05D8)+chr(0x05BC), chr(0xFB38) ),
                ( chr(0x05D9)+chr(0x05BC), chr(0xFB39) ),
                ( chr(0x05DA)+chr(0x05BC), chr(0xFB3A) ),
                ( chr(0x05DB)+chr(0x05BC), chr(0xFB3B) ),
                ( chr(0x05DC)+chr(0x05BC), chr(0xFB3C) ),
                ( chr(0x05DE)+chr(0x05BC), chr(0xFB3E) ),
                ( chr(0x05E0)+chr(0x05BC), chr(0xFB40) ),
                ( chr(0x05E1)+chr(0x05BC), chr(0xFB41) ),
                ( chr(0x05E3)+chr(0x05BC), chr(0xFB43) ),
                ( chr(0x05E4)+chr(0x05BC), chr(0xFB44) ),
                ( chr(0x05E6)+chr(0x05BC), chr(0xFB46) ),
                ( chr(0x05E7)+chr(0x05BC), chr(0xFB47) ),
                ( chr(0x05E8)+chr(0x05BC), chr(0xFB48) ),
                ( chr(0x05E9)+chr(0x05BC), chr(0xFB49) ),
                ( chr(0x05EA)+chr(0x05BC), chr(0xFB4A) ),

                # vav + holam :
                ( chr(0x05D5)+chr(0x05B9), chr(0xFB4B) ),

                # beth + raphe :
                ( chr(0x05D1)+chr(0x05BF), chr(0xFB4C) ),
                # kaph + raphe :
                ( chr(0x05DB)+chr(0x05BF), chr(0xFB4D) ),
                # pe + raphe
                ( chr(0x05E4)+chr(0x05BF), chr(0xFB4E) ),
                )

################################################################################
class DCharacterHBO(DCharacterMotherClass):
    """
        class DCharacterHBO
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
                DCharacterHBO.__eq__

                aliud   :       DCharacterHBO object
        """

        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.contextual_form == aliud.contextual_form) and \
               (self.shin_sin_dot == aliud.shin_sin_dot) and \
               (self.daghesh_mapiq == aliud.daghesh_mapiq) and \
               (self.methegh == aliud.methegh) and \
               (self.specialpoint == aliud.specialpoint) and \
               (self.vowel == aliud.vowel) and \
               (self.raphe == aliud.raphe) and \
               (self.cantillation_mark == aliud.cantillation_mark)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 punctuation = False,
                 contextual_form = None,
                 shin_sin_dot = None,
                 daghesh_mapiq = False,
                 methegh = False,
                 specialpoint = None,
                 vowel = None,
                 raphe = False,
                 cantillation_mark = None):
        """
                DCharacterHBO.__init__

                .. code-block:: none

                    unknown_char                    : bool
                    base_char                       : None or a string
                                                      E.g : "צ", not "TSADI" or "ץ" (final tsadi)
                    contextual_form                 : None or a string
                                                      ("initial+medium+final", "final")
                    punctuation                     : True, False
                    shin_sin_dot                    : None or a string
                                                      ("HEBREW POINT SHIN DOT",
                                                       "HEBREW POINT SIN DOT")
                    daghesh_mapiq                   : bool
                    methegh                         : bool
                    specialpoint                   : None or a string
                                                      ("HEBREW MARK UPPER DOT",
                                                       "HEBREW MARK LOWER DOT")
                    vowel                           : None or string
                                                      see symbols.py::SYMB_VOWELS
                    raphe                           : bool
                    cantillation_mark               : None or a list of strings
                                                      see symbols.py::SYMB_CANTILLATION_MARKS
        """

        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.contextual_form = contextual_form
        self.shin_sin_dot = shin_sin_dot
        self.daghesh_mapiq = daghesh_mapiq
        self.methegh = methegh
        self.specialpoint = specialpoint
        self.vowel = vowel
        self.raphe = raphe
        self.cantillation_mark = cantillation_mark

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterHBO.__repr__
        """

        if self.base_char is None:
            hexnum = ""
        else:
            hexnum = hex(ord(self.base_char))

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + hexnum + "; " + \
               "contextual_form="+repr(self.contextual_form) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "shin_sin_dot="+repr(self.shin_sin_dot) + "; " + \
               "daghesh_mapiq="+repr(self.daghesh_mapiq) + "; " +\
               "methegh="+repr(self.methegh) + "; " +\
               "specialpoint="+repr(self.specialpoint) + "; " +\
               "vowel="+repr(self.vowel) + "; " + \
               "raphe="+repr(self.raphe) + "; " + \
               "cantillation_mark="+repr(self.cantillation_mark)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterHBO.clone
        """
        return DCharacterHBO( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              punctuation = self.punctuation,
                              contextual_form = self.contextual_form,
                              shin_sin_dot = self.shin_sin_dot,
                              daghesh_mapiq = self.daghesh_mapiq,
                              methegh = self.methegh,
                              specialpoint = self.specialpoint,
                              vowel = self.vowel,
                              raphe = self.raphe,
                              cantillation_mark = self.cantillation_mark )

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self, transliteration_method):
        """
                DCharacterHBO.get_transliteration

                method  : string
        """
        return DCharacterHBO.trans__get_transliteration[transliteration_method](
            dstring_object = self.dstring_object,
            dchar = self)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterHBO.get_sourcestr_representation

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

            base_char = self.base_char

            if base_char == "כ" and self.contextual_form == "final":
                base_char = "ך"

            if base_char == "מ" and self.contextual_form == "final":
                base_char = "ם"

            if base_char == "נ" and self.contextual_form == "final":
                base_char = "ן"

            if base_char == "פ" and self.contextual_form == "final":
                base_char = "ף"

            if base_char == "צ" and self.contextual_form == "final":
                base_char = "ץ"

            res.append( base_char )

        if self.shin_sin_dot is not None:
            res.append( SYMB_POINTS.get_default_symbol(self.shin_sin_dot) )

        if self.daghesh_mapiq:
            res.append( DEFAULTSYMB__DAGHESHMAPIQ )

        if self.vowel is not None:
            res.append( SYMB_VOWELS.get_default_symbol(self.vowel) )

        if self.methegh:
            res.append( DEFAULTSYMB__METEG )

        if self.raphe:
            res.append( DEFAULTSYMB__RAFE )

        if self.specialpoint is not None:
            res.append( SYMB_SPECIALPOINTS.get_default_symbol(self.specialpoint) )

        if self.cantillation_mark is not None:
            for cmark in self.cantillation_mark:
                res.append( SYMB_CANTILLATION_MARKS.get_default_symbol(cmark) )

        res = "".join(res)

        # composition with COMPLETE_NORMALIZE_NFC
        # we don't use NFC which "shuffle" the elements in an order incompatible
        # with our code.
        for src, dest in COMPLETE_NORMALIZE_NFC:
            res = res.replace(src, dest)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterHBO.get_usefull_combinations

                Yield, one dchar at a time,  all the usefull combinations of characters,
                i.e. only the 'interesting' characters (not punctuation if it's too simple
                by example).

                NB : this function has nothing to do with linguistic or a strict
                     approach of the language. This function allows only to get the
                     most common and/or usefull characters of the writing system.
        """
        # base_char : we don't use the list stored in symbols.py
        # since we would lost the character's order.
        base_characters = ( 'א',
                            'ב',
                            'ג',
                            'ד',
                            'ה',
                            'ו',
                            'ז',
                            'ח',
                            'ט',
                            'י',
                            'כ',
                            'ל',
                            'מ',
                            'נ',
                            'ס',
                            'ע',
                            'פ',
                            'צ',
                            'ק',
                            'ר',
                            'ש',
                            'ת' )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters:
            for shin_sin_dot in (None,
                                 "HEBREW POINT SHIN DOT",
                                 "HEBREW POINT SIN DOT"):

                if base_char != 'SHIN':
                    shin_sin_dot = None

                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               contextual_form = None,
                               shin_sin_dot = None,
                               daghesh_mapiq = False,
                               methegh = False,
                               specialpoint = None,
                               vowel = None,
                               raphe = False,
                               cantillation_mark = None )

                yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_char :
                                           base_characters,

                                           # contextual_form :
                                           ("initial+medium+final", "final"),

                                           # shin_sin_dot :
                                           (None, "HEBREW POINT SHIN DOT", "HEBREW POINT SIN DOT"),

                                           # vowel :
                                           (None,
                                            "HEBREW POINT SHEVA",
                                            "HEBREW POINT HATAF SEGOL",
                                            "HEBREW POINT HATAF PATAH",
                                            "HEBREW POINT HATAF QAMATS",
                                            "HEBREW POINT HIRIQ",
                                            "HEBREW POINT TSERE",
                                            "HEBREW POINT SEGOL",
                                            "HEBREW POINT PATAH",
                                            "HEBREW POINT QAMATS",
                                            "HEBREW POINT HOLAM",
                                            "HEBREW POINT HOLAM HASER FOR VAV",
                                            "HEBREW POINT QUBUTS",
                                            "HEBREW POINT QAMATS QATAN"),
                                             ))

        for base_char, contextual_form, shin_sin_dot, \
            vowel in combinations:

            add_this_dchar = True

            if base_char == 'ש':
                if contextual_form != "initial+medium+final":
                    add_this_dchar = False

            elif base_char in ('כ', 'מ', 'נ', 'פ', 'צ'):
                if shin_sin_dot != None:
                    add_this_dchar = False

            else:
                if contextual_form != "initial+medium+final" or \
                   shin_sin_dot != None:
                    add_this_dchar = False

            if add_this_dchar:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               contextual_form = contextual_form,
                               shin_sin_dot = shin_sin_dot,
                               daghesh_mapiq = False,
                               methegh = False,
                               specialpoint = None,
                               vowel = vowel,
                               raphe = None,
                               cantillation_mark = None, )

                yield copy.copy(self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterHBO.init_from_transliteration

                src     :       string
                transliteration_method  :       string

                Return <self>.
        """
        self.reset()
        return DCharacterHBO.trans__init_from_transliteration[transliteration_method](dchar = self,
                                                                                      src = src)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterHBO.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.contextual_form = None
        self.shin_sin_dot = None
        self.daghesh_mapiq = False
        self.methegh = False
        self.specialpoint = None
        self.vowel = None
        self.raphe = False
        self.cantillation_mark = None

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterHBO.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.shin_sin_dot = None
        self.daghesh_mapiq = False
        self.methegh = False
        self.specialpoint = None
        self.vowel = None
        self.raphe = False
        self.cantillation_mark = None

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DCharacterHBO.sortingvalue

                Return a SortingValue object

                NB : this function has almost no interest; you must use DStringHBO.sortingvalue()
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

            # base_char :
            res.append( ord(self.base_char) )

            # shin_sin_dot :
            if self.shin_sin_dot is None:
                res.append(0)
            elif self.shin_sin_dot == "HEBREW POINT SHIN DOT":
                res.append(1)
            elif self.shin_sin_dot == "HEBREW POINT SIN DOT":
                res.append(2)
            else:
                raise DCharsError( context = "DCharacterHBO.sortingvalue",
                                   message = "unknown value for shin_sin_dot ="+\
                                             str(self.shin_sin_dot) )

            # vowel :
            if self.vowel is None:
                res.append(0)
            elif self.vowel == "HEBREW POINT PATAH":
                res.append(1)
            elif self.vowel == "HEBREW POINT SEGOL":
                res.append(2)
            elif self.vowel == "HEBREW POINT HIRIQ":
                res.append(3)
            elif self.vowel == "HEBREW POINT QUBUTS":
                res.append(4)
            elif self.vowel == "HEBREW POINT QAMATS":
                res.append(5)
            elif self.vowel == "HEBREW POINT QAMATS QATAN":
                res.append(6)
            elif self.vowel == "HEBREW POINT TSERE":
                res.append(7)
            elif self.vowel == "HEBREW POINT HOLAM":
                res.append(8)
            elif self.vowel == "HEBREW POINT HOLAM HASER FOR VAV":
                res.append(9)
            elif self.vowel == "HEBREW POINT HATAF SEGOL":
                res.append(10)
            elif self.vowel == "HEBREW POINT HATAF PATAH":
                res.append(11)
            elif self.vowel == "HEBREW POINT HATAF QAMATS":
                res.append(12)
            elif self.vowel == "HEBREW POINT SHEVA":
                res.append(13)

            else:
                raise DCharsError( context = "DCharacterHBO.sortingvalue",
                                   message = "unknown vowel ="+\
                                             str(self.vowel) )

            # daghesh_mapiq :
            if not self.daghesh_mapiq:
                res.append(0)
            else:
                res.append(1)

            # methegh :
            if not self.methegh:
                res.append(0)
            else:
                res.append(1)

            # raphe :
            if not self.raphe:
                res.append(0)
            else:
                res.append(1)

            # special point :
            if self.specialpoint is None:
                res.append(0)
            elif self.specialpoint == "HEBREW MARK UPPER DOT":
                res.append(1)
            elif self.specialpoint == "HEBREW MARK LOWER DOT":
                res.append(2)
            else:
                raise DCharsError( context = "DCharacterHBO.sortingvalue",
                                   message = "unknown value for special_point ="+\
                                             str(self.specialpoint) )

        else:
            raise DCharsError( context = "DCharacterHBO.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res
