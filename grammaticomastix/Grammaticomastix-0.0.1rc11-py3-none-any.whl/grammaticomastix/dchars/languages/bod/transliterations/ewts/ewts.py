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
    ❏DChars❏ : dchars/languages/bod/transliterations/ewts/ewts.py
"""

import re
from copy import deepcopy

from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.errors.errors import DCharsError
from dchars.utilities.orderedset import OrderedSet

from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

from dchars.languages.bod.syllabic_structure import SUPERFIXES_ROOT_SUBFIXES, \
                                                    COMMON_CONSONANTS_STACK, \
                                                    PREFIXES, \
                                                    SUPERFIXES, \
                                                    SUFFIXES1, \
                                                    SUFFIXES2

import dchars.languages.bod.transliterations.ewts.ewts_buffer as ewts_buffer

from dchars.languages.bod.internalstructure import ListOfInternalStructures, \
                                                   InternalStructure

from dchars.languages.bod.transliterations.ewts.ewts_symbols import \
                CONSONANTS, CONSONANTS_INVERSED, \
                VOWELS, VOWELS_INVERSED, \
                OTHER_SYMBOLS, OTHER_SYMBOLS_INVERSED, \
                PUNCTUATION, PUNCTUATION_INVERSED, \
                DIACRITICS, DIACRITICS_INVERSED

################################################################################
# List of the available directions for this transliteration method :
#
#  +1 (text->transliteration)
#  -1 (transliteration->text)
#
################################################################################
AVAILABLE_DIRECTIONS = (-1, +1)

################################################################################
# transliteration's patterns :
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.

TRANS_DOT_OR_PLUS = isort_a_lstrings_bylen_nodup(
                    regexstring_list( ('+', '.') ))
TRANS_PUNCTUATION_AND_OTHER_SYMBOL = isort_a_lstrings_bylen_nodup(
                      regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                      regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )
TRANS_CONSONANTS_AND_VOWELS = isort_a_lstrings_bylen_nodup(
                      regexstring_list(tuple(CONSONANTS_INVERSED.keys())) + \
                      regexstring_list(tuple(VOWELS_INVERSED.keys())) )
TRANS_RNAM_BCAD = isort_a_lstrings_bylen_nodup(
                      regexstring_list( (DIACRITICS['SIGN RNAM BCAD'])) )
TRANS_HALANTA = isort_a_lstrings_bylen_nodup(
                      regexstring_list( (DIACRITICS['MARK HALANTA'])) )
TRANS_ANUSVARA_CANDRABINDU = isort_a_lstrings_bylen_nodup(
                      regexstring_list( (DIACRITICS['SIGN RJES SU NGA RO'],
                                         DIACRITICS['SIGN NYI ZLA NAA DA'],
                                         DIACRITICS['SIGN SNA LDAN'] )))

TRANS_PATTERN_TXT = "(?P<dotpointorplus>({0}))?" \
              "(?P<base_char>({1}))" \
              "(?P<halanta>({2}))?" \
              "(?P<anusvara_candrabindu>({3}))?" \
              "(?P<rnam_bcad>({4}))?".format(
    "|".join(prepare_list_to_strformat(TRANS_DOT_OR_PLUS)),
    "|".join(prepare_list_to_strformat(TRANS_CONSONANTS_AND_VOWELS) + \
             prepare_list_to_strformat(TRANS_PUNCTUATION_AND_OTHER_SYMBOL)),
    "|".join(prepare_list_to_strformat(TRANS_HALANTA)),
    "|".join(prepare_list_to_strformat(TRANS_ANUSVARA_CANDRABINDU)),
    "|".join(prepare_list_to_strformat(TRANS_RNAM_BCAD)),
             )

TRANS_PATTERN_TXT = TRANS_PATTERN_TXT.replace('{{', '{')
TRANS_PATTERN_TXT = TRANS_PATTERN_TXT.replace('}}', '}')
TRANS_PATTERN = re.compile(TRANS_PATTERN_TXT)

#///////////////////////////////////////////////////////////////////////////////
def get_intstruct_from_trans_str( _src, dstring_object ):
    """
        function get_intstruct_from_trans_str()

        _src    : (str) transliterated string like "ka".

        Return a ListOfInternalStructures object.

        This function CAN BE VERY SLOW on big <_src>.

        arguments : list of argument. For this function :
                arguments = [ (str)source string,
                              (bool)expected_structure,
                              (bool)look_up_in_the_buffers,
                              (bool)fill_the_buffers ]
    """

    expected_structure = dstring_object.options["expected structure"]
    look_up_in_the_buffers = dstring_object.options["look up in the buffers"] == 'yes'
    fill_the_buffers = dstring_object.options["fill the buffers"] == 'yes'
    anonymize_the_unknown_chars = \
                                 dstring_object.options["anonymize the unknown characters"] == 'yes'

    if len(_src) == 0:
        return ListOfInternalStructures(
            anonymize_the_unknown_chars = anonymize_the_unknown_chars)

    #...........................................................................
    # the quickest way to answer is to look in the buffer :
    #...........................................................................
    if expected_structure == 'Tibetan or Sanskrit' and look_up_in_the_buffers:
        if _src in ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR:
            return ListOfInternalStructures(
                anonymize_the_unknown_chars = \
                anonymize_the_unknown_chars).init_from_pickle_repr(
                  src = ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR[_src],
                  dstring_object = dstring_object)

    #...........................................................................
    # the big loop
    #...........................................................................
    # list of InternalStructure objects.
    istructs = ListOfInternalStructures(
        anonymize_the_unknown_chars=anonymize_the_unknown_chars)
    # we add an empty istruct to create a starting-point for the
    # big loop (for istruct in istructs, see below) :
    istructs.append( InternalStructure(dstring_object = None) )

    # <real_indexes> are defined from the source string, character by character but
    # <indexes> are defined from the string as it appeared to the regex :
    #
    #        E.g. for the transliterated string "²nya²" (with 2 unknown characters ) :
    #              real_indexes : /²/n/y/a/²/ =0,1,2,3,4
    #              indexes :      /²/ny/a/²/  =0,1,2,3
    #
    for index_char, char in enumerate(re.finditer( TRANS_PATTERN, _src )):

        real_indexes = range(char.start(), char.end())

        # None / (str) '.' or '+'
        dotpointorplus = char.group('dotpointorplus')
        # None / (str)
        base_char = char.group('base_char')
        # (bool)
        halanta = char.group('halanta') is not None
        # None / (str)
        anusvara_candrabindu = char.group('anusvara_candrabindu')
        # (bool)
        rnam_bcad = char.group('rnam_bcad') is not None


        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        # initialization of <future_istructs> from <char> :
        #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        future_istructs = ListOfInternalStructures(
            anonymize_the_unknown_chars=anonymize_the_unknown_chars)

        if base_char in PUNCTUATION_INVERSED:
            # we add a new internal structure :
            new_istruct = InternalStructure(
                dstring_object = None,
                punctuation_or_other_symbol = PUNCTUATION_INVERSED[base_char])
            future_istructs.append( new_istruct )
            future_istructs[-1].indexes.add( index_char )
            future_istructs[-1].real_indexes.update( real_indexes  )

        elif base_char in OTHER_SYMBOLS_INVERSED:
            # we add a new internal structure :
            new_istruct = InternalStructure(
                dstring_object = None,
                punctuation_or_other_symbol = OTHER_SYMBOLS_INVERSED[base_char])
            future_istructs.append( new_istruct )
            future_istructs[-1].indexes.add( index_char )
            future_istructs[-1].real_indexes.update( real_indexes  )

        else:

            for index_istruct, istruct in enumerate(istructs):

                # we don't want to complete an unknown character, a punctuation
                # symbol or something equivalent (an other symbol) :
                if not istruct.unknown_character and \
                   istruct.punctuation_or_other_symbol is None:

                    # so we have something to complete :

                    # vowel :
                    if base_char in VOWELS_INVERSED and \
                       istruct.indexes_are_contiguous_to( [index_char,] ) and \
                       istruct.real_indexes_are_contiguous_to(real_indexes):

                        # we add a vowel1 to the current istruct :
                        if istruct.vowel1 is None and \
                           istruct.indexes_are_contiguous_to( [index_char,] ) and \
                           istruct.real_indexes_are_contiguous_to(real_indexes):

                            future_istructs.append( deepcopy(istruct) )

                            # we add the default consonant supporting vowel :
                            if future_istructs[-1].prefix is None and \
                               future_istructs[-1].consonant is None:

                                future_istructs[-1].consonant = "A"

                            future_istructs[-1].vowel1 = VOWELS_INVERSED[base_char]
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                            if anusvara_candrabindu is not None:

                                future_istructs[-1].anusvara_candrabindu = \
                                   DIACRITICS_INVERSED[anusvara_candrabindu]

                            if rnam_bcad:

                                future_istructs[-1].rnam_bcad = True

                        # we add a vowel2 to the current istruct :
                        if istruct.vowel1 is not None and \
                           dotpointorplus == '+' and istruct.vowel2 is None and \
                           istruct.indexes_are_contiguous_to( [index_char,] ) and \
                           istruct.real_indexes_are_contiguous_to(real_indexes):

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].vowel2 = VOWELS_INVERSED[base_char]
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                            # a "rnam bcad" symbol can follow a vowel, as in
                            # "གཏིཿ"="gtiH"
                            if rnam_bcad:
                                future_istructs[-1].rnam_bcad = True

                            # a anusvara/candrabindu symbol may follow a vowel :
                            if anusvara_candrabindu is not None:
                                future_istructs[-1].anusvara_candrabindu = \
                                  DIACRITICS_INVERSED[anusvara_candrabindu]

                        # we add postsuffix 'u to the current istruct :
                        if base_char == VOWELS['U'] and \
                           istruct.consonant is not None and \
                           istruct.vowel1 is not None and \
                           istruct.suffix1 == "-" and \
                           istruct.suffix2 is None and \
                           not istruct.postsuffix_u and \
                           istruct.indexes_are_contiguous_to( [index_char,] ) and \
                           istruct.real_indexes_are_contiguous_to(real_indexes):

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].suffix1 = None
                            future_istructs[-1].postsuffix_u = True
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                    # consonant :
                    elif base_char in CONSONANTS_INVERSED and \
                         istruct.indexes_are_contiguous_to( [index_char,] ) and \
                         istruct.real_indexes_are_contiguous_to(real_indexes):

                        # we add a prefix to the current syllable :
                        if dotpointorplus is None and \
                           not rnam_bcad and \
                           anusvara_candrabindu is None and \
                           istruct.prefix is None and \
                           istruct.superfix is None and \
                           istruct.consonant is None and \
                           istruct.vowel1 is None and \
                           CONSONANTS_INVERSED[base_char] in PREFIXES:

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].prefix = CONSONANTS_INVERSED[base_char]
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                        # we add a superfix to the current syllable :
                        if dotpointorplus is None and \
                           not rnam_bcad and \
                           anusvara_candrabindu is None and \
                           istruct.superfix is None and \
                           istruct.consonant is None and \
                           istruct.vowel1 is None and \
                           CONSONANTS_INVERSED[base_char] in SUPERFIXES:

                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].superfix = CONSONANTS_INVERSED[base_char]
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                        # we add a main consonant to the current syllable :
                        if istruct.consonant is None and \
                           istruct.vowel1 is None and \
                           istruct.subfix is None and \
                           dotpointorplus != '+':
                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].consonant = CONSONANTS_INVERSED[base_char]
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                            # a anusvara/candrabindu symbol may follow a consonant :
                            if anusvara_candrabindu is not None:
                                future_istructs[-1].anusvara_candrabindu = \
                                  DIACRITICS_INVERSED[anusvara_candrabindu]

                            # a "rnam bcad" symbol can follow a consonant, as in
                            # གྲུཌཿ=gruDH.
                            if rnam_bcad:
                                future_istructs[-1].rnam_bcad = True

                            if halanta:
                                future_istructs[-1].halanta = True

                        # we add a subjoined consonant to the current syllable :

                        # let's initialize <part_of_a_common_cons_stack> :
                        cons = []
                        if istruct.consonant is not None:
                            cons.append( istruct.consonant )
                        if istruct.subfix is not None:
                            cons.extend( istruct.subfix )
                        cons.append( CONSONANTS_INVERSED[base_char] )

                        part_of_a_common_cons_stack = tuple(cons) in COMMON_CONSONANTS_STACK

                        if dotpointorplus == '+' and \
                           istruct.consonant is not None and \
                           istruct.suffix1 is None:

                            future_istructs.append( deepcopy(istruct) )

                            if future_istructs[-1].subfix is None:
                                future_istructs[-1].subfix = []
                            future_istructs[-1].subfix.append( CONSONANTS_INVERSED[base_char] )
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                        elif dotpointorplus is None and \
                             istruct.suffix1 is None and \
                             part_of_a_common_cons_stack and \
                             istruct.consonant is not None and \
                             istruct.vowel1 is None:

                            future_istructs.append( deepcopy(istruct) )
                            if future_istructs[-1].subfix is None:
                                future_istructs[-1].subfix = []
                            future_istructs[-1].subfix.append( CONSONANTS_INVERSED[base_char] )
                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                        # we add a suffix-1 to the current syllable :
                        if dotpointorplus is None and \
                           istruct.consonant is not None and \
                           istruct.vowel1 is not None and \
                           istruct.suffix1 is None and \
                           CONSONANTS_INVERSED[base_char] in SUFFIXES1 and \
                           not istruct.postsuffix_u:
                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].suffix1 = CONSONANTS_INVERSED[base_char]

                            # is the suffix has a rnam_bcad/anusvara_candrabindu symbol,
                            # the future istruct gets this diacritic sign :
                            # (e.g. ལབཿ labH where -bH is a suffix)
                            if anusvara_candrabindu is not None:
                                future_istructs[-1].anusvara_candrabindu = \
                                  DIACRITICS_INVERSED[anusvara_candrabindu]
                            if rnam_bcad:
                                future_istructs[-1].rnam_bcad = True

                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

                        # we add a suffix-2 to the current syllable :
                        if dotpointorplus is None and \
                           istruct.consonant is not None and \
                           istruct.vowel1 is not None and \
                           istruct.suffix1 is not None and \
                           istruct.suffix2 is None and \
                           not istruct.postsuffix_u and \
                           CONSONANTS_INVERSED[base_char] in SUFFIXES2:
                            future_istructs.append( deepcopy(istruct) )
                            future_istructs[-1].suffix2 = CONSONANTS_INVERSED[base_char]

                            # is the suffix has a rnam_bcad/anusvara_candrabindu symbol,
                            # the future istruct gets this diacritic sign :
                            if anusvara_candrabindu is not None:
                                future_istructs[-1].anusvara_candrabindu = \
                                  DIACRITICS_INVERSED[anusvara_candrabindu]
                            if rnam_bcad:
                                future_istructs[-1].rnam_bcad = True

                            future_istructs[-1].indexes.add( index_char )
                            future_istructs[-1].real_indexes.update( real_indexes  )

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
        # postsuffixes འིས ('is), འམ ('am), འང ('ang), འི ('i),
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
                    # (a) we don't want to modify the istruct whithout indexes
                    #     [ len(index0.indexes)>0 ]
                    # (b) we don't want to analyse old istructs, hence the condition :
                    #      (index_char in istruct0.indexes or index_char in istruct1.indexes)
                    # (c) we have to check if istruct0 is placed just before istruct1
                    #     [ call to indexes_are_contiguous() functions ]
                    for index0, istruct0 in enumerate(istructs):

                        if index0 != index1 and \
                           (index_char in istruct0.indexes or index_char in istruct1.indexes) and \
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
        # postsuffix འོ ('o)
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
                       (index_char in istruct0.indexes or index_char in istruct1.indexes) and \
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

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (W) we clean the wrong istructs
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:

        # an istruct without indexes ? bad istruct :
        if len(istruct.indexes) ==  0:
            istruct.bad_internalstruct = True

        # a prefix without a main consonant ? bad istruct :
        if istruct.prefix is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True
        # a suffix without a main consonant ? bad istruct :
        if istruct.suffix1 is not None and istruct.consonant is None:
            istruct.bad_internalstruct = True
        # a suffix2 without a suffix1 ? bad istruct :
        if istruct.suffix2 is not None and istruct.suffix1 is None:
            istruct.bad_internalstruct = True

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (W.2) we clean the equivalent istructs
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
                # prefix=STR1; superfix=0; consonant=STR2; subfix=None
                # prefix=None; superfix=0; consonant=STR1; subfix=[STR2,]
                #
                # ... we keep the second istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].superfix is None and \
                       istructs[index_x].superfix == istructs[index_y].superfix and \
                       istructs[index_x].prefix == istructs[index_y].consonant and \
                       istructs[index_y].subfix == [istructs[index_x].consonant, ]:

                        istructs[index_x].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (b) Equivalent istructs :
                #
                # prefix=STR1; superfix=STR2; consonant=STR3; subfix=[STR4, ...]
                # prefix=STR1; superfix=0;    consonant=STR2; subfix=[STR3, STR4, ...]
                #
                # ... we keep the first istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix == istructs[index_y].prefix and \
                       istructs[index_x].superfix == istructs[index_y].consonant and \
                       istructs[index_y].superfix is None and \
                       istructs[index_x].subfix is not None and \
                       istructs[index_y].subfix is not None and \
                       len(istructs[index_y].subfix) >= 2 and \
                       istructs[index_x].consonant == istructs[index_y].subfix[0] and \
                       istructs[index_x].subfix[0] == istructs[index_y].subfix[1]:

                        istructs[index_y].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (c) Equivalent istructs :
                #
                # prefix=0; superfix=STR1; consonant=STR2; subfix = [...]
                # prefix=0; superfix=0;    consonant=STR1; subfix = [STR2, ...]
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
                       istructs[index_y].subfix is not None and \
                       istructs[index_x].consonant == istructs[index_y].subfix[0]:

                        istructs[index_y].bad_internalstruct = True

                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                # (d) Equivalent istructs :
                #
                # prefix=STR1; superfix=STR2; consonant=STR3;
                # prefix=STR1; superfix=0;    consonant=STR2; subfix=[STR3, ...]
                #
                # ... we keep the first istruct as the most natural.
                #  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
                for index_x, index_y in ( (index1, index2),
                                          (index2, index1), ):

                    if istructs[index_x].indexes == istructs[index_y].indexes and \
                       istructs[index_x].real_indexes == istructs[index_y].real_indexes and \
                       istructs[index_x].prefix == istructs[index_y].prefix and \
                       istructs[index_x].superfix == istructs[index_y].consonant and \
                       istructs[index_y].superfix is None and \
                       istructs[index_y].subfix is not None and \
                       istructs[index_x].consonant == istructs[index_y].subfix[0]:

                        istructs[index_y].bad_internalstruct = True

    istructs.clean_off_bad_internalstructs()

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # (W.3) special case : if a syllable is equivalent to "oM" it's not
    #       VOWEL=O+CANDRABINDU(=RJES SU NGA RO), it's simply the
    #       symbol oM.
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
    # (W.4) special case : if a syllable contains only a superfix without prefix
    #       or consonant we treat this superfix as the (main) consonant.
    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    for istruct in istructs:
        if not istruct.unknown_character and \
           istruct.prefix is None and \
           istruct.superfix is not None and \
           istruct.consonant is None:

            istruct.consonant = istruct.superfix
            istruct.superfix = None

    #. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    #
    # "sra" : (consonant)S + (subfix)R [@@BOD-INTERNALSTRUCTURE-001]
    #
    # (W.4.1) special case : prefix=0, superfix='S', consonant='R', subfix=[...]
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
    #
    # "rla" : (consonant)R + (subfix)L [@@BOD-INTERNALSTRUCTURE-002]
    #
    # (W.4.2) special case : prefix=0, superfix='R', consonant='L', subfix=[...]
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
    #
    # "sla" : (consonant)S + (subfix)L [@@BOD-INTERNALSTRUCTURE-003]
    #
    # (W.4.3) special case : prefix=0, superfix='S', consonant='L', subfix=[...]
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
    #
    # "rwa" : (consonant)R + (subfix)W [@@BOD-INTERNALSTRUCTURE-004]
    #
    # (W.4.4) special case : prefix=0, superfix='R', consonant='W', subfix=[...]
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
    #
    # "lwa" : (consonant)L + (subfix)W [@@BOD-INTERNALSTRUCTURE-005]
    #
    # (W.4.5) special case : prefix=0, superfix='L', consonant='W', subfix=[...]
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
    #
    # "swa" : (consonant)L + (subfix)W [@@BOD-INTERNALSTRUCTURE-006]
    #
    # (W.4.6) special case : prefix=0, superfix='S', consonant='W', subfix=[...]
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

    #...........................................................................
    # istructs -> istructs
    #...........................................................................
    # we add the unknown characters, id est we add an istruct object linked to
    # every index not covered by the istructs.
    #...........................................................................
    real_indexes_ok = set()
    for istruct in istructs:
        real_indexes_ok.update( istruct.real_indexes )

    for real_index in range(0, len(_src)):
        if real_index not in real_indexes_ok:
            istructs.append ( InternalStructure( dstring_object = None,
                                                 unknown_character = True,
                                                 punctuation_or_other_symbol = _src[real_index],
                                                 real_indexes = OrderedSet( [real_index,]) ))

    #...........................................................................
    # istructs ---> res.get_the_complete_records() ----> res
    #...........................................................................
    complete_records = istructs.get_the_complete_records( last_index = len(_src)-1,
                                                          use_real_indexes = True )

    if len(complete_records) != 1:
        msg = "Zero or more than one lists of istructs describe the source string : "
        raise DCharsError( context = "ewts.py::get_intstruct_from_str()",
                           message = msg+str(complete_records) )

    res = ListOfInternalStructures(
        anonymize_the_unknown_chars=anonymize_the_unknown_chars)
    for index in complete_records[0]:
        res.append( istructs[index] )

    #...........................................................................
    # buffering ?
    #...........................................................................
    if fill_the_buffers and \
       _src not in ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR and \
       not res.contains_unknown_characters():
        ewts_buffer.EWTS_BUFFER__FROM_TRANS_STR[_src] = res.pickle_repr()

    #...........................................................................
    # we can set the .dstring_object attribute :
    #...........................................................................
    for istruct in res:
        istruct.dstring_object = dstring_object

    return res

#///////////////////////////////////////////////////////////////////////////////
def dstring__get_translit_str(dstring):
    """
        function dstring__get_translit_str()

        dstring : DStringBOD object

        Return a transliterated string corresponding to <dstring>.
    """
    expected_structure = dstring.options["expected structure"]

    #...........................................................................
    # initialization of <choose_sanskrit_structure>
    #...........................................................................
    choose_sanskrit_structure = (expected_structure == "always Sanskrit") or \
                                (expected_structure == "Tibetan or Sanskrit" and \
                                 dstring.istructs.seems_to_be_a_sanskrit_string())

    # internalstructures -> string
    res = []
    for internalstructure in dstring.istructs:

        # let's initialize <part_of_a_valid_list_of_cons> and <part_of_a_common_cons_stack> :
        cons = []
        if internalstructure.prefix is not None:
            cons.append( internalstructure.prefix )
        if internalstructure.superfix is not None:
            cons.append( internalstructure.superfix )
        if internalstructure.consonant is not None:
            cons.append( internalstructure.consonant )
        if internalstructure.subfix is not None:
            for subj_c in internalstructure.subfix:
                cons.extend( subj_c )
        part_of_a_valid_list_of_cons = tuple(cons) in SUPERFIXES_ROOT_SUBFIXES

        cons = []
        if internalstructure.consonant is not None:
            cons.append( internalstructure.consonant )
        if internalstructure.subfix is not None:
            for subj_c in internalstructure.subfix:
                cons.extend( subj_c )
        part_of_a_common_cons_stack = tuple(cons) in COMMON_CONSONANTS_STACK

        if internalstructure.unknown_character:
            res.append( UNKNOWN_CHAR_SYMBOL )

        elif internalstructure.punctuation_or_other_symbol is not None:

            if internalstructure.punctuation_or_other_symbol in PUNCTUATION:
                res.append( PUNCTUATION[internalstructure.punctuation_or_other_symbol] )
            elif internalstructure.punctuation_or_other_symbol in OTHER_SYMBOLS:
                res.append( OTHER_SYMBOLS[internalstructure.punctuation_or_other_symbol] )
            else:
                msg = "unknown char='{0}'".format(internalstructure.punctuation_or_other_symbol)
                raise DCharsError( context = "ewts.py::dstring__get_translit_str",
                                   message = msg )


        else:
            if internalstructure.prefix is not None:
                res.append( CONSONANTS[internalstructure.prefix] )

            if internalstructure.superfix is not None:
                res.append( CONSONANTS[internalstructure.superfix] )

            # for a Tibetan string derived from a Sanskrit string :
            if internalstructure.prefix is not None and \
               (dstring.options["expected structure"] == "always Sanskrit" or \
               (dstring.options["expected structure"] == "Tibetan or Sanskrit" and \
                dstring.istructs.seems_to_be_a_sanskrit_string())):
                res.append( VOWELS['A'] )

            if internalstructure.consonant is not None:

                # dot ?
                if internalstructure.prefix is not None and \
                   part_of_a_valid_list_of_cons:
                    res.append(".")

                res.append( CONSONANTS[internalstructure.consonant] )

            if internalstructure.subfix is not None:
                for subj_c in internalstructure.subfix:
                    if not part_of_a_common_cons_stack:
                        res.append( '+' )
                    res.append( CONSONANTS[subj_c] )

            at_least_one_vowel = False

            if internalstructure.vowel1 is not None and not internalstructure.halanta:
                res.append( VOWELS[internalstructure.vowel1] )
                at_least_one_vowel = True

            if internalstructure.vowel2 is not None and not internalstructure.halanta:
                res.append( '+' )
                res.append( VOWELS[internalstructure.vowel2] )
                at_least_one_vowel = True

            # halanta :
            if internalstructure.halanta:
                res.append( DIACRITICS['MARK HALANTA'] )
                at_least_one_vowel = True

            # no vowel at all ?
            if not at_least_one_vowel and choose_sanskrit_structure:
                res.append( DIACRITICS['MARK HALANTA'] )

            # anusvara
            # e.g. : "galaM"
            if internalstructure.anusvara_candrabindu is not None:
                res.append( DIACRITICS[internalstructure.anusvara_candrabindu] )

            if internalstructure.suffix1 is not None:
                res.append( CONSONANTS[internalstructure.suffix1] )

            if internalstructure.suffix2 is not None:
                res.append( CONSONANTS[internalstructure.suffix2] )

            # for a Tibetan string derived from a Sanskrit string :
            if (internalstructure.suffix1 is not None or \
                internalstructure.suffix2 is not None) and \
               (dstring.options["expected structure"] == "always Sanskrit" or \
               (dstring.options["expected structure"] == "Tibetan or Sanskrit" and \
                dstring.istructs.seems_to_be_a_sanskrit_string())):
                res.append( VOWELS['A'] )

            # rnam bcad :
            # e.g. : "gtiH"
            if internalstructure.rnam_bcad:
                res.append( DIACRITICS['SIGN RNAM BCAD'] )

            if internalstructure.postsuffix_u:
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['U'] )

            if internalstructure.gramm_postsuffix == "'i":
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['I'] )
            elif internalstructure.gramm_postsuffix == "'is":
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['I'] )
                res.append( CONSONANTS["S"] )
            elif internalstructure.gramm_postsuffix == "'am":
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['A'] )
                res.append( CONSONANTS["M"] )
            elif internalstructure.gramm_postsuffix == "'ang":
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['A'] )
                res.append( CONSONANTS["NG"] )
            elif internalstructure.gramm_postsuffix == "r":
                res.append( CONSONANTS["R"] )
            elif internalstructure.gramm_postsuffix == "s":
                res.append( CONSONANTS["S"] )

            if internalstructure.postsuffix_o:
                res.append( CONSONANTS["-"] )
                res.append( VOWELS['O'] )

    res = "".join(res)
    res = res.replace( CONSONANTS['A'], "" )

    return res
