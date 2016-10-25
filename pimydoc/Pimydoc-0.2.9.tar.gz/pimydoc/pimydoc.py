#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Pimydoc Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Pimydoc.
#    Pimydoc is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Pimydoc is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Pimydoc.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Pimydoc by suizokukan (suizokukan @t orange d@t fr)

    Pimydoc : [P]lease [i]nsert my doc[umentation]

    A Python3/GPLv3/OSX-Linux-Windows/CLI project, using no additional modules
    than the ones installed with Python3.
    ____________________________________________________________________________

    Pimydoc inserts in source files the text paragraphs stored in "pimydoc", the
    documentation source file. Moreover, the script updates the text paragraphs
    already present in the source files if the documentation source file has
    changed.
    ____________________________________________________________________________

    usage : $ pimydoc.py      : modify the current directory with a "pimydoc"
                                file in the current directory.

    try pimydoc --help for more options and see README.md for more documentation.
"""

import argparse
import logging
import os
import platform
import re
import shutil
import sys
import urllib.request

# location of the default documentation source file :
DEFAULTCFGFILE_URL = "https://raw.githubusercontent.com/suizokukan/pimydoc/" \
                     "master/pimydoc/pimydoc"

#///////////////////////////////////////////////////////////////////////////////
def remove_and_return_linefeed(src):
    """
        remove_and_return_linefeed()
        ________________________________________________________________________

        Remove the linefeed characters from the end of (str)src.
        This function recognizes three kinds of linefeed characters :
        ▪ the Linux one (\n)
        ▪ the Windows one (\r\n)
        ▪ the ancient OSX one (\r)
        ________________________________________________________________________

        PARAMETER : (str)src, the source string to be cut

        RETURNED VALUE : ((str)the reduced source string,
                          (str)the linefeed characters)
    """
    if src.endswith("\r\n"):
        return src[:-2], "\r\n"
    elif src.endswith("\n"):
        return src[:-1], "\n"
    elif src.endswith("\r"):
        return src[:-1], "\r"
    else:
        return src, ""

#///////////////////////////////////////////////////////////////////////////////
def normpath(_path):
    """
        normpath()
        ________________________________________________________________________

        Return a human-readable (e.g. "~" -> "/home/myhome/" on Linux systems),
        normalized version of a path.
        ________________________________________________________________________

        PARAMETER : (str)_path

        RETURNED VALUE : the expected string
    """
    res = os.path.normpath(os.path.abspath(os.path.expanduser(_path)))

    if res == ".":
        res = os.getcwd()

    return res

#===============================================================================
# project's settings
#
# ▪ for __version__ format string, see https://www.python.org/dev/peps/pep-0440/ :
#   e.g. "0.1.2.dev1" or "0.1a"
#
# ▪ See also https://pypi.python.org/pypi?%3Aaction=list_classifiers
#
#===============================================================================
PROJECT_NAME = "Pimydoc"

# see https://www.python.org/dev/peps/pep-0440/
# e.g. 0.1.2.dev1, 0.0.6a0
PROJECT_VERSION = "0.2.9"

# constants required by Pypi.
__projectname__ = PROJECT_NAME
__author__ = "Xavier Faure (suizokukan)"
__copyright__ = "Copyright 2016, suizokukan"
__license__ = "GPL-3.0"
__licensepypi__ = 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
__version__ = PROJECT_VERSION
__maintainer__ = "Xavier Faure (suizokukan)"
__email__ = "suizokukan@orange.fr"
__status__ = "Beta"
__statuspypi__ = 'Development Status :: 4 - Beta'

################################################################################
class Settings(dict):
    """
        Settings class

        The settings are stored in the documentation source file.
        ________________________________________________________________________

        Use this class to store the settings used by the pimydoc_a_file()
        function.
        The settings are stored as in a dictionary : (str)key->(str)value

        ▪ REGEX_SOURCE_FILTER : regex describing the name of the files to be
                                modified.

        ▪ REGEX_FIND_DOCTITLE : regex describing the name (in the documentation
                                source file) of the titles.
                                See below for more details (docsrc format)

        ▪ STARTSYMB_IN_DOC    : string at the beginning of each line of
                                documentation added in the source files.
                                See below for more details (docsrc format)

        ▪ PROFILE_PYTHON_SPACENBR_FOR_A_TAB : (int) for Python files, number of
                                              spaces replacing a tab character.

        ▪ REMOVE_FINAL_SPACES_IN_NEW_DOCLINES : (str) "True" or "False"

        ▪ COMMENT_STARTSTRING : (str) e.g. "###"

        about the docsrc (documentation source file) format : see README.md
        ________________________________________________________________________

        class attributes : -

        instance attribute(s) : -

        class methods :
            ▪ __init__(self)
            ▪ init_from_line(self, line)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
            Settings.__init__()
            ________________________________________________________________________

            Initialize all the settings to a default value.
            ________________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        dict.__init__(self)

        # this is a direct initialization : see the .init_from_line() method to
        # see how self can be initialized from a file.
        self["REGEX_SOURCE_FILTER"] = ""
        self["REGEX_FIND_DOCTITLE"] = "^\\[(?P<doctitle>.+)\\]$"
        self["STARTSYMB_IN_DOC"] = "| " + "|" + " " # a fancy way to write STARTSYMB_IN_DOC but it
                                                    # avoids, if Pimydoc is applied to this file,
                                                    # to remove this line since this line contains
                                                    # the STARTSYMB_IN_DOC symbols defined in the
                                                    # documentation source file.
        self["PROFILE_PYTHON_SPACENBR_FOR_A_TAB"] = 4
        self["REMOVE_FINAL_SPACES_IN_NEW_DOCLINES"] = "True"
        self["COMMENT_STARTSTRING"] = "###"

    #///////////////////////////////////////////////////////////////////////////
    def init_from_line(self, line):
        """
            Settings.init_from_line()
            ____________________________________________________________________

            Analyse the (str)<line> and set a pair (key, value) in self.
            ____________________________________________________________________

            ARGUMENT : (str)line, the line to be analysed

            RETURNED VALUE : 0 if success, -1 if an important problem occured
        """
        returned_value = 0

        key, value = line.split(":")
        key = key.strip()

        value, _ = remove_and_return_linefeed(value)
        logging.debug("read a new setting : key='%s', value='%s'", key, value)

        if key not in self:
            logging.error("! unknown key '%s'.", key)
            returned_value = -1
        else:
            try:
                if key == "REGEX_FIND_DOCTITLE":
                    self[key] = re.compile(value.lstrip())
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "REGEX_SOURCE_FILTER":
                    self[key] = re.compile(value.lstrip())
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "STARTSYMB_IN_DOC":
                    self[key] = value
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "PROFILE_PYTHON_SPACENBR_FOR_A_TAB":
                    self[key] = int(value)
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "REMOVE_FINAL_SPACES_IN_NEW_DOCLINES":
                    self[key] = value.strip()
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                elif key == "COMMENT_STARTSTRING":
                    self[key] = value.strip()
                    logging.debug("key '%s' set to '%s' (%s).", key, self[key], type(self[key]))

                else:
                    logging.error("! unknown setting key : '%s' (set to '%s')", key, self[key])

            except re.error as error:
                logging.error("! A regex error occured by reading the following line :")
                logging.error(line)
                logging.error("! The key to be read was '%s'", key)
                logging.error("! Error message returned by the script : '%s'", error)
                returned_value = -1

        return returned_value

SETTINGS = Settings()

################################################################################
class CommandLineParser(argparse.ArgumentParser):
    """
        CommandLineParser class
        ________________________________________________________________________

        Use this class to parse the command line arguments.

        Unique instance : args (see at the end of the file)
        ________________________________________________________________________

        class attributes :

            ▪ (str)description
            ▪ (str)epilog

        instance attribute(s) : -

        class methods :

            ▪ __init__()
            ▪ get_args()
    """
    description = "{0} project, v.{1}".format(PROJECT_NAME,
                                              PROJECT_VERSION)

    epilog = "{0}'s author : " \
             "suizokukan (suizokukan _A.T_ orange DOT fr)".format(PROJECT_NAME)

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self):
        """
                CommandLineParser.__init__()
                ________________________________________________________________

                Initialize the object by adding all the arguments.
                ________________________________________________________________

                no PARAMETER, no RETURNED VALUE
        """
        argparse.ArgumentParser.__init__(self,
                                         description=CommandLineParser.description,
                                         epilog=CommandLineParser.epilog,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        self.add_argument('--sourcepath',
                          type=str,
                          default=normpath(os.getcwd()),
                          help="source path of the code")

        self.add_argument("--docsrcfile",
                          type=str,
                          default=normpath(os.path.join(os.getcwd(), "pimydoc")),
                          help="source documentation file name")

        self.add_argument('--verbose',
                          type=int,
                          choices=(0, 1, 2),
                          default=1,
                          help="degree of verbosity of the output. " \
                               "0 : only the error messages; " \
                               "1 : all messages except debug messages; " \
                               "2 : all messages, including debug messages; " \
                               "See also the -vv and -vvv options.")

        self.add_argument('-vv',
                          action='store_true',
                          help="verbosity set to 1 (all messages except debug messages).")

        self.add_argument('-vvv',
                          action='store_true',
                          help="verbosity set to 2 (all messages, including debug messages).")

        self.add_argument('--version', '-v',
                          action='version',
                          version="{0} v. {1}".format(__projectname__, __version__),
                          help="show the version and exit")

        self.add_argument('--remove', '-r',
                          action='store_true',
                          help="Remove every pimydoc line in all the files of the source directory")

        self.add_argument('--securitymode', '-s',
                          action='store_true',
                          help="Security mode : backup files created by Pimdoc are not deleted")

        self.add_argument('--downloadpimydoc',
                          action='store_true',
                          help="download a default pimydoc file in the current directory and exit")

    #///////////////////////////////////////////////////////////////////////////
    def get_args(self):
        """
                CommandLineParser.get_args()
                ________________________________________________________________

                Parse the command line arguments and return the argparse.Namespace
                object.
                ________________________________________________________________

                no PARAMETER

                RETURNED VALUE    : the argparse.Namespace object
        """
        return self.parse_args()

#///////////////////////////////////////////////////////////////////////////////
def download_default_pimydoc():
    """
        download_default_pimydoc()
        ________________________________________________________________________

        Try to generate a default pimydoc file in the current directory.
        ________________________________________________________________________

        no PARAMETER, no RETURNED VALUE
    """
    if os.path.exists("pimydoc"):
        logging.error("Can't generate a default documentation source file : "
                      "the file 'pimydoc' already exists.")
        return

    try:
        with urllib.request.urlopen(DEFAULTCFGFILE_URL) as response, \
             open("pimydoc", 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        logging.info("Successfully downloaded the 'pimydoc' file.")

    except urllib.error.URLError as exception:
        logging.error("An error occured : can't download the file.")
        logging.error("Error returned by Python : "+str(exception))

################################################################################
class DocumentationSource(dict):
    """
        DocumentationSource class

        The settings, the doctitles and the documentation are stored in the
        documentation source file.
        ________________________________________________________________________

        Use this class to read the documentation source file.

        dict: (str)doc title -> a list of (str) lines.
        ________________________________________________________________________

        class attributes : -

        instance attribute(s) : -
            ▪ self.errors : a list of strings, filled by the newline() method.

        class methods :
            ▪ __init__(self, filename)
            ▪ newline(self, line, linenumber, location, current_title)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, filename):
        """
            DocumentationSource.__init__()
            ____________________________________________________________________

            Initialize self and SETTINGS from the content of filename.
            ____________________________________________________________________

            ARGUMENT : (str)filename, the name of the file to be read.

            no RETURNED VALUE
        """
        # ---------------------------------------------
        # entry point of DocumentationSource.__init__()
        logging.debug("DocumentationSource.__init__() : %s", filename)

        # a list of (str)
        self.errors = []

        if not os.path.exists(filename):
            logging.error("! Missing documentation source file '%s'", filename)
            self.errors.append("Can't open '{0}'".format(filename))
            return

        if os.path.isdir(filename):
            logging.error("! '%s' is not a file but a directory.", filename)
            self.errors.append("Can't open '{0}'".format(filename))
            return

        # title(str) : a list of str
        dict.__init__(self)

        # None or the current (str)doc title
        current_title = None

        # None is mandatory if a blank line appears before the first title
        location = None # None / settings / doc

        with open(filename, encoding="utf-8") as src:
            stop = False
            for linenumber, line in enumerate(src.readlines()):

                if line.startswith(SETTINGS["COMMENT_STARTSTRING"]):
                    logging.debug("Skipped commentary line '%s'", line.strip())
                elif line.strip() == "[pimydoc]":
                    location = "settings"
                    logging.debug("settings detected by reading the '%s' line (#%s).",
                                  line.strip(), linenumber)
                else:
                    location, current_title, stop = self.newline(line, linenumber,
                                                                 location, current_title)

                if stop:
                    break

    #///////////////////////////////////////////////////////////////////////////
    def newline(self, line, linenumber, location, current_title):
        """
            DocumentationSource.newline() :  somehow a subfunction of
                                             DocumentationSource.__init__()
            ________________________________________________________________

            Add the line to the settings or the current doc title.
            ________________________________________________________________

            ARGUMENTS :
            ▪ line          : (str) line to be added
            ▪ linenumber    : (int) line number in the source file
            ▪ location      : (str) see __init__() : None, "doc", ...
            ▪ current_title : (str) the current doc title.

            RETURNED VALUE : ((str)location, (str)current_title, (bool)stop)
        """
        stop = False

        find_title = re.search(SETTINGS["REGEX_FIND_DOCTITLE"], line)

        if find_title is not None:
            location = "doc"
            logging.debug("beginning of the doc at line '%s' (#%s)",
                          line.strip(), linenumber)

        if location == "settings":
            separator = line.find(":")

            if separator >= 0:
                if SETTINGS.init_from_line(line) != 0:
                    logging.error("! An error occured : " \
                                  "stop reading the documentation source file.")
                    self.errors.append("Can't read the " \
                                       "line '{0}' (line #{1})".format(line, linenumber))
                    stop = True
            elif len(line.strip()) > 0:
                logging.error("! (reading the documentation source file) " \
                              " Can't read the following line : '%s' (#%s)",
                              line, linenumber)

        elif location == "doc":

            if find_title is None:
                self[current_title].append(line)
            else:
                try:
                    new_title = find_title.group("doctitle")
                except IndexError as error:
                    logging.error("! An error occured : " \
                                  "stop reading the documentation source file.")
                    self.errors.append("Can't read the line '{0}' (line #{1}) : " \
                                       "ill-formed doctitle".format(line, linenumber))
                    self.errors.append("Error returned by Python :"+str(error))
                    stop = True

                if stop is False and new_title in self:
                    logging.error("! doctitle '%s' already defined !", new_title)
                    self.errors.append("Doctitle '{0}' already present " \
                                       "in the documentation source file." \
                                       "See line '{1}' (line #{2})".format(new_title,
                                                                           line, linenumber))

                if stop is False:
                    self[new_title] = []
                    current_title = new_title

                    logging.debug("found a new title : '%s' (#%s)", new_title, linenumber)

        return location, current_title, stop

#///////////////////////////////////////////////////////////////////////////////
def pimydoc_a_file(targetfile_name,
                   docsrc,
                   just_remove_pimydoc_lines,
                   securitymode,
                   read_doctitles):
    """
        pimydoc_a_file()
        ________________________________________________________________________

        Update the documentation in a file.

        Read a target file, removed the old documentation and replace it by the
        new one described in <docsrc>.

        Update read_doctitles
        ________________________________________________________________________

        ARGUMENTS :
        ▪ targetfile_name           : (str) name of the file to be modified
        ▪ docsrc                    : (DocumentationSource) doc content
        ▪ just_remove_pimydoc_lines : (bool) if True, nothing is added but the
                                      pimydoc lines of documentation are removed.
        ▪ securitymode              : (bool) True if the backup files created
                                      by this function have to be kept.
        ▪ read_doctitles            : a dict (str)doctitle->(bool)has the doctitle
                                      been read until now ?

        RETURNED VALUE : read_doctitles
    """

    #...........................................................................
    def rewrite_new_targetfile__line(newtargetfile, new_docline, last_linefeed):
        """
            rewrite_new_targetfile__line()

            this function is a subsubfunction of the pimydoc_a_file() function and
            a subfunction of the rewrite_new_targetfile() function.
            ________________________________________________________________________

            Write a line in the target file. This required a whole function because
            of the problem of the various linefeed characters.
            ________________________________________________________________________

            ARGUMENTS :
            ▪ newtargetfile             : a file descriptor.
            ▪ new_docline               : the line to be added
            ▪ last_linefeed             : the character(s) at the end of the precedent
                                          lines added before

            no RETURNED VALUE
        """
        if SETTINGS["REMOVE_FINAL_SPACES_IN_NEW_DOCLINES"] == "True":
            new_docline, new_doclinefeed = \
                remove_and_return_linefeed(new_docline)
            if new_doclinefeed == "":
                # a special case : see README.md, "(2.1.1) a special case"
                if last_linefeed is not None:
                    new_doclinefeed += last_linefeed
                elif platform.system() == "Windows":
                    new_doclinefeed += "\r\n"
                else:
                    new_doclinefeed += "\n"
                logging.debug("special case : " \
                              "a linefeed has been added to '%s'",
                              new_docline)

            new_docline = new_docline.rstrip()
            new_docline += new_doclinefeed
        logging.debug("+ (%s characters) '%s'",
                      len(new_docline), new_docline.replace(" ", "_"))
        newtargetfile.write(new_docline.encode(encoding="utf-8"))

    #...........................................................................
    def get_lines_with_trigger(targetcontent, docsrc):
        """
            get_lines_with_trigger()

            this function is a subfunction of the pimydoc_a_file() function.
            ________________________________________________________________________

            Return an object required by pimydoc_a_file() : <lines_with_trigger>

            (dict) (int)line number -> (str)name of the doc title to be added after
                                       the line
            ________________________________________________________________________

            ARGUMENTS:
            ▪ targetcontent             : the content of the target file, i.e.
                                          what is returned by
                                          target_file.readlines().
            ▪ docsrc                    : (DocumentationSource object) doc content

            RETURNED VALUE              : (str) the expected dictionary
        """
        res = dict()

        for linenumber, line in enumerate(targetcontent):
            for doctitle in docsrc:
                if doctitle in line:
                    res[linenumber] = doctitle
                    read_doctitles[doctitle] = True
        return res

    #...........................................................................
    def get_startstring(profile, line, doc_title):
        """
            get_startstring()

            this function is a subfunction of the pimydoc_a_file() function.
            ________________________________________________________________________

            Compute the startstring present at the very beginning of <line>
            before the <doc_title>.
            ________________________________________________________________________

            ARGUMENTS:

            ▪ profile                   : (str) "Python", "C++", ...
            ▪ line                      : (str) the line where lies the startstring
            ▪ doc_title                 : (str) a substring of <line>

            RETURNED VALUE              : (str) the startstring
        """
        if profile == "Python":
            if SETTINGS["PROFILE_PYTHON_SPACENBR_FOR_A_TAB"] > 0:
                _line = \
                  line.replace("\t",
                               " "*SETTINGS["PROFILE_PYTHON_SPACENBR_FOR_A_TAB"])
            startstring = _line[:_line.find(doc_title)]
            logging.debug("startstring (Python profile) = '%s'", startstring)
        else:
            startstring = line[:line.find(doc_title)]
            logging.debug("startstring = '%s'", startstring)
        return startstring

    #...........................................................................
    def rewrite_new_targetfile(targetfile_name, just_remove_pimydoc_lines):
        """
            rewrite_new_targetfile()

            this function is a subfunction of the pimydoc_a_file() function.
            ________________________________________________________________________

            Rewrite the target file with the documentation to be added.
            ________________________________________________________________________

            ARGUMENTS :
            ▪ targetfile_name           : (str) name of the file to be modified
            ▪ just_remove_pimydoc_lines : (bool) if True, nothing is added but the
                                          pimydoc lines of documentation are removed.

            no RETURNED VALUE
        """
        # we store the last linefeed characters in order to add it if necessary
        # (see README.md, "(2.1.1) a special case")
        last_linefeed = None

        with open(targetfile_name, "wb") as newtargetfile:
            for linenumber, line in enumerate(targetcontent):
                # let's add a "normal" line, i.e. everything but a Pimydoc-docline.
                if SETTINGS["STARTSYMB_IN_DOC"] not in line and \
                   SETTINGS["STARTSYMB_IN_DOC"].rstrip() not in line:
                    newtargetfile.write(line.encode(encoding="utf-8"))
                else:
                    logging.debug("Line removed from '%s' : '%s'", targetfile_name, line.strip())

                if linenumber in lines_with_trigger:
                    # let's add the expected documentation :
                    doc_content = docsrc[lines_with_trigger[linenumber]]
                    doc_title = lines_with_trigger[linenumber]
                    logging.debug("doc_title = '%s'", doc_title)

                    _, last_linefeed = remove_and_return_linefeed(line)

                    if just_remove_pimydoc_lines is False:
                        logging.info("+ doc to add/update in '%s'; doctitle='%s'",
                                     targetfile_name, doc_title)

                        # what is the "startstring", i.e. the string in <line>
                        # before the doc title ?
                        startstring = get_startstring(profile, line, doc_title)

                        for docline in doc_content:
                            new_docline = startstring+SETTINGS["STARTSYMB_IN_DOC"]+docline
                            rewrite_new_targetfile__line(newtargetfile, new_docline, last_linefeed)

    # ----------------------------
    # here begins pimydoc_a_file()
    logging.debug("- - pimydoc_a_file() : %s", targetfile_name)

    # --------------------------------------
    # choose a profile for the target file :
    profile = None
    if targetfile_name.endswith(".py"):
        profile = "Python"
    elif targetfile_name.endswith(".cpp") or targetfile_name.endswith(".h"):
        profile = "C++"
    logging.debug("for %s, the profile '%s' will be used.", targetfile_name, profile)

    # -------------------------------------------
    # let's read the content of the target file :
    try:
        with open(targetfile_name, 'rt', encoding="utf-8") as target_file:
            targetcontent = target_file.readlines()
    except FileNotFoundError as error:
        logging.debug("! Can't read the content of the file '%s'", targetfile_name)
        logging.debug("! Error returned by Python : (FileNotFoundError) "+str(error))
        logging.debug("! Skipping this file.")
        return read_doctitles
    except UnicodeDecodeError as error:
        logging.debug("! Can't read the content of the file '%s'", targetfile_name)
        logging.debug("! Error returned by Python : (UnicodeDecodeError) "+str(error))
        logging.debug("! Skipping this file.")
        return read_doctitles

    # ---------------------------
    # fill <lines_with_trigger> :
    # (int)line number : (str)name of the doc title to be added after the line
    lines_with_trigger = get_lines_with_trigger(targetcontent, docsrc)

    # -------------
    # backup file :
    shutil.copy(targetfile_name, targetfile_name+"_pimydoc_backup")

    # --------------------------
    # delete (old) target file :
    os.remove(targetfile_name)

    # ------------------------------------------------
    # rewrite (new) target file with the new content :
    rewrite_new_targetfile(targetfile_name, just_remove_pimydoc_lines)

    # -------------------------------------------------------------------
    # give to the new target file the permission of the old target file :
    shutil.copystat(targetfile_name+"_pimydoc_backup", targetfile_name)

    # --------------------
    # remove backup file :
    if securitymode is False:
        os.remove(targetfile_name+"_pimydoc_backup")

    logging.debug("--- done with %s", targetfile_name)

    return read_doctitles

#///////////////////////////////////////////////////////////////////////////////
def pimydoc(args, docsrc):
    """
        pimydoc() function
        ____________________________________________________________________

        Main function of the program : insert and add the documentation
        stored in <docsrc> in the files given by <args>.

        To be called from another script after args  has been filled.
        This function doesn't read the arguments on the command line.
        ____________________________________________________________________

        ARGUMENTS :
        ▪ args                      : (argparse.Namespace) args from the
                                      commande line.
        ▪ docsrc                    : (DocumentationSource object) doc content

        no RETURNED VALUE
    """
    number_of_files = 0
    number_of_discarded_files = 0

    # dict : (str)doctitle->(bool)has the doctile been read ?
    # this dict is updated by pimydoc_a_file().
    read_doctitles = dict(zip(docsrc.keys(), [False,]*len(docsrc)))

    for dirpath, _, filenames in os.walk(normpath(args.sourcepath)):
        for filename in filenames:
            number_of_files += 1
            fullname = os.path.join(normpath(dirpath), filename)

            if re.search(SETTINGS["REGEX_SOURCE_FILTER"], fullname):
                if fullname == args.docsrcfile:
                    logging.info("- discarded the documentation source file '%s'",
                                 fullname)
                    number_of_discarded_files += 1
                elif fullname == args.docsrcfile+"~":
                    logging.info("- discarded the backup of the documentation source file '%s'",
                                 fullname)
                    number_of_discarded_files += 1
                else:
                    read_doctitles = pimydoc_a_file(fullname, docsrc,
                                                    args.remove, args.securitymode,
                                                    read_doctitles)
            else:
                number_of_discarded_files += 1
                if args.vvv is True or args.verbose == 2:
                    logging.info("- discarded '%s'", fullname)

    # ----------------------------------------------------------
    # are they doctitle defined in the documentation source file
    # not read in the source target ?
    for doctitle in read_doctitles:
        if read_doctitles[doctitle] is False:
            logging.info("!!! beware : the doctitle '%s' is defined " \
                         "in the documentation source " \
                         "file but never appears in the source directory.", doctitle)

    logging.info("Read %s file(s), discarded %s file(s), %s file(s) may have been modified.",
                 number_of_files,
                 number_of_discarded_files,
                 number_of_files - number_of_discarded_files)

#///////////////////////////////////////////////////////////////////////////////
def main():
    """
        main()
        ________________________________________________________________________

        Main entry point. Fill the args variable. Launch the pimydoc()
        function.
        ________________________________________________________________________

        no PARAMETER

        no RETURNED VALUE

        exit codes
        | |  0 if success
        | | -1 if the documentation source file doesn't exist
        | | -2 if the documentation source file is ill-formed
    """
    args = CommandLineParser().get_args()

    if args.vv:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    elif args.vvv:
        logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)
    elif args.verbose == 0:
        logging.basicConfig(format="%(message)s", level=logging.ERROR)
    elif args.verbose == 1:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    elif args.verbose == 2:
        logging.basicConfig(format="%(levelname)s %(message)s", level=logging.DEBUG)

    logging.info("=== pimydoc : entry point ===")
    logging.debug("main() : args.docsrcfile='%s'; args.sourcepath='%s'",
                  args.docsrcfile, args.sourcepath)

    if args.securitymode:
        logging.info("Security mode activated : " \
                     "the backup files created by the program will not be deleted.")

    if args.downloadpimydoc:
        download_default_pimydoc()
        sys.exit(0)

    if not os.path.exists(args.docsrcfile):
        logging.error("! The expected documentation source file '%s' doesn't exist.",
                      args.docsrcfile)
        logging.error("=== leaving pimydoc ===")
        sys.exit(-1)

    docsrc = DocumentationSource(args.docsrcfile)

    if len(docsrc.errors) > 0:
        logging.error("! Errors occured by reading the documentation source file :")
        for err_msg in docsrc.errors:
            logging.error(err_msg)
            logging.error("=== leaving pimydoc ===")
            sys.exit(-2)

    if args.remove:
        logging.info("Let's remove every pimydoc line from the source directory.")

    pimydoc(args, docsrc)

    logging.info("=== pimydoc : exit point ===")

    sys.exit(0)

#///////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    main()
