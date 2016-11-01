###########################################################################
#                                                                         #
#  Copyright (C) 2016  Rafal Kobel <rafyco1@gmail.com>                    #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################
""" Modul parsowania xml. """

from __future__                   import print_function
from xml.dom                      import minidom
from django.core.management.base  import CommandError
from django.utils.termcolors      import make_style
from django.core.management.color import supports_color
import abc

class XMLReader(object):
    """ Klasa obiektu parsowania XML. """
    __metaclass__ = abc.ABCMeta
    def __init__(self, xmldoc, param=None):
        self.xml_xmldoc = xmldoc
        self.add_permited([])
        self.xml_name = ""
        self.object = param
        self.init()
        self.render()
        self.xml_permited = []
    def init(self):
        """ Modul inicjalizujacy. """
        pass
    def add_permited(self, permited):
        """ Dodanie tagow ktore moga byc parsowane wewnatrz elementu. """
        try:
            self.xml_permited += permited
        except AttributeError:
            self.xml_permited = permited
    def get_xml_doc(self):
        """ Pobranie xmldoc. """
        return self.xml_xmldoc
    # pylint: disable=C0103
    def getAttribute(self, name):
        """ Pobranie atrybutu dla noda. """
        return self.xml_xmldoc.getAttribute(name)
    def _is_permited(self, name):
        """ Sprawdzenie czy element moze byc parsowany. """
        if self.xml_permited == []:
            return True
        for elem in self.xml_permited:
            if elem.upper() == name.upper():
                return True
        return False
    def pre_render(self):
        """ Czynnosci do wykonania przez inicjalizacja. """
        pass
    def post_render(self):
        """ Czynnosci do wykonania po inicjalizacji. """
        pass
    def render(self):
        """ Renderowanie elementow. """
        if supports_color():
            yellow = make_style(fg='yellow')
        else:
            yellow = lambda text: text
        print("Rendering '" + yellow(self.xml_xmldoc.tagName.upper()) + "'")
        if (self.xml_name != "") and (self.xml_name.upper() !=
                                      self.get_xml_doc().tagName.upper()):
            raise CommandError("Cannot create object from %r" %
                               self.get_xml_doc().tagName)
        self.pre_render()
        for elem in self.get_xml_doc().childNodes:
            if isinstance(elem, minidom.Element):
                if self._is_permited(elem.tagName):
                    self.check(elem.tagName.upper(), elem)
                else:
                    raise CommandError("Unknown element: %r" % elem.tagName)
        self.post_render()
    @abc.abstractmethod
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        raise CommandError("XMLReader must have check method")
