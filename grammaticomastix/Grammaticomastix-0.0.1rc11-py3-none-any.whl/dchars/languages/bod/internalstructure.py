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
    ❏DChars❏ : dchars/languages/bod/internalstructure.py

    * classes InternalStructure, ListOfInternalStructures
    * function get_internal_structure()
"""

from copy import deepcopy
import re

from dchars.utilities.orderedset import OrderedSet
from dchars.utilities.sortingvalue import SortingValue
from dchars.errors.errors import DCharsError
from dchars.languages.bod.symbols import SYMB_CONSONANTS, \
                                         SYMB_SUBJOINED_CONSONANTS, \
                                         SYMB_FIXEDFORM_SUBJOINED_CONSONANTS, \
                                         SYMB_PUNCTUATION, \
                                         SYMB_OTHER_SYMBOLS, \
                                         SYMB_VOWELS, \
                                         SYMB_DIACRITICS, \
                                         SYMB_DIACRITICS__HALANTA, \
                                         SYMB_DIACRITICS__RNAM_BCAD, \
                                         SYMB_DIACRITICS__ANUSV_CANDR, \
                                         SYMB_PUNCTUATION

from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
from dchars.languages.bod.syllabic_structure import PREFIXES, SUPERFIXES, SUBFIXES, ROOT, \
                                                    SUFFIXES1, SUFFIXES2, \
                                                    COMMON_CONSONANTS_STACK, \
                                                    CHILTON_S_LIST
from dchars.languages.bod.symbols import TIBETANSANSKRIT_SYMB_VOWELS, \
                                         TIBETANSANSKRIT_SYMB_CONSONANTS

from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import number_of_occurences

import dchars.languages.bod.buffer as bod_buffer

# sorting methods tables :
from dchars.languages.bod.sorting_methods_tables import BASIC_SORTMETHOD__VOWELS_VALUE, \
                                                        BASIC_SORTMETHOD__CONS_VALUE

################################################################################
# regex pattern used to slice a Tibetan source string :
#
# NB : we use the default_symbols__pattern() function, NOT the normal
#      default_symbols() function since some characters have to be
#      treated apart to work with a regex.
################################################################################
PATTERN_BASECHAR = "|".join( isort_a_lstrings_bylen_nodup(
                             SYMB_CONSONANTS.default_symbols__pattern() + \
                             SYMB_OTHER_SYMBOLS.default_symbols__pattern() + \
                             SYMB_PUNCTUATION.default_symbols__pattern() ))
PATTERN_SUBJOINED_CONSONANTS = "|".join( isort_a_lstrings_bylen_nodup(
    SYMB_SUBJOINED_CONSONANTS.default_symbols__pattern() + \
    SYMB_FIXEDFORM_SUBJOINED_CONSONANTS.default_symbols__pattern() ))
PATTERN_DEPENDENTVOWEL = "|".join( isort_a_lstrings_bylen_nodup(
    SYMB_VOWELS.default_symbols__pattern() ))
PATTERN_DIACRITICS = "|".join( isort_a_lstrings_bylen_nodup(
    SYMB_DIACRITICS.default_symbols__pattern() ))
PATTERN_TXT = "((?P<basechar>{0})" \
              "(?P<subj_consonants>({1})+)?" \
              "((?P<vowel1>{2}))?" \
              "((?P<vowel2>{3}))?" \
              "(?P<diacritics>({4})+)?)"
PATTERN = re.compile(PATTERN_TXT.format( PATTERN_BASECHAR,
                                         PATTERN_SUBJOINED_CONSONANTS,
                                         PATTERN_DEPENDENTVOWEL,
                                         PATTERN_DEPENDENTVOWEL,
                                         PATTERN_DIACRITICS ))

################################################################################
class ListOfInternalStructures(list):
    """
        class ListOfInternalStructures
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, anonymize_the_unknown_chars):
        """
                ListOfInternalStructures.__init__
        """
        list.__init__(self)
        self.anonymize_the_unknown_chars = anonymize_the_unknown_chars

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                ListOfInternalStructures.__repr__
        """
        res = []
        for internalstruct in self:
            res.append( repr(internalstruct) )

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                ListOfInternalStructures.__str__
        """
        res = []
        for internalstruct in self:
            res.append( str(internalstruct) )

        return "; ".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def clean_off_bad_internalstructs(self):
        """
                ListOfInternalStructures.clean_off_bad_internalstructs
        """
        list.__init__(self,
                      [internalstruct for internalstruct in self \
                       if not internalstruct.bad_internalstruct])

    #///////////////////////////////////////////////////////////////////////////
    def contains_unknown_characters(self):
        """
                ListOfInternalStructures.contains_unknown_characters
        """
        res = False

        for istruct in self:
            if istruct.unknown_character:
                res = True
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_all_items_linked_to_index(self, index):
        """
                ListOfInternalStructures.get_all_items_linked_to_index

                Return all InternalStructure objects having <index> in their indexes.
        """
        res = []
        for internalstruct in self:
            if index in internalstruct.indexes:
                res.append(internalstruct)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_the_complete_records(self, last_index, use_real_indexes):
        """
                ListOfInternalStructures.get_the_complete_records

                Return, if they exist, the string(s) allowing to pass from
                0 to last_index, choosing the shortest one(s).

                BEWARE : This function IS VERY SLOW with long objects (if len(self.istructs) > 10)

                use_real_indexes        : if True, real_indexes will be used;
                                          if False, indexes will be used;
        """
        res = []

        #.......................................................................
        # let's use indexes :
        #.......................................................................
        if not use_real_indexes:
            # beginning : <table> begins with lignes whose indexes are equal to 0.
            table = [ [index_line,] for index_line, line in enumerate(self) if 0 in line.indexes]

            # we extract the lines matching the expected result :
            ok_for_res = []
            for index_line, line in enumerate(table):
                if min(self[line[0]].indexes) == 0 and max(self[line[-1]].indexes) == last_index:
                    ok_for_res.append( index_line )

            for index_line in sorted(ok_for_res)[::-1]:
                res.append( table[index_line] )
                table.pop(index_line)

            while len(table) != 0:

                future_table = []

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                for index_line, line in enumerate(table):

                    # $$$traduire$$$on cherche un élément de <self> qui puisse succéder à <line> :
                    indexes_found = []
                    for index_self, obj_self in enumerate(self):
                        if max(self[line[-1]].indexes) + 1 == min(obj_self.indexes):
                            indexes_found.append( index_self )

                    for index_found in indexes_found:
                        # <line> can be prolonged by <obj_self> :
                        new_line = line + [index_found,]

                        # if <new_line> matched what the function have to return, we put <new_line>
                        # apart, in res.
                        if max(self[new_line[-1]].indexes) == last_index:
                            res.append( new_line )
                        else:
                            future_table.append( new_line )

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                table = future_table

        #.......................................................................
        # let's use real_indexes :
        #.......................................................................
        else:
            # <table> is initialized with the lines whose indexes begin with 0.
            table = [ [index_line,] \
                      for index_line, line in enumerate(self) if 0 in line.real_indexes]

            # we extract the lines matching the expected result :
            ok_for_res = []
            for index_line, line in enumerate(table):
                if min(self[line[0]].real_indexes) == 0 and \
                   max(self[line[-1]].real_indexes) == last_index:
                    ok_for_res.append( index_line )

            for index_line in sorted(ok_for_res)[::-1]:
                res.append( table[index_line] )
                table.pop(index_line)

            while len(table) != 0:

                future_table = []

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                for index_line, line in enumerate(table):

                    # $$$traduire$$$on cherche un élément de <self> qui puisse succéder à <line> :
                    indexes_found = []
                    for index_self, obj_self in enumerate(self):
                        if max(self[line[-1]].real_indexes) + 1 == min(obj_self.real_indexes):
                            indexes_found.append( index_self )

                    for index_found in indexes_found:
                        # $$$traduire$$$<line> peut être prolongée par <obj_self> :
                        new_line = line + [index_found,]

                        # if <new_line> matched what the function have to return, we put <new_line>
                        # apart, in res.
                        if max(self[new_line[-1]].real_indexes) == last_index:
                            res.append( new_line )
                        else:
                            future_table.append( new_line )

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                table = future_table

        #.......................................................................
        # let's take the shortest string(s) among <res>.
        #
        # e.g. the function will return [ [1,2], [2,3] ] among [ [1,2], [2,3], [3, 4, 5] ]
        #.......................................................................
        if len(res) == 0:
            return []
        else:
            expected_length = len(min(res, key=len))
            res = [ indexes for indexes in res if len(indexes) == expected_length ]

        if len(res) == 1:
            return res

        #.......................................................................
        # <res> has not ONE string.
        #
        # we have to choose ONE string among the strings presents in <res>.
        # we choose the "string" whose Tibetan representation is the smallest.
        #
        #.......................................................................
        # Some examples illustrating this rule :
        #
        # * gande'i = གནདེའི :
        # gan de'i = གན་དེའི      (ok)
        # gand e'i = གནད་ཨེའི    (too long)
        #
        # * karma = ཀརྨ :
        # ka rma  = ཀ་རྨ        (ok)
        # kar ma  = ཀར་མ    (too long)
        #
        # * tandra = ཏནདྲ་ :
        # tan dra = ཏན་དྲ་      (ok)
        # tand ra = ཏནད་ར    (too long)
        #
        #.......................................................................
        minimal_length = 9999
        selected_indexes = None
        for num_indexes, indexes in enumerate(res):

            unicode_str = ""
            for index in indexes:
                unicode_str += \
                  self[index].get_the_corresponding_string(self.anonymize_the_unknown_chars)

            if len(unicode_str) < minimal_length:
                minimal_length = len(unicode_str)
                selected_indexes = num_indexes

        return [res[selected_indexes], ]

    #///////////////////////////////////////////////////////////////////////////
    def get_the_corresponding_dchars(self, dcharactertype, dstring_object):
        """
                ListOfInternalStructures.get_the_corresponding_dchars
        """
        res = []
        for istruct in self:
            res.extend( istruct.get_the_corresponding_dchars(dcharactertype,
                                                             dstring_object))

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_the_corresponding_string(self):
        """
                ListOfInternalStructures.get_the_corresponding_string

                return a (str)string, not a DString !
        """
        return "".join( [istruct.get_the_corresponding_string(anonymize_the_unknown_chars = \
                                            self.anonymize_the_unknown_chars) for istruct in self ])

    #///////////////////////////////////////////////////////////////////////////
    def get_first_item_with_the_index(self, index):
        """
                ListOfInternalStructures.get_first_item_with_the_index

                Return the first InternalStructure object whose indexes contain <index>
                or None if there's no return value available.
        """
        res = None
        for internalstruct in self:
            if index in internalstruct.indexes:
                res = internalstruct
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def is_identical_to(self, aliud):
        """
                ListOfInternalStructures.is_identical_to
        """
        if len(self) != len(aliud):
            return False

        res = True
        for index, istruct in enumerate(self):
            if not istruct.is_identical_to(aliud[index]):
                res = False
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def init_from_pickle_repr(self, src, dstring_object):
        """
                ListOfInternalStructure.init_from_pickle_repr

                <src>   : list of strings

                Initialize and return self.

                Reciprocal function of self.pickle_repr()
        """
        # Something weird with Pylint : this classe is derived from 'list'
        # and DO have a .clear() member.
        # pylint: disable=E1101
        # -> Instance of 'ListOfInternalStructures' has no 'clear' member
        self.clear()
        for string in src:
            self.append( InternalStructure(dstring_object = dstring_object).init_from_pickle_repr(
                                                                src = string,
                                                                dstring_object = dstring_object))

        return self

    #///////////////////////////////////////////////////////////////////////////
    def pickle_repr(self):
        """
                ListOfInternalStructures.pickle_repr

                Return a convenient representation of <self> for pickling.

                Reciprocal function of self.init_from_pickle_repr()
        """
        res = []
        for istruct in self:
            if istruct.bad_internalstruct:
                raise DCharsError( context = "ListOfInternalStructures.pickle_repr",
                                   message = "istruct.bad_internalstruct=True; "+repr(istruct))
            res.append( istruct.pickle_repr() )

        return tuple(res)

    #///////////////////////////////////////////////////////////////////////////
    def rsort_by_indexes_len__u_items(self):
        """
                ListOfInternalStructures.rsort_by_indexes_len__u_items

                return a list from <self> :

                  * reverse-sorted by the length of the indexes of each InternalStructure object
                  * we don't put in the result the InternalStructure object whose indexes
                    are equal to another one InternalStructure object in <self>.
        """
        res = sorted( self, key=InternalStructure.get_length_of_indexes)[::-1]

        indexes_to_be_deleted = []
        # we mark the InternalStructure objects which must be removed :
        for index_res_internalstruct, res_internalstruct in enumerate(res):

            for internalstruct in self:
                # we test internalstruct != res_internalstruct since we don't want to remove
                # an internalstruct identical with itself !
                if internalstruct != res_internalstruct and \
                   internalstruct.indexes == res_internalstruct.indexes:
                    indexes_to_be_deleted.append( index_res_internalstruct )
                    break

        # we remove them :
        for index in indexes_to_be_deleted[::-1]:
            res.pop(index)

        return res

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_pure_tibetan_string(self, method):
        """
                ListOfInternalStructures.seems_to_be_a_pure_tibetan_string

                for the <method> parameter, see InternalStructure.seems_to_be_a_pure_tibetan_string
        """
        for istruct in self:
            if not istruct.seems_to_be_a_pure_tibetan_string(method):
                return False

        return True       

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_sanskrit_string(self, strict_answer = False):
        """
                ListOfInternalStructures.seems_to_be_a_sanskrit_string
        """
        for istruct in self:
            if istruct.seems_to_be_a_sanskrit_string(strict_answer):
                return True

        return False
            
    #///////////////////////////////////////////////////////////////////////////
    def set_the_dstring_object(self, dstring_object):
        """
                ListOfInternalStructures.set_the_dstring_object

                dstring_object    : DstringBOD object
        """
        for istruct in self:
            istruct.dstring_object = dstring_object

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                ListOfInternalStructures.sortingvalue
        """
        return [ istruct.sortingvalue() for istruct in self ]

################################################################################
class InternalStructure(object):
    """
        class InternalStructure

        Define the internal structure of a Tibetan syllable.

    """

    pickle_markers = "".join( [chr(num) for num in range(0, 0x0018+1)] )

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_character = False,
                 punctuation_or_other_symbol = None,
                 prefix = None,
                 superfix = None,
                 consonant = None,
                 vowel1 = None,
                 vowel2 = None,
                 subfix = None,
                 suffix1 = None,
                 suffix2 = None,
                 postsuffix_u = False,
                 gramm_postsuffix = None,
                 postsuffix_o = False,
                 anusvara_candrabindu = None,
                 rnam_bcad = False,
                 halanta = False,
                 indexes = None,
                 real_indexes = None,
                 ):
        """
                InternalStructure.__init__

                postsuffix_u            : bool
                gramm_postsuffix        : None or a string among ('i 'is 'am 'ang r s)
                postsuffix_o            : bool

                * indexes :       OrderedSet object.
                * real_indexes :  OrderedSet object.

                * <real_indexes> are defined from the source string, character by character
                  but <indexes> are defined from the string as it appeared to the regex :

                        E.g. for the transliterated string "²nya²" (with 2 unknown characters ) :
                                real_indexes : /²/n/y/a/²/ =0,1,2,3,4
                                indexes :      /²/ny/a/²/  =0,1,2,3
        """
        self.bad_internalstruct = False

        self.unknown_character = unknown_character
        self.punctuation_or_other_symbol = punctuation_or_other_symbol
        self.prefix = prefix
        self.superfix = superfix
        self.consonant = consonant
        self.vowel1 = vowel1
        self.vowel2 = vowel2
        self.subfix = subfix
        self.suffix1 = suffix1
        self.suffix2 = suffix2
        self.postsuffix_u = postsuffix_u
        self.gramm_postsuffix = gramm_postsuffix
        self.postsuffix_o = postsuffix_o
        self.anusvara_candrabindu = anusvara_candrabindu
        self.rnam_bcad = rnam_bcad
        self.halanta = halanta

        if indexes is None:
            # not a single set() in order to allow a quick reading of the indexes :
            self.indexes = OrderedSet()
        else:
            self.indexes = indexes

        if real_indexes is None:
            # not a single set() in order to allow a quick reading of the (real) indexes :
            self.real_indexes = OrderedSet()
        else:
            self.real_indexes = real_indexes

        self.dstring_object = dstring_object

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                InternalStructure.__repr__
        """
        res = "unknown_character = {0};" \
              "punctuation/other symbol={1};" \
              "prefix={2};"  \
              "superfix={3};" \
              "consonant={4};"  \
              "vowel1={5};"  \
              "vowel2={6};"  \
              "subfix={7};"  \
              "suffix1={8};"  \
              "suffix2={9};" \
              "postsuffix_u={10};" \
              "gramm_postsuffix={11};" \
              "postsuffix_o={12};" \
              "anusvara_candrabindu={13};" \
              "rnam_bcad={14};" \
              "halanta={15};".format(
                  self.unknown_character,
                  self.punctuation_or_other_symbol,
                  self.prefix,
                  self.superfix,
                  self.consonant,
                  self.vowel1,
                  self.vowel2,
                  self.subfix,
                  self.suffix1,
                  self.suffix2,
                  self.postsuffix_u,
                  self.gramm_postsuffix,
                  self.postsuffix_o,
                  self.anusvara_candrabindu,
                  self.rnam_bcad,
                  self.halanta)

        if not self.bad_internalstruct:
            marker = "[+]"
        else:
            marker = "[-]"

        return "{0}{1}; indexes={2} real_indexes={3}".format(marker,
                                                             res,
                                                             self.indexes,
                                                             self.real_indexes)

    #///////////////////////////////////////////////////////////////////////////
    def __setattr__(self, key, value):
        """
                InternalStructure.__setattr__
        """

        #.......................................................................
        # we check that <key, value> are acceptable arguments.
        #.......................................................................

        if key == "prefix" and value is not None and value not in PREFIXES:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid prefix.".format(value) )

        if key == "superfix" and value is not None and value not in SUPERFIXES:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid superfix.".format(value) )

        if key == "consonant" and value is not None and value not in ROOT:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid main consonant.".format(value) )

        if key == "vowel1" and value is not None and value not in SYMB_VOWELS:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid vowel(#1).".format(value) )

        if key == "vowel2" and value is not None and value not in SYMB_VOWELS:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid vowel(#2).".format(value) )

        if key == "subfix" and value is not None:
            for val in value:
                if val not in SYMB_CONSONANTS:
                    raise DCharsError( context = "InternalStructure.__setitem__",
                                       message = "'{0}' is not a valid subfix.".format(value) )

        if key == "suffix1" and value is not None and value not in SUFFIXES1:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid suffix(#1).".format(value) )

        if key == "suffix2" and value is not None and value not in SUFFIXES2:
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is not a valid suffix(#2).".format(value) )

        if key == "postsuffix_u" and value not in (True, False):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the " \
                                         "'postsuffix_u' attribute.".format(value) )

        if key == "gramm_postsuffix" and value not in (None,
                                                                   "'i",
                                                                   "'is",
                                                                   "'am",
                                                                   "'ang",
                                                                   "r",
                                                                   "s"):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the " \
                                         "'gramm_postsuffix' " \
                                         "attribute.".format(value) )

        if key == "postsuffix_o" and value not in (True, False):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the 'postsuffix_o' "\
                                         "attribute.".format(value) )

        if key == "anusvara_candrabindu" and value not in (None,
                                                           'SIGN RJES SU NGA RO',
                                                           'SIGN NYI ZLA NAA DA',
                                                           'SIGN SNA LDAN',):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the 'anusvara_candrabindu' "\
                                         " attribute.".format(value) )

        if key == "halanta" and value not in (True, False):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the 'halanta' " \
                                         "attribute.".format(value) )

        if key == "rnam_bcad" and value not in (True, False):
            raise DCharsError( context = "InternalStructure.__setitem__",
                               message = "'{0}' is a wrong value for the 'rnam_bcad' " \
                                         "attribute.".format(value) )

        #.......................................................................
        # we set the attribute :
        #.......................................................................
        object.__setattr__(self, key, value)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                InternalStructure.__str__
        """

        res = []

        if self.bad_internalstruct:
            res.append("-")

        if self.unknown_character:
            res.append("(unknown character)")

        if self.punctuation_or_other_symbol is not None:
            res.append( "(punct/other symbol)" + str(self.punctuation_or_other_symbol) )

        if self.prefix is not None:
            res.append( "(prefix)" + str(self.prefix) )

        if self.superfix is not None:
            res.append( "(superfix)" + str(self.superfix) )

        if self.consonant is not None:
            res.append( "(consonant)" + str(self.consonant) )

        if self.subfix is not None:
            res.append( "(subfix)" + str(self.subfix) )

        if self.vowel1 is not None:
            res.append( "(vowel1)" + str(self.vowel1) )

        if self.vowel2 is not None:
            res.append( "(vowel2)" + str(self.vowel2) )

        if self.suffix1 is not None:
            res.append( "(suffix1)" + str(self.suffix1) )

        if self.suffix2 is not None:
            res.append( "(suffix2)" + str(self.suffix2) )

        if self.postsuffix_u:
            res.append( "(postsuffix 'u)" )

        if self.gramm_postsuffix is not None:
            res.append( "(postsuffix " + str(self.gramm_postsuffix) + ")" )

        if self.postsuffix_o:
            res.append( "(postsuffix 'o)" )

        if self.anusvara_candrabindu:
            res.append( "(anusvara/candrabindu)" + str(self.anusvara_candrabindu) )

        if self.rnam_bcad:
            res.append( "(rnam bcad)" )

        if self.halanta:
            res.append( "(halanta)" )

        return "".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def check_default_value(self,
              unknown_character = False,
              punctuation_or_other_symbol = None,
              prefix = None,
              superfix = None,
              consonant = None,
              vowel1 = None,
              vowel2 = None,
              subfix = None,
              suffix1 = None,
              suffix2 = None,
              postsuffix_u = False,
              gramm_postsuffix = None,
              postsuffix_o = False,
              anusvara_candrabindu = None,
              rnam_bcad = False,
              halanta = False):
        """
                Return True if <self> has the default values or the values passed as an argument.

                NB : the indexes are not checked.
        """

        res = True
        for argument_value, self_value in (
                (unknown_character, self.unknown_character),
                (punctuation_or_other_symbol, self.punctuation_or_other_symbol),
                (prefix, self.prefix),
                (superfix, self.superfix),
                (consonant, self.consonant),
                (vowel1, self.vowel1),
                (vowel2, self.vowel2),
                (subfix, self.subfix),
                (suffix1, self.suffix1),
                (suffix2, self.suffix2),
                (postsuffix_u, self.postsuffix_u),
                (gramm_postsuffix, self.gramm_postsuffix),
                (postsuffix_o, self.postsuffix_o),
                (anusvara_candrabindu, self.anusvara_candrabindu),
                (rnam_bcad, self.rnam_bcad),
                (halanta, self.halanta),
                ):

            if argument_value != self_value:
                res = False
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_min_of_indexes(self):
        """
                InternalStructure.get_min_of_indexes

                special function used by sorted(ListOfInternalStructures object,
                                                key = InternalStructure.get_min_of_indexes)
        """
        return min(list(self.indexes))

    #///////////////////////////////////////////////////////////////////////////
    def get_the_corresponding_dchars(self, dcharactertype, dstring_object):
        """
                InternalStructure.get_the_corresponding_dchars

                Return a list of dcharacters, not a (str)string !

                By returning a list and not a DString object we avoid some problems
                with the trigger list.
        """
        res = []

        if self.unknown_character:
            new_dchar = dcharactertype(dstring_object = None)
            new_dchar.unknown_char = True
            new_dchar.base_char = self.punctuation_or_other_symbol
            res.append( new_dchar )

        elif self.punctuation_or_other_symbol is not None:
            new_dchar = dcharactertype(dstring_object = None)
            new_dchar.base_char = self.punctuation_or_other_symbol
            new_dchar.punctuation = new_dchar.base_char in SYMB_PUNCTUATION
            res.append( new_dchar )

        else:
            if self.prefix is not None:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = self.prefix
                res.append( new_dchar )

            if self.superfix is not None:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = self.superfix
                res.append( new_dchar )

            if self.consonant is not None:
                if self.superfix is None:
                    # no superfix character :
                    new_dchar = dcharactertype(dstring_object = None)
                    new_dchar.base_char = self.consonant
                    res.append( new_dchar )
                else:
                    # superfix character followed by the main consonant :
                    res[-1].subj_consonants = [self.consonant,]

            if self.subfix is not None:
                if res[-1].subj_consonants is None:
                    res[-1].subj_consonants = []

                for subj_c in self.subfix:
                    res[-1].subj_consonants.append( subj_c )

            if self.vowel1 is not None:
                if len(res)==0:
                    new_dchar = dcharactertype(dstring_object = None)
                    new_dchar.base_char = "A"
                    res.append( new_dchar )
                res[-1].vowel1 = self.vowel1

            if self.vowel2 is not None:
                res[-1].vowel2 = self.vowel2

            if self.suffix1 is not None:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = self.suffix1
                res.append( new_dchar )

            if self.suffix2 is not None:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = self.suffix2
                res.append( new_dchar )

            # res[-1] can be the main consonant but it can be a suffix, like
            # in ལབཿ (labH) where -bH takes the rnam bcad.
            res[-1].halanta = self.halanta
            res[-1].rnam_bcad = self.rnam_bcad
            res[-1].anusvara_candrabindu = self.anusvara_candrabindu

            if self.postsuffix_u:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "U"
                res.append( new_dchar )

            if self.gramm_postsuffix == "'i":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "I"
                res.append( new_dchar )

            elif self.gramm_postsuffix == "'is":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "I"
                res.append( new_dchar )
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "S"
                res.append( new_dchar )

            elif self.gramm_postsuffix == "'am":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "A"
                res.append( new_dchar )
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "M"
                res.append( new_dchar )

            elif self.gramm_postsuffix == "'ang":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "A"
                res.append( new_dchar )
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "NG"
                res.append( new_dchar )

            elif self.gramm_postsuffix == "r":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "R"

            elif self.gramm_postsuffix == "s":
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "S"

            if self.postsuffix_o:
                new_dchar = dcharactertype(dstring_object = None)
                new_dchar.base_char = "-"
                new_dchar.vowel1 = "O"
                res.append( new_dchar )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_the_corresponding_string(self,
                                     anonymize_the_unknown_chars):
        """
                InternalStructure.get_the_corresponding_string

                * anonymize_the_unknown_chars : (bool) value of the option
                  "anonymize the unknown characters". Why don't we use the expected
                  dstring_object.options["anonymize the unknown characters"] ?
                  Because this function is called by a function setting (in a first time)
                  dstring_object to None (and latter) to the true value of dstring_object.

                return a (str)string
        """
        if self.unknown_character:
            if anonymize_the_unknown_chars:
                return UNKNOWN_CHAR_SYMBOL
            else:
                return self.punctuation_or_other_symbol

        res = []

        if self.punctuation_or_other_symbol is not None:

            if self.punctuation_or_other_symbol in SYMB_PUNCTUATION:
                res.append( SYMB_PUNCTUATION.get_default_symbol(self.punctuation_or_other_symbol) )
            elif self.punctuation_or_other_symbol in SYMB_OTHER_SYMBOLS:
                res.append( SYMB_OTHER_SYMBOLS.get_default_symbol(self.punctuation_or_other_symbol))
            else:
                message = "unknown character="+str(self.punctuation_or_other_symbol)
                raise DCharsError( context = "InternalStructure.get_the_corresponding_string",
                                   message = message )

        else:

            if self.prefix is not None:
                res.append( SYMB_CONSONANTS.get_default_symbol(self.prefix) )

            if self.superfix is not None:
                res.append( SYMB_CONSONANTS.get_default_symbol(self.superfix) )

            if self.consonant is not None:
                if self.superfix is None:
                    res.append( SYMB_CONSONANTS.get_default_symbol(self.consonant) )
                else:
                    res.append( SYMB_SUBJOINED_CONSONANTS.get_default_symbol(self.consonant) )

            if self.subfix is not None:
                for subj_c in self.subfix:
                    res.append( SYMB_SUBJOINED_CONSONANTS.get_default_symbol(subj_c) )

            if self.vowel1 is not None:
                res.append( SYMB_VOWELS.get_default_symbol(self.vowel1) )

            if self.vowel2 is not None:
                res.append( SYMB_VOWELS.get_default_symbol(self.vowel2) )

            if self.suffix1 is not None:
                res.append( SYMB_CONSONANTS.get_default_symbol(self.suffix1) )

            if self.suffix2 is not None:
                res.append( SYMB_CONSONANTS.get_default_symbol(self.suffix2) )

            if self.halanta:
                res.append( SYMB_DIACRITICS__HALANTA )

            if self.rnam_bcad:
                res.append( SYMB_DIACRITICS__RNAM_BCAD )

            if self.anusvara_candrabindu is not None:
                res.append( SYMB_DIACRITICS.get_default_symbol(self.anusvara_candrabindu) )

            if self.postsuffix_u:
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("U") )

            if self.gramm_postsuffix == "'i":
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("I") )

            elif self.gramm_postsuffix == "'is":
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("I") )
                res.append( SYMB_CONSONANTS.get_default_symbol("S") )

            elif self.gramm_postsuffix == "'am":
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("A") )
                res.append( SYMB_CONSONANTS.get_default_symbol("M") )

            elif self.gramm_postsuffix == "'ang":
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("A") )
                res.append( SYMB_CONSONANTS.get_default_symbol("NG") )

            elif self.gramm_postsuffix == "r":
                res.append( SYMB_CONSONANTS.get_default_symbol("R") )

            elif self.gramm_postsuffix == "s":
                res.append( SYMB_CONSONANTS.get_default_symbol("S") )

            if self.postsuffix_o:
                res.append( SYMB_CONSONANTS.get_default_symbol("-") )
                res.append( SYMB_VOWELS.get_default_symbol("O") )

        res = "".join(res)
        res = res.replace("FAKE_A", "")

        return res

    #///////////////////////////////////////////////////////////////////////////
    def have_indexes_common_with(self, internalstruct_object):
        """
                InternalStructure.have_indexes_common_with

                internalstruct_object : InternalStructure object

                Return either True if <self> shares at least one index with
                <internalstruct_object>.
        """
        res = False

        for index in self.indexes:
            if index in internalstruct_object.indexes:
                res = True
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_length_of_indexes(self):
        """
                InternalStructure.get_length_of_indexes

                special function used by sorted(ListOfInternalStructures object,
                                                key = InternalStructure.get_length_of_indexes)
        """
        return len(self.indexes)

    #///////////////////////////////////////////////////////////////////////////
    def indexes_are_contiguous_to(self, indexes):
        """
                InternalStructure.indexes_are_contiguous_to

                Returns True (1) if min(indexes)-1 is in self.indexes (2) if self.indexes
                is empty.
        """
        if len(self.indexes)==0:
            return True
        else:
            return min(indexes)-1 in self.indexes

    #///////////////////////////////////////////////////////////////////////////
    def init_from_pickle_repr(self, src, dstring_object):
        """
                InternalStructure.init_from_pickle_repr

                Initialize and return self.

                <src> is a string defining the attributes of <self> BUT

                .bad_internalstruct (assumed as False)
                .dstring_object (initialized as None)

                Recriprocal function of self.pickle_repr()
        """

        #.......................................................................
        # default values :
        #.......................................................................
        self.bad_internalstruct = False
        self.indexes = None
        self.real_indexes = None

        self.unknown_character = False
        self.punctuation_or_other_symbol = None
        self.prefix = None
        self.superfix = None
        self.consonant = None
        self.vowel1 = None
        self.vowel2 = None
        self.subfix = None
        self.suffix1 = None
        self.suffix2 = None
        self.postsuffix_u = False
        self.gramm_postsuffix = None
        self.postsuffix_o = False
        self.anusvara_candrabindu = None
        self.rnam_bcad = False
        self.halanta = False

        #.......................................................................
        # we add the informations stored in <src> :
        #.......................................................................
        current_substring = ""

        for char in src:

            if char in InternalStructure.pickle_markers:

                if char == chr(0x0001):
                    self.unknown_character = True
                    self.punctuation_or_other_symbol = current_substring

                elif char == chr(0x0002):
                    self.postsuffix_u = True

                elif char == chr(0x0003):
                    self.postsuffix_o = True

                elif char == chr(0x0004):
                    self.rnam_bcad = True

                elif char == chr(0x0005):
                    self.halanta = True

                elif char == chr(0x0006):
                    self.punctuation_or_other_symbol = current_substring

                elif char == chr(0x0007):
                    self.prefix = current_substring

                elif char == chr(0x0008):
                    self.superfix = current_substring

                elif char == chr(0x0009):
                    self.consonant = current_substring

                elif char == chr(0x000A):
                    self.vowel1 = "A"

                elif char == chr(0x000B):
                    self.vowel1 = "I"

                elif char == chr(0x000C):
                    self.vowel1 = "O"

                elif char == chr(0x000D):
                    self.vowel1 = "U"

                elif char == chr(0x000E):
                    self.vowel1 = "E"

                elif char == chr(0x000F):
                    self.vowel1 = current_substring

                elif char == chr(0x0010):
                    self.vowel2 = current_substring

                elif char == chr(0x0011):
                    self.subfix = current_substring.split(";")

                elif char == chr(0x0012):
                    self.suffix1 = current_substring

                elif char == chr(0x0013):
                    self.suffix2 = current_substring

                elif char == chr(0x0014):
                    self.gramm_postsuffix = current_substring

                elif char == chr(0x0015):
                    self.anusvara_candrabindu = 'SIGN RJES SU NGA RO'

                elif char == chr(0x0016):
                    self.anusvara_candrabindu = current_substring

                elif char == chr(0x0017):
                    first_number, length = map(int, current_substring.split(";"))
                    self.indexes = OrderedSet(range(first_number, first_number+length))

                elif char == chr(0x0018):
                    first_number, length = map(int, current_substring.split(";"))
                    self.real_indexes = OrderedSet(range(first_number, first_number+length))

                else:
                    raise DCharsError( context = "InternalStructure.init_from_pickle_repr",
                                       message = "unknown marker = "+repr(char))

                current_substring = ""

            else:
                current_substring += char

        self.dstring_object = dstring_object

        return self

    #///////////////////////////////////////////////////////////////////////////
    def pickle_repr(self):
        """
                InternalStructure.pickle_repr

                Return an convenient representation of <self> for pickling.

                Assume that .bad_internalstruct is True and doesn't record the
                value of .dstring_object, .indexes and .real_indexes.

                Reciprocal function of self.init_from_pickle_repr()
        """
        res = []

        if self.unknown_character:
            res.append( str(self.punctuation_or_other_symbol)+chr(0x0001) )

        if self.postsuffix_u:
            res.append( chr(0x0002) )

        if self.postsuffix_o:
            res.append( chr(0x0003) )

        if self.rnam_bcad:
            res.append( chr(0x0004) )

        if self.halanta:
            res.append( chr(0x0005) )

        if self.punctuation_or_other_symbol is not None:
            res.append( str(self.punctuation_or_other_symbol) + chr(0x0006) )

        if self.prefix is not None:
            res.append( str(self.prefix) + chr(0x0007) )

        if self.superfix is not None:
            res.append( str(self.superfix) + chr(0x0008) )

        if self.consonant is not None:
            res.append( str(self.consonant) + chr(0x0009) )

        if self.vowel1 is not None:
            if self.vowel1 == 'A':
                res.append( chr(0x000A) )
            elif self.vowel1 == 'I':
                res.append( chr(0x000B) )
            elif self.vowel1 == 'O':
                res.append( chr(0x000C) )
            elif self.vowel1 == 'U':
                res.append( chr(0x000D) )
            elif self.vowel1 == 'E':
                res.append( chr(0x000E) )
            else:
                res.append( str(self.vowel1) + chr(0x000F) )

        if self.vowel2 is not None:
            res.append( str(self.vowel2) + chr(0x0010) )

        if self.subfix is not None:
            res.append( ";".join(self.subfix) + chr(0x0011) )

        if self.suffix1 is not None:
            res.append( str(self.suffix1) + chr(0x0012))

        if self.suffix2 is not None:
            res.append( str(self.suffix2) + chr(0x0013))

        if self.gramm_postsuffix is not None:
            res.append( str(self.gramm_postsuffix) + chr(0x0014))

        if self.anusvara_candrabindu is not None:
            if self.anusvara_candrabindu == 'SIGN RJES SU NGA RO':
                res.append( chr(0x0015) )
            else:
                res.append( str(self.anusvara_candrabindu) + chr(0x0016) )

        res.append( str(min(self.indexes)) + ";" + str(len(self.indexes)) + chr(0x0017) )
        res.append( str(min(self.real_indexes)) + ";" + str(len(self.real_indexes)) + chr(0x0018) )

        return "".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def real_indexes_are_contiguous_to(self, real_indexes):
        """
                InternalStructure.indexes_are_contiguous_to

                realindex : list/set of "real indexes"
        """
        if len(self.real_indexes)==0 or len(real_indexes)==0:
            return True

        return min(real_indexes) - 1 == max(self.real_indexes)

    #///////////////////////////////////////////////////////////////////////////
    def is_identical_to(self, aliud):
        """
                InternalStructure.is_identical_to

                Test all attributes but .bad_internalstruct and .dstring_object
        """

        res = self.unknown_character == aliud.unknown_character and \
               self.punctuation_or_other_symbol == aliud.punctuation_or_other_symbol and \
               self.prefix == aliud.prefix and \
               self.superfix == aliud.superfix and \
               self.consonant == aliud.consonant and \
               self.vowel1 == aliud.vowel1 and \
               self.vowel2 == aliud.vowel2 and \
               self.subfix == aliud.subfix and \
               self.suffix1 == aliud.suffix1 and \
               self.suffix2 == aliud.suffix2 and \
               self.postsuffix_u == aliud.postsuffix_u and \
               self.gramm_postsuffix == aliud.gramm_postsuffix and \
               self.postsuffix_o == aliud.postsuffix_o and \
               self.anusvara_candrabindu == aliud.anusvara_candrabindu and \
               self.rnam_bcad == aliud.rnam_bcad and \
               self.halanta == aliud.halanta and \
               self.indexes == aliud.indexes and \
               self.real_indexes == aliud.real_indexes

        return res

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_sanskrit_string(self, strict_answer):
        """
                InternalStructures.seems_to_be_a_sanskrit_string
        """
        if strict_answer:

            if self.rnam_bcad:
                return True

            if self.anusvara_candrabindu is not None:
                return True

            if self.halanta:
                return True

            if self.vowel1 in TIBETANSANSKRIT_SYMB_VOWELS:
                return True

            if self.consonant in TIBETANSANSKRIT_SYMB_CONSONANTS or \
               self.suffix1 in TIBETANSANSKRIT_SYMB_CONSONANTS or \
               self.suffix2 in TIBETANSANSKRIT_SYMB_CONSONANTS:
                return True

            return False

        else:

            # @@BOD-INTERNALSTRUCTURE-007
            # rnam bcad is not an evidence  གཏིཿ = gtiH (NOT gatiH)
            # if self.rnam_bcad:
            #    return True

            # @@BOD-INTERNALSTRUCTURE-008
            # rjes su nga ro isn't an evidence of a Sanskrit word
            # if self.anusvara_candrabindu is not None:
            #     return True

            if self.halanta:
                return True

            if self.vowel1 in TIBETANSANSKRIT_SYMB_VOWELS:
                return True

            if self.consonant in TIBETANSANSKRIT_SYMB_CONSONANTS or \
               self.suffix1 in TIBETANSANSKRIT_SYMB_CONSONANTS or \
               self.suffix2 in TIBETANSANSKRIT_SYMB_CONSONANTS:
                return True

        return False

    #///////////////////////////////////////////////////////////////////////////
    def seems_to_be_a_pure_tibetan_string(self, method):
        """
                InternalStructures.seems_to_be_a_pure_tibetan_string

                method :
                "standard" : grammatical analyse of the word
                "Chilton's list" : Chilton made a list of the possible
                                   prefixed+superfixed+root consonants

                see  http://www.tibet.columbia.edu/iats/it/IATS-X_Chilton_slides.pdf, slide 32
        """
        if method == 'standard':

            # some words are followed by a TSHEG :
            if self.punctuation_or_other_symbol:
                return True

            if self.prefix is not None and \
               self.prefix not in ('-', 'G', 'D', 'B', 'M'):
                return False

            if self.consonant is not None and \
               self.consonant not in ('K', 'KH', 'G', 'NG', 'C', 'CH', 'J', 'NY',
                                      'T', 'TH', 'D', 'N',  'P', 'PH', 'B', 'M',
                                      'TS','TSH','DZ',
                                      'W', 'ZH', 'Z',
                                      '-', 'Y', 'R', 'L', 
                                      'SH', 'S', 'H',
                                      'A',):
                return False

            if self.superfix is not None and \
               self.superfix not in ('R', 'L', 'S'):
                return False

            if self.subfix is not None and \
               self.subfix not in ('Y', 'R', 'L', 'W'):
                return False

            if self.suffix1 is not None and \
               self.suffix1 not in ('G', 'NG', 'D', 'N', 'B', 'M', '-', 'R', 'L', 'S'):
                return False

            if self.suffix2 is not None and \
               self.suffix2 not in ('S', 'D'):
                return False

            if self.vowel1 is not None and \
               self.vowel1 not in ('A', 'E', 'I', 'O'):
                return False

            if self.vowel2 is not None and \
               self.vowel2 not in ('A', 'U',):
                return False

            # is the stack of consontants defined as in 
            # http://www.thlib.org/reference/transliteration/tibstacks.php ?
            cons = []
            if self.consonant is not None:
                cons.append( self.consonant )
            if self.subfix is not None:
                for subj_c in self.subfix:
                    cons.extend( subj_c )
            if len(cons)>=2 and tuple(cons) not in COMMON_CONSONANTS_STACK:
                return False

            if self.seems_to_be_a_sanskrit_string(strict_answer = True):
                return False

            return True
    
        elif method == "Chilton's list":

            # some words are followed by a TSHEG :
            if self.punctuation_or_other_symbol:
                return True

            cons = ( self.prefix, self.superfix, self.consonant )
            if cons not in CHILTON_S_LIST:
                return False
    
            if self.seems_to_be_a_sanskrit_string(strict_answer = True):
                return False

            return True

        else:
            # error : wrong method's name.
            return None

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                InternalStructure.sortingvalue

                Return an SortingValue object
        """
        res = SortingValue()

        #=======================================================================
        #
        # for more details, see the documentation (@@BOD-INTERNALSTRUCTURE-009a)
        #
        if self.dstring_object.options["sorting method"] == "basic":

            if self.unknown_character:
                # unknown character :
                res.append(1)
                return res

            #...................................................................
            # known character :
            #...................................................................
            res.append(0)

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # main consonant :
            res.append( BASIC_SORTMETHOD__CONS_VALUE[self.consonant] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # type :
            if self.superfix is None and self.prefix is None:
                res.append(0)
            elif self.superfix is None and self.prefix is not None:
                res.append(1)
            elif self.superfix is not None and self.prefix is None:
                res.append(2)
            else:
                res.append(3)

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # superfix :
            res.append( BASIC_SORTMETHOD__CONS_VALUE[self.superfix] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # prefix :
            res.append( BASIC_SORTMETHOD__CONS_VALUE[self.prefix] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # subfix :
            if self.subfix is None:
                res.append( 0 )
            else:
                for subfix_consonant in self.subfix:
                    res.append( BASIC_SORTMETHOD__CONS_VALUE[subfix_consonant] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # vowel1 :
            if self.vowel1 not in BASIC_SORTMETHOD__VOWELS_VALUE:
                raise DCharsError( context="InternalStructure.sortingvalue",
                                    message="unknown vowel used as a vowel1="+\
                                            str(self.vowel1) )
            else:
                res.append( BASIC_SORTMETHOD__VOWELS_VALUE[self.vowel1] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # vowel2 :
            if self.vowel2 not in BASIC_SORTMETHOD__VOWELS_VALUE:
                raise DCharsError( context="InternalStructure.sortingvalue",
                                    message="unknown vowel used as a vowel2="+\
                                            str(self.vowel2) )
            else:
                res.append( BASIC_SORTMETHOD__VOWELS_VALUE[self.vowel2] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # suffix1 :
            res.append( BASIC_SORTMETHOD__CONS_VALUE[self.suffix1] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # suffix2 :
            res.append( BASIC_SORTMETHOD__CONS_VALUE[self.suffix2] )

            #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
            # rnam bcad :
            if not self.rnam_bcad:
                res.append(0)
            else:
                res.append(1)

            # other suffixes :
            if not self.postsuffix_u:
                res.append(0)
            else:
                res.append(1)

            if not self.postsuffix_o:
                res.append(0)
            else:
                res.append(1)

            if self.gramm_postsuffix is None:
                res.append(0)
            elif self.gramm_postsuffix == "'i":
                res.append(1)
            elif self.gramm_postsuffix == "'is":
                res.append(2)
            elif self.gramm_postsuffix == "'am":
                res.append(3)
            elif self.gramm_postsuffix == "'ang":
                res.append(4)
            elif self.gramm_postsuffix == "r":
                res.append(5)
            elif self.gramm_postsuffix == "s":
                res.append(6)

        return res

#///////////////////////////////////////////////////////////////////////////////
def get_intstructures_from_dstring(dstring_object):
    """
        function get_intstructures_from_dstring()

        return a ListOfInternalStructures object which describes <dstring_object>.

        .. code-block:: python

            ************
            * CONTENTS *
            ************

            (1) we cut the <dstring_object> into several <istructs>
            (2) we clean the istructs
                (2.1) we clean the wrong istructs
                (2.2) we clean the equivalent istructs
            (3) istructs -> istructs_ok ---> (sort) ---> istructs_ok

    """
    anonymize_the_unknown_chars = \
                                dstring_object.options["anonymize the unknown characters"] == 'yes'

    # list of InternalStructure objects.
    istructs = ListOfInternalStructures(anonymize_the_unknown_chars)

    # we add an empty istruct to create a starting-point for the
    # big loop (for istruct in istructs, see below).
    istructs.append( InternalStructure(dstring_object=None) )

    #...........................................................................
    # (1) we cut the <dstring_object> into several <istructs>
    #...........................................................................
    for index_dchar, dchar in enumerate(dstring_object):

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # initialization of <future_istructs> from <dchar> :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        future_istructs = ListOfInternalStructures(anonymize_the_unknown_chars)
        dchar_used_at_least_onetime = False

        if dchar.unknown_char:
            # unknown character :
            dchar_used_at_least_onetime = True
            future_istructs.append( InternalStructure(
                dstring_object=None,
                unknown_character = True,
                punctuation_or_other_symbol = dchar.base_char ))
            future_istructs[-1].indexes.add( index_dchar )

        elif dchar.base_char in SYMB_PUNCTUATION or dchar.base_char in SYMB_OTHER_SYMBOLS:
            # punctuation/other symbol ?
            dchar_used_at_least_onetime = True
            future_istructs.append(
                InternalStructure(dstring_object=None,
                                  punctuation_or_other_symbol = dchar.base_char ) )
            future_istructs[-1].indexes.add( index_dchar )

        else:

            for istruct in istructs:
                # it may happen that istruct.indexes is empty : it's normal since we
                # have to start new istructs from nothing.

                # prefix ?
                if dchar.base_char in PREFIXES and \
                   (dchar.vowel1 is None or dchar.vowel1 == 'A') and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   (dchar.subj_consonants is None) and \
                   not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.prefix is None and \
                   istruct.consonant is None and \
                   istruct.subfix is None and \
                   (istruct.vowel1 is None or istruct.vowel2 is None == 'A') and \
                   (istruct.vowel1 is None or istruct.vowel2 is None == 'A') and \
                   istruct.suffix1 is None and \
                   istruct.suffix2 is None:

                    dchar_used_at_least_onetime = True

                    # prefix-1 : we add dchar.base_char as a prefix to the last istruct:
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].prefix = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                # superfix ?
                if dchar.base_char in SUPERFIXES and \
                   (dchar.subj_consonants is not None) and \
                   not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.superfix is None and \
                   istruct.consonant is None and \
                   istruct.subfix is None and \
                   (istruct.vowel1 is None or istruct.vowel2 is None == 'A') and \
                   (istruct.vowel1 is None or istruct.vowel2 is None == 'A') and \
                   istruct.suffix1 is None and \
                   istruct.suffix2 is None:

                    dchar_used_at_least_onetime = True

                    # superfix-1 : we add dchar.base_char as a superfix to the last istruct:
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].superfix = dchar.base_char
                    future_istructs[-1].consonant = dchar.subj_consonants[0]
                    future_istructs[-1].indexes.add( index_dchar )

                    # superfix-2(vowel) : we set the vowel of the last istruct :
                    future_istructs[-1].vowel1 = dchar.vowel1
                    future_istructs[-1].vowel2 = dchar.vowel2
                    # "halanta" symbol :
                    future_istructs[-1].halanta = dchar.halanta
                    # "rnam bcad" symbol :
                    future_istructs[-1].rnam_bcad = dchar.rnam_bcad
                    # "anusvara/candrabindu" symbol :
                    future_istructs[-1].anusvara_candrabindu = dchar.anusvara_candrabindu

                    # superfix-3(subfix) : we set the subfix consonant(s) of
                    # the last istruct :
                    if future_istructs[-1].subfix is None:
                        future_istructs[-1].subfix = []

                    for subj_c in dchar.subj_consonants[1:]:
                        future_istructs[-1].subfix.append( subj_c )


                # main consonant ?
                if not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.consonant is None and \
                   (istruct.vowel1 is None or istruct.vowel1 == 'A') and \
                   (istruct.vowel2 is None or istruct.vowel2 == 'A') and \
                   istruct.suffix1 is None and \
                   istruct.suffix2 is None:

                    dchar_used_at_least_onetime = True

                    # consonant-1 : we add dchar.base_char as the main consonant of
                    # the last istruct:
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].consonant = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                    # consonant-2(vowel) : we set the vowel of the last istruct :
                    future_istructs[-1].vowel1 = dchar.vowel1
                    future_istructs[-1].vowel2 = dchar.vowel2
                    # "halanta" symbol :
                    future_istructs[-1].halanta = dchar.halanta
                    # "rnam bcad" symbol :
                    future_istructs[-1].rnam_bcad = dchar.rnam_bcad
                    # "anusvara/candrabindu" symbol :
                    future_istructs[-1].anusvara_candrabindu = dchar.anusvara_candrabindu

                    # consonant-3(subfix) : we set the subfix consonant(s) of
                    # the last istruct :
                    if dchar.subj_consonants is not None:

                        if future_istructs[-1].subfix is None:
                            future_istructs[-1].subfix = []

                        for subj_c in dchar.subj_consonants:
                            future_istructs[-1].subfix.append( subj_c )

                if dchar.base_char in SUFFIXES1 and \
                   dchar.subj_consonants is None and \
                   (dchar.vowel1 is None or dchar.vowel1 == 'A') and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.consonant is not None and \
                   istruct.suffix1 is None and \
                   istruct.suffix2 is None:

                    dchar_used_at_least_onetime = True

                    # suffix1-1 : we add dchar.base_char as the suffix1 of the last istruct:
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].suffix1 = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                # suffix of the second kind ?
                if dchar.base_char in SUFFIXES2 and \
                   not istruct.unknown_character and \
                   (dchar.vowel1 is None or dchar.vowel1 == 'A') and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   dchar.subj_consonants is None and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.consonant is not None and \
                   istruct.suffix1 is not None and \
                   istruct.suffix2 is None:

                    dchar_used_at_least_onetime = True

                    # suffix2-1 : we add dchar.base_char as the suffix2 of the last istruct:
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].suffix2 = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                # postsuffix 'u ?
                if dchar.base_char == "-" and \
                   dchar.vowel1 == "U" and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.suffix1 is None and \
                   istruct.suffix2 is None and \
                   istruct.indexes_are_contiguous_to( [index_dchar,] ) and \
                   istruct.consonant is not None:
                    dchar_used_at_least_onetime = True

                    # we add dchar.base_char as the "postsuffix 'u" of the last istruct :
                    future_istructs.append( deepcopy(istruct) )
                    future_istructs[-1].postsuffix_u = True
                    future_istructs[-1].indexes.add( index_dchar )

            #...................................................................
            if dchar.base_char in SYMB_CONSONANTS:

                dchar_used_at_least_onetime = True

                # prefix of a new future istruct :
                if dchar.subj_consonants is None and \
                   (dchar.vowel1 is None or dchar.vowel1 == 'A') and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   dchar.base_char in PREFIXES:

                    future_istructs.append( InternalStructure(dstring_object=None) )
                    future_istructs[-1].prefix = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                # superfix of a new future istruct :
                if dchar.subj_consonants is None and \
                   (dchar.vowel1 is None or dchar.vowel1 == 'A') and \
                   (dchar.vowel2 is None or dchar.vowel2 == 'A') and \
                   dchar.base_char in SUPERFIXES:

                    future_istructs.append( InternalStructure(dstring_object=None) )
                    future_istructs[-1].superfix = dchar.base_char
                    future_istructs[-1].indexes.add( index_dchar )

                # consonant of a new future istruct :
                future_istructs.append( InternalStructure(dstring_object=None) )
                future_istructs[-1].consonant = dchar.base_char
                future_istructs[-1].vowel1 = dchar.vowel1
                future_istructs[-1].vowel2 = dchar.vowel2
                if dchar.subj_consonants is not None:
                    future_istructs[-1].subfix = dchar.subj_consonants
                future_istructs[-1].indexes.add( index_dchar )
                future_istructs[-1].anusvara_candrabindu = dchar.anusvara_candrabindu
                future_istructs[-1].rnam_bcad = dchar.rnam_bcad
                future_istructs[-1].halanta = dchar.halanta

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # if <dchar> has not be used, we add an InternalStructure object marked as
        # unknown character :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if not dchar_used_at_least_onetime:
            # we add an istruct concerning <dchar>, marked as "unknown character" :
            future_istructs.append( InternalStructure(dstring_object=None,
                                                      unknown_character = True,
                                                      punctuation_or_other_symbol = dchar.base_char,
                                                      ))
            future_istructs[-1].indexes.add( index_dchar )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # <istructs> += <future_istructs>  :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        istructs += future_istructs

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # we clean the doublets :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # doublets :
        for index_istruct, istruct in enumerate(istructs):
            for index_istruct2, istruct2 in enumerate(istructs):

                if index_istruct != index_istruct2 and \
                   not istruct.bad_internalstruct and \
                   not istruct2.bad_internalstruct:
                    if istruct.is_identical_to(istruct2):
                        istruct2.bad_internalstruct = True

        istructs.clean_off_bad_internalstructs()

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (2) we clean the istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (2.1) we clean the wrong istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:

        # an istruct without indexes ? bad istruct :
        if len(istruct.indexes) ==  0:
            istruct.bad_internalstruct = True

        # a prefix without a main consonant ? bad istruct :
        if istruct.prefix is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True
        # a superfix without a main consonant ? bad istruct :
        if istruct.superfix is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True
        # a suffix without a main consonant ? bad istruct :
        if istruct.suffix1 is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True
        # a suffix2 without a suffix1 ? bad istruct :
        if istruct.suffix2 is not None and istruct.suffix1 is None:
            istruct.bad_internalstruct = True

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (2.2) we clean the equivalent istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for index1, istruct1 in enumerate(istructs):
        for index2, istruct2 in enumerate(istructs):

            if index1 != index2 and \
               not istruct1.bad_internalstruct and \
               not istruct2.bad_internalstruct and \
               istruct1.indexes == istruct2.indexes:

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (a) Equivalent istructs :
                #
                # prefix=STR1; superfix=0; consonant=STR2; subfix=[STR3, ...]
                # prefix=STR1; superfix=STR2; consonant=STR3; subfix=[...]
                #
                # ... we keep the second istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix == istructs[index_y].prefix and \
                       istructs[index_x].superfix is None and \
                       istructs[index_x].consonant == istructs[index_y].superfix and \
                       istructs[index_x].subfix is not None and \
                       istructs[index_x].subfix[0] == istructs[index_y].consonant:

                        istructs[index_x].bad_internalstruct = True

    istructs.clean_off_bad_internalstructs()

    #...........................................................................
    # (3) istructs -> istructs_ok ---> (sort) ---> istructs_ok
    #...........................................................................
    # we get all istructs :
    # (1) which are not conflicting with the indexes of the others istructs
    #     whose indexes' length is smaller.
    # (2) wich are unique concerning their indexes (we don't want to have an
    #     istruct with indexes={0} accepted in istructs_ok and another
    #     one istruct with, too, indexes={0} rejected as having indexes in
    #     common with the first one : both istructs must be rejected.
    # (3 which are sorted by the indexes' length, in reversed order (longest first)
    #
    # point (2) are (3) are under the responsibility of rsort_by_indexes_len__u_items
    istructs_ok = ListOfInternalStructures(anonymize_the_unknown_chars)
    for new_istruct in istructs.rsort_by_indexes_len__u_items():

        keep_this_istruct = True
        for istruct in istructs_ok:
            if istruct != new_istruct and \
               istruct.have_indexes_common_with(new_istruct) and \
               len(istruct.indexes) >= len(new_istruct.indexes):

                keep_this_istruct = False
                break

        if keep_this_istruct:
            # we can add the new istruct to istructs_ok :
            istructs_ok.append( new_istruct )

    sorted_istructs_ok = sorted( istructs_ok, key=InternalStructure.get_min_of_indexes)
    istructs_ok = ListOfInternalStructures(
        anonymize_the_unknown_chars =\
                            dstring_object.options["anonymize the unknown characters"] == 'yes' )

    istructs_ok.extend( sorted_istructs_ok )

    #...........................................................................
    # we can set the .dstring_object attribute :
    #...........................................................................
    for istruct in istructs_ok:
        istruct.dstring_object = dstring_object

    return istructs_ok

#///////////////////////////////////////////////////////////////////////////////
def get_intstruct_from_str(_src,
                           dstring_object):
    """
        function get_intstruct_from_str()

        _src    : (str) Tibetan string like "ཀ"

        Return a ListOfInternalStructures object

        This function CAN BE VERY SLOW for long <_src> strings if no buffer is used.

        .. code-block:: python

            ************
            * CONTENTS *
            ************

            (1) the quickest way to answer is to look in the buffer
            (2) the big loop
                (2.1) initialization of <future_istructs> from <char> :
                (2.2) halanta
                (2.3) rnam bcad
                (2.4) anusvara/candrabindu
                (2.5) other characteristics
                      (2.5.1) punctuation symbol
                      (2.5.2) other symbol
                      (2.5.3) everything but punctuation symbol or the so-called "other symbol"
                              (2.5.3.1) no subjoined consonant
                              (2.5.3.2) one subjoined consonant
                              (2.5.3.3) at least two subjoined consonant
                              (2.5.3.4) vowels & diacritic signs for all new future istructs
                                        having a new main consonant
                              (2.5.3.5) we add the postsuffix 'u to (a copy of) the current istruct
                      (2.5.4) we clean the doublets
                      (2.5.5) postsuffixes འིས ('is), འམ ('am), འང ('ang), འི ('i)
                      (2.5.6) postsuffix འོ ('o)
            (3) finishing off
                (3.1) we clean the wrong istructs
                (3.2) we clean the equivalent istructs
                (3.3) special case : the 'oM' syllable
                (3.4) special cases : ambiguous syllables
                      (3.4.1) : "sra"
                      (3.4.2) : "rla"
                      (3.4.3) : "sla"
                      (3.4.4) : "rwa"
                      (3.4.5) : "lwa"
                      (3.4.6) : "swa"
                (3.5) the unknown characters are added
                (3.6) <istructs> is sorted
                (3.7) filling the buffers
    """
    anonymize_the_unknown_chars = \
                 dstring_object.options["anonymize the unknown characters"] == 'yes'

    if len(_src) == 0:
        return ListOfInternalStructures(anonymize_the_unknown_chars)

    expected_structure = dstring_object.options["expected structure"] == 'yes'
    fill_the_buffers = dstring_object.options["fill the buffers"] == 'yes'
    look_up_in_the_buffers = dstring_object.options["look up in the buffers"] == 'yes'

    #...........................................................................
    # (1) the quickest way to answer is to look in the buffer
    #...........................................................................
    if expected_structure == 'Tibetan or Sanskrit' and look_up_in_the_buffers:
        if _src in bod_buffer.BUFFER__FROM_STR:
            return ListOfInternalStructures(anonymize_the_unknown_chars).init_from_pickle_repr(
                src = bod_buffer.BUFFER__FROM_STR[_src],
                dstring_object = dstring_object
                )

    #...........................................................................
    # (2) the big loop
    #...........................................................................
    # list of InternalStructure objects :
    istructs = ListOfInternalStructures(anonymize_the_unknown_chars)

    # we add an empty istruct to create a starting-point for the
    # big loop (for istruct in istructs, see below) :
    istructs.append( InternalStructure(dstring_object = None) )

    # <real_indexes> are defined from the source string, character by character but
    # <indexes> are defined from the string as it appeared to the regex :
    for real_index_char, char in enumerate(re.finditer( PATTERN, _src )):

        indexes = range(char.start(), char.end())

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.1) initialization of <future_istructs> from <char>
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        future_istructs = ListOfInternalStructures(anonymize_the_unknown_chars)

        data = char.groupdict()
        base_char   = data['basechar']
        # E.g.
        #       subj_consonants       = [ chr(0x0F90), chr(0x0FB1) ]
        #       subj_consonants__name = ['K', 'Y']
        subj_consonants = data['subj_consonants']
        if subj_consonants is None:
            subj_consonants__name = None
        else:
            subj_consonants__name = list(map(SYMB_SUBJOINED_CONSONANTS.get_the_name_for_this_symbol,
                                             subj_consonants))

        vowel1 = data['vowel1']
        vowel2 = data['vowel2']
        diacritics = data['diacritics']

        base_char__punctuation = SYMB_PUNCTUATION.get_the_name_for_this_symbol(base_char)
        base_char__other_symbols = SYMB_OTHER_SYMBOLS.get_the_name_for_this_symbol(base_char)
        base_char__consonant = SYMB_CONSONANTS.get_the_name_for_this_symbol(base_char)
        base_char__vowel1 = SYMB_VOWELS.get_the_name_for_this_symbol(vowel1)
        base_char__vowel2 = SYMB_VOWELS.get_the_name_for_this_symbol(vowel2)

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.2) halanta
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        halanta_nbr = number_of_occurences( source_string = diacritics,
                                            symbols = SYMB_DIACRITICS__HALANTA )

        if halanta_nbr > 1:
            err_msg = "In '{0}' (start={1}, end={2}), \
                      'halanta' defined several times."
            raise DCharsError( context = "ewts.py::get_intstruct_from_str",
                               message = err_msg.format(char.string,
                                                        char.start(),
                                                        char.end()))

        halanta = (halanta_nbr > 0)

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.3) rnam bcad
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        rnam_bcad_nbr = number_of_occurences( source_string = diacritics,
                                            symbols = SYMB_DIACRITICS__RNAM_BCAD )

        if rnam_bcad_nbr > 1:
            err_msg = "In '{0}' (start={1}, end={2}), \
                      'rnam_bcad' defined several times."
            raise DCharsError( context = "ewts.py::get_intstruct_from_str",
                               message = err_msg.format(char.string,
                                                        char.start(),
                                                        char.end()))

        rnam_bcad = (rnam_bcad_nbr > 0)

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.4) anusvara/candrabindu
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        anusvara_candrabindu_nbr = number_of_occurences( source_string = diacritics,
                                                         symbols = SYMB_DIACRITICS__ANUSV_CANDR )

        if anusvara_candrabindu_nbr > 1:
            err_msg = "In '{0}' (start={1}, end={2}), \
                      'anusvara_candrabindu' defined several times."
            raise DCharsError( context = "ewts.py::get_intstruct_from_str",
                               message = err_msg.format(char.string,
                                                        char.start(),
                                                        char.end()))

        anusvara_candrabindu = None
        for anusvara_candrabindu_char in SYMB_DIACRITICS__ANUSV_CANDR:
            anusvara_candrabindu_name = \
              SYMB_DIACRITICS.defaultsymbol2name[anusvara_candrabindu_char]

            if SYMB_DIACRITICS.are_these_symbols_in_a_string(name=anusvara_candrabindu_name,
                                                             string=diacritics):
                anusvara_candrabindu = anusvara_candrabindu_name
                break

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5) other characteristics
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.1) punctuation symbol
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        if base_char__punctuation is not None:
            # punctuation symbol :

            # we add a new internal structure :
            new_istruct = InternalStructure( dstring_object = None,
                                             punctuation_or_other_symbol = base_char__punctuation )

            future_istructs.append( new_istruct )
            future_istructs[-1].indexes.update( indexes )
            future_istructs[-1].real_indexes.add( real_index_char  )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.2) other symbol
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        elif base_char__other_symbols is not None:
            # "other symbol" : not punctuation nor consonant :

            # we add a new internal structure :
            new_istruct = InternalStructure(
                dstring_object = None,
                punctuation_or_other_symbol = base_char__other_symbols )

            future_istructs.append( new_istruct )
            future_istructs[-1].indexes.update( indexes )
            future_istructs[-1].real_indexes.add( real_index_char  )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.3) everything but punctuation symbols or the so-called "other symbols"
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        else:

            for index_istruct, istruct in enumerate(istructs):

                if not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None and \
                   istruct.indexes_are_contiguous_to( indexes ) and \
                   istruct.real_indexes_are_contiguous_to( [real_index_char,] ):

                    future_istructs_with_new_cons = []

                    if base_char__consonant is not None:

                        # (2.5.3.1) no subjoined consonant
                        if subj_consonants is None:

                            #...................................................
                            # <base_char__consonant> as a prefix
                            if base_char__consonant in PREFIXES and \
                               base_char__vowel1 is None and \
                               not rnam_bcad and \
                               anusvara_candrabindu is None and \
                               istruct.prefix is None and \
                               istruct.consonant is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].prefix = base_char__consonant
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                            #...................................................
                            # <base_char__consonant> as a superfix
                            if base_char__consonant in SUPERFIXES and \
                               base_char__vowel1 is None and \
                               subj_consonants is not None and \
                               not rnam_bcad and \
                               anusvara_candrabindu is None and \
                               istruct.prefix is None and \
                               istruct.consonant is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].superfix = base_char__consonant
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                            #...................................................
                            # <base_char__consonant> as a main consonant
                            if istruct.consonant is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].consonant = base_char__consonant
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                                # we have created a future istruct with a new main consonant :
                                future_istructs_with_new_cons.append(
                                    len(future_istructs)-1 )

                        # (2.5.3.2) one subjoined consonant
                        elif len(subj_consonants) == 1:

                            #...................................................
                            # base_char__consonant + subj_consonants[0] > MAIN CONSONANT + SUBFIX
                            if subj_consonants__name[0] in SUBFIXES and \
                               istruct.consonant is None and \
                               istruct.subfix is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].consonant = base_char__consonant
                                future_istructs[-1].subfix = [subj_consonants__name[0], ]
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                                # we have created a future istruct with a new main consonant :
                                future_istructs_with_new_cons.append(
                                    len(future_istructs)-1 )

                            #...................................................
                            # base_char__consonant + subj_consonants[0] > SUPERFIX + MAIN CONSONANT
                            if base_char__consonant in SUPERFIXES and \
                               istruct.superfix is None and \
                               istruct.consonant is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].superfix = base_char__consonant
                                future_istructs[-1].consonant = subj_consonants__name[0]
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                                # we have created a future istruct with a new main consonant :
                                future_istructs_with_new_cons.append(
                                    len(future_istructs)-1 )

                        # (2.5.3.3) at least two subjoined consonant
                        else:

                            #...................................................
                            # base_char__consonant + subj_consonants[0, 1, ...]
                            # > SUPERFIX + MAIN CONSONANT + SUBFIX
                            if base_char__consonant in SUPERFIXES and \
                               istruct.superfix is None and \
                               istruct.consonant is None and \
                               istruct.subfix is None:

                                future_istructs.append( deepcopy(istruct) )
                                future_istructs[-1].superfix = base_char__consonant
                                future_istructs[-1].consonant = subj_consonants__name[0]
                                future_istructs[-1].subfix = [subj_consonants__name[index] \
                                     for index in range(1, len(subj_consonants__name)) ]
                                future_istructs[-1].indexes.update( indexes )
                                future_istructs[-1].real_indexes.add( real_index_char  )

                                # we have created a future istruct with a new main consonant :
                                future_istructs_with_new_cons.append( len(future_istructs)-1 )

                        #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
                        # (2.5.3.4) vowels & diacritic signs for all new future istructs
                        # having a new main consonant
                        #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
                        for num_future_istruct in future_istructs_with_new_cons:

                            future_istruct = future_istructs[num_future_istruct]

                            # vowel(s) of the main consonant :
                            if base_char__vowel1 is not None and \
                               future_istruct.consonant is not None and \
                               future_istruct.vowel1 is None or istruct.vowel1 == 'A':

                                # vowel1 for the main consonant :
                                future_istruct.vowel1 = base_char__vowel1
                                future_istruct.indexes.update( indexes )
                                future_istruct.real_indexes.add( real_index_char  )

                            elif not halanta:
                                # default vowel for a main consonant:
                                future_istruct.vowel1 = 'A'

                            if base_char__vowel2 is not None and \
                               future_istruct.consonant is not None and \
                               future_istruct.vowel1 is not None and \
                               future_istruct.vowel2 is None:

                                future_istruct.vowel2 = base_char__vowel2
                                future_istruct.indexes.update( indexes )
                                future_istruct.real_indexes.add( real_index_char  )

                            # halanta ?
                            future_istruct.halanta = halanta

                            # anusvara/candrabindu ?
                            future_istruct.anusvara_candrabindu = anusvara_candrabindu

                            # rnam bcad ?
                            future_istruct.rnam_bcad = rnam_bcad

                        #.......................................................
                        # (2.5.3.5) we add the postsuffix 'u to (a copy of) the current istruct
                        #.......................................................
                        if base_char__consonant == '-' and \
                           base_char__vowel1 == 'U' and \
                           base_char__vowel2 is None and \
                           subj_consonants is None and \
                           diacritics is None and \
                           istruct.consonant is not None:
                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].postsuffix_u = True
                            future_istructs[-1].indexes.update( indexes )
                            future_istructs[-1].real_indexes.add( real_index_char  )

                        #.......................................................
                        # a suffix1 ?
                        #.......................................................
                        if base_char__consonant in SUFFIXES1 and \
                           subj_consonants is None and \
                           (base_char__vowel1 is None or base_char__vowel1 == 'A') and \
                           istruct.consonant is not None and \
                           istruct.vowel1 is not None and \
                           istruct.suffix1 is None and \
                           not istruct.postsuffix_u and \
                           not istruct.gramm_postsuffix and \
                           not istruct.postsuffix_o:

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].suffix1 = base_char__consonant
                            future_istructs[-1].rnam_bcad = rnam_bcad
                            future_istructs[-1].anusvara_candrabindu = anusvara_candrabindu
                            future_istructs[-1].indexes.update( indexes )
                            future_istructs[-1].real_indexes.add( real_index_char  )

                        #.......................................................
                        # a suffix2 ?
                        #.......................................................
                        if base_char__consonant in SUFFIXES2 and \
                           subj_consonants is None and \
                           istruct.consonant is not None and \
                           istruct.suffix1 is not None and \
                           istruct.suffix2 is None and \
                           not istruct.postsuffix_u and \
                           not istruct.gramm_postsuffix and \
                           not istruct.postsuffix_o:

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].suffix2 = base_char__consonant
                            future_istructs[-1].rnam_bcad = rnam_bcad
                            future_istructs[-1].anusvara_candrabindu = anusvara_candrabindu
                            future_istructs[-1].indexes.update( indexes )
                            future_istructs[-1].real_indexes.add( real_index_char  )

                        #.......................................................
                        # we create new istructs :
                        #.......................................................
                        # a prefix ?
                        if base_char__consonant in PREFIXES and \
                           base_char__vowel1 is None and \
                           not rnam_bcad and \
                           anusvara_candrabindu is None and \
                           subj_consonants is None:

                            future_istructs.append(
                                InternalStructure(dstring_object = None,
                                                  prefix = base_char__consonant) )
                            future_istructs[-1].indexes.update( indexes )
                            future_istructs[-1].real_indexes.add( real_index_char  )

                        # a main consonant, maybe followed by subfix consonant(s) ?
                        # vowel's choice :
                        _base_char__vowel1 = deepcopy(base_char__vowel1)
                        _base_char__vowel2 = deepcopy(base_char__vowel2)
                        if halanta:
                            _base_char__vowel1 = None
                        elif base_char__vowel1 is None:
                            _base_char__vowel1 = 'A'

                        future_istructs.append( InternalStructure(
                            dstring_object = None,
                            consonant = base_char__consonant,
                            halanta = halanta,
                            anusvara_candrabindu = anusvara_candrabindu,
                            rnam_bcad = rnam_bcad,
                            vowel1 = _base_char__vowel1,
                            vowel2 = _base_char__vowel2))

                        if subj_consonants is not None:
                            future_istructs[-1].subfix = subj_consonants__name

                        future_istructs[-1].indexes.update( indexes )
                        future_istructs[-1].real_indexes.add( real_index_char  )

                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                # we have to keep the current istruct as one of the future istructs :
                #
                # E.g., let read the word "khi'is", id est khi + suffix 'is.
                # The program will read khi'i as 'i is a valid suffix so we have to
                # keep the word khi in memory; the program will read 'is as an
                # isolated word and will join "khi" and "'is" later.
                #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                future_istructs.append( deepcopy((istruct) ))

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # <istructs> += <future_istructs>  :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        istructs += future_istructs

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.4) we clean the doublets
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # doublets :
        for index_istruct, istruct in enumerate(istructs):
            for index_istruct2, istruct2 in enumerate(istructs):

                if index_istruct != index_istruct2 and \
                   not istruct.bad_internalstruct and \
                   not istruct2.bad_internalstruct:

                    if istruct.is_identical_to(istruct2):
                        istruct2.bad_internalstruct = True

        istructs.clean_off_bad_internalstructs()

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.5) postsuffixes འིས ('is), འམ ('am), འང ('ang), འི ('i)
        #
        # E.g. with འིས ('is) :
        # if we found an istruct equivalent to འིས ('is) we try to find another istruct which
        # could take 'is as a postsuffix (in gramm_postsuffix)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        new_istructs = []
        for postsuffix_name, consonant, vowel, suffix1 in (
                ("'i",  '-', "I", None),
                ("'is", '-', "I", 'S'),
                ("'am", '-', "A", 'M'),
                ("'ang",'-', "A", 'NG'),
                ):

            for index1, istruct1 in enumerate(istructs):

                if istruct1.prefix is None and \
                   istruct1.consonant == consonant and \
                   istruct1.vowel1 == vowel and \
                   istruct1.vowel2 is None and \
                   istruct1.subfix is None and \
                   istruct1.suffix1 == suffix1 and \
                   istruct1.suffix2 is None and \
                   not istruct1.postsuffix_u and \
                   istruct1.gramm_postsuffix is None:

                    # we have istruct1 as an istruct equivalent to 'is/'am/... ; let's try to find
                    # istruct0 as an istruct which could take 'is/'am/... as a postsuffix :
                    #
                    # NB :
                    # (a) we don't want to modify the istruct without
                    #     indexes [ len(index0.indexes)>0 ]
                    # (b) we don't want to analyse old istructs, hence the condition :
                    #      (index_char in istruct0.indexes or index_char in istruct1.indexes)
                    # (c) we have to check if istruct0 is placed just before istruct1
                    #     [ call to indexes_are_contiguous() functions ]
                    for index0, istruct0 in enumerate(istructs):

                        if index0 != index1 and \
                           (real_index_char in istruct0.real_indexes or \
                            real_index_char in istruct1.real_indexes) and \
                           len(istruct0.indexes)>0 and \
                           not istruct0.unknown_character and \
                           istruct0.punctuation_or_other_symbol is None and \
                           istruct0.suffix1 is None and \
                           istruct0.suffix2 is None and \
                           istruct0.gramm_postsuffix is None and \
                           istruct0.indexes_are_contiguous_to( istruct1.indexes ) and \
                           istruct0.real_indexes_are_contiguous_to( istruct1.real_indexes ):

                            # ok, istruct0 will take 'is/'am/... as a postsuffix :
                            new_istruct = deepcopy( istruct0 )
                            new_istruct.gramm_postsuffix = postsuffix_name
                            new_istruct.indexes.update( istruct1.indexes )
                            new_istruct.real_indexes.update( istruct1.real_indexes )
                            new_istructs.append( new_istruct )

        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # (2.5.6) postsuffix འོ ('o)
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        for index1, istruct1 in enumerate(istructs):

            if istruct1.prefix is None and \
               istruct1.consonant == "-" and \
               istruct1.vowel1 == "O" and \
               istruct1.vowel2 is None and \
               istruct1.subfix is None and \
               istruct1.suffix1 is None and \
               istruct1.suffix2 is None and \
               not istruct1.postsuffix_u and \
               istruct1.gramm_postsuffix is None:

                # we have istruct1 as an istruct equivalent to 'o; let's try to find
                # istruct0 as an istruct which could take 'o as a postsuffix :
                #
                # NB :
                # (a) we don't want to modify the istruct whithout indexes [ len(index0.indexes)>0 ]
                # (b) we have to check if istruct0 is placed just before istruct1
                #     [ call to indexes_are_contiguous() functions ]
                for index0, istruct0 in enumerate(istructs):

                    if index0 != index1 and \
                       (real_index_char in istruct0.real_indexes or \
                        real_index_char in istruct1.real_indexes) and \
                       len(istruct0.indexes)>0 and \
                       not istruct0.unknown_character and \
                       istruct0.punctuation_or_other_symbol is None and \
                       istruct0.suffix1 is None and \
                       istruct0.suffix2 is None and \
                       not istruct0.postsuffix_o and \
                       istruct0.indexes_are_contiguous_to( istruct1.indexes ) and \
                       istruct0.real_indexes_are_contiguous_to( istruct1.real_indexes ):

                        # ok, istruct0 will take 'o as a postsuffix :
                        new_istruct = deepcopy( istruct0 )
                        new_istruct.postsuffix_o = True
                        new_istruct.indexes.update( istruct1.indexes )
                        new_istruct.real_indexes.update( istruct1.real_indexes )
                        new_istructs.append( new_istruct )

        istructs += new_istructs

    istructs.clean_off_bad_internalstructs()

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3) finishing off
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.1) we clean the wrong istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:

        # an istruct without indexes ? bad istruct :
        if len(istruct.indexes) ==  0:
            istruct.bad_internalstruct = True

        # an istruct with superfix without any main consonant ? bad istruct :
        if istruct.superfix is not None and \
           istruct.consonant is None:
            istruct.bad_internalstruct = True

        # an istruct with subfix without any main consonant ? bad istruct :
        if istruct.subfix is not None and \
           istruct.consonant is None:
            istruct.bad_internalstruct = True

        # a prefix without a main consonant ? bad istruct :
        if istruct.prefix is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True

        # # a suffix without a main consonant ? bad istruct :
        # if istruct.suffix1 is not None and istruct.consonant is None:
        #     istruct.bad_internalstruct = True
        # # a suffix2 without a suffix1 ? bad istruct :
        # if istruct.suffix2 is not None and istruct.suffix1 is None:
        #     istruct.bad_internalstruct = True

    istructs.clean_off_bad_internalstructs()

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.2) we clean the equivalent istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for index1, istruct1 in enumerate(istructs):
        for index2, istruct2 in enumerate(istructs):

            if index1 != index2 and \
               not istruct1.bad_internalstruct and \
               not istruct2.bad_internalstruct and \
               istruct1.indexes == istruct2.indexes:

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (a) Equivalent istructs :
                #
                # prefix=STR1; superfix=0; consonant=STR2; suffix1=None
                # prefix=None; superfix=0; consonant=STR1; suffix1=STR2
                #
                # ... we keep the second istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix == istructs[index_y].consonant and \
                       istructs[index_x].superfix is None and \
                       istructs[index_x].superfix == istructs[index_y].superfix and \
                       istructs[index_x].consonant == istructs[index_y].suffix1:

                        istructs[index_x].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (b) Equivalent istructs :
                #
                # prefix=STR1; superfix=0; consonant=-A; vowel1=I
                # prefix=None; superfix=0; consonant=STR1; suffix1=suffix=None gramm_postsuffix='i
                #
                # ... we keep the second istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix == istructs[index_y].consonant and \
                       istructs[index_x].superfix is None and \
                       istructs[index_x].superfix == istructs[index_y].superfix and \
                       istructs[index_x].consonant == "-":

                        istructs[index_x].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (c) Equivalent istructs :
                #
                # prefix0=0; superfix=STR1; consonant=STR2; subfix=None
                # prefix0=0; superfix=0;    consonant=STR1; subfix=[STR2,]
                #
                # ... we keep the first istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix is None and \
                       istructs[index_x].prefix == istructs[index_y].prefix and \
                       istructs[index_x].superfix == istructs[index_y].consonant and \
                       istructs[index_y].superfix is None and \
                       istructs[index_x].subfix is None and \
                       istructs[index_y].subfix is not None and \
                       len(istructs[index_y].subfix)==1 and \
                       istructs[index_x].consonant == istructs[index_y].subfix[0]:

                        istructs[index_y].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (d) Equivalent istructs :
                #
                # prefix0=0; superfix=STR1; consonant=STR2; subfix=[STR3, ...]
                # prefix0=0; superfix=0;    consonant=STR1; subfix=[STR2, STR3, ...]
                #
                # ... we keep the first istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix is None and \
                       istructs[index_x].prefix == istructs[index_y].prefix and \
                       istructs[index_x].superfix == istructs[index_y].consonant and \
                       istructs[index_y].superfix is None and \
                       istructs[index_x].subfix is not None and \
                       istructs[index_y].subfix is not None and \
                       len(istructs[index_y].subfix)>=2 and \
                       istructs[index_x].consonant == istructs[index_y].subfix[0] and \
                       istructs[index_x].subfix[0] == istructs[index_y].subfix[1]:

                        istructs[index_y].bad_internalstruct = True

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.3) special case : the 'oM' syllable
    #
    #       if a syllable is equivalent to "oM" it's not
    #       VOWEL=O+CANDRABINDU(=RJES SU NGA RO), it's simply the
    #       symbol oM.
    #
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.check_default_value(consonant = "A",
                                       vowel1 = 'O',
                                       anusvara_candrabindu = 'SIGN RJES SU NGA RO'):

            istruct.punctuation_or_other_symbol = 'SYLLABLE OM'
            istruct.anusvara_candrabindu = None
            istruct.vowel1 = None
            istruct.consonant = None

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4) special cases : ambiguous syllables
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.1) : "sra"
    #
    # "sra" : (consonant)S + (subfix)R [@@BOD-INTERNALSTRUCTURE-001]
    #
    #       special case : prefix=0, superfix='S', consonant='R', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='S', subfix=['R', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'S' and \
           istruct.consonant == 'R':

            istruct.superfix = None
            istruct.consonant = 'S'
            if istruct.subfix is None:
                istruct.subfix = ['R',]
            else:
                istruct.subfix.insert(0, "R")

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.2) : "rla"
    #
    # "rla" : (consonant)R + (subfix)L [@@BOD-INTERNALSTRUCTURE-002]
    #
    #       special case : prefix=0, superfix='R', consonant='L', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='R', subfix=['L', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'R' and \
           istruct.consonant == 'L':

            istruct.superfix = None
            istruct.consonant = 'R'
            if istruct.subfix is None:
                istruct.subfix = ['L',]
            else:
                istruct.subfix.insert(0, "L")

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.3) : "sla"
    #
    # "sla" : (consonant)S + (subfix)L [@@BOD-INTERNALSTRUCTURE-003]
    #
    #       special case : prefix=0, superfix='S', consonant='L', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='S', subfix=['L', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'S' and \
           istruct.consonant == 'L':

            istruct.superfix = None
            istruct.consonant = 'S'
            if istruct.subfix is None:
                istruct.subfix = ['L',]
            else:
                istruct.subfix.insert(0, "L")

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.4) : "rwa"
    #
    # "rwa" : (consonant)R + (subfix)W [@@BOD-INTERNALSTRUCTURE-004]
    #
    #       special case : prefix=0, superfix='R', consonant='W', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='R', subfix=['W', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'R' and \
           istruct.consonant == 'W':

            istruct.superfix = None
            istruct.consonant = 'R'
            if istruct.subfix is None:
                istruct.subfix = ['W',]
            else:
                istruct.subfix.insert(0, "W")

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.5) : "lwa"
    #
    # "lwa" : (consonant)L + (subfix)W [@@BOD-INTERNALSTRUCTURE-005]
    #
    #       special case : prefix=0, superfix='L', consonant='W', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='R', subfix=['W', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'L' and \
           istruct.consonant == 'W':

            istruct.superfix = None
            istruct.consonant = 'L'
            if istruct.subfix is None:
                istruct.subfix = ['W',]
            else:
                istruct.subfix.insert(0, "W")

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (3.4.6) : "swa"
    #
    # "swa" : (consonant)L + (subfix)W [@@BOD-INTERNALSTRUCTURE-006]
    #
    #       special case : prefix=0, superfix='S', consonant='W', subfix=[...]
    #       must be treated as if we have :
    #                      prefix=0, superfix=0,   consonant='S', subfix=['W', ...]
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix == 'S' and \
           istruct.consonant == 'W':

            istruct.superfix = None
            istruct.consonant = 'S'
            if istruct.subfix is None:
                istruct.subfix = ['W',]
            else:
                istruct.subfix.insert(0, "W")

    istructs.clean_off_bad_internalstructs()

    #...........................................................................
    # (3.5) the unknown characters are added
    # istructs -> istructs
    #...........................................................................
    # we add the unknown characters, i.e. we add an istruct object linked to
    # every index not covered by the istructs.
    #...........................................................................
    indexes_ok = set()
    for istruct in istructs:
        indexes_ok.update( istruct.indexes )

    for index in range(0, len(_src)):
        if index not in indexes_ok:
            istructs.append ( InternalStructure( dstring_object = None,
                                                 unknown_character = True,
                                                 punctuation_or_other_symbol = _src[index],
                                                 indexes = OrderedSet( [index,]) ))

    #...........................................................................
    # (3.6) <istructs> is sorted
    # istructs ---> res.get_the_complete_records() ----> res
    #...........................................................................
    complete_records = istructs.get_the_complete_records( last_index = len(_src)-1,
                                                          use_real_indexes = False )

    if len(complete_records) != 1:
        msg = "Zero or more than one lists of istructs describe the source string : "
        raise DCharsError( context = "ewts.py::get_intstruct_from_str()",
                           message = msg+str(complete_records) )
    else:
        complete_records = complete_records[0]

    res = ListOfInternalStructures(anonymize_the_unknown_chars)
    for index in complete_records:
        res.append( istructs[index] )

    #...........................................................................
    # (3.7) filling the buffers
    #...........................................................................
    if fill_the_buffers and \
       _src not in bod_buffer.BUFFER__FROM_STR and \
       not res.contains_unknown_characters():
        bod_buffer.BUFFER__FROM_STR[_src] = res.pickle_repr()

    #...........................................................................
    # we can set the .dstring_object attribute :
    #...........................................................................
    for istruct in res:
        istruct.dstring_object = dstring_object

    return res
