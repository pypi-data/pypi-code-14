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
    ❏DChars❏ : dchars/dchars.py
"""

# problem with Pylint :
# pylint: disable=E0611
# "No name 'errors' in module 'dchars.errors'"
from dchars.errors.errors import DCharsError
import os.path
from dchars.languages_name import LANGUAGES_NAME, \
                                  BIBLICAL_HEBREW__NAME, \
                                  LANGUAGES_AND_TRANSLITERATIONS
import dchars.config_ini
from dchars.config_ini_data import DATA
#...............................................................................
# CONFIG_INI : options read in the configuration file.
#...............................................................................

# problem with Pylint :
# pylint: disable=F0401
# "Unable to import 'configparser'"
import configparser, codecs
CONFIG_INI = configparser.ConfigParser()
# about the following line : why not simply CONFIG_INI.read( "dchars", "config.ini") ?
# -> once installed, DChars have to know the exact path to config.ini,
# hence the following line (idea given by Frank Zago)
CONFIG_INI_FILENAME =  os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "config.ini" )
# Something's wrong with configparser : instead of simply writing
#     DATA.read( open(CONFIG_INI_FILENAME, "r", encoding="utf-8") )
# we have to use this strange hack :
CONFIG_INI.readfp( codecs.open(CONFIG_INI_FILENAME, "r", "utf-8") )

# we check the accurency of the informations stored in the config.ini file :
dchars.config_ini.check(CONFIG_INI)

#...............................................................................
# LANGUAGES : informations about each language. Please use three kinds of keys
#             for each language : English name, iso639-3 name and original name.
#
#                     (iso639-3 name,
#                      string type's name,
#                      default transliteration method,
#                      default options)
#
#...............................................................................

LANGUAGES = {

                #...............................................................
                "Ænglisc" :
                ("ang",
                 "DStringANG",
                 CONFIG_INI["ang"]["transliteration method"],

                 {DATA["ang"].get_optionname("sorting method"): \
                  CONFIG_INI["ang"]["sorting method"],

                  DATA["ang"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["ang"]["anonymize the unknown characters"],
                 }
                ),

                #...............................................................
                "བོད་ཡིག"         :
                ("bod",
                 "DStringBOD",
                  CONFIG_INI["bod"]["transliteration method"],

                  {DATA["bod"].get_optionname("sorting method")        : \
                   CONFIG_INI["bod"]["sorting method"],

                   DATA["bod"].get_optionname("expected structure")    : \
                   CONFIG_INI["bod"]["expected structure"],

                   DATA["bod"].get_optionname("look up in the buffers"): \
                   CONFIG_INI["bod"]["look up in the buffers"],

                   DATA["bod"].get_optionname("fill the buffers")      : \
                   CONFIG_INI["bod"]["fill the buffers"],

                   DATA["bod"].get_optionname("anonymize the unknown characters") : \
                   CONFIG_INI["bod"]["anonymize the unknown characters"],
                 },
                ),

                #...............................................................
                "romanz" :
                ("fro",
                 "DStringFRO",
                 CONFIG_INI["fro"]["transliteration method"],

                 {DATA["lat"].get_optionname("sorting method"): \
                  CONFIG_INI["fro"]["sorting method"],

                  DATA["lat"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["fro"]["anonymize the unknown characters"],
                 }
                ),

                #...............................................................
                "Ἑλληνικὴ γλῶττα":
                ("grc",
                 "DStringGRC",
                 CONFIG_INI["grc"]["transliteration method"],

                 {DATA["grc"].get_optionname("sorting method"): \
                  CONFIG_INI["grc"]["sorting method"],

                  DATA["grc"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["grc"]["anonymize the unknown characters"],

                  DATA["grc"].get_optionname("ignore accents"): \
                  CONFIG_INI["grc.gutenberg"]["ignore accents"],

                  DATA["grc"].get_optionname("ignore smooth breathing"): \
                  CONFIG_INI["grc.gutenberg"]["ignore smooth breathing"],

                  DATA["grc"].get_optionname("ignore diaeresis"): \
                  CONFIG_INI["grc.gutenberg"]["ignore diaeresis"],

                  DATA["grc"].get_optionname("ignore iota subscript"): \
                  CONFIG_INI["grc.gutenberg"]["ignore iota subscript"],

                  DATA["grc"].get_optionname("transliteration for upsilon"): \
                  CONFIG_INI["grc.gutenberg"]["transliteration for upsilon"],

                  DATA["grc"].get_optionname("hh becomes h"): \
                  CONFIG_INI["grc.gutenberg"]["hh becomes h"],

                  DATA["grc"].get_optionname("ignore makron and brakhu"): \
                  CONFIG_INI["grc.gutenberg"]["ignore makron and brakhu"],
                 }
                ),

                #...............................................................
                BIBLICAL_HEBREW__NAME :
                ("hbo",
                 "DStringHBO",
                 CONFIG_INI["hbo"]["transliteration method"],

                 {DATA["hbo"].get_optionname("sorting method"): \
                  CONFIG_INI["hbo"]["sorting method"],

                  DATA["hbo"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["hbo"]["anonymize the unknown characters"],
                 }
                ),

                #...............................................................
                "日本語" :
                ("jpn",
                 "DStringJPN",
                 CONFIG_INI["jpn"]["transliteration method"],

                 {DATA["jpn"].get_optionname("sorting method"): \
                  CONFIG_INI["jpn"]["sorting method"],

                  DATA["jpn"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["jpn"]["anonymize the unknown characters"],

                  DATA["jpn"].get_optionname("long vowels written with circumflex"): \
                  CONFIG_INI["jpn.shepburn"]["long vowels written with circumflex"],

                  DATA["jpn"].get_optionname("katakanas written with upper case letters"): \
                  CONFIG_INI["jpn.shepburn"]["katakanas written with upper case letters"],

                  DATA["jpn"].get_optionname("ou becomes ō"): \
                  CONFIG_INI["jpn.shepburn"]["ou becomes ō"],
                 }
                ),

                #...............................................................
                "latīna" :
                ("lat",
                 "DStringLAT",
                 CONFIG_INI["lat"]["transliteration method"],

                 {DATA["lat"].get_optionname("sorting method"): \
                  CONFIG_INI["lat"]["sorting method"],

                  DATA["lat"].get_optionname("anonymize the unknown characters"): \
                  CONFIG_INI["lat"]["anonymize the unknown characters"],
                 }
                ),

                #...............................................................
                "संस्कृतम्" :
                ("san",
                 "DStringSAN",
                 CONFIG_INI["san"]["transliteration method"],

                {DATA["san"].get_optionname("sorting method"): \
                 CONFIG_INI["san"]["sorting method"],

                 DATA["san"].get_optionname("anonymize the unknown characters"): \
                 CONFIG_INI["san"]["anonymize the unknown characters"],
                 }
                ),
            }

# dict : key(language's name, iso639-3) : corresponding dstring type
# E.g.   LOADED_LANGUAGES["bod"] = dchars.languages.bod.dstring.DStringBOD
LOADED_LANGUAGES = {}

#///////////////////////////////////////////////////////////////////////////////
def new_dstring(language, transliteration_method=None, options=None):
    """
        Return a DString* type, e.g. DStringBOD for Tibetan.

        _language               : str
        transliteration_method  : str / None to use defaulttransliteration
        options                 : dict of strings
    """

    #...........................................................................
    # error : unknown language's name.
    #...........................................................................
    if not language in LANGUAGES_NAME:

        msg = "unknown language : '{0}'; known languages={1}".format(
            language,
            list(LANGUAGES.keys() ))

        raise DCharsError( context = "dchars/dchars.py",
                           message = msg,
                         )

    #...........................................................................
    # original language's name :
    #...........................................................................
    _language = LANGUAGES_NAME[language]

    #...........................................................................
    # we get the informations from LANGUAGES :
    #...........................................................................
    (language_iso639_3_name,
     dstring_name,
     default_trans_method,
     default_options) = LANGUAGES[_language]

    #...........................................................................
    # we import the module linked to dstring_name :
    #...........................................................................
    if language_iso639_3_name not in LOADED_LANGUAGES:

        # the following lines are equivalent, e.g. to :
        #    from dchars.languages.lat.dstring import DStringLAT
        #
        # (see http://docs.python.org/3.3/library/functions.html?highlight=__import__#__import__)
        module_name = "dchars.languages.{0}.dstring".format(language_iso639_3_name)
        module = __import__( module_name, globals(), locals(), [dstring_name,], 0)
        dstring_type = getattr( module, dstring_name )
        LOADED_LANGUAGES[language_iso639_3_name] = dstring_type
    else:
        dstring_type = LOADED_LANGUAGES[language_iso639_3_name]

    #...........................................................................
    # if no transliteration method specified as argument, we get the default method :
    #...........................................................................
    _transliteration_method = transliteration_method
    if _transliteration_method is None:
        _transliteration_method = default_trans_method

    # error : unknown transliteration method
    if not _transliteration_method in LANGUAGES_AND_TRANSLITERATIONS[_language]:

        msg = "unknown transliteration method : '{0}'; known methods={1}".format(
            _transliteration_method,
            LANGUAGES_AND_TRANSLITERATIONS[_language]
            )

        raise DCharsError( context = "dchars/dchars.py",
                           message = msg,
                         )
    #...........................................................................
    # _options is either equal to <options> either equal to the default options :
    #...........................................................................
    if options is None:
        _options = default_options.copy()
    else:
        _options = default_options.copy()
        # we add the options given in the arguments :
        for option in options:
            _options[option] = options[option]

    #...........................................................................
    # return value :
    #...........................................................................
    dstring = type( 'DString',
                    (dstring_type,),
                    {'iso639_3_name' : language_iso639_3_name,
                     'transliteration_method' : _transliteration_method,
                     'options' : _options} )

    return dstring

#///////////////////////////////////////////////////////////////////////////////
def sort_a_list_of_words(words, dstring_object):
    """
        sort_a_list_of_words function :

        * words : iterable of (unicode) words, like ["Μῆνιν", "ἄειδε", ...]
        * dstring_object, DSTRING object, like new_dstring(language="grc")

        Return an object whose type is type(words), sorted.
    """
    # list of (unicode) words -> list of (DString*) words
    dstring_words = map(dstring_object, words)

    # we sort the list :
    sorted_words = sorted(dstring_words, key=dstring_object.sortingvalue)

    # we return a list of (unicode) words :
    return type(words)(map(dstring_object.__str__, sorted_words))

