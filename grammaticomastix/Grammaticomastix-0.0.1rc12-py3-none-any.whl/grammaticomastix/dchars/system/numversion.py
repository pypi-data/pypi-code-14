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
        ❏DChars❏ : dchars/system/numversion.py

        version of the program

        * class VersionOfTheProgram
"""

import os
from dchars.errors.errors import DCharsError

################################################################################
class VersionOfTheProgram(object):
    """
        class VersionOfTheProgram

                Keeps the current number of version in a file.
    """

    NUMVERSION_FILE = "numversion"

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __init__(self):
        """
                VersionOfTheProgram.__init__

                Ouvre le fichier dans lequel se trouve le numéro de version
                et initialise l'objet.
        """

        # version number + release number :
        self.numversion = ""

        #   We define the path where lies the file from this source code file; this
        # method allows to launch the code from another path that the usual
        # 'root path'.
        raw_name = os.path.join(os.path.abspath( os.path.dirname( __file__)),
                                self.NUMVERSION_FILE)
        full_name_of_the_file = os.path.abspath(raw_name)


        # We ensure that the appropriate file exists :
        if not os.path.exists(full_name_of_the_file):
            # the file doesn't exist :
            msg = "The file where the number of version is kept doesn't exist; " + \
                  "name of the file : " + full_name_of_the_file
            raise DCharsError(context = "VersionOfTheProgram.__init__",
                              message = msg)

        else:
            # the file exists : we read the number of the version :
            with open(full_name_of_the_file,"r") as numversionfile:

                self.numversion = numversionfile.read()
                # deleting of the final \n :
                self.numversion = self.numversion.strip()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __repr__(self):
        """
                VersionOfTheProgram.__repr__
        """
        return str(self.numversion)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def __str__(self):
        """
                VersionOfTheProgram.__str__
        """
        return str(self.numversion)

	#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def only_the_release_number(self):
        """
				VersionOfTheProgram.only_the_release_number
		"""
        return str(self.numversion[-1])

	#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def only_the_version_number(self):
        """
				VersionOfTheProgram.only_the_version_number
		"""
        return str(self.numversion[:-1])

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def short_description(self):
        """
                VersionOfTheProgram.short_description

                This function returns a compact description of the number of the
                version.
        """

        res = str(self.numversion)
        res = res.replace(".","")
        return res
