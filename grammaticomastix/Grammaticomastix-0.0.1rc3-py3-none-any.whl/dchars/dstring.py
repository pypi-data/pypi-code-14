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
    ❏DChars❏ : dchars/dstring.py
"""

# problem with Pylint :
# pylint: disable=E0611
# "No name 'errors' in module 'dchars.dchars'"
from dchars.errors.errors import DCharsError
import io
import copy

################################################################################
class DStringMotherClass(list):
    """
        class DStringMotherClass, motherclass for all DString* classes

		the three following attributes are created by the call to dchars.py::new_dstring() :

        self.iso639_3_name             : (str)
        self.transliteration_method    : (str)
        self.options                   : (dict)
    """

    #///////////////////////////////////////////////////////////////////////////
    def __add__(self, aliud):
        """
                DStringMotherClass.__add__
        """
        res = self.clone()

        for dchar in aliud:
            res.append( dchar.clone() )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def __enter__(self):
        """
                DStringMotherClass.__enter__
        """
        return self

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                DStringMotherClass.__eq__

                aliud   :       DString* object
        """

        if len(aliud) != len(self):
            return False

        res = True

        for index, dchar in enumerate(self):
            if dchar != aliud[index]:
                res = False
                break

        return res

    #///////////////////////////////////////////////////////////////////////////
    def __exit__(self, typ, value, traceback):
        """
                DStringMotherClass.__exit__
        """
        if self.srcfile is None:
            raise DCharsError( context = "DStringMotherClass.read",
                               message = "no file attached to this object" )

        self.srcfile.close()

    #///////////////////////////////////////////////////////////////////////////
    def __ge__(self, aliud):
        """
                DStringMotherClass.__ge__
        """
        if self == aliud:
            return True

        return self.sortingvalue() > aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __getitem__(self, arg):
        """
                DStringMotherClass.__getitem__
        """
        # list.__getitem__(self, arg) return either a DCharacter object if <arg>
        # is an integer either a list object.
        if type(arg)==int:
            return list.__getitem__(self, arg)

        else:
            res = type(self)()
            for dchar in list.__getitem__(self, arg):
                res.append( copy.copy( dchar ))

        return res

    #///////////////////////////////////////////////////////////////////////////
    def __gt__(self, aliud):
        """
                DStringMotherClass.__gt__
        """
        return self.sortingvalue() > aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, iterable = None):
        """
                DStringMotherClass.__init__
        """
        if iterable is not None:
            list.__init__(self, iterable)

        self.srcfile = None

    #///////////////////////////////////////////////////////////////////////////
    def __le__(self, aliud):
        """
                DStringMotherClass.__le__
        """
        if self == aliud:
            return True

        return self.sortingvalue() < aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __lt__(self, aliud):
        """
                DStringMotherClass.__lt__
        """
        return self.sortingvalue() < aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __ne__(self, aliud):
        """
                DStringMotherClass.__ne__
        """
        return not self.__eq__(aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                DStringMotherClass.__repr__
        """
        res = []

        # pylint: disable=E1101
        # We disable this error in order to avoid the message :
        # "Instance of 'DStringMotherClass' has no 'iso639_3_name' member"
        #
        # Since DString* classes are created by dchars.py::new_dstring,
        # we're sure that this members exist.
        res.append("(DStringMotherClass : '{0}'/'{1}'/{2}; {3} character(s))".format(
            self.iso639_3_name,
            self.transliteration_method,
            self.options,
            len(self),
            ))

        for index_dchar, dchar in enumerate(self):
            res.append( "#("+str(index_dchar)+")"+repr(dchar) )

        return "\n".join( string for string in res )

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                DStringMotherClass.__str__
        """
        return "".join( str(element) for element in self )

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DStringMotherClass.clone
        """
        res = type(self)()

        for dchar in self:
            res.append( dchar.clone() )

        return res

    #///////////////////////////////////////////////////////////////////////////
    def diff(self, aliud):
        """
                DStringMotherClass.diff

                debugging-oriented function.

                aliud   :       DString* object
        """
        res = []
        for index_dchar, dchar in enumerate(self):

            if len(aliud) <= index_dchar:
                res.append( "{0} : (1) / ~~".format(index_dchar)+" : "+str(dchar))
            elif self[index_dchar] == aliud[index_dchar]:
                res.append( "{0} : (1) == (2)".format(index_dchar)+" : "+str(dchar))
            else:
                res.append( "{0} : (1) != (2)".format(index_dchar) + "\n" +\
                             "(1)=="+repr(dchar) + "\n" +\
                             "(2)=="+repr(aliud[index_dchar]),)
                break

        return "\n".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def endswith(self, aliud):
        """
                DStringMotherClass.endswith

                Return True if <self> ends with <aliud>

                <aliud> is a DString*.
        """
        # A problem here :
        #
        #       This function should compare, one by one, all dcharacters in <self>
        # and in <aliud>. But DChars add some informations about the vowels that
        # can lead to confusion : e.g. "ཀོགས" (kogs) can be analysed as "kogsa" and
        # won't by analysed as ending with "ས" (s). To avoid this we compare the
        # string representation :
        return str(self).endswith( str(aliud) )

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DStringMotherClass.get_sourcestr_representation

                Return a string.
        """
        res = []

        for dchar in self:
            res.append( dchar.get_sourcestr_representation() )

        return "".join(res)

    #///////////////////////////////////////////////////////////////////////////
    def init_from_str(self, src):
        """
                DStringMotherClass.init_from_str

                This function should be overloaded.
        """
        pass

    #///////////////////////////////////////////////////////////////////////////
    def open(self,
             filename,
             mode='r',
             buffering=-1,
             encoding=None,
             errors=None,
             newline=None,
             closefd=True,
             opener=None):
        """
                DStringMotherClass.open

                wrapper around io.open in order to write something like :

                .. code-block:: python

                    import dchars.dchars as dchars
                    DSTRING_SAN = dchars.new_dstring(language='संस्कृतम्',
                                  transliteration_method="itrans")

                   with DSTRING_SAN().open("z", 'r').read() as src:
                        print(src.get_transliteration())

                   with DSTRING_SAN().open("z", 'r') as src:
                        for line in src.readlines():
                           print(line.get_transliteration())
        """

        # we call io.open() since a call to open() would call self.open()
        self.srcfile = io.open(file=filename,
                               mode=mode,
                               buffering=buffering,
                               encoding=encoding,
                               errors=errors,
                               newline=newline,
                               closefd=closefd,
                               opener=opener)

        if 'r' not in mode:
            raise DCharsError(context="DStringMotherClass.open",
                              message="open() can only work with the 'r' mode.")

        return self

    #///////////////////////////////////////////////////////////////////////////
    def percentage_of_unknown_characters(self):
        """
                DStringMotherClass.percentage_of_unknown_characters

                Return the ratio "number of unknown characters/length" or 0
                if the object is empty.
        """
        if len(self)==0:
            return 0

        return 100.0*len([unknown_char for unknown_char in self if unknown_char.unknown_char==True])/len(self)

    #///////////////////////////////////////////////////////////////////////////
    def read(self):
        """
                DStringMotherClass.read

                see DStringMotherClass.open for some code examples.
        """
        if self.srcfile is None:
            raise DCharsError( context = "DStringMotherClass.read",
                               message = "no file attached to this object" )

        self.init_from_str( self.srcfile.read() )

        return self

    #///////////////////////////////////////////////////////////////////////////
    def readlines(self):
        """
                DStringMotherClass.readline

                see DStringMotherClass.open for some code examples.
        """
        if self.srcfile is None:
            raise DCharsError( context = "DStringMotherClass.read",
                               message = "no file attached to this object" )

        for _line in self.srcfile.readlines():

            if _line[-2:] == '\r\n':
                line = _line[:-2]
            elif _line[-1:] == '\n':
                line = _line[:-1]
            elif _line[-1:] == '\r':
                line = _line[:-1]
            else:
                line = _line

            res = type(self)()
            res.init_from_str( line )
            yield res

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DStringMotherClass.set_to_its_most_visual_form

                Modify <self> in place and change each character into its
                "most simple" representation
        """
        for dchar in self:
            dchar.set_to_its_most_visual_form()

    #///////////////////////////////////////////////////////////////////////////
    def sortingvalue(self):
        """
                DStringMotherClass.sortingvalue

                This is a basic function which should be overloaded. For some
                languages (ex : grc) this way to compute a sorting value (by
                adding the sorting values of each character) is wrong.
        """
        return  [ dchar.sortingvalue() for dchar in self  ]

    #///////////////////////////////////////////////////////////////////////////
    def startswith(self, aliud):
        """
                DStringMotherClass.startswith

                Return True if <self> begins with <aliud>

                <aliud> is a DString*.
        """
        # see DStringMotherClass.startswith to understand this (strange) way
        # to compare the two strings.
        return str(self).startswith( str(aliud) )

