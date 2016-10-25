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
    ❏DChars❏ : dchars/languages/grc/dcharacter.py
"""

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError

from dchars.utilities.sortingvalue import SortingValue
from dchars.dcharacter import DCharacterMotherClass
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
from dchars.languages.grc.symbols import SYMB_LOWER_CASE, \
                                         SYMB_UPPER_CASE, \
                                         SYMB_OTHER_SYMBOLS, \
                                         DEFAULTSYMB__PNEUMAPSILON, \
                                         DEFAULTSYMB__PNEUMADASU, \
                                         DEFAULTSYMB__TONOSOXEIA, \
                                         DEFAULTSYMB__TONOSBAREIA, \
                                         DEFAULTSYMB__TONOSPERISPOMENE, \
                                         DEFAULTSYMB__MEKOSBRAXU, \
                                         DEFAULTSYMB__MEKOSMAKRON, \
                                         DEFAULTSYMB__HUPOGEGRAMMENE, \
                                         DEFAULTSYMB__DIALYTIKA
import unicodedata
import copy
import itertools

# known transliterations :
import dchars.languages.grc.transliterations.basic.basic as basictrans
import dchars.languages.grc.transliterations.betacode.betacode as betacodetrans
import dchars.languages.grc.transliterations.perseus.perseus as perseustrans
import dchars.languages.grc.transliterations.gutenberg.gutenberg as gutenbergtrans

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
# the problem : NFD( 0x1F71 ) = 0x03B1 + 0x0301
#               NFC( 0x03B1 + 0x0301 ) = 0x03AC (and not 0x1F71 as expected)
#               ... so we have to help NFC : 0x03AC will become 0x1F71
#
################################################################################
COMPLETE_NORMALIZE_NFC = (
                # Ά -> Ά
                ( chr(0x0386), chr(0x1FBB) ),
                # Έ -> Έ
                ( chr(0x0388), chr(0x1FC9) ),
                # Ή -> Ή
                ( chr(0x0389), chr(0x1FCB) ),
                # Ί -> Ί
                ( chr(0x038A), chr(0x1FDB) ),
                # Ό -> Ό
                ( chr(0x038C), chr(0x1FF9) ),
                # Ύ -> Ύ
                ( chr(0x038E), chr(0x1FEB) ),
                # Ώ -> Ώ
                ( chr(0x038F), chr(0x1FFB) ),
                # ΐ -> ΐ
                ( chr(0x0390), chr(0x1FD3) ),
                # ά -> ά
                ( chr(0x03AC), chr(0x1F71) ),
                # έ -> έ
                ( chr(0x03AD), chr(0x1F73) ),
                # ί -> ί
                ( chr(0x03AF), chr(0x1F77) ),
                # ΰ -> ΰ
                ( chr(0x03B0), chr(0x1FE3) ),
                # ό -> ό
                ( chr(0x03CC), chr(0x1F79) ),
                # ύ -> ύ
                ( chr(0x03CD), chr(0x1F7B) ),
                # ώ -> ώ
                ( chr(0x03CE), chr(0x1F7D) ),

               )

################################################################################
# we complete the function unicodedata.normalize('NFC', ...)
#
# the problem : NFD( 0x1F71 ) = 0x03B1 + 0x0301
#               NFC( 0x03B1 + 0x0301 ) = 0x03AC (and not 0x1F71 as expected)
#               ... so we have to help NFC : 0x03AC will become 0x1F71
#
################################################################################
COMPLETE_NORMALIZE_NFC = (
                # Ά -> Ά
                ( chr(0x0386), chr(0x1FBB) ),
                # Έ -> Έ
                ( chr(0x0388), chr(0x1FC9) ),
                # Ή -> Ή
                ( chr(0x0389), chr(0x1FCB) ),
                # Ί -> Ί
                ( chr(0x038A), chr(0x1FDB) ),
                # Ό -> Ό
                ( chr(0x038C), chr(0x1FF9) ),
                # Ύ -> Ύ
                ( chr(0x038E), chr(0x1FEB) ),
                # Ώ -> Ώ
                ( chr(0x038F), chr(0x1FFB) ),
                # ΐ -> ΐ
                ( chr(0x0390), chr(0x1FD3) ),
                # ά -> ά
                ( chr(0x03AC), chr(0x1F71) ),
                # έ -> έ
                ( chr(0x03AD), chr(0x1F73) ),
                # ί -> ί
                ( chr(0x03AF), chr(0x1F77) ),
                # ΰ -> ΰ
                ( chr(0x03B0), chr(0x1FE3) ),
                # ό -> ό
                ( chr(0x03CC), chr(0x1F79) ),
                # ύ -> ύ
                ( chr(0x03CD), chr(0x1F7B) ),
                # ώ -> ώ
                ( chr(0x03CE), chr(0x1F7D) ),

                # ῦ̈ -> ῧ
                ( chr(0x1FE6) + chr(0x0308), chr(0x1FE7) ),
               )

################################################################################
class DCharacterGRC(DCharacterMotherClass):
    """
        class DCharacterGRC
    """

    # transliteration's functions :
    trans__get_transliteration = {
          "basic" : basictrans.dchar__get_translit_str,
          "betacode": betacodetrans.dchar__get_translit_str,
          "perseus" : perseustrans.dchar__get_translit_str,
          "gutenberg" : gutenbergtrans.dchar__get_translit_str,
          }

    trans__init_from_transliteration = {
          "basic" : basictrans.dchar__init_from_translit_str,
          "betacode": betacodetrans.dchar__init_from_translit_str,
          "perseus" : perseustrans.dchar__init_from_translit_str,
          "gutenberg" : None,
          }

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DCharacterGRC.__eq__

                aliud   :       DCharacterGRC object
        """

        return (self.unknown_char == aliud.unknown_char) and \
               (self.base_char == aliud.base_char) and \
               (self.punctuation == aliud.punctuation) and \
               (self.capital_letter == aliud.capital_letter) and \
               (self.contextual_form == aliud.contextual_form) and \
               (self.tonos == aliud.tonos) and \
               (self.pneuma == aliud.pneuma) and \
               (self.hypogegrammene == aliud.hypogegrammene) and \
               (self.dialutika == aliud.dialutika) and \
               (self.mekos == aliud.mekos)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char = False,
                 base_char = None,
                 contextual_form = None,
                 punctuation = False,
                 capital_letter = False,
                 tonos = None,
                 pneuma = None,
                 hypogegrammene = False,
                 dialutika = False,
                 mekos=None):
        """
                DCharacterGRC.__init__

                .. code-block:: none

                    unknown_char                    : bool
                    base_char                       : None or a string
                    contextual_form                 : None or a string
                                                      ("initial+medium+final"+"initial",
                                                       "initial+medium", "final", "medium+final")
                    punctuation                     : True, False
                    capital_letter                  : True, False

                    mekos(μῆκος)                    : None, "βραχύ", "μακρόν"
                    tonos(τόνος)                    : None, "ὀξεῖα", "βαρεῖα", "περισπωμένη"
                    pneuma(πνεῦμα)                  : None, "ψιλὸν", "δασὺ"
                    hypogegrammene(ὑπογεγραμμένη)   : True, False
                    dialutika(διαλυτικά)            : True, False
        """
        DCharacterMotherClass.__init__(self,
                                       dstring_object = dstring_object,
                                       unknown_char = unknown_char,
                                       base_char = base_char,
                                       punctuation = punctuation)

        self.dstring_object = dstring_object
        self.contextual_form = contextual_form
        self.capital_letter = capital_letter
        self.tonos = tonos
        self.pneuma = pneuma
        self.hypogegrammene = hypogegrammene
        self.dialutika = dialutika
        self.mekos = mekos

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DCharacterGRC.__repr__
        """

        return "unknown_char="+repr(self.unknown_char) + "; " + \
               "base_char="+repr(self.base_char) + "; " + \
               "contextual_form="+repr(self.contextual_form) + "; " + \
               "punctuation="+repr(self.punctuation) + "; " + \
               "capital_letter="+repr(self.capital_letter) + "; " + \
               "tonos="+repr(self.tonos) + "; " + \
               "pneuma="+repr(self.pneuma) + "; " + \
               "hypogegrammene="+repr(self.hypogegrammene) + "; " + \
               "dialutika="+repr(self.dialutika) + "; " + \
               "mekos="+repr(self.mekos)

    #///////////////////////////////////////////////////////////////////////////
    def clearAccentuation(self):
        """
                DCharacterGRC.clearAccentuation
        """
        self.tonos = None

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterGRC.clone
        """
        return DCharacterGRC( dstring_object = self.dstring_object,
                              unknown_char = self.unknown_char,
                              base_char = self.base_char,
                              contextual_form = self.contextual_form,
                              punctuation = self.punctuation,
                              capital_letter = self.capital_letter,
                              tonos = self.tonos,
                              pneuma = self.pneuma,
                              hypogegrammene = self.hypogegrammene,
                              dialutika = self.dialutika,
                              mekos = self.mekos )

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self, ignore_makron = False):
        """
                DCharacterGRC.get_sourcestr_representation

                PARAMETER :
                o  (bool) ignore_makron : if True, no makron will be added on the
                                          characters

                RETURN VALUE : a (str) string.
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
            elif self.base_char in SYMB_OTHER_SYMBOLS:
                # other symbol :
                res.append( self.base_char )
            elif not self.capital_letter:
                # lower case :

                base_char = self.base_char
                if base_char =='β' and \
                   not self.capital_letter and \
                   self.contextual_form == "medium+final":
                    base_char = "ϐ"
                elif base_char =='σ' and \
                     not self.capital_letter and \
                     self.contextual_form == "final":
                    base_char = "ς"

                res.append( SYMB_LOWER_CASE.get_default_symbol(base_char) )
            else:
                # upper case :
                res.append( SYMB_UPPER_CASE.get_default_symbol(self.base_char) )

        # CAVEAT : order matters !
        # e.g. : pneuma then tonos, NOT tonos then pneuma
        # unicodedata.normalize('NFC', chr(0x03BF)+chr(0x0314)+chr(0x301) ) = chr(0x1F45) (ok)
        # unicodedata.normalize('NFC', chr(0x03BF)+chr(0x0301)+chr(0x314) ) =
        #                                               chr(0x03CC) + chr(0x314) [NOT OK !]

        if self.pneuma == 'ψιλὸν':
            res.append( DEFAULTSYMB__PNEUMAPSILON )
        elif self.pneuma == 'δασὺ':
            res.append( DEFAULTSYMB__PNEUMADASU )

        if self.tonos == 'ὀξεῖα':
            res.append( DEFAULTSYMB__TONOSOXEIA )
        elif self.tonos == 'βαρεῖα':
            res.append( DEFAULTSYMB__TONOSBAREIA )
        elif self.tonos == 'περισπωμένη':
            res.append( DEFAULTSYMB__TONOSPERISPOMENE )

        if self.mekos == 'βραχύ':
            res.append( DEFAULTSYMB__MEKOSBRAXU )
        elif self.mekos == 'μακρόν' and not ignore_makron:
            res.append( DEFAULTSYMB__MEKOSMAKRON )

        if self.hypogegrammene == True:
            res.append( DEFAULTSYMB__HUPOGEGRAMMENE )

        if self.dialutika == True:
            res.append( DEFAULTSYMB__DIALYTIKA )

        res = "".join(res)

        # (1/2) composition with unicodedata.normalize :
        res = unicodedata.normalize('NFC', res)
        # (2/2) composition with COMPLETE_NORMALIZE_NFC :
        for before, after in COMPLETE_NORMALIZE_NFC:
            res = res.replace(before, after)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self, transliteration_method, options):
        """
                DCharacterGRC.get_transliteration

                method  : string
        """
        return DCharacterGRC.trans__get_transliteration[transliteration_method](
            dstring_object = self.dstring_object,
            dchar = self,
            options = options)

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DCharacterGRC.get_usefull_combinations

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
        base_characters  = ( 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι',
                             'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ',
                             'τ', 'υ', 'φ', 'χ', 'ψ', 'ω',
                             'ϝ', 'ϗ', 'ϡ', 'ϛ', 'ϙ', )

        #-----------------------------------------------------------------------
        # (1/2) simple characters
        #-----------------------------------------------------------------------
        for base_char in base_characters:
            for capital_letter in (False, True):
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               contextual_form = "initial+medium+final",
                               punctuation = False,
                               capital_letter = capital_letter,
                               tonos = None,
                               pneuma = None,
                               hypogegrammene = False,
                               dialutika = False,
                               mekos = None)

                yield copy.copy(self)

        #-----------------------------------------------------------------------
        # (2/2) complex characters
        #-----------------------------------------------------------------------
        combinations = (itertools.product(
                                           # base_chars
                                           base_characters,

                                           # contextual_form
                                           ("initial", "medium", "final",
                                            "initial+medium", "medium+final",
                                            "initial+medium+final"),

                                           # capital_letter
                                           (False, True),

                                           # tonos
                                           ( None, "ὀξεῖα", "βαρεῖα", "περισπωμένη" ),

                                           # pneuma
                                           ( None, "ψιλὸν",  "δασὺ" ),

                                           # hypogegrammene
                                           (False, True),

                                           # dialutika
                                           (False, True),

                                           # mekos
                                           ( None, "βραχύ", "μακρόν" ),
                                           ))

        for base_char, contextual_form, capital_letter, \
            tonos, pneuma, hypogegrammene, dialutika, mekos in combinations:

            add_this_dchar = True

            if base_char == 'ρ':
                if contextual_form != "initial+medium+final" or \
                   tonos is not None or \
                   hypogegrammene == True or \
                   dialutika == True or \
                   mekos is not None:

                    add_this_dchar = False

            elif base_char in ('β', 'σ'):
                if tonos is not None or \
                   pneuma is not None or \
                   hypogegrammene == True or \
                   dialutika == True or \
                   mekos is not None:

                    add_this_dchar = False

            elif base_char in ('α', 'η', 'ω'):
                if contextual_form != "initial+medium+final" or \
                   dialutika == True or \
                   mekos is not None:

                    add_this_dchar = False

            elif base_char in ('ε', 'ο'):
                if contextual_form != "initial+medium+final" or \
                   hypogegrammene == True or \
                   tonos == "περισπωμένη" or \
                   hypogegrammene == True or \
                   dialutika == True or \
                   mekos is not None:

                    add_this_dchar = False

            elif base_char in ('ι', 'υ'):
                if contextual_form != "initial+medium+final" or \
                   hypogegrammene == True or \
                   mekos is not None:

                    add_this_dchar = False

            else:
                if contextual_form != "initial+medium+final" or \
                   tonos is not None or \
                   pneuma is not None or \
                   hypogegrammene == True or \
                   dialutika == True or \
                   mekos is not None:

                    add_this_dchar = False

            if add_this_dchar:
                self.__init__( dstring_object = self.dstring_object,
                               base_char = base_char,
                               contextual_form = contextual_form,
                               punctuation = False,
                               capital_letter = capital_letter,
                               tonos = tonos,
                               pneuma = pneuma,
                               hypogegrammene = hypogegrammene,
                               dialutika = dialutika,
                               mekos=mekos)

                yield copy.copy(self)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, src, transliteration_method):
        """
                DCharacterGRC.init_from_transliteration

                src     :       string
                transliteration_method  : string

                Return <self>.
        """
        self.reset()
        return DCharacterGRC.trans__init_from_transliteration[transliteration_method](dchar = self,
                                                                                      src = src)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterGRC.reset
        """
        self.unknown_char = True
        self.base_char = None
        self.punctuation = False
        self.contextual_form = None
        self.capital_letter = False
        self.tonos = None
        self.pneuma = None
        self.hypogegrammene = False
        self.dialutika = False
        self.mekos = None

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterGRC.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                Function used by the Logotheras project.
        """
        self.contextual_form = False
        self.capital_letter = True
        self.tonos = None
        self.pneuma = None
        self.hypogegrammene = False
        self.dialutika = False
        self.mekos = None
        
    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DCharacterGRC.sortingvalue

                Return a SortingValue object

                NB : this function has almost no interest; you must use DStringGRC.sortingvalue()
                     to compare two strings. Use this function if you just want to compare
                     two characters.
        """
        res = SortingValue()

        if self.dstring_object.options["sorting method"] == "default":

            if self.unknown_char:
                # unknown char :
                res.append(1)

                # Some base_char may contain more than one character, like "β2".
                base_char_num = 0
                for index_char, char in enumerate(self.base_char):
                    base_char_num += ord(char) << index_char
                res.append( base_char_num )

                return res

            # known char :
            res.append(0)

            # base_char :
            #
            # Some base_char may contain more than one character, like "β2".
            #
            base_char_num = 0
            for index_char, char in enumerate(self.base_char):
                base_char_num += ord(char) << index_char
            res.append( base_char_num )

            # pneuma :
            if self.pneuma is None:
                res.append(0)
            elif self.pneuma == "ψιλὸν":
                res.append(1)
            elif self.pneuma == "δασὺ":
                res.append(2)
            else:
                raise DCharsError( context = "DCharacterGRC.sortingvalue",
                                   message = "unknown value for pneuma ="+\
                                             str(self.pneuma) )

            # tonos :
            if self.tonos is None:
                res.append(0)
            elif self.tonos == "ὀξεῖα":
                res.append(1)
            elif self.tonos == "βαρεῖα":
                res.append(2)
            elif self.tonos == "περισπωμένη":
                res.append(3)
            else:
                raise DCharsError( context = "DCharacterGRC.sortingvalue",
                                   message = "unknown value for tonos ="+\
                                             str(self.tonos) )

            # hypogegrammene :
            if not self.hypogegrammene:
                res.append(0)
            else:
                res.append(1)

            # mekos :
            if self.mekos is None:
                res.append( 0 )
            elif self.mekos == "βραχύ":
                res.append( 0 )
            elif self.mekos == "μακρόν":
                res.append( 1 )
            else:
                raise DCharsError( context = "DCharacterGRC.sortingvalue",
                                   message = "unknown value for mekos ="+\
                                             str(self.mekos) )

        else:
            raise DCharsError( context = "DCharacterGRC.sortingvalue",
                               message = "unknown sorting method ="+\
                                         str(self.dstring_object.options["sorting method"]) )

        return res
