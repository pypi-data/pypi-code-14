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
Obiekt generujacy strone typu 'input'.

Obiekt generuje kod obsugujacy strone agregujaca widoki.

Dostepne znaczniki
==================

    1. B{TABLE} - Tabela do ktorej nalezy wstawic dane.
        - I{name} - Nazwa tabeli.
    2. B{INPUT} - Element przyjmujacy dane L{wiecej <ajango.database.inputs>}.

Generowany obiekt
=================

L{ajango.site.sites.input}
"""

from django.core.management.base import CommandError
from ajango.generator.views import ViewBase
from ajango.database.inputs import input_factory

class View(ViewBase):
    """ Klasa generujaca widok wprowadzania danych. """
    def __init__(self, xmldoc, importRenderer, app):
        self.table = ""
        self.inputs = []
        ViewBase.__init__(self, xmldoc, importRenderer, app)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = "input"
        self.add_permited(["TABLE", "INPUT"])
    def post_init(self):
        """ Czynnosci do wykonania po inicjalizacji. """
        if self.table == "":
            raise CommandError("Table name isn't define")
        if len(self.inputs) == 0:
            raise CommandError("Don't define any input object")
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if super(View, self).check(name, xmldoc_elem):
            return True
        if name.upper() == "TABLE":
            self.table = xmldoc_elem.getAttribute("name")
            return True
        if name.upper() == "INPUT":
            self.inputs.append(input_factory(xmldoc_elem))
            return True
        return False
    def execute(self, view, view_name='view'):
        """ Wykonanie zadan obiektu. """
        self.add_import("models", ".")
        self.add_line("%s.set_models(models)" % view_name)
        self.add_line("%s.set_table_name(%r)" % (view_name, self.table))
        for elem in self.inputs:
            elem.execute(self, view_name)
