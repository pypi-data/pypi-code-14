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
    ❏DChars❏ : dchars/languages/san/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError
from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

from dchars.languages.san.symbols import SYMB_CONSONANTS, \
                                         SYMB_OTHER_SYMBOLS, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_INDEPENDENT_VOWELS, \
                                         SYMB_DEPENDENT_VOWELS, \
                                         SYMB_DIACRITICS, \
                                         FAKE_A__SYMBOL

from dchars.languages.san.symbols import DEFAULTSYMB__VIRAMA, \
                                         DEFAULTSYMB__ANUDATTA, \
                                         DEFAULTSYMB__NUKTA

import unicodedata
import copy
import itertools

################################################################################
# known transliterations :
################################################################################
import dchars.languages.san.transliterations.itrans.itrans as trans_itrans
import dchars.languages.san.transliterations.iso15919.iso15919 as trans_iso15919

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
################################################################################
PRE_NORMALIZE_NFC = (
                # क़ (q)
                ( chr(0x0915) + chr(0x093C), chr(0x958)),

                # ख़ (ḵẖ)
                ( chr(0x0916) + chr(0x093C), chr(0x959)),

                # ग़ (ġ)
                ( chr(0x0917) + chr(0x093C), chr(0x95A)),

                # ज़ (z)
                ( chr(0x091C) + chr(0x093C), chr(0x95B)),

                # ड़ (ṛ)
                ( chr(0x0921) + chr(0x093C), chr(0x95C)),

                # ढ़ (ṛh)
                ( chr(0x0922) + chr(0x093C), chr(0x95D)),

                # फ़ (f)
                ( chr(0x092B) + chr(0x093C), chr(0x95E)),

                # य़ (ẏ)
                ( chr(0x092F) + chr(0x093C), chr(0x95F)),
               )

POST_NORMALIZE_NFC = (
                # NFC modifies the order of anudatta(0x0952), anusvara (0x0902) and virama (0x94D) :
                ( chr(0x094D) + chr(0x0952) + chr(0x0902),
                  chr(0x0902) + chr(0x0952) + chr(0x094D) ),

                # NFC modifies the order of anudatta(0x0952) and udatta(0x0951) :
                ( chr(0x0952) + chr(0x0951), chr(0x0951) + chr(0x0952) ),

                # NFC modifies the order of anudatta(0x0952)+anusvara(0x0902) :
                ( chr(0x0952) + chr(0x0902), chr(0x0902) + chr(0x0952) ),

    )

################################################################################
class DCharacterSAN(DCharacterMotherClass):
    """
        class DCharacterSAN

        DO NOT CREATE A DStringSAN object directly but use instead the
        dchars.py::new_dstring function.
    """

    # transliteration's functions :
    trans__get_transliteration = {
          "itrans" : trans_itrans.dchar__get_translit_str,
          "iso15919" : trans_iso15919.dchar__get_translit_str,
          }

    trans__init_from_transliteration = {
          "itrans" : trans_itrans.dchar__init_from_translit_str,
          "iso15919" : trans_iso15919.dchar__init_from_translit_str,
          }

    # sorting value for the visarga character :
    sortingvalue_for_visarga = [0, 100, 0, 1, 0, 0, 0]

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DCharacterSAN.__eq__

                aliud   :       DCharacterSAN object
        """

        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.accent == aliud.accent) and \
               (self.nukta == aliud.nukta) and \
               (self.anusvara_candrabindu == aliud.anusvara_candrabindu) and \
               (self.virama == aliud.virama) and \
               (self.anudatta == aliud.anudatta) and \
               (self.is_an_independent_vowel == aliud.is_an_independent_vowel) and \
               (self.dependentvowel == aliud.dependentvowel)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 punctuation = False,
                 accent = None,
                 nukta = False,
                 anusvara_candrabindu = None,
                 virama = False,
                 anudatta = False,
                 is_an_independent_vowel = False,
                 dependentvowel = None):
        """
                DCharacterSAN.__init__

                .. code-block:: none

                    unknown_char                    : bool
                    base_char                       : None or a string with the NAME of the
                                                      character not the character itself.
                    accent                          : None or a string
                                                      ("DEVANAGARI STRESS SIGN UDATTA",
                                                       "DEVANAGARI GRAVE ACCENT"
                                                       "DEVANAGARI ACUTE ACCENT"
                                                      )
                                                      but not "DEVANAGARI STRESS SIGN ANUDATTA",
                                                      see anudatta below.
                    punctuation                     : bool
                    nukta                           : bool
                    anusvara_candrabindu            : None, or a string
                                                      ("DEVANAGARI SIGN ANUSVARA",
                                                       "DEVANAGARI SIGN INVERTED CANDRABINDU",
                                                       'DEVANAGARI SIGN CANDRABINDU'
                                                      )
                    virama                          : bool
                    anudatta                        : bool
                    is_an_independent_vowel         : bool
                    dependentvowel                  : None, or a string
                                                      see symbol.SYMB_DEPENDENT_VOWELS
         """

        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.accent = accent
        self.nukta = nukta
        self.anusvara_candrabindu = anusvara_candrabindu
        self.virama = virama
        self.anudatta = anudatta
        self.is_an_independent_vowel = is_an_independent_vowel
        self.dependentvowel = dependentvowel

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterSAN.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "accent="+repr(self.accent) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "nukta="+repr(self.nukta) + "; " + \
               "anusvara_candrabindu="+repr(self.anusvara_candrabindu) + "; " +\
               "virama="+repr(self.virama) + "; " +\
               "anudatta="+repr(self.anudatta) + "; " +\
               "is_an_independent_vowel="+repr(self.is_an_independent_vowel) + "; " +\
               "dependentvowel="+repr(self.dependentvowel)

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterSAN.clone
        """
        return DCharacterSAN( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              punctuation = self.punctuation,
                              accent = self.accent,
                              nukta = self.nukta,
                              anusvara_candrabindu = self.anusvara_candrabindu,
                              virama = self.virama,
                              anudatta = self.anudatta,
                              is_an_independent_vowel = self.is_an_independent_vowel,
                              dependentvowel = self.dependentvowel )

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringCharacterSAN.get_usefull_combinations

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
        base_characters__vowels = (
                                      'SHORT A',
                                      'A',
                                      'AA',
                                      'I',
                                      'II',
                                      'U',
                                      'UU',
                                      'VOCALIC R',
                                      'VOCALIC RR',
                                      'VOCALIC L',
                                      'VOCALIC LL',
                                      'SHORT E',
                                      'E',
                                      'SHORT O',
                                      'O',
                                      'AI',
                                      'AU',
                                    )

        base_characters  = ( 'KA',
                             'KHA',
                             'GA',
                             'GHA',
                             'NGA',
                             'CA',
                             'CHA',
                             'JA',
                             'JHA',
                             'NYA',
                             'TTA',
                             'TTHA',
                             'DDA',
                             'DDHA',
                             'NNA',
                             'TA',
                             'THA',
                             'DA',
                             'DHA',
                             'NA',
                             'PA',
                             'PHA',
                             'BA',
                             'BHA',
                             'MA',
                             'YA',
                             'RA',
                             'LA',
                             'LLA',
                             'VA',
                             'SHA',
                             'SSA',
                             'SA',
                             'HA',
                             'DEVANAGARI SIGN VISARGA', )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters__vowels:

            self.__init__( dstring_object = self.dstring_object,
                           base_char = base_char,
                           accent = None,
                           punctuation = False,
                           nukta = False,
                           anusvara_candrabindu = None,
                           virama = False,
                           anudatta = False,
                           is_an_independent_vowel = True,
                           dependentvowel = None,
                         )

            yield copy.copy(self)

        for base_char in base_characters:

            self.__init__( dstring_object = self.dstring_object,
                           base_char = base_char,
                           accent = None,
                           punctuation = False,
                           nukta = False,
                           anusvara_candrabindu = None,
                           virama = False,
                           anudatta = False,
                           is_an_independent_vowel = False,
                           dependentvowel = None,
                         )

            yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_chars
                                           base_characters,

                                           # anusvara_candrabindu
                                           #(None,
                                           # "DEVANAGARI SIGN ANUSVARA",
                                           # "DEVANAGARI SIGN INVERTED CANDRABINDU",
                                           # 'DEVANAGARI SIGN CANDRABINDU',
                                           # ),

                                           # virama
                                           #( False, True ),

                                           # anudatta
                                           #( False, True ),

                                           # dependentvowel
                                           (      None,
                                                  'AA',
                                                  'I',
                                                  'II',
                                                  'U',
                                                  'UU',
                                                  'VOCALIC R',
                                                  'VOCALIC RR',
                                                  #'CANDRA E',
                                                  #'SHORT E',
                                                  'E',
                                                  'AI',
                                                  #'CANDRA O',
                                                  #'SHORT O',
                                                  'O',
                                                  'AU',
                                                  'VOCALIC L',
                                                  'VOCALIC LL',
                                           ),

                                           ))

        for base_char, dependentvowel in combinations:

            add_this_char = True

            if base_char == 'DEVANAGARI SIGN VISARGA':
                if dependentvowel is not None:
                    add_this_char = False

            if add_this_char:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               accent = None,
                               punctuation = None,
                               nukta = False,
                               anusvara_candrabindu = None,
                               virama = False,
                               anudatta = False,
                               is_an_independent_vowel = False,
                               dependentvowel = dependentvowel,
                              )

            yield copy.copy(self)

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self,
                            prev_dchar,
                            transliteration_method):
        """
                DCharacterSAN.get_transliteration

                prev_dchar              :       None or a DCharacterSAN object
                transliteration_method  :       str
        """
        return DCharacterSAN.trans__get_transliteration[transliteration_method](
            dstring_object = self.dstring_object,
            prev_dchar=prev_dchar,
            dchar=self)

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterSAN.get_sourcestr_representation

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
                res.append( SYMB_PUNCTUATION.get_default_symbol(self.base_char) )

            else:
                if self.base_char in SYMB_OTHER_SYMBOLS:
                    # "other symbol" : not punctuation nor consonant nor
                    # independent vowel.
                    res.append( SYMB_OTHER_SYMBOLS.get_default_symbol(self.base_char) )
                elif not self.is_an_independent_vowel:
                    # consonant :
                    res.append( SYMB_CONSONANTS.get_default_symbol(self.base_char) )
                else:
                    # independent vowel :
                    res.append( SYMB_INDEPENDENT_VOWELS.get_default_symbol(self.base_char) )

                # dependent vowel ?
                if self.dependentvowel is not None:
                    # yes :
                    res.append( SYMB_DEPENDENT_VOWELS.get_default_symbol(self.dependentvowel) )

        if self.nukta:
            res.append( DEFAULTSYMB__NUKTA )

        if self.accent is not None:
            res.append( SYMB_DIACRITICS.get_default_symbol(self.accent) )

        if self.virama:
            res.append( DEFAULTSYMB__VIRAMA )

        if self.anudatta:
            res.append( DEFAULTSYMB__ANUDATTA )

        if self.anusvara_candrabindu is not None:
            res.append( SYMB_DIACRITICS.get_default_symbol(self.anusvara_candrabindu) )

        res = "".join(res)

        # we have to delete the fake symbol for 'a' since there's no symbol in devanagari for
        # the vowel 'a'.
        res = res.replace(FAKE_A__SYMBOL, "")

        # (1/3) composition with PRE_NORMALIZE_NFC :
        for src, dest in PRE_NORMALIZE_NFC:
            res = res.replace(src, dest)
        # (2/3) composition with unicodedata.normalize :
        res = unicodedata.normalize('NFC', res)
        # (3/3) composition with POST_NORMALIZE_NFC :
        for src, dest in POST_NORMALIZE_NFC:
            res = res.replace(src, dest)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterSAN.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.accent = None
        self.nukta = False
        self.anusvara_candrabindu = None
        self.virama = False
        self.anudatta = False
        self.is_an_independent_vowel = False
        self.dependentvowel = None

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterSAN.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.accent = None
        self.nukta = False
        self.anusvara_candrabindu = None
        self.virama = False
        self.anudatta = False

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self,
                                  src,
                                  transliteration_method):
        """
                DCharacterSAN.init_from_transliteration

                src                     : string
                transliteration_method  :       str

                Return <self>.
        """
        self.reset()
        return DCharacterSAN.trans__init_from_transliteration[transliteration_method](dchar = self,
                                                                                      src = src)
    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DCharacterSAN.sortingvalue

                Return an SortingValue object

                Output : a list of number :
                  [(un)known_char,
                   base_char,
                   nukta,
                   virama/dependent vowel,
                   anusvara/candrabindu,
                   anudatta,
                   accent]

                !!! BEWARE : the number #4 (anusvara/candrabindu) will be equal to 999 if
                !!! this character is followed by a visarga : see DStringSAN.sortingvalue()

                !!! BEWARE : if you modify this function, don't forget to change the
                !!! attribute DCharacterSAN.sortingvalue_for_visarga
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
            if self.base_char == 'SHORT A':
                res.append(0)
            elif self.base_char == 'A':
                res.append(1)
            elif self.base_char == 'AA':
                res.append(2)
            elif self.base_char == 'I':
                res.append(3)
            elif self.base_char == 'II':
                res.append(4)
            elif self.base_char == 'U':
                res.append(5)
            elif self.base_char == 'UU':
                res.append(6)
            elif self.base_char == 'VOCALIC R':
                res.append(7)
            elif self.base_char == 'VOCALIC RR':
                res.append(8)
            elif self.base_char == 'VOCALIC L':
                res.append(9)
            elif self.base_char == 'VOCALIC LL':
                res.append(10)
            elif self.base_char == 'SHORT E':
                res.append(11)
            elif self.base_char == 'E':
                res.append(12)
            elif self.base_char == 'AI':
                res.append(13)
            elif self.base_char == 'SHORT O':
                res.append(14)
            elif self.base_char == 'O':
                res.append(15)
            elif self.base_char == 'AU':
                res.append(16)
            elif self.base_char == 'DEVANAGARI SIGN VISARGA':
                res.append(100)
            elif self.base_char == 'KA':
                res.append(101)
            elif self.base_char == 'KHA':
                res.append(102)
            elif self.base_char == 'GA':
                res.append(103)
            elif self.base_char == 'GHA':
                res.append(104)
            elif self.base_char == 'NGA':
                res.append(105)
            elif self.base_char == 'CA':
                res.append(106)
            elif self.base_char == 'CHA':
                res.append(107)
            elif self.base_char == 'JA':
                res.append(108)
            elif self.base_char == 'JHA':
                res.append(109)
            elif self.base_char == 'NYA':
                res.append(110)
            elif self.base_char == 'TTA':
                res.append(111)
            elif self.base_char == 'TTHA':
                res.append(112)
            elif self.base_char == 'DDA':
                res.append(113)
            elif self.base_char == 'DDHA':
                res.append(114)
            elif self.base_char == 'NNA':
                res.append(115)
            elif self.base_char == 'TA':
                res.append(116)
            elif self.base_char == 'THA':
                res.append(117)
            elif self.base_char == 'DA':
                res.append(118)
            elif self.base_char == 'DHA':
                res.append(119)
            elif self.base_char == 'NA':
                res.append(120)
            elif self.base_char == 'PA':
                res.append(121)
            elif self.base_char == 'PHA':
                res.append(122)
            elif self.base_char == 'BA':
                res.append(123)
            elif self.base_char == 'BHA':
                res.append(124)
            elif self.base_char == 'MA':
                res.append(125)
            elif self.base_char == 'YA':
                res.append(126)
            elif self.base_char == 'RA':
                res.append(127)
            elif self.base_char == 'LA':
                res.append(128)
            elif self.base_char == 'LLA':
                res.append(129)
            elif self.base_char == 'VA':
                res.append(130)
            elif self.base_char == 'SHA':
                res.append(131)
            elif self.base_char == 'SSA':
                res.append(132)
            elif self.base_char == 'SA':
                res.append(133)
            elif self.base_char == 'HA':
                res.append(134)
            else:
                # E.g. "1", ...
                base_char_num = 0
                for index_char, char in enumerate(self.base_char):
                    base_char_num += ord(char) << index_char
                res.append( 1000 + base_char_num )

            # nukta :
            if not self.nukta:
                res.append( 0 )
            else:
                res.append( 1 )

            # dependent vowel :
            # virama :
            if self.virama:
                res.append( 0 )
            else:
                if self.dependentvowel is None:
                    res.append(1)
                elif self.dependentvowel == "A":
                    res.append(2)
                elif self.dependentvowel == "AA":
                    res.append(3)
                elif self.dependentvowel == "I":
                    res.append(4)
                elif self.dependentvowel == "II":
                    res.append(5)
                elif self.dependentvowel == "U":
                    res.append(6)
                elif self.dependentvowel == "UU":
                    res.append(7)
                elif self.dependentvowel == "VOCALIC R":
                    res.append(8)
                elif self.dependentvowel == "VOCALIC RR":
                    res.append(9)
                elif self.dependentvowel == "VOCALIC L":
                    res.append(10)
                elif self.dependentvowel == "VOCALIC LL":
                    res.append(11)
                elif self.dependentvowel == "CANDRA E":
                    res.append(12)
                elif self.dependentvowel == "SHORT E":
                    res.append(13)
                elif self.dependentvowel == "E":
                    res.append(14)
                elif self.dependentvowel == "AI":
                    res.append(15)
                elif self.dependentvowel == "CANDRA O":
                    res.append(16)
                elif self.dependentvowel == "SHORT O":
                    res.append(17)
                elif self.dependentvowel == "O":
                    res.append(18)
                elif self.dependentvowel == "AU":
                    res.append(19)
                else:
                    raise DCharsError( context = "DCharacterSAN.sortingvalue",
                                       message = "unknown value for dependentvowel ="+\
                                                 str(self.dependentvowel) )
            # anusvara / candrabindu :
            if self.anusvara_candrabindu is None:
                res.append( 0 )
            elif self.anusvara_candrabindu == "DEVANAGARI SIGN ANUSVARA":
                res.append( 1 )
            elif self.anusvara_candrabindu == "DEVANAGARI SIGN CANDRABINDU":
                res.append( 2 )
            elif self.anusvara_candrabindu == "DEVANAGARI SIGN INVERTED CANDRABINDU":
                res.append( 3 )
            else:
                raise DCharsError( context = "DCharacterSAN.sortingvalue",
                                   message = "unknown value for anusvara_candrabindu ="+\
                                             str(self.anusvara_candrabindu) )
            # anudatta :
            if not self.anudatta:
                res.append( 0 )
            else:
                res.append( 1 )

            # accent :
            if self.accent is None:
                res.append( 0 )
            elif self.accent == "DEVANAGARI STRESS SIGN UDATTA":
                res.append( 1 )
            elif self.accent == "DEVANAGARI GRAVE ACCENT":
                res.append( 2 )
            elif self.accent == "DEVANAGARI ACUTE ACCENT":
                res.append( 3 )
            else:
                raise DCharsError( context = "DCharacterSAN.sortingvalue",
                                   message = "unknown value for accent ="+\
                                             str(self.accent) )

        else:
            raise DCharsError( context = "DCharacterSAN.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res
