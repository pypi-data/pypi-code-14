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
    ❏DChars❏ : dchars/dcharacter.py
"""

################################################################################
class DCharacterMotherClass(object):
    """
        class DCharacterMotherClass, motherclass for all DCharacter* classes
    """

    #///////////////////////////////////////////////////////////////////////////
    def __ge__(self, aliud):
        """
                DCharacterMotherClass.__ge__

                aliud   :       DCharacterLAT object
        """
        # Pylint can't know that <self> has a 'sortingvalue' member
        # created by the derived class (e.g. : DCharacterGRC)
        # pylint: disable=E1101
        # -> Instance of 'DCharacterMotherClass' has no 'sortingvalue' member
        return (self.sortingvalue() > aliud.sortingvalue()) or (self == aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __gt__(self, aliud):
        """
                DCharacterMotherClass.__gt__

                aliud   :       DCharacterLAT object
        """
        # Pylint can't know that <self> has a 'sortingvalue' member
        # created by the derived class (e.g. : DCharacterGRC)
        # pylint: disable=E1101
        # -> Instance of 'DCharacterMotherClass' has no 'sortingvalue' member
        return self.sortingvalue() > aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self,
                 dstring_object,
                 unknown_char,
                 base_char,
                 punctuation):
        """
                DCharacterMotherClass.__init__

                dstring_object  : DString* object
                unknown_char    : bool
                base_char       : str
                punctuation     : bool
        """
        self.dstring_object = dstring_object
        self.unknown_char = unknown_char
        self.base_char = base_char
        self.punctuation = punctuation

    #///////////////////////////////////////////////////////////////////////////
    def __le__(self, aliud):
        """
                DCharacterMotherClass.__le__

                aliud   :       DCharacterLAT object
        """
        # Pylint can't know that <self> has a 'sortingvalue' member
        # created by the derived class (e.g. : DCharacterGRC)
        # pylint: disable=E1101
        # -> Instance of 'DCharacterMotherClass' has no 'sortingvalue' member
        return (self.sortingvalue() < aliud.sortingvalue()) or (self == aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __lt__(self, aliud):
        """
                DCharacterMotherClass.__lt__

                aliud   :       DCharacterLAT object
        """
        # Pylint can't know that <self> has a 'sortingvalue' member
        # created by the derived class (e.g. : DCharacterGRC)
        # pylint: disable=E1101
        # -> Instance of 'DCharacterMotherClass' has no 'sortingvalue' member
        return self.sortingvalue() < aliud.sortingvalue()

    #///////////////////////////////////////////////////////////////////////////
    def __ne__(self, aliud):
        """
                DCharacterMotherClass.__ne__

                aliud   :       DCharacterLAT object
        """
        # Pylint can't know that <self> has an '__eq__' member
        # created by the derived class (e.g. : DCharacterGRC)
        # pylint: disable=E1101
        # -> Instance of 'DCharacterMotherClass' has no 'sortingvalue' member
        return not self.__eq__(aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __str__(self):
        """
                DCharacterMotherClass.__str__
        """
        return self.get_sourcestr_representation()

    #///////////////////////////////////////////////////////////////////////////
    def clone(self):
        """
                DCharacterMotherClass.clone
        """
        return DCharacterMotherClass( dstring_object = self.dstring_object,
                                      unknown_char  = self.unknown_char,
                                      base_char = self.base_char,
                                      punctuation = self.punctuation )

    #///////////////////////////////////////////////////////////////////////////
    def get_sourcestr_representation(self):
        """
                DCharacterMotherClass.get_sourcestr_representation

                This function should be overloaded
        """
        return "unknown_char={0}; base_char={1}; punctuation={2};".format(self.unknown_char,
                                                                          self.base_char,
                                                                          self.punctuation)

    #///////////////////////////////////////////////////////////////////////////
    def reset(self):
        """
                DCharacterMotherClass.reset

                This function should be overloaded
        """
        self.dstring_object = None
        self.unknown_char = False
        self.base_char = None
        self.punctuation = False

    #///////////////////////////////////////////////////////////////////////////
    def set_to_its_most_visual_form(self):
        """
                DCharacterMotherClass.set_to_its_most_visual_form

                Modify <self> in place and change it to "most simple" representation.

                This function should be overloaded

                Function used by the Logotheras project.
        """
        pass

