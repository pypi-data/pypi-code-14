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
    ❏DChars❏ : dchars/languages/san/transliterations/itrans/itrans.py
"""


from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.dicttools import invertdict
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
import re

################################################################################
# List of the available directions for this transliteration method :
#
#  +1 (text->transliteration)
#  -1 (transliteration->text)
#
################################################################################
AVAILABLE_DIRECTIONS = (-1, +1)

################################################################################
# transliteration's equivalences :
################################################################################
TRANS_EQUIVALENCES = (
                      ("aa",    "A"),
                      ("ii",    "I"),
                      ("uu",    "U"),
                      ("RRi",   "R^i"),
                      ("RRI",   "R^I"),
                      ("LLi",   "L^i"),
                      ("LLI",   "L^I"),
                      ("w",     "v"),
                      ("x",     "kSh"),
                      ("GY",    "j~n"),
                      (".n",    "M"),
                      (".m",    "M"),

                      ("z",     "J"),
                     )

################################################################################
# transliteration's symbols :
################################################################################

#
# * CAVEAT ! If you modify these dictionaries, don't forget to modify their
#            corresponding symbols' dictionaries in symbols.py !
#
# * CAVEAT ! No duplicate value allowed in these dictionaries !
#
CONSONANTS = {
                 'KA'            : 'k',
                 'KHA'           : 'kh',
                 'GA'            : 'g',
                 'GHA'           : 'gh',
                 'NGA'           : '~N',
                 'CA'            : 'ch',
                 'CHA'           : 'Ch',
                 'JA'            : 'j',
                 'JHA'           : 'jh',
                 'NYA'           : '~n',
                 'TTA'           : 'T',
                 'TTHA'          : 'Th',
                 'DDA'           : 'D',
                 'DDHA'          : 'Dh',
                 'NNA'           : 'N',
                 'TA'            : 't',
                 'THA'           : 'th',
                 'DA'            : 'd',
                 'DHA'           : 'dh',
                 'NA'            : 'n',
                 'NNNA'          : 'NNN',     # (???) see above
                 'PA'            : 'p',
                 'PHA'           : 'ph',
                 'BA'            : 'b',
                 'BHA'           : 'bh',
                 'MA'            : 'm',
                 'YA'            : 'y',
                 'RA'            : 'r',
                 'RRA'           : 'RRR',     # (???) see above
                 'LA'            : 'l',
                 'LLA'           : 'L',
                 'LLLA'          : 'LLL',     # (???) see above
                 'VA'            : 'v',
                 'SHA'           : 'sh',
                 'SSA'           : 'Sh',
                 'SA'            : 's',
                 'HA'            : 'h',

                 'DEVANAGARI SIGN VISARGA'         : 'H',
             }

CONSONANTS_URDU = {
                 'URDU_q'                          : 'q',
                 'URDU_K'                          : 'K',
                 'URDU_G'                          : 'G',
                 'URDU_z'                          : 'z',
                 'URDU_f'                          : 'f',
                 'URDU_.D'                         : '.D',
                 'URDU_.Dh'                        : '.Dh',
                 }

# URDU_CONSONANT_2_CONSONANT['q'] = 'k' + nukta
URDU_CONSONANT_2_CONSONANT = {
                 'q'                            : 'KA',
                 'K'                            : 'KHA',
                 'G'                            : 'GA',
                 'z'                            : 'JA',
                 'f'                            : 'PA',
                 '.D'                           : 'DDA',
                 '.Dh'                          : 'DDHA',
                 }

# the name of the vowels (the keys of this dictionary) must be consistent
# with symbols.py::SYMB_(IN)DEPENDENT_VOWELS
VOWELS = {
                'SHORT A'                       : '-a',         # (???) see above
                'A'                             : 'a',
                'AA'                            : 'A',
                'I'                             : 'i',
                'II'                            : 'I',
                'U'                             : 'u',
                'UU'                            : 'U',
                'VOCALIC R'                     : 'R^i',
                'VOCALIC L'                     : 'L^i',
                'CANDRA E'                      : 'CANDRAe',    # (???) see above
                'SHORT E'                       : '-e',         # (???) see above
                'E'                             : 'e',
                'AI'                            : 'ai',
                'CANDRA O'                      : 'CANDRAo',    # (???) see above
                'SHORT O'                       : '-o',         # (???) see above
                'O'                             : 'o',
                'AU'                            : 'au',
                'VOCALIC RR'                    : 'R^I',
                'VOCALIC LL'                    : 'L^I',
         }

VOWELS_IN_HIATUS = {
                'A'                             : '/a',
                'AA'                            : '/A',
                'I'                             : '+i',
                'U'                             : '+u',
                'UU'                            : '/U',
                'II'                            : '+I',         # (???) see above
                'E'                             : '/e',
                'AI'                            : '+ai',        # (???) see above
                'O'                             : '+o',         # (???) see above
                'AU'                            : '+au',        # (???) see above
                'SHORT E'                       : '/-e',        # (???) see above
                'SHORT O'                       : '/+o',        # (???) see above

                # strange definitions of hiatus vowels, but that's the way it's defined
                # in the reference file. See the documentation
                'VOCALIC R'                     : 'R^i',
                'VOCALIC L'                     : 'L^i',
                'VOCALIC RR'                    : 'R^I',
                'VOCALIC LL'                    : 'L^I',
         }

OTHER_SYMBOLS = {
              'DEVANAGARI OM'                           : "<OM>",               # (???) see above

              'DEVANAGARI DIGIT ZERO'                   : '0',
              'DEVANAGARI DIGIT ONE'                    : '1',
              'DEVANAGARI DIGIT TWO'                    : '2',
              'DEVANAGARI DIGIT THREE'                  : '3',
              'DEVANAGARI DIGIT FOUR'                   : '4',
              'DEVANAGARI DIGIT FIVE'                   : '5',
              'DEVANAGARI DIGIT SIX'                    : '6',
              'DEVANAGARI DIGIT SEVEN'                  : '7',
              'DEVANAGARI DIGIT HEIGHT'                 : '8',
              'DEVANAGARI DIGIT NINE'                   : '9',
    }

# PUNCTUATION[base_char] = transliterated character
PUNCTUATION = {
               'DEVANAGARI DANDA'                        : '.',
               'DEVANAGARI DOUBLE DANDA'                 : '..',
               'DEVANAGARI ABBREVIATION SIGN'            : '°',                  # (???) see above
               'DEVANAGARI SIGN HIGH SPACING DOT'        : "<HIGH SPACING DOT>", # (???) see above
               'DEVANAGARI SIGN AVAGRAHA'                : ".a",
               ' '                                       : ' ',
               '.'                                       : '<.>',                # (???) see above
               '\n'                                      : '\n',                 # (???) see above
               '\r'                                      : '\r',                 # (???) see above
               '\t'                                      : '\t',                 # (???) see above
               }

DIACRITICS = {
      'DEVANAGARI SIGN INVERTED CANDRABINDU'    : '~.N',                # (???) see above
      'DEVANAGARI SIGN CANDRABINDU'             : '.N',
      'DEVANAGARI SIGN ANUSVARA'                : 'M',
      'DEVANAGARI STRESS SIGN UDATTA'           : "\\'",
      'DEVANAGARI STRESS SIGN ANUDATTA'         : '\\_',
      'DEVANAGARI GRAVE ACCENT'                 : "<GRAVE ACCENT>",     # (???) see above
      'DEVANAGARI ACUTE ACCENT'                 : "<ACUTE ACCENT>",     # (???) see above
    }

CONSONANTS_INVERSED = invertdict(CONSONANTS)
CONSONANTS_URDU_INVERSED = invertdict(CONSONANTS_URDU)
VOWELS_INVERSED = invertdict(VOWELS)
VOWELS_IN_HIATUS_INVERSED = invertdict(VOWELS_IN_HIATUS)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)
DIACRITICS_INVERSED = invertdict(DIACRITICS)
URDU_CONSONANT_2_CONSONANT_INVERSED = invertdict( URDU_CONSONANT_2_CONSONANT )

################################################################################
# transliteration's patterns :
# PATTERN  is used to cut one complex characters into its elements.
# PATTERN2 is used to cut several complex characters into a list of complex characters.
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.
BASE_CHAR = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(CONSONANTS_INVERSED.keys())) + \
                regexstring_list(tuple(CONSONANTS_URDU_INVERSED.keys())) + \
                regexstring_list(tuple(VOWELS_IN_HIATUS_INVERSED.keys())) + \
                regexstring_list(tuple(VOWELS_INVERSED.keys())) + \
                regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )

ANUDATTA = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI STRESS SIGN ANUDATTA']),])

ACCENT   = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI STRESS SIGN UDATTA']),
                 re.escape(DIACRITICS['DEVANAGARI ACUTE ACCENT']),
                 re.escape(DIACRITICS['DEVANAGARI GRAVE ACCENT']),
                ])

ANUSVARA_CANDRABINDU = isort_a_lstrings_bylen_nodup(
                [re.escape(DIACRITICS['DEVANAGARI SIGN ANUSVARA']),
                 re.escape(DIACRITICS['DEVANAGARI SIGN CANDRABINDU']),
                 re.escape(DIACRITICS['DEVANAGARI SIGN INVERTED CANDRABINDU']),
                 ])

PATTERN_TXT = "((?P<base_char>({0}))" \
              "(?P<anudatta>({1}))?" \
              "(?P<accent>({2}))?" \
              "(?P<anusvara_candrabindu>({3}))?)".format(
                            "|".join(prepare_list_to_strformat(BASE_CHAR)),
                            "|".join(prepare_list_to_strformat(ANUDATTA)),
                            "|".join(prepare_list_to_strformat(ACCENT)),
                            "|".join(prepare_list_to_strformat(ANUSVARA_CANDRABINDU)),
                            )

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "(({0})" \
               "({1})?" \
               "({2})?" \
               "({3})?)".format(
                             "|".join(prepare_list_to_strformat(BASE_CHAR)),
                             "|".join(prepare_list_to_strformat(ANUDATTA)),
                             "|".join(prepare_list_to_strformat(ACCENT)),
                             "|".join(prepare_list_to_strformat(ANUSVARA_CANDRABINDU)),
                             )

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')
PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, prev_dchar, dchar):
    """
        function dchar__get_translit_str()

        prev_dchar, dchar : DCharacterSAN object

        Return a transliterared string corresponding to <char>.
    """
    res = []

    if dchar.unknown_char:
        if dstring_object.options["anonymize the unknown characters"] == 'yes':
            return UNKNOWN_CHAR_SYMBOL
        else:
            return dchar.base_char

    if dchar.base_char is not None:

        if dchar.punctuation:
            # punctuation symbol :
            res.append( PUNCTUATION[dchar.base_char] )

        elif dchar.base_char in OTHER_SYMBOLS:
            # not a punctuation symbol nor a consonant or an independent vowel :
            res.append( OTHER_SYMBOLS[dchar.base_char] )

        elif not dchar.is_an_independent_vowel:
            # consonant :
            if not dchar.nukta:
                # pure devanagari consonant :
                res.append( CONSONANTS[dchar.base_char] )
            else:
                # Urdu consonant :
                # dchar.base_char(KA) -> "q"
                urdu_letter = URDU_CONSONANT_2_CONSONANT_INVERSED[dchar.base_char]
                res.append( urdu_letter )

            # dependent vowel ?
            if dchar.dependentvowel is not None:
                res.append( VOWELS[dchar.dependentvowel] )

        else:
            # independent vowel :

            # hiatus ?
            if prev_dchar is None:
                # no hiatus : there's no preceding character.
                res.append( VOWELS[dchar.base_char] )

            elif not prev_dchar.is_an_independent_vowel and \
                 prev_dchar.dependentvowel is not None and \
                 prev_dchar.anusvara_candrabindu is None and \
                 not prev_dchar.virama:
                # yes, hiatus : a consonnant(prev_dchar) is followed by a vowel :
                res.append( VOWELS_IN_HIATUS[dchar.base_char] )

            elif prev_dchar.is_an_independent_vowel and \
                 prev_dchar.anusvara_candrabindu is None:
                 # yes, hiatus : a vowel(prev_dchar) is followed by a vowel :
                res.append( VOWELS_IN_HIATUS[dchar.base_char] )

            else:
                # no, no hiatus : no dependent vowel before the current character.
                res.append( VOWELS[dchar.base_char] )

    if dchar.anudatta:
        res.append( DIACRITICS['DEVANAGARI STRESS SIGN ANUDATTA'] )

    if dchar.accent is not None:
        res.append( DIACRITICS[dchar.accent] )

    if dchar.anusvara_candrabindu is not None:
        res.append( DIACRITICS[dchar.anusvara_candrabindu] )

    return "".join( res )

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function init_from_transliteration()

        dchar   :       DCharacterSAN object
        src     :       string

        Initialize and return <dchar>.

    """
    element = re.match(PATTERN, src)

    if element is None:
        dchar.unknown_char = True
        dchar.base_char = dchar.base_char

    else:
        dchar.unknown_char = False
        dchar.anudatta = element.group('anudatta') is not None
        dchar.nukta = False

        accent = element.group('accent')
        if accent is None:
            dchar.accent = None
        else:
            dchar.accent = DIACRITICS_INVERSED[accent]

        anusvara_candrabindu = element.group('anusvara_candrabindu')
        if anusvara_candrabindu is None:
            dchar.anusvara_candrabindu = None
        else:
            dchar.anusvara_candrabindu = DIACRITICS_INVERSED[anusvara_candrabindu]

        base_char = element.group('base_char')
        if base_char in PUNCTUATION_INVERSED:
            # punctuation symbol :
            dchar.punctuation = True
            dchar.base_char = PUNCTUATION_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

        elif base_char in OTHER_SYMBOLS_INVERSED:
            # not a punctuation symbol nor a consonant or an independent vowel :
            dchar.punctuation = False
            dchar.base_char = OTHER_SYMBOLS_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

        elif base_char in CONSONANTS_INVERSED:
            # pure devanagari consonant :
            dchar.punctuation = False
            dchar.base_char = CONSONANTS_INVERSED[base_char]
            dchar.nukta = False
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

            if dchar.base_char != "DEVANAGARI SIGN VISARGA":
                dchar.virama = True # by default, this consonant has no vowel.

        elif base_char in URDU_CONSONANT_2_CONSONANT:
            # Urdu consonant :
            dchar.punctuation = False
            dchar.base_char = URDU_CONSONANT_2_CONSONANT[base_char]
            dchar.nukta = True
            dchar.is_an_independent_vowel = False
            dchar.dependentvowel = None

            if dchar.base_char != "DEVANAGARI SIGN VISARGA":
                dchar.virama = True # by default, this consonant has no vowel.

        else:
            # independent vowel ? If it's eventually a dependent vowel,
            # it will be analyzed in dstring__init_from_translit_str()
            dchar.punctuation = False
            dchar.is_an_independent_vowel = True
            dchar.dependentvowel = None
            dchar.nukta = False

            if base_char in VOWELS_INVERSED:
                dchar.base_char = VOWELS_INVERSED[base_char]
            else:
                dchar.base_char = VOWELS_IN_HIATUS_INVERSED[base_char]

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring, dcharactertype, src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterSAN
        src             :       string

        Initialize <dstring>.
    """

    for start, dest in TRANS_EQUIVALENCES:
        src = src.replace( start, dest )

    last_real_index = -1
    for element in re.finditer(PATTERN2, src):

        real_indexes = range(element.start(), element.end())

        # we add the unknown chars placed BEFORE OR WITHIN the recognized characters :
        # pylint: disable=W0612
        # Unused variable 'i'
        for i in range( last_real_index+1, min(real_indexes) ):
            new_dcharacter = dcharactertype(dstring_object=dstring)
            new_dcharacter.unknown_char = True
            new_dcharacter.base_char = src[i]
            dstring.append( new_dcharacter )

        # we add the character read by the regex :
        string = element.string[element.start():element.end()]
        new_character = dcharactertype(dstring_object=dstring).init_from_transliteration(
            string,
            transliteration_method="itrans")

        if len(dstring)==0:
            dstring.append(new_character)

        else:

            prev_dchar = dstring[-1]

            if not prev_dchar.is_an_independent_vowel and \
               not prev_dchar.punctuation and \
               prev_dchar.dependentvowel is None and \
               prev_dchar.anusvara_candrabindu is None and \
               new_character.is_an_independent_vowel:

               # dependent vowel : we won't add another character to <dstring>
               # but we modify dstring[-1] :
                dstring[-1].dependentvowel = new_character.base_char
                dstring[-1].accent = new_character.accent
                dstring[-1].anusvara_candrabindu = new_character.anusvara_candrabindu
                dstring[-1].virama = new_character.virama
                dstring[-1].anudatta = new_character.anudatta

            else:
                # normal case :
                dstring.append(new_character)

        last_real_index = max(real_indexes)

    # we add the unknown chars placed AFTER the recognized characters :
    # pylint: disable=W0612
    # Unused variable 'i'
    for i in range( last_real_index+1, len(src) ):
        new_dcharacter = dcharactertype(dstring_object=dstring)
        new_dcharacter.unknown_char = True
        new_dcharacter.base_char = src[i]
        dstring.append( new_dcharacter )
