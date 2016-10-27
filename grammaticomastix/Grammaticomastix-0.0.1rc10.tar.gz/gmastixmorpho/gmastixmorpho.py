#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    GmastixMorpho Copyright (C) 2016 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of GmastixMorpho.
#    GmastixMorpho is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GmastixMorpho is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GmastixMorpho.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏GmastixMorpho❏ : gmastixmorpho.py

    main file of the GmastixMorpho project.

    See the main page at https://github.com/suizokukan/gmastixmorpho .
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
    ˮ

    GmastixMorpho format for the database:
    ˮ
    ˮ GmastixMorpho.search() calls Hermaia.search() and transforms
    ˮ the result to fit the value returned by GmastixMorpho.search().
    ˮ
    ˮ GmastixMorpho expects the value corresponding 'context' follows
    ˮ the following format : "AAA=BBB;CCC=DDD;EEE=FFF" where AAA...FFF
    ˮ are strings.
    ˮ
    ˮ E.g. Hermaia.search() returns a list of string(s) like :
    ˮ
    ˮ      ( {'sourceword' : "are",
    ˮ         'inflection' : "verb",
    ˮ         'context'    : "tense=present;number=plural;person=3",
    ˮ         'accuracy'   : 0.5},
    ˮ      )
    ˮ
    ˮ GmastixMorpho.search() will call GmastixMorpho.hermaia2gmastixmorpho()
    ˮ to transform this list of dicts, expanding the "context" value :
    ˮ
    ˮ      ( {'sourceword' : "are",
    ˮ         'inflection' : "verb",
    ˮ         'tense'      : "present",
    ˮ         'number'     : "plural",
    ˮ         'person3'    : "3",
    ˮ         'accuracy'   : 0.5},
    ˮ      )
    ˮ

    about the dumpfile format:
    ˮ A dumpfile is a text file made of an optional header and of the data.
    ˮ An empty line (=made of spaces) will be discarded.
    ˮ A line beginning with ### will be discarded (=commentary line)
    ˮ
    ˮ header : (optional)
    ˮ     "version number=XXX", XXX being an integer
    ˮ
    ˮ     e.g. :
    ˮ     "version number=3"
    ˮ
    ˮ data :
    ˮ     one line per entry :
    ˮ     AAA□BBB□CCC□DDD, AAA,BBB,CCC,DDD being strings that may be empty.
    ˮ
    ˮ         AAA : (str) the analysed form
    ˮ         BBB : (str) the dictionary/base form
    ˮ         CCC : (str) the inflection name
    ˮ         DDD : (str) the 'context'(='analyse') string.
    ˮ
    ˮ
    ˮ         AAA : you may use the underscore '_' symbol to separate different
    ˮ         words, somethink like "has_been_given"
    ˮ
    ˮ         DDD : GmastixMorpho expects the value corresponding 'context' follows
    ˮ         the following format : "AAA=BBB;CCC=DDD;EEE=FFF" where AAA...FFF
    ˮ         are strings.
    ˮ
    ˮ     e.g. :
    ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
    ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
    ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
"""
import collections
import os
import sqlite3

from hermaia.hermaia import Hermaia, HermaiaError
from hermaia.hermaia import VERSION as HERMAIA_VERSION

import logger
LOGGER = logger.get_logger(__name__)  # you may add e.g. level=logger.INFO .

# (str)
VERSION = "0.0.5"
LOGGER.info("GmastixMorpho version: %s", VERSION)
LOGGER.info("Hermaia version used by GmastixMorpho :"+str(HERMAIA_VERSION))

################################################################################
#    DbAndDump class
#    ________________________________________________________________________
#
#       Simple way to store in GmastixMorpho.files the name of a database
#    of and its dump file.
#    ____________________________________________________________________
#
#    instance attributes :
#    ● databasefile          : (str) the name of the database.
#    ● dumpfile              : (str) the name of the dump file.
DbAndDump = collections.namedtuple("DbAndDump",
                                   ["databasefile",
                                    "dumpfile"])


################################################################################
class GmastixMorpho(object):
    """
        GmastixMorpho class : may be used as a context manager, or not : see the
                              __enter__()/enter(), __exit__()/exist() methods.
        ________________________________________________________________________

        Use GmastixMorpho to search data into Hermaia databases.
        ________________________________________________________________________

        class attribute :

        DEFAULT_DIRECTORY       : the directory where the databases and the
                                  dumpfiles are stored by default.

        instance attributes :

        ● files                 : dict with the names of the databases and of
                                  the dumpfiles.
                                    dict: (str)language name → DbAndDump
        ● hermaia               : Hermaia objects
                                    dict: (str)language name → Hermaia object
        ● src_directory         : source directory where the databases and the
                                  dumpfiles are stored.

        methods :
        ● __enter__(self):
        ● __exit__(self, type, value, traceback)
        ● __init__(self, languages, src_directory=None):
        ● enter(self)
        ● exit(self)
        ● hermaia2gmastixmorpho(src)
        ● infos(self, language)
        ● search(self, language, src, minimal_accuracy=1)
        ● update_db_from_dumpfile(self, language)
    """
    DEFAULT_DIRECTORY = os.path.join("gmastixmorpho", "databases")

    #///////////////////////////////////////////////////////////////////////////
    def __enter__(self):
        """
            GmastixMorpho.__enter__()
            ___________________________________________________________________

            First function to be called after __init__() at the end of
            the with... statement .

            This function is called AFTER self.__init__() .
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self
        """
        LOGGER.debug("GmastixMorpho.__enter__()")
        self.enter()
        return self

    #///////////////////////////////////////////////////////////////////////////
    def __exit__(self, type, value, traceback):
        """
            GmastixMorpho.__exit__()
            ___________________________________________________________________

            Last function called before shutting down <self> in a with...
            statement.
            ___________________________________________________________________

            ARGUMENTS :
            ▪ type      : the type of the exception
            ▪ value     : the exception instance raised.
            ▪ traceback : a traceback instance.

            no RETURNED VALUE
        """
        # problem with Pylint :
        # pylint: disable=W0622
        # Redefining built-in 'type' (redefined-builtin)

        LOGGER.debug("GmastixMorpho.__exit__()")

        self.exit()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 languages,
                 src_directory=None):
        """
            GmastixMorpho.__init__()
            ___________________________________________________________________
            ___________________________________________________________________

            ARGUMENTS:
            ▪ languages         : a list of strings. E.g. ("fra", "grc",)
            ▪ src_directory     : the directory where the databases and the
                                  dumpfiles are stored.
                                  None or a string : if None, src_directory
                                  will be set to the default directory
                                  i.e. GmastixMorpho.DEFAULT_DIRECTORY .
            RETURNED VALUE
        """
        LOGGER.debug("GmastixMorpho.__init__() : languages=%s", languages)

        self.hermaia = dict()

        self.src_directory = src_directory
        if self.src_directory is None:
            self.src_directory = GmastixMorpho.DEFAULT_DIRECTORY

        self.files = dict()

        for language in languages:

            database_name = os.path.join(self.src_directory, "database."+language)
            dumpfile_name = os.path.join(self.src_directory, "dumpfile."+language)

            if not os.path.exists(database_name):
                LOGGER.info("missing database file : where is '{0}' ?".format(database_name))
            if not os.path.exists(dumpfile_name):
                LOGGER.info("missing dumpfile : where is '{0}' ?".format(dumpfile_name))

            self.files[language] = DbAndDump(databasefile=database_name,
                                             dumpfile=dumpfile_name)

            if os.path.exists(dumpfile_name):
                # the dump file exists but not the database :
                self.hermaia[language] = Hermaia(database=sqlite3.connect(database_name),
                                                 dumpfile=open(dumpfile_name, mode="r"))
            elif os.path.exists(database_name):
                # the dump file doesn't exist :                
                self.hermaia[language] = Hermaia(database=sqlite3.connect(database_name))
            else:
                LOGGER.error("can't open the database nor the dumpfile.")

    #///////////////////////////////////////////////////////////////////////////
    def enter(self):
        """
            GmastixMorpho.__enter__()
            ___________________________________________________________________

            First function to be called after __init__() at the end of
            the with... statement .

            This function is called AFTER self.__init__() .
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("GmastixMorpho.enter()")

        for language in self.hermaia:
            self.hermaia[language].enter()

    #///////////////////////////////////////////////////////////////////////////
    def exit(self):
        """
            GmastixMorpho.__exit__()
            ___________________________________________________________________

            Last function called before shutting down <self> in a with...
            statement.
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("GmastixMorpho.exit()")

        for language in self.hermaia:
            self.hermaia[language].exit()

    #///////////////////////////////////////////////////////////////////////////
    @staticmethod
    def hermaia2gmastixmorpho(src):
        """
            GmastixMorpho.hermaia2gmastixmorpho()
            ___________________________________________________________________

            Use this method to transform a result search returned by Hermaia
            into a result adapted for GmastixMorpho.

            GmastixMorpho format for the database:
            ˮ
            ˮ GmastixMorpho.search() calls Hermaia.search() and transforms
            ˮ the result to fit the value returned by GmastixMorpho.search().
            ˮ
            ˮ GmastixMorpho expects the value corresponding 'context' follows
            ˮ the following format : "AAA=BBB;CCC=DDD;EEE=FFF" where AAA...FFF
            ˮ are strings.
            ˮ
            ˮ E.g. Hermaia.search() returns a list of string(s) like :
            ˮ
            ˮ      ( {'sourceword' : "are",
            ˮ         'inflection' : "verb",
            ˮ         'context'    : "tense=present;number=plural;person=3",
            ˮ         'accuracy'   : 0.5},
            ˮ      )
            ˮ
            ˮ GmastixMorpho.search() will call GmastixMorpho.hermaia2gmastixmorpho()
            ˮ to transform this list of dicts, expanding the "context" value :
            ˮ
            ˮ      ( {'sourceword' : "are",
            ˮ         'inflection' : "verb",
            ˮ         'tense'      : "present",
            ˮ         'number'     : "plural",
            ˮ         'person3'    : "3",
            ˮ         'accuracy'   : 0.5},
            ˮ      )
            ˮ
            ___________________________________________________________________

            ARGUMENT:
            ▪ src : something returned by Hermaia.search(), i.e. a list of dict.

            RETURNED VALUE : a list of dict
        """
        res = []

        for element in src:
            # <element> : a dict
            res.append(dict())

            # key=(str); value:a string
            #   if key=="context", value is a string defining a dict. see the
            #   documentation above in the docstring.
            for key, value in element.items():
                if key != "context":
                    res[-1][key] = value
                else:
                    # <value> is a string following this format :
                    #   "key1=value1;key2=value2"
                    subdict = dict([key_and_value.split("=") for key_and_value in value.split(";")])

                    for keyword, keyword_value in subdict.items():
                        res[-1][keyword] = keyword_value

        return res

    #///////////////////////////////////////////////////////////////////////////
    def infos(self, language=None, full_details=True):
        """
            GmastixMorpho.infos()
            ___________________________________________________________________

            Return informations about the <language> data stored in the
            database.
            ___________________________________________________________________

            ARGUMENT :
            ▪ language          : str or None; if None, all the known languages
                                  will be used.
            ▪ full_details      : (bool) if True, the database will be read
                                  entirely.

            RETURNED VALUE : the expected string
        """
        LOGGER.debug("GmastixMorpho.infos() : language=%s", language)

        if language is not None:
            res = ["GmastixMorpho.infos() : language='{0}'".format(language)]
            res.append("  o source directory  : {0}".format(self.src_directory))
            res.append("  o source files      : {0}".format(self.files[language]))

            return "\n".join(res) + "\n  o " + self.hermaia[language].infos(full_details)
        else:
            res = []
            for lang in self.hermaia:
                res.append("\nGmastixMorpho.infos() : lang='{0}'".format(lang))
                res.append("o source directory  : {0}".format(self.src_directory))
                res.append("o source files      : {0}".format(self.files[lang]))

                res.append(self.hermaia[lang].infos(full_details))

            return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def search(self, language, searched_form, minimal_accuracy=1):
        """
            GmastixMorpho.search()
            ___________________________________________________________________

              Search the <searched_form> in the database. Return a list of the
            matching values placed into a dictionary. The list is
            empty if no result could be found.

            E.g. :
               ( {'sourceword' : "are",
                  'inflection' : "verb",
                  'tense'      : "present",
                  'number'     : "plural",
                  'person3'    : "3",
                  'accuracy'   : 0.5},
               )
            ___________________________________________________________________

            PARAMETER :
            ▪ language          : (str)
            ▪ searched_form     : (str)
            ▪ minimal_accuracy  : (float) minimal accuracy returned by
                                  textdiff_distance()
                                  minimal_accuracy ∈ [0;1]

            RETURNED VALUE : a list of dicts (an empty list if there's no
                             result). The results are sorted by 'accuracy',
                             the first result being the most interesting.
        """
        LOGGER.debug("GmastixMorpho.search(); " \
                     "language='%s' searched_form='%s'; minimal_accuracy=%s",
                     language, searched_form, minimal_accuracy)

        if language not in self.hermaia:
            LOGGER.error("GmastixMorpho.analyse() : unknown language='%s' .", language)

        res = self.hermaia[language].search(searched_form=searched_form,
                                            minimal_accuracy=minimal_accuracy)

        # We have to call GmastixMorpho.hermaia2gmastixmorpho() since there's a
        # conversion to be done between the Hermaia format and the GmastixMorpho
        # one.
        return self.hermaia2gmastixmorpho(res)

    #///////////////////////////////////////////////////////////////////////////
    def update_db_from_dumpfile(self, language):
        """
            GmastixMorpho.update_db_from_dumpfile()
            ___________________________________________________________________

            Remove the content of a database and replace it with the content
            of a dumpfile.

            about the dumpfile format:
            ˮ A dumpfile is a text file made of an optional header and of the data.
            ˮ An empty line (=made of spaces) will be discarded.
            ˮ A line beginning with ### will be discarded (=commentary line)
            ˮ
            ˮ header : (optional)
            ˮ     "version number=XXX", XXX being an integer
            ˮ
            ˮ     e.g. :
            ˮ     "version number=3"
            ˮ
            ˮ data :
            ˮ     one line per entry :
            ˮ     AAA□BBB□CCC□DDD, AAA,BBB,CCC,DDD being strings that may be empty.
            ˮ
            ˮ         AAA : (str) the analysed form
            ˮ         BBB : (str) the dictionary/base form
            ˮ         CCC : (str) the inflection name
            ˮ         DDD : (str) the 'context'(='analyse') string.
            ˮ
            ˮ
            ˮ         AAA : you may use the underscore '_' symbol to separate different
            ˮ         words, somethink like "has_been_given"
            ˮ
            ˮ         DDD : GmastixMorpho expects the value corresponding 'context' follows
            ˮ         the following format : "AAA=BBB;CCC=DDD;EEE=FFF" where AAA...FFF
            ˮ         are strings.
            ˮ
            ˮ     e.g. :
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
            ___________________________________________________________________

            PARAMETER :
            ▪ language  : (str)

            RETURNED VALUE : (bool)success
        """
        LOGGER.debug("GmastixMorpho.update_db_from_dumpfile(); language='%s'", language)

        if not os.path.exists(self.files[language].dumpfile):
            LOGGER.error("No dumpfile '%s'", self.files[language].dumpfile)
            return False

        success = True

        try:
            self.hermaia[language].init_from_dumpfile()

        except HermaiaError as exception:
            LOGGER.error("update_db_from_dumpfile() : an error occured; message=%s", exception)
            success = False

        return success
