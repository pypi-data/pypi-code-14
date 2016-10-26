#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Grammaticomastix Copyright (C) 2016 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Grammaticomastix.
#    Grammaticomastix is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Grammaticomastix is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Grammaticomastix.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏Grammaticomastix❏ : grammaticomastix.py

    See the main page at https://github.com/suizokukan/grammaticomastix .
    ____________________________________________________________________________

    coding standards:
    ˮ ▶ class docstring : normal classes
    ˮ
    ˮ For each class, give the following informations :
    ˮ class attribute(s), instance attribute(s), method(s)
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ ▶ class docstring : namedtuple classes
    ˮ
    ˮ For each class, give only the instance attribute(s).
    ˮ Sort the elements of these three lists alphabetically.
    ˮ Specify if an element is inherited or added to the mother
    ˮ class, using the special characters ●, ◐ and ○ :
    ˮ         ● method/attribute added in comparison from parent classes (=1st definition)
    ˮ         ◐ method/attribute inherited and redifined
    ˮ         ○ method/attribute inherited and not modified
    ˮ
    ˮ For each function or method give the list of the arguments, each
    ˮ one beginning with the ▪ symbol :
    ˮ         ARGUMENTS:
    ˮ         ▪ prefix    : (str)
    ˮ         ▪ src       : (str)
    ˮ
    ˮ         RETURNED VALUE : the expected string
    ˮ
    ˮ
    ˮ ▶ __init__()
    ˮ
    ˮ The arguments of an __init__() method have to be written one
    ˮ argument by line. If a __init__() method is called inside
    ˮ a __init__() method, the arguments have also to be be written
    ˮ one argument by line.
"""

PROJECT_NAME = "Grammaticomastix"
VERSION = "0.0.1c4"

#===============================================================================
# project's settings
#
# o for __version__ format string, see https://www.python.org/dev/peps/pep-0440/ :
#   e.g. "0.1.2.dev1" or "0.1a"
#
# o See also https://pypi.python.org/pypi?%3Aaction=list_classifiers
#
#===============================================================================
__projectname__ = PROJECT_NAME
__version__ = VERSION
__laststableversion__ = VERSION
__author__ = "Xavier Faure (suizokukan / 94.23.197.37)"
__copyright__ = "Copyright 2015, suizokukan"
__license__ = "GPL-3.0"
__licensepypi__ = 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
__maintainer__ = "Xavier Faure (suizokukan)"
__email__ = "suizokukan@orange.fr"
__status__ = "Alpha"
__statuspypi__ = 'Development Status :: 2 - Pre-Alpha'

import argparse
import configparser
import sys
import grammaticomastix.globalvars as globalvars
import grammaticomastix.logger as logger

import grammaticomastix.cfgfile as cfgfile
from grammaticomastix.interface.linuxcli.interface import main_linuxcli
from grammaticomastix.interface.qt5.interface import main_qt5

# %%
# comment choisir l'interface ?
# --interface > config file
# si lancement avec ./grammaticomastix-qt5, l'interface sera forcément Qt

def entrypoint():
    # cas de figure le plus général : on ne sait pas encore quelle interface utiliser.

    LOGGER = logger.get_logger(__name__)

    LOGGER.info("{0} v. {1}".format(PROJECT_NAME, VERSION))

    globalvars.CMDLINEPARSER=CommandLineParser()
    globalvars.CMDLINEPARSER=globalvars.CMDLINEPARSER.parse_args()

    configfile_ok = cfgfile.read()

    if globalvars.CMDLINEPARSER.interface=="qt5":
        main_qt5()
    elif globalvars.CMDLINEPARSER.interface=="linuxcli":
        main_linuxcli()        
    elif configfile_ok and globalvars.CFGFILEPARSER["interface"]["interface"]=="qt5":
        main_qt5()
    elif configfile_ok and globalvars.CFGFILEPARSER["interface"]["interface"]=="linuxcli":
        main_linuxcli()
    else:
        main_linuxcli()

def entrypoint_qt5():
    globalvars.LOGGER = logger.get_logger(__name__)  # you may add e.g. level=logger.INFO .
    globalvars.LOGGER.info("{0} v. {1} : qt5 interface".format(PROJECT_NAME, VERSION))
    main_qt5()

################################################################################
class CommandLineParser(argparse.ArgumentParser):
    """
        CommandLineParser class
    """
    description = "CLI for {0}.".format(PROJECT_NAME)

    epilog = "{0}'s author : " \
             "suizokukan (suizokukan _A.T_ orange DOT fr)".format(PROJECT_NAME)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
                CommandLineParser.__init__

                Initialize the object by adding all the arguments.
        """

        argparse.ArgumentParser.__init__(self,
                                         description=CommandLineParser.description,
                                         epilog=CommandLineParser.epilog,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        self.add_argument('sourcestring',
                          nargs="?",
                          type=str,
                          help="source string to be analyzed",
                          default="")

        self.add_argument('--interface',
                          choices=("qt5", "linuxcli",),                          
                          type=str,
                          required=False,
                          help="linuxcli")

        self.add_argument('--version',
                          action='version',
                          version="{0} v. {1}".format(__projectname__, __version__),
                          help="# Show the version and exit")

#///////////////////////////////////////////////////////////////////////////////
#/////////////////////////////// STARTING POINT ////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    # by default, let's call the "normal" main function, not the mainqt() one :
    entrypoint()
