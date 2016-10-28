#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    Hermaia Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Hermaia.
#    Hermaia is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Hermaia is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Hermaia.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏Hermaia❏ : hermaia.py

    ἕρμαια is an Ancient Greek name meaning "gifts from Hermes" hence "gifts,
    treasures".
    Use Hermaia to read and store textual forms that have been analysed.

    See the project's main page at https//github.com/suizokukan/hermaia
    ____________________________________________________________________________

    Hermaia stores data in a SQL database with the help of the Python's sqlite3
    module and can read/write data from/to a text dump file.

    An Hermaia object can be used with and without with statement. Enter and exit
    functions are duplicated :

        __enter__ <-> enter()
        __exit__  <-> exit()

    E.g. using the with statement :

        with sqlite3.connect("database.db") as database:
            with open('dumpfile.txt', "w") as dumpfile:
                with Hermaia(database = database, dumpfile = dumpfile) as h:
                    ....

    about the database structure:
    ˮ
    ˮ (Pseudo SQL code)
    ˮ
    ˮ CREATE TABLE metadata
    ˮ              (versionnumber INTEGER PRIMARY KEY,
    ˮ              timestamp INT)
    ˮ
    ˮ CREATE TABLE forms
    ˮ              (numid INTEGER PRIMARY KEY,
    ˮ              form TEXT,
    ˮ              sourceword TEXT,
    ˮ              inflection_id INTEGER,
    ˮ              context VARCHAR(Hermaia.varchar_maxlen_context))
    ˮ
    ˮ CREATE TABLE inflections
    ˮ              (numid INTEGER PRIMARY KEY,
    ˮ               name VARCHAR(Hermaia.varchar_maxlen_inflectionname))
    ˮ
    ˮ E.g. four records in English as they are stored in the database (in the
    ˮ 'forms' table), the inflection numbers being described in the 'inflections'
    ˮ table.
    ˮ
    ˮ         form:               "mice"
    ˮ         sourceword:         "mouse"
    ˮ         inflection:         17
    ˮ         context:            "number=plural"
    ˮ
    ˮ         form:               "are"
    ˮ         sourceword:         "be"
    ˮ         inflection:         34
    ˮ         context:            "tense=present;number=plural;person=1"
    ˮ
    ˮ         form:               "are"
    ˮ         sourceword:         "be"
    ˮ         inflection:         34
    ˮ         context:            "tense=present;number=plural;person=2"
    ˮ
    ˮ         form:               "are"
    ˮ         sourceword:         "be"
    ˮ         inflection:         34
    ˮ         context:            "tense=present;number=plural;person=3"
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
    ˮ         DDD : (str) the analyse string. This string has no format.
    ˮ                     For an example of one possible format, see
    ˮ                     the GmastixMorpho project which uses Hermaia.
    ˮ
    ˮ     e.g. :
    ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
    ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
    ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
    ˮ
    ˮ     NB : the "analyse string" follows here a specifical format, used
    ˮ          by the GmastixMorpho project. Other formats are welcome !
    _____________________________________________________________________________

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
"""
import datetime

import hermaia.utilities as utilities
from hermaia.hermaiaerror import HermaiaError
import logger
LOGGER = logger.get_logger(__name__)  # you may add e.g. level=logger.INFO .

VERSION = "0.1.3"

################################################################################
class Hermaia(object):
    """
        Hermaia class : may be used as a context manager, or not : see the
                        __enter__()/enter(), __exit__()/exist() methods.
        ________________________________________________________________________

        With an Hermaia object you may read data from a database, save the
        database to a text dumpfile and initialize a database from the dumpfile.
        ________________________________________________________________________

        class attributes :

        ● separator_in_dumpfile         : separator used in the dumpfile to
                                          separate the fields
        ● carriage_return_in_dumpfile   : symbol used in the dumpfile at the end
                                          of the line
        ● max_operations_before_commit  : insert/update operations will commit
                                          after the following number of
                                          operations
        ● varchar_maxlen_inflectionname : maximal length of 'name' in column
                                          inflections.name
        ● varchar_maxlen_context        : maximal length of 'name' in column
                                          forms.context.

        instance attributes :

        ● database               : None or a sqlite3.Connection object
        ● database_cursor        : None or sqlite3.Cursor
        ● dumpfile               : None or a _io.TextIOWrapper object (=open())

        methods :

        ● __enter__(self):
        ● __exit__(self, type, value, traceback):
        ● __init__(self,
                   database=None,
                   dumpfile=None
        ● add_data(self,
                   form,
                   sourceword,
                   inflection,
                   context)
        ● commit(self)
        ● create_structure(self)
        ● do_the_tables_exist(self)
        ● dumpfile__add_data(self,
                             form,
                             sourceword,
                             inflection,
                             context
        ● dumpfile__add_version(self, versionnumber)
        ● dumpfile__write_from_db(self)
        ● enter(self)
        ● exit(self)
        ● get_inflection_id(self, inflection_name)
        ● get_inflection_name(self, inflection_id)
        ● get_versionnumber_and_timestamp(self)
        ● infos(self, full_details=True)
        ● init_from_dumpfile(self)
        ● search(self, form, minimal_accuracy=1)
        ● write_versionnumber_and_tstamp(self, versionnumber, timestamp=None)
    """

    # separator used in the dumpfile to separate the fields :
    separator_in_dumpfile = chr(0x25A1)
    # symbol used in the dumpfile at the end of the line :
    carriage_return_in_dumpfile = "\n"

    # insert/update operations will commit after the following number of
    # operations :
    max_operations_before_commit = 1000

    # maximal length of 'name' in column inflections.name :
    varchar_maxlen_inflectionname = 255
    # maximal length of 'name' in column forms.context :
    varchar_maxlen_context = 255

    #///////////////////////////////////////////////////////////////////////////
    def __enter__(self):
        """
            Hermaia.__enter__()
            ___________________________________________________________________

            First function to be called after __init__() at the end of
            the with... statement .

            This function is called AFTER self.__init__() .
            ___________________________________________________________________

            no ARGUMENT

            RETURNED VALUE : self
        """
        LOGGER.debug("Hermaia.__enter__()")
        self.enter()
        return self

    #///////////////////////////////////////////////////////////////////////////
    def __exit__(self, type, value, traceback):
        """
            Hermaia.__exit__()
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

        LOGGER.debug("Hermaia.__exit__()")

        self.exit()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 database=None,
                 dumpfile=None):
        """
            Hermaia.__init__()
            ___________________________________________________________________

            Initialize <self> without loading any data. To load data,
            e.g. from a dumpfile, see self.init_from_dumpfile().

            This function is called BEFORE self.__enter__() .

            about the database structure:
            ˮ
            ˮ (Pseudo SQL code)
            ˮ
            ˮ CREATE TABLE metadata
            ˮ              (versionnumber INTEGER PRIMARY KEY,
            ˮ              timestamp INT)
            ˮ
            ˮ CREATE TABLE forms
            ˮ              (numid INTEGER PRIMARY KEY,
            ˮ              form TEXT,
            ˮ              sourceword TEXT,
            ˮ              inflection_id INTEGER,
            ˮ              context VARCHAR(Hermaia.varchar_maxlen_context))
            ˮ
            ˮ CREATE TABLE inflections
            ˮ              (numid INTEGER PRIMARY KEY,
            ˮ               name VARCHAR(Hermaia.varchar_maxlen_inflectionname))
            ˮ
            ˮ E.g. four records in English as they are stored in the database (in the
            ˮ 'forms' table), the inflection numbers being described in the 'inflections'
            ˮ table.
            ˮ
            ˮ         form:               "mice"
            ˮ         sourceword:         "mouse"
            ˮ         inflection:         17
            ˮ         context:            "number=plural"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=1"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=2"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=3"
            ˮ
            ___________________________________________________________________

            ARGUMENTS :
            ▪ database : None or a sqlite3.Connection object
            ▪ dumpfile : None or a _io.TextIOWrapper object, i.e. the
                         returned value to a call to open()

            if <database> is None, no access to the database is allowed.
            if <dumpfile> is None, no access to the dumpfile is allowed.

            no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.__init__() database=%s; dumpfile=%s",
                     str(database), str(dumpfile))

        if hasattr(database, "upper"):
            msg = "<database> can't be a string : see the documentation"
            raise HermaiaError(context="Hermaia.__init__()",
                               message=msg)

        if hasattr(dumpfile, "upper"):
            msg = "<dumpfile> can't be a string : see the documentation"
            raise HermaiaError(context="Hermaia.__init__()",
                               message=msg)

        self.database = database
        self.dumpfile = dumpfile
        self.database_cursor = None     # will be initialized by self.__enter__()

        # number of INSERTs which have not been followed by a commit :
        self.nbr_of_uncommited_operations = 0

    #///////////////////////////////////////////////////////////////////////////
    def add_data(self,
                 form,
                 sourceword,
                 inflection,
                 context):
        """
            Hermaia.add_data()
            ___________________________________________________________________

            Add <form>, <sourceword>, <context>, to the database.
            If the values are already in the database, an exception is raised.

            ✓ unittests : see the HermaiaTests.test__add_data*() methods.
            ___________________________________________________________________

            PARAMETERS :

            ▪ formv       : (str)
            ▪ sourceword  : (str)
            ▪ inflection  : (str)
            ▪ context     : (str)

                E.g. form:              "are"
                     sourceword:        "be"
                     inflection:        "verb"
                     analyse:           "tense=present;number=plural;person=1

            no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.add_data() " \
                     "form='%s' sourceword='%s' inflection='%s' context='%s'",
                     form, sourceword, inflection, context)

        #-----------------------------------------------------------------------
        # is there an available database ?
        if self.database is None:
            msg = "No database specified"
            raise HermaiaError(context="Hermaia.add_data()",
                               message=msg)

        # is <inflection> too long ?
        if len(inflection) > Hermaia.varchar_maxlen_inflectionname:
            msg = "String too long " \
                  "(limit=Hermaia.varchar_maxlen_inflectionname={0}) : '{1}', len={2}"
            raise HermaiaError(context="Hermaia.add_data()",
                               message=msg.format(Hermaia.varchar_maxlen_inflectionname,
                                                  inflection,
                                                  len(inflection)))

        # is <context> too long ?
        if len(context) > Hermaia.varchar_maxlen_context:
            msg = "String too long " \
                  "(limit=Hermaia.varchar_maxlen_context={0}) : '{1}', len={2}"
            raise HermaiaError(context="Hermaia.add_data()",
                               message=msg.format(Hermaia.varchar_maxlen_context,
                                                  context,
                                                  len(context)))

        #-----------------------------------------------------------------------
        # does <inflection> exist in the table "inflections" or do we have to
        # add <inflection> in this table ?
        if self.get_inflection_id(inflection) is None:
            # yes, we have to add <inflection> in the "inflections" table :
            sql_order = "INSERT INTO inflections VALUES (?, ?)"
            self.database_cursor.execute(sql_order,
                                         (None, inflection,))
            self.commit()

        #-----------------------------------------------------------------------
        # what's the <inflection_id> corresponding to <inflection> ?
        inflection_id = self.get_inflection_id(inflection)

        #-----------------------------------------------------------------------
        # Do the three values <form>, <sourceword>, <inflection_id>, <context> already exist
        # in the database ?
        sql_order = "SELECT form, sourceword, inflection_id, context " \
                    "FROM forms " \
                    "WHERE form=? AND sourceword=? AND inflection_id=? AND context=?"

        self.database_cursor.execute(sql_order,
                                     (form, sourceword, inflection_id, context))

        if self.database_cursor.fetchone() is not None:
            msg = "The database has already the three values " \
                  "form='{0}',sourceword='{1}',inflection='{2}'/#{3}, context='{4}'"
            raise HermaiaError(context="Hermaia.add_data()",
                               message=msg.format(form,
                                                  sourceword,
                                                  inflection, inflection_id,
                                                  context))

        #-----------------------------------------------------------------------
        # adding the values :
        sql_order = "INSERT INTO forms VALUES (?, ?, ?, ?, ?)"
        self.database_cursor.execute(sql_order,
                                     (None, form, sourceword, inflection_id, context))

        self.commit()

    #///////////////////////////////////////////////////////////////////////////
    def commit(self):
        """
            Hermaia.commit()
            ___________________________________________________________________

            Commit the changes in the database if necessary.
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.commit()")

        if self.nbr_of_uncommited_operations >= Hermaia.max_operations_before_commit:
            # yes, it's time to commit :
            self.database.commit()
            self.nbr_of_uncommited_operations = 0
        else:
            # no, it's not time yet :
            self.nbr_of_uncommited_operations += 1

    #///////////////////////////////////////////////////////////////////////////
    def create_structure(self):
        """
            Hermaia.create_structure()
            ___________________________________________________________________

            Create the tables of the database.

            about the database structure:
            ˮ
            ˮ (Pseudo SQL code)
            ˮ
            ˮ CREATE TABLE metadata
            ˮ              (versionnumber INTEGER PRIMARY KEY,
            ˮ              timestamp INT)
            ˮ
            ˮ CREATE TABLE forms
            ˮ              (numid INTEGER PRIMARY KEY,
            ˮ              form TEXT,
            ˮ              sourceword TEXT,
            ˮ              inflection_id INTEGER,
            ˮ              context VARCHAR(Hermaia.varchar_maxlen_context))
            ˮ
            ˮ CREATE TABLE inflections
            ˮ              (numid INTEGER PRIMARY KEY,
            ˮ               name VARCHAR(Hermaia.varchar_maxlen_inflectionname))
            ˮ
            ˮ E.g. four records in English as they are stored in the database (in the
            ˮ 'forms' table), the inflection numbers being described in the 'inflections'
            ˮ table.
            ˮ
            ˮ         form:               "mice"
            ˮ         sourceword:         "mouse"
            ˮ         inflection:         17
            ˮ         context:            "number=plural"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=1"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=2"
            ˮ
            ˮ         form:               "are"
            ˮ         sourceword:         "be"
            ˮ         inflection:         34
            ˮ         context:            "tense=present;number=plural;person=3"
            ˮ
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.create_structure()")

        #-----------------------------------------------------------------------
        # is there an available database ?
        if self.database is None:
            msg = "No database specified"
            raise HermaiaError(context="Hermaia.create_structure()",
                               message=msg)

        #-----------------------------------------------------------------------
        # creating the database tables :
        sql_order = "CREATE TABLE metadata " \
                    "(versionnumber INTEGER PRIMARY KEY, " \
                    "timestamp INT)"
        self.database_cursor.execute(sql_order)

        sql_order = "CREATE TABLE forms " \
                    "(numid INTEGER PRIMARY KEY, " \
                    "form TEXT, " \
                    "sourceword TEXT, " \
                    "inflection_id INTEGER, " \
                    "context VARCHAR({0}))".format(Hermaia.varchar_maxlen_context)
        self.database_cursor.execute(sql_order)

        sql_order = "CREATE TABLE inflections " \
                    "(numid INTEGER PRIMARY KEY, " \
                    "name VARCHAR({0}))".format(Hermaia.varchar_maxlen_inflectionname)
        self.database_cursor.execute(sql_order)

        # we force the commit and we do not call the self.commit() method :
        self.database.commit()

        # version number and timestamp : let's write default values into the database.
        self.write_versionnumber_and_tstamp(versionnumber=0, timestamp=None)

    #///////////////////////////////////////////////////////////////////////////
    def do_the_tables_exist(self):
        """
            Hermaia.do_the_tables_exist()
            ___________________________________________________________________

            Return either True if all the expected tables are in the database,
            either False.

            ✓ unittests : see the HermaiaTests.test__do_the_table_exist()
                          method.
            ___________________________________________________________________

            RETURNED VALUE : bool
        """
        LOGGER.debug("Hermaia.do_the_tables_exist()")

        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.do_the_tables_exist()",
                               message=msg)

        sql_order = "SELECT * FROM sqlite_master WHERE type='table' AND name='forms'"
        self.database_cursor.execute(sql_order)
        table_forms = self.database_cursor.fetchone() is not None

        sql_order = "SELECT * FROM sqlite_master WHERE type='table' AND name='inflections'"
        self.database_cursor.execute(sql_order)
        table_inflections = self.database_cursor.fetchone() is not None

        sql_order = "SELECT * FROM sqlite_master WHERE type='table' AND name='metadata'"
        self.database_cursor.execute(sql_order)
        table_metadata = self.database_cursor.fetchone() is not None

        return table_forms and table_inflections and table_metadata

    #///////////////////////////////////////////////////////////////////////////
    def dumpfile__add_data(self,
                           form,
                           sourceword,
                           inflection,
                           context):
        """
            Hermaia.dumpfile__add_data()
            ___________________________________________________________________

            Write the values <form>, <sourceword>, <inflection>, <context>
            into the dump file.

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
            ˮ         DDD : (str) the analyse string. This string has no format.
            ˮ                     For an example of one possible format, see
            ˮ                     the GmastixMorpho project which uses Hermaia.
            ˮ
            ˮ     e.g. :
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
            ˮ
            ˮ     NB : the "analyse string" follows here a specifical format, used
            ˮ          by the GmastixMorpho project. Other formats are welcome !
            ___________________________________________________________________

            PARAMETERS :

            ▪ form         : (str)
            ▪ sourceword   : (str)
            ▪ inflection   : (str)
            ▪ context      : (str)

                E.g. form:              "are"
                     sourceword:        "be"
                     inflection:        34
                     analyse:           "tense=present;number=plural;person=1

            no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.add_to_dumpfile() " \
                     "form='%s' sourceword='%s' inflection='%s' context='%s'",
                     form, sourceword, inflection, context)

        #-----------------------------------------------------------------------
        # is there an available dump file ?
        if self.dumpfile is None:
            msg = "No dumpfile specified"
            raise HermaiaError(context="Hermaia.add_to_dumpfile()",
                               message=msg)

        #-----------------------------------------------------------------------
        # adding the values :
        string = "{2}{0}{3}{0}{4}{0}{5}{1}"
        self.dumpfile.write(string.format(Hermaia.separator_in_dumpfile,
                                          Hermaia.carriage_return_in_dumpfile,
                                          form,
                                          sourceword,
                                          inflection,
                                          context))

    #///////////////////////////////////////////////////////////////////////////
    def dumpfile__add_version(self,
                              versionnumber):
        """
            Hermaia.dumpfile__add_version()
            ___________________________________________________________________

            Write versionnumber into the dumpfile.

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
            ˮ         DDD : (str) the analyse string. This string has no format.
            ˮ                     For an example of one possible format, see
            ˮ                     the GmastixMorpho project which uses Hermaia.
            ˮ
            ˮ     e.g. :
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
            ˮ
            ˮ     NB : the "analyse string" follows here a specifical format, used
            ˮ          by the GmastixMorpho project. Other formats are welcome !
            ___________________________________________________________________

            PARAMETER :
            ▪ versionnumber : (int)

            no RETURNED VALUE
        """
        self.dumpfile.write("version number={0}\n".format(versionnumber))

    #///////////////////////////////////////////////////////////////////////////
    def dumpfile__write_from_db(self):
        """
            Hermaia.dumpfile__write_from_db()
            ___________________________________________________________________

            Write the entire database into the dumpfile.

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
            ˮ         DDD : (str) the analyse string. This string has no format.
            ˮ                     For an example of one possible format, see
            ˮ                     the GmastixMorpho project which uses Hermaia.
            ˮ
            ˮ     e.g. :
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "aime□aimer□verb/first group□tense=present;number=sg;person=1"
            ˮ     "a_aimé□aimer□verb/first group□tense=passé composé;number=sg;person=3"
            ˮ
            ˮ     NB : the "analyse string" follows here a specifical format, used
            ˮ          by the GmastixMorpho project. Other formats are welcome !

            ✓ unittests : see the HermaiaTests.test__write_from_db() method.
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.dumpfile__write_from_db()")

        #-----------------------------------------------------------------------
        # is there an available dump file ?
        if self.dumpfile is None:
            msg = "No dumpfile specified"
            raise HermaiaError(context="Hermaia.write_to_dumpfile()",
                               message=msg)

        #-----------------------------------------------------------------------
        # is there a database cursor ?
        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.write_to_dumpfile()",
                               message=msg)

        #-----------------------------------------------------------------------
        # writing the database into the dumpfile :
        versionnumber, _ = self.get_versionnumber_and_timestamp()
        self.dumpfile__add_version(versionnumber)

        sql_order = "SELECT form, sourceword, inflection_id, context " \
                    "FROM forms "
        self.database_cursor.execute(sql_order)

        for form, sourceword, inflection_id, context in self.database_cursor.fetchall():

            inflection = self.get_inflection_name(inflection_id)

            self.dumpfile__add_data(form=form,
                                    sourceword=sourceword,
                                    inflection=inflection,
                                    context=context)

    #///////////////////////////////////////////////////////////////////////////
    def enter(self):
        """
            Hermaia.enter()
            ___________________________________________________________________

            First function to be called (after __init__())

            This function is called AFTER self.__init__() .
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.enter()")

        # if there's an available database :
        if self.database is not None:

            # cursor used by <self> to read/write into the database :
            self.database_cursor = self.database.cursor()

            # is the database empty (=without any table) ?
            if not self.do_the_tables_exist():
                # if the database is empty we add the tables :
                self.create_structure()

        else:
            LOGGER.error(context="Hermaia.enter()",
                         message="self.database=None !")

    #///////////////////////////////////////////////////////////////////////////
    def exit(self):
        """
            Hermaia.exit()
            ___________________________________________________________________

            Last function called before shutting down <self>.
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.exit()")

        #-----------------------------------------------------------------------
        # oprations not yet commited ?
        if self.nbr_of_uncommited_operations > 0:
            self.nbr_of_uncommited_operations = 0
            self.database.commit()

    #///////////////////////////////////////////////////////////////////////////
    def get_inflection_id(self, inflection_name):
        """
            Hermaia.get_inflection_id()
            ___________________________________________________________________

            Return the inflection id stored in the database corresponding
            to <inflection_name>.

            ✓ unittests : see the HermaiaTests.test__get_inflection_id()
                          method.
            ___________________________________________________________________

            PARAMETER :
            ▪ inflection_name       : (str)

            RETURNED VALUE : None (nothing was found) or an integer
        """
        LOGGER.debug("Hermaia.get_inflection_id() : inflection_name='%s'", inflection_name)

        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.get_inflection_id()",
                               message=msg)

        sql_order = "SELECT numid " \
                    "FROM inflections " \
                    "WHERE name=?"
        self.database_cursor.execute(sql_order, (inflection_name,))

        res = self.database_cursor.fetchone()

        if res is None:
            return None
        else:
            return res[0]

    #///////////////////////////////////////////////////////////////////////////
    def get_inflection_name(self, inflection_id):
        """
            Hermaia.get_inflection_name()
            ___________________________________________________________________

            Return the inflection name stored in the database corresponding
            to <inflection_id>.

            ✓ unittests : see the HermaiaTests.test__get_inflection_name()
                          method.
            ___________________________________________________________________

            PARAMETER :
            ▪ inflection_id         : (integer)

            RETURNED VALUE : None (nothing was found) or a string
        """
        LOGGER.debug("Hermaia.get_inflection_name() : inflection_id='%s'", inflection_id)

        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.get_inflection_name()",
                               message=msg)

        sql_order = "SELECT name " \
                    "FROM inflections " \
                    "WHERE numid=?"
        self.database_cursor.execute(sql_order, (inflection_id,))

        res = self.database_cursor.fetchone()

        if res is None:
            return None
        else:
            return res[0]

    #///////////////////////////////////////////////////////////////////////////
    def get_versionnumber_and_timestamp(self):
        """
            Hermaia.get_versionnumber_and_timestamp()
            ___________________________________________________________________

            Return the database version number and the database timestamp.
            ___________________________________________________________________

            no PARAMETER.

            RETURNED VALUE : ((int) version number, (int)timestamp))
        """
        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.get_versionnumber_and_timestamp()",
                               message=msg)

        try:
            sql_order = "SELECT versionnumber, timestamp " \
                        "FROM metadata"
            self.database_cursor.execute(sql_order)

            db_res = self.database_cursor.fetchall()[0]

            return db_res[0], db_res[1]

        except IndexError as exception:
            message = "can't read versionnumber and timestamp in the database;\n" \
                      "Python message: "+str(exception)
            raise HermaiaError(context="Hermaia.get_versionnumber_and_timestamp()",
                               message=message)

    #///////////////////////////////////////////////////////////////////////////
    def infos(self, full_details=True):
        """
            Hermaia.infos()
            ___________________________________________________________________

            return informations about self : version number and timestamp,
            and (if full_details is set to True) statistics about the content
            of the database.
            ___________________________________________________________________

            ARGUMENT:
            ▪ full_details      : (bool) if True, the database will be read
                                  entirely.

            RETURNED VALUE : the expected string
        """
        res = []
        versionnumber, timestamp = self.get_versionnumber_and_timestamp()

        # version number, timestamp :
        res.append("o versionnumber={0}\n" \
                   "o timestamp={1}({2})".format(versionnumber,
                                                 timestamp,
                                                 datetime.datetime.fromtimestamp(timestamp)))

        # data :
        if full_details:
            id2name = dict()

            sql_order = "SELECT numid, name " \
                        "FROM inflections "
            self.database_cursor.execute(sql_order)
            for numid, name in self.database_cursor.fetchall():
                if name not in id2name:
                    id2name[numid] = name

            sql_order = "SELECT inflection_id, form " \
                        "FROM forms"
            self.database_cursor.execute(sql_order)
            inflections_number = dict()
            forms_number = 0
            for inflection_id, _ in self.database_cursor.fetchall():
                if id2name[inflection_id] not in inflections_number:
                    inflections_number[id2name[inflection_id]] = 0
                inflections_number[id2name[inflection_id]] += 1
                forms_number += 1

            res.append("o inflections :")
            for inflection in inflections_number:
                res.append("  - '{0}' : {1}".format(inflection, inflections_number[inflection]))

            res.append("o {0} word(s) in the database".format(forms_number))

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_dumpfile(self):
        """
            Hermaia.init_from_dumpfile()
            ___________________________________________________________________

            Read the data from the dumpfile and write them into the database.

            ✓ unittests : see the HermaiaTests.test__init_from_dumpfile*()
                          methods.
            ___________________________________________________________________

            no ARGUMENT, no RETURNED VALUE
        """
        LOGGER.debug("Hermaia.init_from_dumpfile()")

        #-----------------------------------------------------------------------
        # is there an available dump file ?
        if self.dumpfile is None:
            msg = "No dumpfile specified"
            raise HermaiaError(context="Hermaia.init_from_dumpfile()",
                               message=msg)

        #-----------------------------------------------------------------------
        # is there an available database ?
        if self.database is None:
            msg = "No database specified"
            raise HermaiaError(context="Hermaia.init_from_dumpfile()",
                               message=msg)

        #-----------------------------------------------------------------------
        # let's clear all content in the database :
        sql_order = "DELETE FROM metadata"
        self.database_cursor.execute(sql_order)

        sql_order = "DELETE FROM forms"
        self.database_cursor.execute(sql_order)

        sql_order = "DELETE FROM inflections"
        self.database_cursor.execute(sql_order)

        #-----------------------------------------------------------------------
        # reading the data :
        timestamp = utilities.get_current_timestamp()
        versionnumber = 0       # default value, to be initialized. See below.

        try:
            for _line in self.dumpfile:

                if len(_line.strip()) == 0 or _line.startswith("###"):
                    # empty line or a commentary
                    pass

                elif _line.startswith("version number"):
                    versionnumber = int(_line.split("=")[1])

                else:
                    # we remove the carriage return symbol(s) :
                    line = _line[:-len(Hermaia.carriage_return_in_dumpfile)]

                    try:
                        # we split the <line> into the expected values :
                        (form,
                         sourceword,
                         inflection,
                         context) = line.split(Hermaia.separator_in_dumpfile)
                    except ValueError as exception:
                        msg = "Can't read the dump file;\n" \
                              "Line to be read={0}\n" \
                              "Python error='{1}'".format(_line, exception)
                        raise HermaiaError(context="Hermaia.init_from_dumpfile()",
                                           message=msg)

                    # we add the values into the database :
                    self.add_data(form=form,
                                  sourceword=sourceword,
                                  inflection=inflection,
                                  context=context)

        except ValueError as exception:
            msg = "Can't read the dump file; python error='{0}'".format(exception)
            raise HermaiaError(context="Hermaia.init_from_dumpfile()",
                               message=msg)

        # let's write the version number and the timestamp into the database :
        self.write_versionnumber_and_tstamp(versionnumber, timestamp)

    #///////////////////////////////////////////////////////////////////////////
    def search(self, searched_form, minimal_accuracy=1):
        """
            Hermaia.search()
            ___________________________________________________________________

              Search the <searched_form> in the database. Return a list of the
            matching values placed into a dictionary. The list is
            empty if no result could be found.

            ✓ unittests : see the HermaiaTests.test__search*()
                          methods.
            ___________________________________________________________________

            PARAMETER :
            ▪ searched_form     : (str)
            ▪ minimal_accuracy  : (float) minimal accuracy returned by
                                  textdiff_distance()
                                  minimal_accuracy ∈ [0;1]

            RETURNED VALUE : a list of dicts (an empty list if there's no
                             result). The results are sorted by 'accuracy',
                             the first result being the most interesting.

                E.g. ( {'sourceword' : "are",
                        'inflection' : "verb",
                        'context'    : "tense=present;number=plural;person=3",
                        'accuracy'   : (float) ∈ [0;1]},
                     )
        """
        LOGGER.debug("Hermaia.search() : search='%s'", searched_form)

        #-----------------------------------------------------------------------
        # is there an available database ?
        if self.database is None:
            msg = "No database specified"
            raise HermaiaError(context="Hermaia.search()",
                               message=msg)

        #-----------------------------------------------------------------------
        # let's look into the database :
        if minimal_accuracy == 1:
            # fast search : we don't have to test the entire database.

            sql_order = "SELECT sourceword, inflection_id, context " \
                        "FROM forms " \
                        "WHERE form=?"
            self.database_cursor.execute(sql_order, (searched_form,))

            res = []
            for sourceword, inflection_id, context in self.database_cursor.fetchall():

                inflection = self.get_inflection_name(inflection_id)
                res.append({'sourceword'  : sourceword,
                            'inflection'  : inflection,
                            'context'     : context,
                            'accuracy'    : 1})

        else:
            # slow search : we have to test the entire database.

            sql_order = "SELECT form, sourceword, inflection_id, context " \
                        "FROM forms"
            self.database_cursor.execute(sql_order)

            res = []
            for form, sourceword, inflection_id, context in self.database_cursor.fetchall():

                accuracy = utilities.textdiff_distance(searched_form, form)
                if accuracy >= minimal_accuracy:
                    inflection = self.get_inflection_name(inflection_id)
                    res.append({'sourceword'  : sourceword,
                                'inflection'  : inflection,
                                'context'     : context,
                                'accuracy'    : accuracy})

            # let's sort the result :
            res = sorted(res,
                         key=lambda res: res["accuracy"])[::-1]

        return res

    #///////////////////////////////////////////////////////////////////////////
    def write_versionnumber_and_tstamp(self, versionnumber, timestamp=None):
        """
            Hermaia.write_versionnumber_and_tstamp()
            ___________________________________________________________________

            Write into the database its version number and its timestamp.
            ___________________________________________________________________

            ARGUMENTS :
            ▪ versionnumber     : (int)
            ▪ timestamp         : int or None to get the current timestamp.

            no RETURNED VALUE
        """
        LOGGER.debug("write_versionnumber_and_tstamp : versionnumber=%s; timestamp=%s",
                     versionnumber, timestamp)

        #-----------------------------------------------------------------------
        # is there a database cursor ?
        if self.database_cursor is None:
            msg = "no database cursor"
            raise HermaiaError(context="Hermaia.write_versionnumber_and_tstamp()",
                               message=msg)

        if timestamp is None:
            timestamp = utilities.get_current_timestamp()

        sql_order = "DELETE FROM metadata"
        self.database_cursor.execute(sql_order)

        sql_order = "INSERT INTO metadata VALUES (?, ?)"
        self.database_cursor.execute(sql_order,
                                     (versionnumber, timestamp,))
        self.commit()
