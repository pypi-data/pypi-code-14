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
    ❏DChars❏ : dchars/languages/bod/transliterations/bodsan/bodsan.py
"""

from dchars.errors.errors import DCharsError

from dchars.dchars import new_dstring

from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL

from dchars.languages.bod.internalstructure import ListOfInternalStructures, \
                                                   InternalStructure

from dchars.languages.bod.transliterations.bodsan.bodsan_symbols import \
                CONSONANTS, CONSONANTS_INVERSED, \
                DEPENDENT_VOWELS, DEPENDENT_VOWELS_INVERSED, \
                INDEPENDENT_VOWELS, INDEPENDENT_VOWELS_INVERSED, \
                OTHER_SYMBOLS, OTHER_SYMBOLS_INVERSED, \
                PUNCTUATION, PUNCTUATION_INVERSED, \
                DIACRITICS, DIACRITICS_INVERSED

from dchars.languages.san.symbols import SYMB_CONSONANTS as SAN__SYMB_CONSONANTS, \
                                         SYMB_DEPENDENT_VOWELS as SAN__SYMB_DEPENDENT_VOWELS, \
                                         SYMB_INDEPENDENT_VOWELS as SAN__SYMB_INDEPENDENT_VOWELS, \
                                         SYMB_OTHER_SYMBOLS as SAN__SYMB_OTHER_SYMBOLS, \
                                         SYMB_PUNCTUATION as SAN__SYMB_PUNCTUATION, \
                                         SYMB_DIACRITICS as SAN__SYMB_DIACRITICS

################################################################################
# List of the available directions for this transliteration method :
#
#  +1 (text->transliteration)
#  -1 (transliteration->text)
#
################################################################################
AVAILABLE_DIRECTIONS = (-1, +1)

#///////////////////////////////////////////////////////////////////////////////
def get_intstruct_from_trans_str( _src, dstring_object ):
    """
        function get_intstruct_from_trans_str()

        _src    : (str) transliterated string like "क".

        Return a ListOfInternalStructures object.
    """

    # list of InternalStructure objects.
    istructs = ListOfInternalStructures(anonymize_the_unknown_chars =\
                                dstring_object.options["anonymize the unknown characters"] == 'yes')

    # we read <_src> through a DSTRING_SAN object :
    dstring_san = new_dstring(language='संस्कृतम्',
                              transliteration_method="iso15919")
    dstring_san = dstring_san(_src)

    # In Sanskrit, if a consonant is followed by a virama, it means that the following
    # consonants are part of a cluster of consonants.
    #
    # E.g. in कर्म (0915=ka, 0930=ra, 094D=virama, 092E=ma) we have something like kar+ma,
    # the -m- having no vowel.
    #
    place_consonant_among_subjc = False

    for dchar_san in dstring_san:

        if dchar_san.unknown_char:
            new_istruct = InternalStructure( dstring_object = dstring_object,
                                             unknown_character = True )
            istructs.append(new_istruct)

        else:

            # punctation symbol :
            if dchar_san.base_char in SAN__SYMB_PUNCTUATION:
                unicode_symb = SAN__SYMB_PUNCTUATION.get_default_symbol(dchar_san.base_char)
                new_istruct = InternalStructure( dstring_object = dstring_object,
                                                 punctuation_or_other_symbol = \
                                                   PUNCTUATION_INVERSED[unicode_symb] )
                istructs.append(new_istruct)

                place_consonant_among_subjc = False

            # other symbol :
            elif dchar_san.base_char in SAN__SYMB_OTHER_SYMBOLS:
                unicode_symb = SAN__SYMB_OTHER_SYMBOLS.get_default_symbol(dchar_san.base_char)
                new_istruct = InternalStructure( dstring_object = dstring_object,
                                                 punctuation_or_other_symbol = \
                                                   OTHER_SYMBOLS_INVERSED[unicode_symb] )
                istructs.append(new_istruct)

                place_consonant_among_subjc = False

            # independent vowel:
            elif dchar_san.base_char in SAN__SYMB_INDEPENDENT_VOWELS:

                #...............................................................
                # _independent_vowel will be added as an independent vowel :
                #...............................................................
                if  dstring_object.options["san2bod quality"] == "normal" and \
                    dchar_san.base_char=='O':
                    #====================
                    # @@BOD2SAN-NORM-004
                    # (independent vowel) ओ(ō) > औ(au)
                    #====================
                    _independent_vowel = "AU"

                elif dstring_object.options["san2bod quality"] == "low" and \
                     dchar_san.base_char=='O':
                    #====================
                    # @@BOD2SAN-LOW-004
                    # (independent vowel) ओ(ō) > औ(au)
                    #====================
                    _independent_vowel = "AU"

                elif dstring_object.options["san2bod quality"] == "low" and \
                     dchar_san.base_char in ('AA', 'II', 'UU'):
                    #====================
                    # @@BOD2SAN-LOW-006
                    # (independent vowel) long vowels > short vowels
                    #====================
                    _independent_vowel = {'AA' : 'A',
                                          'II' : 'I',
                                          'UU' : 'U'}[dchar_san.base_char]

                else:
                    _independent_vowel = dchar_san.base_char

                unicode_symb = SAN__SYMB_INDEPENDENT_VOWELS.get_default_symbol(_independent_vowel)
                new_istruct = InternalStructure( dstring_object = dstring_object,
                                                 consonant = "A",
                                                 vowel1 = INDEPENDENT_VOWELS_INVERSED[unicode_symb])
                istructs.append(new_istruct)

                place_consonant_among_subjc = False

            # consonant :
            elif dchar_san.base_char in SAN__SYMB_CONSONANTS:

                if dchar_san.base_char == 'DEVANAGARI SIGN VISARGA':
                    # special case : the visarga symbol is placed among consonants in Sanskrit,
                    # among diacritics in Tibetan.

                    if dstring_object.options["san2bod quality"] == "normal" and \
                       dchar_san.base_char=='DEVANAGARI SIGN VISARGA':
                        #====================
                        # @@BOD2SAN-NORM-001
                        # the visarga is omitted if "san2bod quality" == "normal"
                        #====================
                        pass
                    elif dstring_object.options["san2bod quality"] == "low" and \
                         dchar_san.base_char=='DEVANAGARI SIGN VISARGA':
                        #===================
                        # @@BOD2SAN-LOW-001
                        # the visarga is omitted if "san2bod quality" == "low"
                        #===================
                        pass
                    else:
                        unicode_symb = SAN__SYMB_CONSONANTS.get_default_symbol(dchar_san.base_char)
                        istructs[-1].rnam_bcad = True

                        place_consonant_among_subjc = False

                elif not place_consonant_among_subjc:
                    # consonant to be placed as a main consonant
                    # (and not among subjoined consonants) :

                    #...........................................................
                    # _base_char will be added as a main consonant :
                    #...........................................................
                    if  dstring_object.options["san2bod quality"] == "normal" and \
                        dchar_san.base_char=='VA':
                        #====================
                        # @@BOD2SAN-NORM-002
                        # the व(va) becomes ब(ba) if "san2bod quality" == "normal"
                        #====================
                        _base_char = "BA"

                    elif dstring_object.options["san2bod quality"] == "low" and \
                         dchar_san.base_char=='VA':
                        #===================
                        # @@BOD2SAN-LOW-002
                        # the व(va) becomes ब(ba) if "san2bod quality" == "normal"
                        #===================
                        _base_char = "BA"

                    elif (dstring_object.options["san2bod quality"] == "low" and \
                        dchar_san.base_char in ('TTA',
                                                'TTHA',
                                                'DDA',
                                                'DDHA',
                                                'NNA')):
                        #===================
                        # @@BOD2SAN-LOW-007
                        # retroflex consonant > non-retroflex consonant
                        # retroflex consonant + aspiration > non-retroflex
                        # consonant without aspiration
                        #===================
                        _base_char = {'TTA'   : "TA",
                                      'TTHA'  : "TA",
                                      'DDA'   : "DA",
                                      'DDHA'  : "DA",
                                      'NNA'   : "NA"
                                      }[dchar_san.base_char]

                    elif (dstring_object.options["san2bod quality"] == "low" and \
                        dchar_san.base_char in ('KHA',
                                                'GHA',
                                                'THA',
                                                'CHA',
                                                'JHA',
                                                'TTHA',
                                                'DDHA',
                                                'PHA',
                                                'BHA')):
                        #===================
                        # @@BOD2SAN-LOW-008
                        # consonant + aspiration > consonant without aspiration
                        #===================
                        _base_char = {'KHA'   : "KA",
                                      'GHA'   : "GA",
                                      'THA'   : "TA",
                                      'CHA'   : "CA",
                                      'JHA'   : "JA",
                                      'DHA'   : "DA",
                                      'TTHA'  : "TTA",
                                      'DDHA'  : "DDA",
                                      'PHA'   : "PA",
                                      'BHA'   : "BA"
                                      }[dchar_san.base_char]

                    else:
                        # general case :
                        _base_char = dchar_san.base_char

                    unicode_symb = SAN__SYMB_CONSONANTS.get_default_symbol(_base_char)
                    bod_consonant = CONSONANTS_INVERSED[unicode_symb]

                    new_istruct = InternalStructure( dstring_object = dstring_object,
                                                     consonant = bod_consonant )
                    istructs.append(new_istruct)

                    if dchar_san.virama:
                        place_consonant_among_subjc = True

                else:
                    # consonant to be placed among subjoined consonants
                    # (and not as a main consonant) :
                    if istructs[-1].subfix is None:
                        istructs[-1].subfix = []

                    unicode_symb = SAN__SYMB_CONSONANTS.get_default_symbol(dchar_san.base_char)
                    cons = CONSONANTS_INVERSED[unicode_symb]

                    add_this_consonant = True
                    if dstring_object.options["san2bod quality"] == "low" and \
                       istructs[-1].subfix == [] and \
                       istructs[-1].consonant == cons:
                        #===================
                        # @@BOD2SAN-LOW-008
                        # geminate consonant > 0
                        #===================
                        add_this_consonant = False
                        # no more subjoinded consonant : the other one will be treated
                        # like main consonants :
                        place_consonant_among_subjc = False

                    if add_this_consonant:
                        istructs[-1].subfix.append( cons )

                        if not dchar_san.virama:
                            place_consonant_among_subjc = False

                # dependent vowel :
                if dchar_san.dependentvowel is not None and dchar_san.dependentvowel != "A":

                    #...........................................................
                    # _dependent_vowel will be added as a dependent vowel :
                    #...........................................................
                    if  dstring_object.options["san2bod quality"] == "normal" and \
                        dchar_san.dependentvowel=='O':
                        #====================
                        # @@BOD2SAN-NORM-003
                        # (dependent vowel) ओ(ō) > औ(au)
                        #====================
                        _dependent_vowel = "AU"

                    elif dstring_object.options["san2bod quality"] == "low" and \
                         dchar_san.dependentvowel=='O':
                        #====================
                        # @@BOD2SAN-LOW-003
                        # (dependent vowel) ओ(ō) > औ(au)
                        #====================
                        _dependent_vowel = "AU"

                    elif  dstring_object.options["san2bod quality"] == "low" and \
                          dchar_san.dependentvowel in ('AA', 'II', 'UU'):
                        #====================
                        # @@BOD2SAN-LOW-005
                        # (dependent vowel) long vowels > short vowels
                        #====================
                        _dependent_vowel = {'AA' : 'A',
                                            'II' : 'I',
                                            'UU' : 'U'}[dchar_san.dependentvowel]

                    else:
                        _dependent_vowel = dchar_san.dependentvowel

                    unicode_symb = \
                      SAN__SYMB_DEPENDENT_VOWELS.get_default_symbol(_dependent_vowel)

                    istructs[-1].vowel1 = DEPENDENT_VOWELS_INVERSED[unicode_symb]

            # anusvara/candrabindu :
            if dchar_san.anusvara_candrabindu is not None:
                unicode_symb = \
                  SAN__SYMB_DIACRITICS.get_default_symbol(dchar_san.anusvara_candrabindu)

                istructs[-1].anusvara_candrabindu = DIACRITICS_INVERSED[unicode_symb]

    res = ListOfInternalStructures(anonymize_the_unknown_chars =\
                                dstring_object.options["anonymize the unknown characters"] == 'yes')

    # we add a tsheg after a "real" syllable (id est, not a punctuation sign, ...)
    for istruct in istructs:
        res.append(istruct)

        if istruct.consonant is not None:
            res.append( InternalStructure(
                dstring_object = dstring_object,
                punctuation_or_other_symbol = 'MARK INTERSYLLABIC TSHEG' ))

    return res

#///////////////////////////////////////////////////////////////////////////////
def dstring__get_translit_str(dstring):
    """
        function dstring__get_translit_str()

        dstring : DStringBOD object

        Return a transliterated string corresponding to <dstring>.
    """

    res = []
    for internalstructure in dstring.istructs:

        if internalstructure.unknown_character:
            res.append( UNKNOWN_CHAR_SYMBOL )

        elif internalstructure.punctuation_or_other_symbol is not None:

            if internalstructure.punctuation_or_other_symbol in PUNCTUATION:

                # if internalstructure.punctuation_or_other_symbol !="MARK INTERSYLLABIC TSHEG":
                #     res.append( PUNCTUATION[internalstructure.punctuation_or_other_symbol] )
                res.append( PUNCTUATION[internalstructure.punctuation_or_other_symbol] )

            elif internalstructure.punctuation_or_other_symbol in OTHER_SYMBOLS:
                res.append( OTHER_SYMBOLS[internalstructure.punctuation_or_other_symbol] )

            else:
                msg = "unknown char='{0}'={1}".format(
                    internalstructure.punctuation_or_other_symbol,
                    [hex(ord(c)) for c in internalstructure.punctuation_or_other_symbol])

                raise DCharsError( context = "bodsan.py::dstring__get_translit_str",
                                   message = msg )

        else:

            if internalstructure.prefix is not None:
                res.append( CONSONANTS[internalstructure.prefix] )
                res.append( DIACRITICS['MARK HALANTA'] )

            if internalstructure.superfix is not None:
                res.append( CONSONANTS[internalstructure.superfix] )

            if internalstructure.consonant is not None:
                if internalstructure.consonant != 'A':
                    res.append( CONSONANTS[internalstructure.consonant] )

            if internalstructure.subfix is not None:
                for subj_c in internalstructure.subfix:
                    res.append( DIACRITICS['MARK HALANTA'] )
                    res.append( CONSONANTS[subj_c] )

            if internalstructure.vowel1 is not None and \
               not internalstructure.halanta:

                if internalstructure.consonant == 'A':
                    # independent vowel :
                    res.append( INDEPENDENT_VOWELS[internalstructure.vowel1] )

                elif internalstructure.consonant is not None and internalstructure.vowel1 != 'A':
                    # dependent vowel :
                    res.append( DEPENDENT_VOWELS[internalstructure.vowel1] )

            if internalstructure.vowel2 is not None and \
               not internalstructure.halanta and \
               internalstructure.vowel1 != 'A':
                res.append( DEPENDENT_VOWELS[internalstructure.vowel2] )

            # halanta :
            if internalstructure.halanta:
                res.append( DIACRITICS['MARK HALANTA'] )

            # anusvara :
            if internalstructure.anusvara_candrabindu is not None:
                res.append( DIACRITICS[internalstructure.anusvara_candrabindu] )

            if internalstructure.suffix1 is not None:
                res.append( CONSONANTS[internalstructure.suffix1] )

            if internalstructure.suffix2 is not None:
                res.append( DIACRITICS['MARK HALANTA'] )

            # rnam bcad :
            if internalstructure.rnam_bcad:
                res.append( DIACRITICS['SIGN RNAM BCAD'] )

            if internalstructure.postsuffix_u:
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

            if internalstructure.gramm_postsuffix == "'i":
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

            elif internalstructure.gramm_postsuffix == "'is":
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

            elif internalstructure.gramm_postsuffix == "'am":
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

            elif internalstructure.gramm_postsuffix == "'ang":
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

            elif internalstructure.gramm_postsuffix == "r":
                res.append( CONSONANTS["R"] )
            elif internalstructure.gramm_postsuffix == "s":
                res.append( CONSONANTS["S"] )

            if internalstructure.postsuffix_o:
                msg = "invalid Tibetan dstring; cannot convert it into Sanskrit; dstring=" + \
                      str(dstring)

                raise DCharsError( context = "dstring__get_translit_str()",
                                   message = msg )

    res = "".join(res)

    return res
