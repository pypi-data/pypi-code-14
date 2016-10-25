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
    ❏DChars❏ : dchars/config_ini.py

    functions check() and write_config_ini()
"""

import os.path
import datetime
from dchars.config_ini_data import DATA as CONFIG_INI_DATA
from dchars.errors.errors import DCharsError

#///////////////////////////////////////////////////////////////////////////////
def check(src):
    """
        check() :

        Check if the values given to the options are consistent with DATA.

        src     :       something like src = configparser.ConfigParser()
    """
    for section in src.sections():

        dot = section.find(".")
        if dot == -1:
            # no dot :
            language = section
        else:
            # at least one dot in language name :
            language = section[:dot]

        for name, value in list(src[section].items()):

            if not CONFIG_INI_DATA[language].known_name( name ):
                msg = "unknown name : '{0}'; check config_ini_data.py".format(name)
                raise DCharsError( context = "config_ini.py::check",
                                   message = msg)

            if not CONFIG_INI_DATA[language].name_have_a_known_value( name, value ):
                msg = "unknown value '{0}' for name {1}; check config_ini_data.py. ".format(value,
                                                                                            name)
                raise DCharsError( context = "config_ini.py::check",
                                   message = msg)

#///////////////////////////////////////////////////////////////////////////////
def write_config_ini():
    """
        write_config_ini function : write CONFIG_INI_DATA content to a
        config file.

        Overwrite the config.ini file with an header and the expected comments.
        The usual way to write a config.ini file would not allow to write the
        header and the comments, so we use a less sophisticated approach.
    """

    with open( os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "config.ini" ),
               "w") as config_file:

        #-----------------------------------------------------------------------
        # header :
        #-----------------------------------------------------------------------
        config_file.write( "#"*80 + "\n" )
        config_file.write( "#" + "\n" )
        config_file.write( "# " + "DChars : default values used by DString* objects" + "\n" )
        config_file.write( "#" + "\n" )
        config_file.write( "# " + "file automatically created by the function" + "\n" )
        config_file.write( "# " + "config_ini.py::write_config_ini() ." + "\n" )
        config_file.write( "# " + "Creation time : "+str(datetime.datetime.now())[:19] + "\n" )
        config_file.write( "# " + "\n" )
        config_file.write( "# You can modify this file by changing the values affected to\n" +\
                           "# the options; but if you want to change the name or the\n" + \
                           "# number of the options you have to modify dchars.py and/or\n" + \
                           "# config_ini_data.py and/or config_ini.py." + "\n" )
        config_file.write( "#" + "\n" )
        config_file.write( "# " + "Beware : sections' name follows the norm ISO 639-3 : grc,\n" )
        config_file.write( "# " + "         lat, hbo, ...\n" )
        config_file.write( "# " + "Beware : sections' name can use subdivision(s) thanks to a\n" )
        config_file.write( "# " + "         dot like [grc.gutenberg] but the first letters must\n" )
        config_file.write( "# " + "         be the ISO 639-3 name of the language.\n")
        config_file.write( "#" + "\n" )
        config_file.write( "#"*80 + "\n" )
        config_file.write( "\n" )

        #-----------------------------------------------------------------------
        # sections, language by language
        #-----------------------------------------------------------------------
        for language_name in CONFIG_INI_DATA:

            config_file.write( "# " + "-"*78 + "\n" )
            config_file.write( "# " + CONFIG_INI_DATA[language_name].header + "\n" )
            config_file.write( "# " + "-"*78 + "\n" )

            config_file.write( "[" + language_name + "]" + "\n" )

            current_subsection = ""     # e.g. "grc.gutenberg"
            for data in CONFIG_INI_DATA[language_name]:

                if current_subsection != data.subsection:

                    if data.subsection != "":
                        config_file.write( "[" + data.subsection + "]" + "\n" )
                    current_subsection = data.subsection

                _values = ('\"{0}\"'.format(string) for string in data.values)
                config_file.write( "# accepted values : " + " or ".join(_values) + "\n" )
                full_optionname = "LANGUAGES['{0}']['{1}']".format( language_name,
                                                                    data.optionname )
                config_file.write( "# stored in <LANGUAGES> as " + full_optionname + "\n" )
                config_file.write( data.name + " = " + data.defaultvalue + "\n" )

                config_file.write( "\n" )
