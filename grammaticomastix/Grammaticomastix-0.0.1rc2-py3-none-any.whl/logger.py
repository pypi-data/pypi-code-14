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
    ❏Grammaticomastix❏ : logger.py

    logging's facility : this is just an example of how to write the
                         getLogger() function required by Grammaticomastix.

    See the main page at https://github.com/suizokukan/gmastix .
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

import collections
import logging

# counter of messages sent to the logger :
#       (str)key → (int)
#  e.g. "ERRROR" → 3
MSG_COUNT = collections.defaultdict(int)

# Thanks to these constants it's possible to write the following lines :
#       import logger
#       LOGGER = logger.get_logger(__name__, level=logger.DEBUG)
#
# ... instead of these ones :
#       import logger
#       import logging
#       LOGGER = logger.get_logger(__name__, level=logging.DEBUG)
#
DEBUG = logging.DEBUG
WARNING = logging.WARNING
INFO = logging.INFO
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

################################################################################
class MessageCounterHandler(logging.Handler):
    """
        MessageCounterHandler class
        ________________________________________________________________________

        Handler used to count the number of times a certain kind of level
        messages has been emitted.
        ____________________________________________________________________

        no class attribute

        instance attribute:
        ○ msg_count     : collections.dict(int) : str → int
                          a counter of messages' levels :
                                e.g. {"ERROR" : 3, "CRITICAL" : 0}

        methods :
        ◐ __init__(self, level)
        ○ emit(self, record)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, level):
        """
            MessageCounterHandler.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ level : (int) e.g. logging.DEBUG

            no RETURNED VALUE
        """
        super(MessageCounterHandler, self).__init__(level=level)

    #///////////////////////////////////////////////////////////////////////////
    def emit(self, record):
        """
            MessageCounterHandler.emit()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENT:
            ▪ record    : (str) the string to be emitted

            no RETURNED VALUE
        """
        MSG_COUNT[record.levelname] += 1

# the file to be used for the logging :
LOGGER_FILELOG = logging.FileHandler(filename="grammaticomastix.lastlog", mode="w")
# the basic class used for the logging :
DEFAULTLOGGER = logging.getLoggerClass() # a logging.Logger object

################################################################################
class GMastixLogger(DEFAULTLOGGER):
    """
        GMastixLogger class
        ________________________________________________________________________

        Class returned by get_logger : GMastixLogger is derived from
                                       logging.Logger
        ____________________________________________________________________

        no class attribute

        no instance attribute:

        methods :
        ◐ __init__(self, name, level)
        ● report(self)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, name, level):
        """
            GMastixLogger.__init__()
            ____________________________________________________________________
            ____________________________________________________________________

            ARGUMENTS:
            ▪ name      : (str) logger's name
            ▪ level     : (int) e.g. logging.DEBUG

            no RETURNED VALUE
        """
        DEFAULTLOGGER.__init__(self, name=name, level=level)

        self.setLevel(level)

        # this handler has to be to be handler #0 (see the .report() method),
        # so we have to define it first :
        self.addHandler(MessageCounterHandler(level))

        LOGGER_FILELOG.setLevel(level)
        LOGGER_FILELOG.setFormatter(logging.Formatter("%(name)s::%(levelname)s : %(message)s"))
        self.addHandler(LOGGER_FILELOG)

        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter("%(name)s::%(levelname)s : %(message)s"))
        console.setLevel(logging.ERROR)
        self.addHandler(console)

    #///////////////////////////////////////////////////////////////////////////
    @staticmethod
    def report():
        """
            GMastixLogger.report()
            ____________________________________________________________________

            Return a string about the number of warnings, errors and critical
            messages.
            ____________________________________________________________________

            no ARGUMENTS

            RETURNED VALUE: the expected (str)string.
        """
        res = []

        if "WARNING" in MSG_COUNT:
            res.append("▪ warning message(s) : {0}".format(MSG_COUNT["WARNING"]))
        if "ERROR" in MSG_COUNT:
            res.append("▪ error message(s) : {0}".format(MSG_COUNT["ERROR"]))
        if "CRITICAL" in MSG_COUNT:
            res.append("▪ critical message(s) : {0}".format(MSG_COUNT["ERROR"]))

        if len(res) > 0:
            res = ["Logging report :"] + res
            return "\n".join(res)
        else:
            return "(logging report : no warning, no error, nothing critical)"

#///////////////////////////////////////////////////////////////////////////////
def get_logger(name, level=logging.INFO):
    """
        get_logger()
        _______________________________________________________________________

        Function to be called at the beginning of a script to define a logger
        with a specifical name.

        This function should be called with __name__ as an argument :
                e.g. : logger = logger.get_logger(__name__, logger.DEBUG)
        ________________________________________________________________________

        ARGUMENTS:
        ▪ name         : (str) name of the logging object.
        ▪ level        : (int) e.g. logging.DEBUG

        RETURNED VALUE : a logging.Logger object (here a GMastixLogger object)
    """
    return GMastixLogger(name=name, level=level)
