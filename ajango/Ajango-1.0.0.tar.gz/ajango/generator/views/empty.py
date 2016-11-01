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
"""
Obiekt generujacy strone typu 'empty'.

Obiekt generuje kod obsugujacy strone wyswietlajaca proste napisy.

Dostepne znaczniki
==================

    1. B{ECHO} - Tag okalajacy tekst do wyswietlenia.

Generowany obiekt
=================

L{ajango.site.sites.empty}
"""

from xml.dom                     import minidom
from django.core.management.base import CommandError
from ajango.generator.views      import ViewBase

class EchoElem(object):
    """ Klasa obiektu wyswietlajacego. """
    def __init__(self, text):
        self.text = text
    def set_text(self, text):
        """ Ustawienie tekstu do wyswietlenia. """
        self.text = text
    def render(self, view_name='view'):
        """ Renderowanie elementu. """
        return "%s.add_echo(%r)" % (view_name, self.text)

class View(ViewBase):
    """ Klasa widoku wyswietlajacego. """
    def __init__(self, xmldoc, importRenderer, app):
        self.code_elems = []
        ViewBase.__init__(self, xmldoc, importRenderer, app)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = "empty"
        self.add_permited(["ECHO"])
    def execute(self, view, view_name='view'):
        """ Wykonanie zadan obiektu. """
        for elem in self.code_elems:
            self.add_line(elem.render(view_name))
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if ViewBase.check(self, name, xmldoc_elem):
            return True
        if name.upper() == "ECHO":
            if isinstance(xmldoc_elem.childNodes[0], minidom.Text):
                self.code_elems.append(
                    EchoElem(xmldoc_elem.childNodes[0].toxml()))
                return True
            else:
                raise CommandError("This element in ECHO is not str")
        return False
