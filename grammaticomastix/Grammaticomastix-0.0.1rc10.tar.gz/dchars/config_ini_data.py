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
    ❏DChars❏ : dchars/config_ini_data.py

    Data related to the config.ini file, especially the dict <DATA>.
"""

from dchars.errors.errors import DCharsError

################################################################################
class ConfigValue(object):
    """
        class ConfigValue : define the equivalent to the following lines in
        a config.ini file :

            [bod.bodsan]                -> subsection (can be empty if no subsection)

            # "high", "normal", "low"   -> list of values
            san2bod quality : high      -> name : defaultvalue
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__( self, subsection, values, name, defaultvalue, optionname ):
        """
                ConfigValue.__init__

                subsection      :       (str) can be empty
                values          :       (tuple of str)
                name            :       (str)
                defaultvalue    :       (str)
                optionname      :       (str)   (name of the option in dchars.py::LANGUAGES)
        """
        self.subsection = subsection
        self.values = values
        self.name = name
        self.defaultvalue = defaultvalue
        self.optionname = optionname

    #///////////////////////////////////////////////////////////////////////////
    def __repr__( self ):
        """
                ConfigValue.__repr__
        """
        txt = "subsection={0}; values={1}; name={2}; defaultvalue={3}; optionname={4};"
        return txt.format( self.subsection,
                           self.values,
                           self.name,
                           self.defaultvalue,
                           self.optionname )

################################################################################
class ConfigValuesForOneLanguage(list):
    """
        class ConfigValuesForOneLanguage

        A list of <ConfigValue> objects, with a header specific to the language.
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, header):
        """
                ConfigValuesForOneLanguage.__init__

                header  :       (str)
        """
        list.__init__(self)
        self.header = header

    #///////////////////////////////////////////////////////////////////////////
    def known_name(self, name):
        """
                ConfigValuesForOneLanguage.known_name

                name    :       (str)

                Return either True if <name> exists in self, either False
        """
        res = False

        for configvalue in self:
            if configvalue.name == name:
                res = True
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def name_have_a_known_value(self, name, value):
        """
                ConfigValuesForOneLanguage.name_have_a_known_value

                name    :       (str)
                value   :       (str)

                Return either True if <value> is a correct value for <name>, either False
        """
        res = False

        for configvalue in self:
            if configvalue.name == name and value in configvalue.values:
                res = True
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_cvalue_for_this_optionname(self, optionname):
        """
                ConfigValuesForOneLanguage.get_cvalue_for_this_optionname

                optionname :    (str)
        """
        found = False
        res = None

        for configvalue in self:
            if configvalue.optionname == optionname:
                found = True
                res = configvalue

        if not found:
            msg = "unknown optionname = {0}; known optionnames = {1}.".format( optionname,
                                                                   [cv.optionname for cv in self] )
            raise DCharsError( context = \
                                  "ConfigValuesForOneLanguage.get_cvalue_for_this_optionname",
                               message = msg )
        return res

    #///////////////////////////////////////////////////////////////////////////
    def get_optionname(self, name):
        """
                ConfigValuesForOneLanguage.get_optionname

                name    :       (str)
        """
        found = False
        res = None

        for configvalue in self:
            if configvalue.name == name:
                found = True
                res = configvalue.optionname

        if not found:
            msg = "unknown name = {0}; known names = {1}.".format( name,
                                                                   [cv.name for cv in self] )
            raise DCharsError( context = "ConfigValuesForOneLanguage.get_optionname",
                               message = msg )
        return res

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ænglisc (Old English)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ANG_DATA = ConfigValuesForOneLanguage(header = 'Ænglisc (Old English)')
ANG_DATA.append( ConfigValue( subsection = '',
                              values = ("basic",),
                              name = 'transliteration method',
                              defaultvalue = 'basic',
                              optionname = "transliteration method" ))

ANG_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

ANG_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# བོད་ཡིག (Tibetan)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BOD_DATA = ConfigValuesForOneLanguage(header = "བོད་ཡིག (Tibetan)")
BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("ewts", "bodsan"),
                              name = 'transliteration method',
                              defaultvalue = 'ewts',
                              optionname = "transliteration method" ))

BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("always Tibetan",
                                        "Tibetan or Sanskrit",
                                        "always Sanskrit"),
                              name = 'expected structure',
                              defaultvalue = 'Tibetan or Sanskrit',
                              optionname = "expected structure" ))

BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'look up in the buffers',
                              defaultvalue = 'yes',
                              optionname = "look up in the buffers" ))

BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'fill the buffers',
                              defaultvalue = 'no',
                              optionname = "fill the buffers" ))

BOD_DATA.append( ConfigValue( subsection = '',
                              values = ("basic",),
                              name = 'sorting method',
                              defaultvalue = 'basic',
                              optionname = "sorting method" ))

BOD_DATA.append( ConfigValue( subsection = 'bod.bodsan',
                              values = ("high", "normal", "low"),
                              name = 'san2bod quality',
                              defaultvalue = 'high',
                              optionname = "bodsan.san2bod quality" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# romanz (Old English)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FRO_DATA = ConfigValuesForOneLanguage(header = 'Ænglisc (Old English)')
FRO_DATA.append( ConfigValue( subsection = '',
                              values = ("basic",),
                              name = 'transliteration method',
                              defaultvalue = 'basic',
                              optionname = "transliteration method" ))

FRO_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

FRO_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Ἑλληνικὴ γλῶττα (Ancient Greek)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GRC_DATA = ConfigValuesForOneLanguage(header = "Ἑλληνικὴ γλῶττα (Ancient Greek)")
GRC_DATA.append( ConfigValue( subsection = '',
                              values = ("basic", "betacode", "perseus", "gutenberg"),
                              name = 'transliteration method',
                              defaultvalue = 'basic',
                              optionname = "transliteration method" ))

GRC_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

GRC_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'ignore smooth breathing',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:ignore smooth breathing" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'ignore accents',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:ignore accents" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'ignore iota subscript',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:ignore iota subscript" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'ignore diaeresis',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:ignore diaeresis" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'hh becomes h',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:hh becomes h" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("u", "y", "u or y"),
                              name = 'transliteration for upsilon',
                              defaultvalue = 'u or y',
                              optionname = "gutenberg:transliteration for upsilon" ))

GRC_DATA.append( ConfigValue( subsection = 'grc.gutenberg',
                              values = ("yes", "no"),
                              name = 'ignore makron and brakhu',
                              defaultvalue = 'yes',
                              optionname = "gutenberg:ignore makron and brakhu" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  "עִבְֿרִיתֿ מִקְרָאִיתֿ"  (Biblical Hebrew)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HBO_DATA = ConfigValuesForOneLanguage(header = '"עִבְֿרִיתֿ מִקְרָאִיתֿ" (Biblical Hebrew)')
HBO_DATA.append( ConfigValue( subsection = '',
                              values = ("basic",),
                              name = 'transliteration method',
                              defaultvalue = 'basic',
                              optionname = "transliteration method" ))

HBO_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

HBO_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 日本語 (Japanese)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JPN_DATA = ConfigValuesForOneLanguage(header = '日本語 (Japanese)')
JPN_DATA.append( ConfigValue( subsection = '',
                              values = ("shepburn",),
                              name = 'transliteration method',
                              defaultvalue = 'shepburn',
                              optionname = "transliteration method" ))

JPN_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

JPN_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

JPN_DATA.append( ConfigValue( subsection = 'jpn.shepburn',
                              values = ("yes", "no"),
                              name = 'long vowels written with circumflex',
                              defaultvalue = 'no',
                              optionname = "long vowels written with circumflex" ))

JPN_DATA.append( ConfigValue( subsection = 'jpn.shepburn',
                              values = ("yes", "no"),
                              name = 'katakanas written with upper case letters',
                              defaultvalue = 'no',
                              optionname = "katakanas written with upper case letters" ))

JPN_DATA.append( ConfigValue( subsection = 'jpn.shepburn',
                              values = ("yes", "no"),
                              name = "ou becomes ō",
                              defaultvalue = 'no',
                              optionname = "ou becomes ō" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# latīna (Latin)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LAT_DATA = ConfigValuesForOneLanguage(header = 'latīna (Latin)')
LAT_DATA.append( ConfigValue( subsection = '',
                              values = ("basic",),
                              name = 'transliteration method',
                              defaultvalue = 'basic',
                              optionname = "transliteration method" ))

LAT_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

LAT_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# संस्कृतम् (Sanskrit)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SAN_DATA = ConfigValuesForOneLanguage(header = 'संस्कृतम् (Sanskrit)')
SAN_DATA.append( ConfigValue( subsection = '',
                              values = ("iso15919", "itrans"),
                              name = 'transliteration method',
                              defaultvalue = 'iso15919',
                              optionname = "transliteration method" ))

SAN_DATA.append( ConfigValue( subsection = '',
                              values = ("yes", "no"),
                              name = 'anonymize the unknown characters',
                              defaultvalue = 'no',
                              optionname = "anonymize the unknown characters" ))

SAN_DATA.append( ConfigValue( subsection = '',
                              values = ("default",),
                              name = 'sorting method',
                              defaultvalue = 'default',
                              optionname = "sorting method" ))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA : a dict of language name (ISO 639-3) : <ConfigValuesForOneLanguage> object
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DATA = {
        "ang"   : ANG_DATA,
        "bod"   : BOD_DATA,
        "fro"   : FRO_DATA,
        "grc"   : GRC_DATA,
        "hbo"   : HBO_DATA,
        "jpn"   : JPN_DATA,
        "lat"   : LAT_DATA,
        "san"   : SAN_DATA,
       }
