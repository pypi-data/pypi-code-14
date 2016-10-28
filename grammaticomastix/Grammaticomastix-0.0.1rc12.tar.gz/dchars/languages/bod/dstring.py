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
    ❏DChars❏ : dchars/languages/bod/dstring.py
"""

import pickle
import os.path

# problem with Pylint :
# pylint: disable=E0611
# many errors like "No name 'extensions' in module 'dchars'"
from dchars.errors.errors import DCharsError
from dchars.languages.bod.dcharacter import DCharacterBOD
from dchars.languages.bod.symbols import TSHEG_SYMBOL, SPACE_SYMBOL
from dchars.dstring import DStringMotherClass

import dchars.languages.bod.buffer as bod_buffer
import dchars.languages.bod.transliterations.ewts.ewts_buffer as ewts_buffer
import dchars.languages.bod.internalstructure as istruct

################################################################################
# known transliterations :
################################################################################
import dchars.languages.bod.transliterations.ewts.ewts as trans_ewts
import dchars.languages.bod.transliterations.ewts.ucombinations as trans_ewts_ucombinations

import dchars.languages.bod.transliterations.bodsan.bodsan as trans_bodsan

################################################################################
# substitutions :
################################################################################
INIT_FROM_STR__SUBSTITUTIONS = (

                # ཀྵ -> ཀྵ
                ( chr(0x0F40) + chr(0x0FB5), chr(0x0F69) ),
                # གྷ -> གྷ
                ( chr(0x0F42) + chr(0x0FB7), chr(0x0F43) ),
                # ཌྷ -> ཌྷ
                ( chr(0x0F4C) + chr(0x0FB7), chr(0x0F4D) ),
                # དྷ -> དྷ
                ( chr(0x0F51) + chr(0x0FB7), chr(0x0F52) ),
                # བྷ -> བྷ
                ( chr(0x0F56) + chr(0x0FB7), chr(0x0F57) ),
                # ཛྷ -> ཛྷ
                ( chr(0x0F5B) + chr(0x0FB7), chr(0x0F5C) ),
                #  ཱི ->  ཱི
                ( chr(0x0F71) + chr(0x0F72), chr(0x0F73) ),
                #  ཱུ ->  ཱུ
                ( chr(0x0F71) + chr(0x0F74), chr(0x0F75) ),
                #  ཱྀ -> ཱྀ
                ( chr(0x0F71) + chr(0x0F80), chr(0x0F81) ),
                #  ྐྵ ->  ྐྵ
                ( chr(0x0F90) + chr(0x0FB5), chr(0x0FB9) ),
                #  ྒྷ ->  ྒྷ
                ( chr(0x0F92) + chr(0x0FB7), chr(0x0F93) ),
                #  ྜྷ ->  ྜྷ
                ( chr(0x0F9C) + chr(0x0FB7), chr(0x0F9D) ),
                #  ྡྷ ->  ྡྷ
                ( chr(0x0FA1) + chr(0x0FB7), chr(0x0FA2) ),
                #  ྦྷ ->  ྦྷ
                ( chr(0x0FA6) + chr(0x0FB7), chr(0x0FA7) ),
                #  ྫྷ ->  ྫྷ
                ( chr(0x0FAB) + chr(0x0FB7), chr(0x0FAC) ),
                #  ྲྀ ->  ྲྀ
                ( chr(0x0FB2) + chr(0x0F80), chr(0x0F76) ),
                #  ླྀ ->  ླྀ
                ( chr(0x0FB3) + chr(0x0F80), chr(0x0F78) ),
                )

################################################################################
class DStringBOD(DStringMotherClass):
    """
        class DStringBOD

        DO NOT CREATE A DStringBOD object directly but use instead the
        dchars.py::new_dstring() function.
    """

    # transliterations' methods : available direction(s) :
    trans__directions = {
          "ewts"        : trans_ewts.AVAILABLE_DIRECTIONS,
          "bodsan"      : trans_bodsan.AVAILABLE_DIRECTIONS,
        }

    trans__get_transliteration = {
          "ewts"   : trans_ewts.dstring__get_translit_str,
          "bodsan" : trans_bodsan.dstring__get_translit_str,
          }

    trans__get_intstruct_from_trans_str = {
        "ewts"   : trans_ewts.get_intstruct_from_trans_str,
        "bodsan" : trans_bodsan.get_intstruct_from_trans_str,
        }

    trans__get_transl_ucombinations = {
        "ewts"   : trans_ewts_ucombinations.get_usefull_combinations,
        # "bodsan" : ...
        }

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, str_src = None):
        """
                DStringBOD.__init__

		        the three following attributes have been created by the call to
				dchars.py::new_dstring() :

                self.iso639_3_name             : (str)
                self.transliteration_method    : (str)
                self.options                   : (dict)
        """
        DStringMotherClass.__init__(self)

        # internal structure(s) corresponding to self's content :
        # Should be initialized by self.init_from_transliteration() or
        # by self.init_from_str().
        #
        # We can't set self.istructs to an empty ListOfInternalStructures object,
        # since this objects needs option(s) to be initialized.
        self.istructs = None

        self.are_the_options_valid()

        # Pylint can't know that <self> has an 'options' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'options' member"
        if self.options["look up in the buffers"] == 'yes' and not bod_buffer.BUFFER_LOADED:
            bod_buffer.BUFFER_LOADED = self.load_the_buffers()

        if str_src is not None:
            self.init_from_str(str_src)

    #///////////////////////////////////////////////////////////////////////////
    def __setattr__(self, key, value):
        """
                DStringBOD.__setattr__
        """
        #.......................................................................
        # we set the attribute :
        #.......................................................................
        object.__setattr__(self, key, value)

        #.......................................................................
        # we check the validity of the option(s) :
        #.......................................................................
        if key == "options":
            self.are_the_options_valid()

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                DStringBOD.__str__
        """
        return self.get_sourcestr_representation()

    #///////////////////////////////////////////////////////////////////////////
    def are_the_options_valid(self):
        """
                DStringBOD.are_the_options_valid

                Raise an error if self.options isn't correctly initialized.
        """

        #.......................................................................
        # options["expected_structure"]
        #.......................................................................

        # Pylint can't know that <self> has an 'options' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'options' member"

        expected_structure = self.options["expected structure"]

        if expected_structure not in ('always Sanskrit',
                                      'always Tibetan',
                                      'Tibetan or Sanskrit'
                                     ):
            raise DCharsError( context = "DStringBOD.are_the_options_valid",
                               message = "wrong options; unknown 'expected structure' : "+\
                                         str(self.options) )

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DStringBOD.get_sourcestr_representation

                Return a string.
        """
        # why not :
        #       return "".join([str(char) for char in self])    ?
        #
        # -> the normal way to get the string representation of a DStringBOD
        # object is to use the istructs representation. By calling str(char)
        # we would call DCharacterBOD.get_sourcestr_representation(), simply
        # sticking the string representations of the characters.
        #
        return self.istructs.get_the_corresponding_string()

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_combinations(self):
        """
                DStringBOD.get_usefull_combinations

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

        dchar = DCharacterBOD(self)
        for dchar in dchar.get_usefull_combinations():

            already_present = False
            for dchar2 in self:
                if str(dchar) == str(dchar2):
                    already_present = True

            if not already_present:
                self.append( dchar )

        self.update_istructs()

        return self

    #///////////////////////////////////////////////////////////////////////////
    def get_usefull_transl_combinations(self):
        """
                DStringBOD.get_usefull_transl_combinations

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
        # -> "Instance of 'DStringBOD' has no 'transliteration_method' member"
        res = DStringBOD.trans__get_transl_ucombinations[self.transliteration_method]()
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_transliteration(self):
        """
                DStringBOD.get_transliteration
        """
        # Pylint can't know that <self> has a 'trans__get_transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'trans__get_transliteration_method' member"
        res = DStringBOD.trans__get_transliteration[self.transliteration_method](self)
        return res

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, str_src):
        """
                DStringBOD.init_from_str

                Function called by __init__(), initialize <self> and return
                <indexes_of_unrecognized_chars>.

                str_src : str
        """
        for before, after in INIT_FROM_STR__SUBSTITUTIONS:
            str_src = str_src.replace(before, after)

        # this is the function used to get the internal structure from a unicode string :

        # empty istructs object :
        self.istructs = istruct.get_intstruct_from_str(_src = "",
                                                       dstring_object = self)

        # We cut <src> into several substrings since the get_intstruct_from_str
        # function is VERY SLOW for long objects.

        # We use str.split() in order to distinguish the common characters from the TSHEG character;
        # we add a space after each substring except to the last one. The rules followed by
        # str.split() explain the strange use of <last_substring>.
        #
        #       E.g :    " a bc  e ".split(" ")
        #             ->['', 'a', 'bc', '', 'e', '']
        #
        #       E.g :    " a bc  e".split(" ")
        #             ->['', 'a', 'bc', '', 'e']
        #
        splitted_str = str_src.split(TSHEG_SYMBOL)
        for index_substring, substring in enumerate(splitted_str):

            last_substring = (index_substring == len(splitted_str) - 1)

            if substring == '' and not last_substring:
                self.istructs.extend( istruct.get_intstruct_from_str( _src = TSHEG_SYMBOL,
                                                                      dstring_object = self))
            else:
                self.istructs.extend( istruct.get_intstruct_from_str( _src = substring,
                                                                      dstring_object = self ))

                if not last_substring:
                    self.istructs.extend( istruct.get_intstruct_from_str( _src = TSHEG_SYMBOL,
                                                                          dstring_object = self ))

        # let's modify the list of DCharacters :
        self.update_dchars()

    #///////////////////////////////////////////////////////////////////////////
    def init_from_transliteration(self, trans_src):
        """
                DStringBOD.init_from_transliteration

                trans_src     :       string

                Return <self>
        """
        # this is the function used to get the internal structure from a transliterated string :
        #
        # Pylint can't know that <self> has a 'transliteration_method' member
        # created when <self> has been initialized by new_dstring() :
        # pylint: disable=E1101
        # -> "Instance of 'DStringBOD' has no 'transliteration_method' member"
        get_intstruct = DStringBOD.trans__get_intstruct_from_trans_str[self.transliteration_method]

        # We cut <trans_src> into several substrings since the get_intstruct_from_trans_str
        # function is VERY SLOW for long objects.
        self.istructs = get_intstruct( _src = "",
                                       dstring_object = self )

        # We use str.split() in order to distinguish the common characters from the space character;
        # we add a space after each substring except to the last one. The rules followed by
        # str.split() explain the strange use of <last_substring>.
        #
        #       E.g :    " a bc  e ".split(" ")
        #             ->['', 'a', 'bc', '', 'e', '']
        #
        #       E.g :    " a bc  e".split(" ")
        #             ->['', 'a', 'bc', '', 'e']
        #
        splitted_str = trans_src.split(SPACE_SYMBOL)
        for index_substring, substring in enumerate(splitted_str):

            last_substring = (index_substring == len(splitted_str) - 1)

            if substring == '' and not last_substring:
                self.istructs.extend( get_intstruct( _src = SPACE_SYMBOL,
                                                     dstring_object = self ))

            else:
                self.istructs.extend( get_intstruct( _src = substring,
                                                     dstring_object = self ))

                if not last_substring:
                    self.istructs.extend( get_intstruct( _src = SPACE_SYMBOL,
                                                        dstring_object = self ))

        # internalstructures -> string
        for internalstructure in self.istructs:
            for dchar in internalstructure.get_the_corresponding_dchars(
                    dstring_object = self,
                    dcharactertype = DCharacterBOD):
                self.append( dchar )

        return self

    #///////////////////////////////////////////////////////////////////////////
    def is_identical_to(self, aliud):
        """
                DStringBOD.is_identical_to
        """

        #.......................................................................
        # are the two list of DCharacterDOB objects identical ?
        #.......................................................................
        if len(self) != len(aliud):
            return False

        identical = True
        for index, dchar in enumerate(self):
            if dchar.is_identical_to( aliud[index] ):
                identical = False

        if not identical:
            return False

        #.......................................................................
        # are the two istructs identical ?
        #.......................................................................
        return self.istructs.is_identical_to( aliud.istructs )

    #///////////////////////////////////////////////////////////////////////////
    def load_the_buffers(self):
        """
                DStringBOD.load_the_buffers

                Return True if the buffers have been successfully loaded.
        """
        # we load the buffer into BUFFER__FROM_STR :
        filename = bod_buffer.BUFFER__FROM_STR__FNAME
        if not os.path.exists( filename ):
            raise DCharsError( context = " DStringBOD.__init__",
                               message = "Missing file : "+str(filename) )

        with open( bod_buffer.BUFFER__FROM_STR__FNAME, 'rb' ) as bufferfile:
            bod_buffer.BUFFER__FROM_STR = pickle.loads( bufferfile.read() )

        # we load the buffer into EWTS_BUFFER__FROM_TRANS_STR :
        filename = str(ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR__FNAME)
        if not os.path.exists( filename ):
            raise DCharsError( context = " DStringBOD.__init__",
                               message = "Missing file : "+str(filename) )

        with open( ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR__FNAME, 'rb' ) as bufferfile:
            ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR = pickle.loads( bufferfile.read() )

        return True

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_pure_tibetan_string(self, method):
        """
                DStringBOD.seems_to_be_a_pure_tibetan_string

                for the <method> parameter, see InternalStructure.seems_to_be_a_pure_tibetan_string
        """
        return self.istructs.seems_to_be_a_pure_tibetan_string(method)

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_sanskrit_string(self, strict_answer = False):
        """
                DStringBOD.seems_to_be_a_sanskrit_string

                Return a boolean.
        """
        return self.istructs.seems_to_be_a_sanskrit_string(strict_answer)

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DStringBOD.set_to_its_most_visual_form

                Modify <self> in place and change each character into its
                "most simple" representation

                Function used by the Logotheras project.
        """
        for dchar in self:
            dchar.set_to_its_most_visual_form()

        self.update_istructs()

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringBOD.sortingvalue

                Return an SortingValue object
        """
        return self.istructs.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def update_istructs(self):
        """
                DStringBOD.update_istructs

        """
        self.istructs = istruct.get_intstructures_from_dstring(self)
        self.update_dchars()

    #///////////////////////////////////////////////////////////////////////////
    def update_dchars(self):
        """
                DStringBOD.update_dchars
        """
        self.clear()

        if 'istructs' in self.__dict__:
            for char in self.istructs.get_the_corresponding_dchars(dcharactertype=DCharacterBOD,
                                                                   dstring_object=self):
                self.append( char )
