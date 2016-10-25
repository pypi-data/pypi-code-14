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
    ❏DChars❏ : dchars/languages/jpn/transliterations/shepburn/shepburn.py
"""

from collections import OrderedDict

from dchars.utilities.regexstring import regexstring_list
from dchars.utilities.dicttools import invertdict
from dchars.utilities.lstringtools import isort_a_lstrings_bylen_nodup
from dchars.utilities.lstringtools import prepare_list_to_strformat
from dchars.symbols.symbols import UNKNOWN_CHAR_SYMBOL
from dchars.languages.jpn.symbols import DEFAULTSYMB__CHOONPU, \
                                         HIRAGANA_TO_HIRAGANA_DAKUTEN, \
                                         HIRAGANA_TO_HIRAGANA_HANDAKUTEN, \
                                         KATAKANA_TO_KATAKANA_DAKUTEN, \
                                         KATAKANA_TO_KATAKANA_HANDAKUTEN, \
                                         HIRAGANA_TO_KATAKANA, \
                                         HIRAGANA_DAKUTEN_TO_HIRAGANA, \
                                         HIRAGANA_HANDAKUTEN_TO_HIRAGANA, \
                                         KATAKANA_TO_HIRAGANA, \
                                         SMALL_HIRAGANA_TO_HIRAGANA, \
                                         SMALL_KATAKANA_TO_KATAKANA, \
                                         KATAKANA_DAKUTEN_TO_KATAKANA, \
                                         KATAKANA_HANDAKUTEN_TO_KATAKANA
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
        ("â", "ā",),
        ("ê", "ē"),
        ("ô", "ō"),
        ("û", "ū"),

        ("Â", "Ā",),
        ("Ê", "Ē"),
        ("Ô", "Ō"),
        ("Û", "Ū"),
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
# HIRAGANA[base_char] = transliterated character

# about "ー" (the chōonpu 長音符 symbol),
# confer http://en.wikipedia.org/wiki/Ch%C5%8Donpu
CHOONPU = {
      'ー'      : "ー",
    }

HIRAGANA = {
      'あ'        : "a",
      'い'        : "i",
      'う'        : "u",
      'え'        : "e",
      'お'        : "o",
      'か'        : "ka",
      'き'        : "ki",
      'く'        : "ku",
      'け'        : "ke",
      'こ'        : "ko",
      'さ'        : "sa",
      'し'        : "shi",
      'す'        : "su",
      'せ'        : "se",
      'そ'        : "so",
      'た'        : "ta",
      'ち'        : "chi",
      'つ'        : "tsu",
      'て'        : "te",
      'と'        : "to",
      'な'        : "na",
      'に'        : "ni",
      'ぬ'        : "nu",
      'ね'        : "ne",
      'の'        : "no",
      'は'        : "ha",
      'ひ'        : "hi",
      'ふ'        : "fu",
      'へ'        : "he",
      'ほ'        : "ho",
      'ま'        : "ma",
      'み'        : "mi",
      'む'        : "mu",
      'め'        : "me",
      'も'        : "mo",
      'や'        : "ya",
      'ゆ'        : "yu",
      'よ'        : "yo",
      'ら'        : "ra",
      'り'        : "ri",
      'る'        : "ru",
      'れ'        : "re",
      'ろ'        : "ro",
      'わ'        : "wa",
      'ゐ'        : "wi",
      'ゑ'        : "we",
      'を'        : "wo",
      'ん'        : "n[0]",

      'ぁ'      : "[-]a",
      'ぃ'      : "[-]i",
      'ぅ'      : "[-]u",
      'ぇ'      : "[-]e",
      'ぉ'      : "[-]o",
      'ゕ'      : "[-]ka",
      'ゖ'      : "[-]ke",
      'っ'      : "[-]tsu",
      'ゃ'      : "[-]ya",
      'ゅ'      : "[-]yu",
      'ょ'      : "[-]yo",
      'ゎ'      : "[-]wa",
    }

HIRAGANA_DAKUTEN = {
      'が'        : "ga",
      'ぎ'        : 'gi',
      'ぐ'        : 'gu',
      'げ'        : 'ge',
      'ご'        : 'go',
      'ざ'        : 'za',
      'じ'        : 'ji',
      'ず'        : 'zu',
      'ぜ'        : 'ze',
      'ぞ'        : 'zo',
      'だ'        : 'da',
      'ぢ'        : 'ji*', # required but officially without the '*'
      'づ'        : 'zu*', # required but officially without the '*'
      'で'        : 'de',
      'ど'        : 'do',
      'ば'        : 'ba',
      'び'        : 'bi',
      'ぶ'        : 'bu',
      'べ'        : 'be',
      'ぼ'        : 'bo',
    }

HIRAGANA_HANDAKUTEN = {
      'ぱ'        : "pa",
      'ぴ'        : 'pi',
      'ぷ'        : 'pu',
      'ぺ'        : 'pe',
      'ぽ'        : 'po',
    }

KATAKANA = {
      'ア'        : "A",
      'イ'        : "I",
      'ウ'        : "U",
      'エ'        : "E",
      'オ'        : "O",
      'カ'        : "KA",
      'キ'        : "KI",
      'ク'        : "KU",
      'ケ'        : "KE",
      'コ'        : "KO",
      'サ'        : "SA",
      'シ'        : "SHI",
      'ス'        : "SU",
      'セ'        : "SE",
      'ソ'        : "SO",
      'タ'        : "TA",
      'チ'        : "CHI",
      'ツ'        : "TSU",
      'テ'        : "TE",
      'ト'        : "TO",
      'ナ'        : "NA",
      'ニ'        : "NI",
      'ヌ'        : "NU",
      'ネ'        : "NE",
      'ノ'        : "NO",
      'ハ'        : "HA",
      'ヒ'        : "HI",
      'フ'        : "FU",
      'ヘ'        : "HE",
      'ホ'        : "HO",
      'マ'        : "MA",
      'ミ'        : "MI",
      'ム'        : "MU",
      'メ'        : "ME",
      'モ'        : "MO",
      'ヤ'        : "YA",
      'ユ'        : "YU",
      'ヨ'        : "YO",
      'ラ'        : "RA",
      'リ'        : "RI",
      'ル'        : "RU",
      'レ'        : "RE",
      'ロ'        : "RO",
      'ワ'        : "WA",
      'ヰ'        : "WI",
      'ヱ'        : "WE",
      'ヲ'        : "WO",
      'ン'        : "N[0]",

      'ァ'      : "[-]A",
      'ィ'      : "[-]I",
      'ゥ'      : "[-]U",
      'ェ'      : "[-]E",
      'ォ'      : "[-]O",
      'ヵ'      : "[-]KA",
      'ヶ'      : "[-]KE",
      'ッ'      : "[-]TSU",
      'ャ'      : "[-]YA",
      'ュ'      : "[-]YU",
      'ョ'      : "[-]YO",
      'ヮ'      : "[-]WA",
    }

KATAKANA_DAKUTEN = {
      'ガ'        : "GA",
      'ギ'        : 'GI',
      'グ'        : 'GU',
      'ゲ'        : 'GE',
      'ゴ'        : 'GO',
      'ザ'        : 'ZA',
      'ジ'        : 'JI',
      'ズ'        : 'ZU',
      'ゼ'        : 'ZE',
      'ゾ'        : 'ZO',
      'ダ'        : 'DA',
      'ヂ'        : 'JI*',  # required but officially without the '*'
      'ヅ'        : 'ZU*',  # required but officially without the '*'
      'デ'        : 'DE',
      'ド'        : 'DO',
      'バ'        : 'BA',
      'ビ'        : 'BI',
      'ブ'        : 'BU',
      'ベ'        : 'BE',
      'ボ'        : 'BO',
    }

KATAKANA_HANDAKUTEN = {
      'パ'        : "PA",
      'ピ'        : 'PI',
      'プ'        : 'PU',
      'ペ'        : 'PE',
      'ポ'        : 'PO',
    }

# OTHER_SYMBOLS[base_char] = transliterated character
OTHER_SYMBOLS = {
               '0'       : '0',
               '1'       : '1',
               '2'       : '2',
               '3'       : '3',
               '4'       : '4',
               '5'       : '5',
               '6'       : '6',
               '7'       : '7',
               '8'       : '8',
               '9'       : '9',
         }

# PUNCTUATION[base_char] = transliterated character
PUNCTUATION = {'-'       : '-',
               ')'       : ')',
               '('       : '(',
               '['       : '[',
               ']'       : ']',
               '{'       : '{',
               '}'       : '}',
               ' '       : ' ',
               '.'       : '.',
               ','       : ',',
               ';'       : '?',
               '!'       : '!',
               '·'       : ';',
               '"'       : '"',
               "'"       : "'",
               "—"       : "_",
               ":"       : ":",
               '\n'      : '\n',
               '\r'      : '\r',
               '\t'      : '\t',
              }

CHOONPU_INVERSED = invertdict(CHOONPU)
HIRAGANA_INVERSED = invertdict(HIRAGANA)
HIRAGANA_DAKUTEN_INVERSED = invertdict(HIRAGANA_DAKUTEN)
HIRAGANA_HANDAKUTEN_INVERSED = invertdict(HIRAGANA_HANDAKUTEN)
KATAKANA_INVERSED = invertdict(KATAKANA)
KATAKANA_DAKUTEN_INVERSED = invertdict(KATAKANA_DAKUTEN)
KATAKANA_HANDAKUTEN_INVERSED = invertdict(KATAKANA_HANDAKUTEN)
OTHER_SYMBOLS_INVERSED = invertdict(OTHER_SYMBOLS)
PUNCTUATION_INVERSED = invertdict(PUNCTUATION)

# Be carefull : order matters, hence the use of an OrderedDict object.
COMPOSED_TRANSCRIPTIONS = OrderedDict((

        ("shi[-]ya"      , "sha"),
        ("shi[-]yu"      , "shu"),
        ("shi[-]yo"      , "sho"),
        ("shi[-]yâ"      , "shâ"),
        ("shi[-]yû"      , "shû"),
        ("shi[-]yô"      , "shô"),
        ("shi[-]yā"      , "shā"),
        ("shi[-]yū"      , "shū"),
        ("shi[-]yō"      , "shō"),

        ("ji[-]ya"      , "ja"),
        ("ji[-]yu"      , "ju"),
        ("ji[-]yo"      , "jo"),
        ("ji[-]yâ"      , "jâ"),
        ("ji[-]yû"      , "jû"),
        ("ji[-]yô"      , "jô"),
        ("ji[-]yā"      , "jā"),
        ("ji[-]yū"      , "jū"),
        ("ji[-]yō"      , "jō"),

        ("chi[-]ya"      , "cha"),
        ("chi[-]yu"      , "chu"),
        ("chi[-]yo"      , "cho"),
        ("chi[-]yâ"      , "châ"),
        ("chi[-]yû"      , "chû"),
        ("chi[-]yô"      , "chô"),
        ("chi[-]yā"      , "chā"),
        ("chi[-]yū"      , "chū"),
        ("chi[-]yō"      , "chō"),

        ("KI[-]Y"    , "KY"),
        ("GI[-]Y"    , "GY"),
        ("NI[-]Y"    , "NY"),
        ("HI[-]Y"    , "HY"),
        ("BI[-]Y"    , "BY"),
        ("PI[-]Y"    , "PY"),
        ("MI[-]Y"    , "MY"),
        ("RI[-]Y"    , "RY"),

        ("SHI[-]YA"      , "SHA"),
        ("SHI[-]YU"      , "SHU"),
        ("SHI[-]YO"      , "SHO"),
        ("SHI[-]YÂ"      , "SHÂ"),
        ("SHI[-]YÛ"      , "SHÛ"),
        ("SHI[-]YÔ"      , "SHÔ"),
        ("SHI[-]YĀ"      , "SHĀ"),
        ("SHI[-]YŪ"      , "SHŪ"),
        ("SHI[-]YŌ"      , "SHŌ"),

        ("JI[-]YA"      , "JA"),
        ("JI[-]YU"      , "JU"),
        ("JI[-]YO"      , "JO"),
        ("JI[-]YÂ"      , "JÂ"),
        ("JI[-]YÛ"      , "JÛ"),
        ("JI[-]YÔ"      , "JÔ"),
        ("JI[-]YĀ"      , "JĀ"),
        ("JI[-]YŪ"      , "JŪ"),
        ("JI[-]YŌ"      , "JŌ"),

        ("CHI[-]YA"      , "CHA"),
        ("CHI[-]YU"      , "CHU"),
        ("CHI[-]YO"      , "CHO"),
        ("CHI[-]YÂ"      , "CHÂ"),
        ("CHI[-]YÛ"      , "CHÛ"),
        ("CHI[-]YÔ"      , "CHÔ"),
        ("CHI[-]YĀ"      , "CHĀ"),
        ("CHI[-]YŪ"      , "CHŪ"),
        ("CHI[-]YŌ"      , "CHŌ"),

        # "traditional" Hepburn ,
        #("n[0]b"        , "mb"),
        #("n[0]m"        , "mm"),
        #("n[0]p"        , "mp"),

        ("n[0]y"        , "n'y"),

        ("n[0]a"        , "n'a"),
        ("n[0]ā"        , "n'ā"),
        ("n[0]e"        , "n'e"),
        ("n[0]ē"        , "n'ē"),
        ("n[0]i"        , "n'i"),
        ("n[0]ī"        , "n'ī"),
        ("n[0]o"        , "n'o"),
        ("n[0]ō"        , "n'ō"),
        ("n[0]u"        , "n'u"),
        ("n[0]ū"        , "n'ū"),

        ("Aー"                   , "Ā"),
        ("Eー"                   , "Ē"),
        ("Iー"                   , "Ī"),
        ("Oー"                   , "Ō"),
        ("Uー"                   , "Ū"),

        ("ki[-]y"    , "ky"),
        ("gi[-]y"    , "gy"),
        ("ni[-]y"    , "ny"),
        ("hi[-]y"    , "hy"),
        ("bi[-]y"    , "by"),
        ("pi[-]y"    , "py"),
        ("mi[-]y"    , "my"),
        ("ri[-]y"    , "ry"),

        # sokuon : http://en.wikipedia.org/wiki/Sokuon
        ("[-]tsush"        , "ssh"),
        ("[-]tsuj"         , "jj"),
        ("[-]tsuch"        , "tch"),
        ("[-]tsuts"        , "tts"),
        ("[-]tsuk"         , "kk"),
        ("[-]tsug"         , "gg"),
        ("[-]tsus"         , "ss"),
        ("[-]tsuz"         , "zz"),
        ("[-]tsut"         , "tt"),
        ("[-]tsud"         , "dd"),
        ("[-]tsuh"         , "hh"),
        ("[-]tsub"         , "bb"),
        ("[-]tsup"         , "pp"),
    ))

################################################################################
# transliteration's patterns :
# PATTERN  is used to cut one complex characters into its elements.
# PATTERN2 is used to cut several complex characters into a list of complex characters.
################################################################################

# in order to build the pattern strings for the regexes we have to SORT the
# result : (|a|b|t|th) won't find 'th' in "theatre" but (th|a|b|t) will.
# We delete the possible duplicates in the resulting string.

LETTERS = isort_a_lstrings_bylen_nodup(
                regexstring_list(tuple(CHOONPU.keys())) + \
                regexstring_list(tuple(HIRAGANA_INVERSED.keys())) + \
                regexstring_list(tuple(HIRAGANA_DAKUTEN_INVERSED.keys())) + \
                regexstring_list(tuple(HIRAGANA_HANDAKUTEN_INVERSED.keys())) + \
                regexstring_list(tuple(KATAKANA_INVERSED.keys())) + \
                regexstring_list(tuple(KATAKANA_DAKUTEN_INVERSED.keys())) + \
                regexstring_list(tuple(KATAKANA_HANDAKUTEN_INVERSED.keys())) + \
                regexstring_list(tuple(OTHER_SYMBOLS_INVERSED.keys())) + \
                regexstring_list(tuple(PUNCTUATION_INVERSED.keys())) )

PATTERN_TXT = "(?P<base_char>({0}))".format("|".join(prepare_list_to_strformat(LETTERS)),)

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT = PATTERN_TXT.replace('{{', '{')
PATTERN_TXT = PATTERN_TXT.replace('}}', '}')
PATTERN = re.compile(PATTERN_TXT)

PATTERN_TXT2 = "({0})".format("|".join(prepare_list_to_strformat(LETTERS)),)

# we inverse the effect of prepare_list_to_strformat()
PATTERN_TXT2 = PATTERN_TXT2.replace('{{', '{')
PATTERN_TXT2 = PATTERN_TXT2.replace('}}', '}')

PATTERN2 = re.compile(PATTERN_TXT2)

#///////////////////////////////////////////////////////////////////////////////
def dchar__get_translit_str(dstring_object, dchar):
    """
        function dchar__get_translit_str()

        dchar : DCharacterJPN object

        Return a transliterared string corresponding to <dchar>.
    """
    res = []

    if dchar.unknown_char:
        if dstring_object.options["anonymize the unknown characters"] == 'yes':
            return UNKNOWN_CHAR_SYMBOL
        else:
            return dchar.base_char

    if dchar.base_char is not None:

        if dchar.punctuation:
            res.append( PUNCTUATION[dchar.base_char] )

        elif dchar.chartype == 'hiragana':

            if dchar.diacritic is None:
                if dchar.smallsize:
                    res.append( "[-]" )

                res.append( HIRAGANA[dchar.base_char] )

            elif dchar.diacritic == 'dakuten':
                res.append( HIRAGANA_DAKUTEN[ HIRAGANA_TO_HIRAGANA_DAKUTEN[ dchar.base_char ] ] )
            elif dchar.diacritic == 'handakuten':
                res.append( \
                    HIRAGANA_HANDAKUTEN[ HIRAGANA_TO_HIRAGANA_HANDAKUTEN[ dchar.base_char ]])

        elif dchar.chartype == 'katakana':

            if dchar.diacritic is None:
                if dchar.smallsize:
                    res.append( "[-]" )

                res.append( KATAKANA[ HIRAGANA_TO_KATAKANA[dchar.base_char]] )
            elif dchar.diacritic == 'dakuten':
                res.append( KATAKANA_DAKUTEN[ \
                    KATAKANA_TO_KATAKANA_DAKUTEN[ HIRAGANA_TO_KATAKANA[dchar.base_char]]] )
            elif dchar.diacritic == 'handakuten':
                res.append( KATAKANA_HANDAKUTEN[ \
                    KATAKANA_TO_KATAKANA_HANDAKUTEN[ HIRAGANA_TO_KATAKANA[dchar.base_char]]] )

        elif dchar.chartype == 'choonpu':

            res.append( DEFAULTSYMB__CHOONPU )

    return "".join( res )

#///////////////////////////////////////////////////////////////////////////////
def dchar__init_from_translit_str(dchar, src):
    """
        function dchar__init_from_translit_str()

        dchar   :       DCharacterJPN object
        src     :       string

        Initialize and return <dchar>.

    """
    element = re.match(PATTERN, src)

    if element is None:
        dchar.unknown_char = True
        dchar.base_char = dchar.base_char

    else:
        dchar.unknown_char = False

        base_char = element.group('base_char')
        if base_char in CHOONPU_INVERSED:
            dchar.chartype = "choonpu"
            dchar.diacritic = None
            dchar.smallsize = False
            dchar.base_char = DEFAULTSYMB__CHOONPU

        elif base_char in HIRAGANA_INVERSED:
            dchar.chartype = "hiragana"
            dchar.diacritic = None

            if HIRAGANA_INVERSED[base_char] not in SMALL_HIRAGANA_TO_HIRAGANA:
                dchar.smallsize = False
                dchar.base_char = HIRAGANA_INVERSED[base_char]
            else:
                # small hiragana ;
                dchar.smallsize = True
                dchar.base_char = SMALL_HIRAGANA_TO_HIRAGANA[ HIRAGANA_INVERSED[base_char] ]

            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in HIRAGANA_DAKUTEN_INVERSED:
            dchar.chartype = "hiragana"
            dchar.smallsize = False
            dchar.diacritic = "dakuten"
            dchar.base_char = HIRAGANA_DAKUTEN_TO_HIRAGANA[ HIRAGANA_DAKUTEN_INVERSED[base_char] ]
            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in HIRAGANA_HANDAKUTEN_INVERSED:
            dchar.chartype = "hiragana"
            dchar.smallsize = False
            dchar.diacritic = "handakuten"
            dchar.base_char = \
              HIRAGANA_HANDAKUTEN_TO_HIRAGANA[ HIRAGANA_HANDAKUTEN_INVERSED[base_char] ]
            dchar.capital_letter = False
            dchar.punctuation = False

        if base_char in KATAKANA_INVERSED:
            dchar.chartype = "katakana"
            dchar.diacritic = None

            if KATAKANA_INVERSED[base_char] not in SMALL_KATAKANA_TO_KATAKANA:
                dchar.smallsize = False
                dchar.base_char = KATAKANA_TO_HIRAGANA[ KATAKANA_INVERSED[base_char] ]
            else:
                # small katakana ;
                dchar.smallsize = True
                dchar.base_char = \
                  KATAKANA_TO_HIRAGANA[ SMALL_KATAKANA_TO_KATAKANA[KATAKANA_INVERSED[base_char]] ]

            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in KATAKANA_DAKUTEN_INVERSED:
            dchar.chartype = "katakana"
            dchar.smallsize = False
            dchar.diacritic = "dakuten"
            dchar.base_char = \
              KATAKANA_TO_HIRAGANA[ KATAKANA_DAKUTEN_TO_KATAKANA[ \
                                                    KATAKANA_DAKUTEN_INVERSED[base_char] ] ]
            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in KATAKANA_HANDAKUTEN_INVERSED:
            dchar.chartype = "katakana"
            dchar.smallsize = False
            dchar.diacritic = "handakuten"

            dchar.base_char = \
              KATAKANA_TO_HIRAGANA[ KATAKANA_HANDAKUTEN_TO_KATAKANA[ \
                                                    KATAKANA_HANDAKUTEN_INVERSED[base_char] ] ]
            dchar.capital_letter = False
            dchar.punctuation = False

        elif base_char in PUNCTUATION:
            dchar.chartype = "other"
            dchar.smallsize = False
            dchar.base_char = PUNCTUATION_INVERSED[base_char]
            dchar.capital_letter = False
            dchar.punctuation = True

    return dchar

#///////////////////////////////////////////////////////////////////////////////
def dstring__init_from_translit_str(dstring, dcharactertype, src):
    """
        function dstring__init_from_translit_str()

        dstring         :       DString object
        dcharactertype  :       type of DCharacterJPN
        src             :       string

        Initialize <dstring>.
    """
    for start, dest in TRANS_EQUIVALENCES:
        src = src.replace( start, dest )

    for after, before in COMPOSED_TRANSCRIPTIONS.items():
        src = src.replace( before, after )

    #...........................................................................
    # if a 'n'/'N' isn't followed by a vowel, n > "n[0]", N > "N[0]"

    # indexes of the 'n' / 'N' to be replaced :
    n_indexes = []
    N_indexes = []
    for index, char in enumerate(src):

        if char == 'n' or char == 'N':

            if index == len(src)-1:
                # this 'n'/'N' is the last character of <src> :
                if char == 'n':
                    n_indexes.append(index)
                else:
                    N_indexes.append(index)
            else:
                if src[index+1] not in ('a', 'e', 'i', 'o', 'u',
                                        'â', 'ê', 'ô', 'û',
                                        'ā', 'ē', 'ō', 'ū',
                                        'A', 'E', 'I', 'O', 'U',
                                        'Â', 'Ê', 'Î', 'Ô', 'Û',
                                        'Ā', 'Ē', 'Ī', 'Ō', 'Ū',
                                        '[',
                                        ):
                    if char == 'n':
                        n_indexes.append(index)
                    else:
                        N_indexes.append(index)

    # the selected 'n'/'N' becomes "n[0]" / "N[0]"
    for index in n_indexes:
        src = src[:index] + "n[0]" + src[index+1:]
    for index in N_indexes:
        src = src[:index] + "N[0]" + src[index+1:]

    #...........................................................................
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
        new_character = dcharactertype(dstring_object=dstring).init_from_transliteration(string,
                                                                   "shepburn")
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

#///////////////////////////////////////////////////////////////////////////////
def dstring__trans__get_trans(dstring_object):
    """
        function dstring__trans__get_trans

        Return a (unicode) string corresponding to the <dstring_object>.
    """
    res = []

    for dchar in dstring_object:
        res.append( dchar__get_translit_str(dstring_object = dstring_object,
                                            dchar = dchar))

    res = "".join( res )

    for before, after in COMPOSED_TRANSCRIPTIONS.items():
        res = res.replace(before, after)

    # ん,ン > "n[0]" > "n"
    res = res.replace("n[0]", "n")

    if dstring_object.options["ou becomes ō"] == 'yes':
        res = res.replace("ou", "ō")
        res = res.replace("OU", "Ō")

    if dstring_object.options["long vowels written with circumflex"] == 'yes':
        res = res.replace("ā", "â")
        res = res.replace("ē", "ê")
        res = res.replace("ō", "ô")
        res = res.replace("ū", "û")

    if dstring_object.options["katakanas written with upper case letters"] == 'no':
        res = res.lower()

    return res
