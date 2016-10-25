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
    ❏DChars❏ : dchars/languages/bod/dcharacter.py
"""
from dchars.dcharacter import DCharacterMotherClass
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

from dchars.languages.bod.symbols import SYMB_CONSONANTS, \
                                         SYMB_SUBJOINED_CONSONANTS, \
                                         SYMB_FIXEDFORM_SUBJOINED_CONSONANTS, \
                                         SYMB_OTHER_SYMBOLS, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_VOWELS, \
                                         FAKE_A__SYMBOL, \
                                         SYMB_DIACRITICS, \
                                         SYMB_DIACRITICS__HALANTA, \
                                         SYMB_DIACRITICS__RNAM_BCAD

import copy
import itertools

################################################################################
class DCharacterBOD(DCharacterMotherClass):
    """
        class DCharacterBOD
    """

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DCharacterBOD.__eq__

                aliud   :       DCharacterBOD object
        """

        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.subj_consonants == aliud.subj_consonants) and \
               (self.punctuation == aliud.punctuation) and \
               (self.rnam_bcad == aliud.rnam_bcad) and \
               (self.halanta == aliud.halanta) and \
               (self.anusvara_candrabindu == aliud.anusvara_candrabindu) and \
               (self.vowel1 == aliud.vowel1) and \
               (self.vowel2 == aliud.vowel2)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 subj_consonants = None,
                 punctuation = False,
                 rnam_bcad = False,
                 halanta = False,
                 anusvara_candrabindu = None,
                 vowel1 = None,
                 vowel2 = None):
        """
                DCharacterBOD.__init__

                .. code-block:: none

                    unknown_char                    : bool
                    base_char                       : None or a string with the NAME of the
                                                      character, not the character itself.
                    subj_consonants                 : None or a list of the NAME of the characters,
                                                      not the characters themselves.
                    rnam_bcad                       : bool
                    punctuation                     : bool
                    halanta                         : bool
                    anusvara_candrabindu            : None, or a string
                                                      see symbol.SYMB_DIACRITICS__ANUSV_CANDR
                    vowel1                          : None, or a string
                    vowel2                            see symbol.SYMB_VOWELS
         """

        DCharacterMotherClass.__init__(self,
                                       dstring_object = None,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.subj_consonants = subj_consonants
        self.rnam_bcad = rnam_bcad
        self.halanta = halanta
        self.anusvara_candrabindu = anusvara_candrabindu
        self.vowel1 = vowel1
        self.vowel2 = vowel2

        self.dstring_object = dstring_object

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterBOD.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "subj_consonants="+repr(self.subj_consonants) + "; " + \
               "rnam_bcad="+repr(self.rnam_bcad) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "halanta="+repr(self.halanta) + "; " +\
               "anusvara_candrabindu="+repr(self.anusvara_candrabindu) + "; " + \
               "vowel1="+repr(self.vowel1) + "; " +\
               "vowel2="+repr(self.vowel2)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterBOD.clone
        """
        return DCharacterBOD( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              subj_consonants = self.subj_consonants,
                              punctuation = self.punctuation,
                              rnam_bcad = self.rnam_bcad,
                              halanta = self.halanta,
                              anusvara_candrabindu = self.anusvara_candrabindu,
                              vowel1 = self.vowel1,
                              vowel2 = self.vowel2 )

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterBOD.get_usefull_combinations

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
        base_characters  = ('K',
                            'KH',
                            'G',
                            'GH',
                            'NG',
                            'C',
                            'CH',
                            'J',
                            'NY',
                            'TT',
                            'TTH',
                            'DD',
                            'DDH',
                            'NN',
                            'T',
                            'TH',
                            'D',
                            'DH',
                            'N',
                            'P',
                            'PH',
                            'B',
                            'BH',
                            'M',
                            'TS',
                            'TSH',
                            'DZ',
                            'DZH',
                            'W',
                            'ZH',
                            'Z',
                            '-',
                            'Y',
                            'R',
                            'L',
                            'SH',
                            'SS',
                            'S',
                            'H',
                            'KSS',

                            'KK',
                            'RR',

                            'A',
                           )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters:

            self.__init__( dstring_object = self.dstring_object,
                           base_char = base_char,
                           subj_consonants = None,
                           rnam_bcad = False,
                           punctuation = False,
                           halanta = False,
                           anusvara_candrabindu = None,
                           vowel1 = None,
                           vowel2 = None )

            yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_chars
                                           base_characters,

                                           # vowel
                                           (      None,
                                                  'AA',
                                                  'I',
                                                  'II',
                                                  'U',
                                                  'UU',
                                                  'VOCALIC R',
                                                  'VOCALIC RR',
                                                  'VOCALIC L',
                                                  'VOCALIC LL',
                                                  'E',
                                                  'AI',
                                                  'O',
                                                  'AU',
                                           )))

        for base_char, vowel in combinations:

            self.__init__( dstring_object = self.dstring_object,
                           base_char = base_char,
                           subj_consonants = None,
                           rnam_bcad = False,
                           punctuation = False,
                           halanta = False,
                           anusvara_candrabindu = None,
                           vowel1 = vowel,
                           vowel2 = None )

            yield copy.copy(self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterBOD.init_from_transliteration

                src             : string
                prev_dchar      : DCharacterBOD object
                transliteration_method: string

                Return <self>.
        """
        self.reset()
        # Pylint can't know that <self> has a 'trans__init_from_transliteration' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'trans__init_from_transliteration' member"
        return DCharacterBOD.trans__init_from_transliteration[transliteration_method](dchar = self,
                                                                                      src = src)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterBOD.get_sourcestr_representation

                Return a string

                This function IS NOT THE REGULAR WAY to get the string representation
                of a DString object by sticking string representations of the
                different DCharacters. Use this fonction only to get the string
                representation of ONE DCharacter.
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
        # ok, the function will decompose <self> :
        #.......................................................................
        res = []

        if self.base_char is not None:

            if self.punctuation:
                # punctuation symbol :
                res.append( SYMB_PUNCTUATION.get_default_symbol(self.base_char) )

            else:
                if self.base_char in SYMB_OTHER_SYMBOLS:
                    # "other symbol" : not punctuation nor consonant :
                    res.append( SYMB_OTHER_SYMBOLS.get_default_symbol(self.base_char) )
                elif self.base_char in SYMB_CONSONANTS:
                    # normal consonant :
                    res.append( SYMB_CONSONANTS.get_default_symbol(self.base_char) )
                elif self.base_char in SYMB_FIXEDFORM_SUBJOINED_CONSONANTS:
                    # special, fixedform subjoined consonant :
                    res.append( SYMB_FIXEDFORM_SUBJOINED_CONSONANTS.get_default_symbol(
                        self.base_char) )

                # subj_consonants ?
                if self.subj_consonants is not None:
                    for subj_c in self.subj_consonants:
                        res.append( SYMB_SUBJOINED_CONSONANTS.get_default_symbol(subj_c) )

                # dependent vowel ?
                if self.vowel1 is not None:
                    res.append( SYMB_VOWELS.get_default_symbol(self.vowel1) )

                if self.vowel2 is not None:
                    res.append( SYMB_VOWELS.get_default_symbol(self.vowel2) )

                # halanta symbol ?
                if self.halanta:
                    res.append( SYMB_DIACRITICS__HALANTA )

                # anusvara/candrabindu symbol ?
                if self.anusvara_candrabindu is not None:
                    res.append( SYMB_DIACRITICS.get_default_symbol(self.anusvara_candrabindu) )

                # rnam bcad symbol ?
                if self.rnam_bcad:
                    res.append( SYMB_DIACRITICS__RNAM_BCAD )

        res = "".join(res)

        # we have to delete the fake symbol for 'a' since there's no symbol in Tibetan for
        # the vowel 'a'.
        res = res.replace(FAKE_A__SYMBOL, "")

        return res

    #///////////////////////////////////////////////////////////////////////////
    def is_identical_to(self, aliud):
        """
                DCharacterBOD.is_identical_to

                aliud   :       DCharacterBOD object

                Test every attribute of a DCharacterBOD object except .dstring_object
        """

        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.subj_consonants == aliud.subj_consonants) and \
               (self.punctuation == aliud.punctuation) and \
               (self.rnam_bcad == aliud.rnam_bcad) and \
               (self.halanta == aliud.halanta) and \
               (self.anusvara_candrabindu == aliud.anusvara_candrabindu) and \
               (self.vowel1 == aliud.vowel1) and \
               (self.vowel2 == aliud.vowel2)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterBOD.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.subj_consonants = None
        self.punctuation = False
        self.rnam_bcad = False
        self.halanta = False
        self.anusvara_candrabindu = None
        self.vowel1 = None
        self.vowel2 = None

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterBOD.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.subj_consonants = None
        self.rnam_bcad = False
        self.halanta = False
        self.anusvara_candrabindu = None
        self.vowel1 = None
        self.vowel2 = None
