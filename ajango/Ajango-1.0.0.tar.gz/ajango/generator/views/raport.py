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
Obiekt generujacy raport.

Obiekt generuje strone raportu.

Dostepne znaczniki
==================

    1. B{QUERY} - Zapytanie o dane. L{wiecej <ajango.database.query>}.
    2. B{COLUMN} - Kolumna z danymi L{wiecej <ajango.database.columns>}.
    3. B{TEMPLATE} - Ustatienie pliku I{HTML} z szablonem widoku raportu.
        - I{src} - nazwa pliku.
    4. B{LIST} - Ustawienie trybu listy
        - I{value} - I{True} jesli tryb listy ma byc wlaczony lub I{False} wpw.

Generowany obiekt
=================

L{ajango.site.sites.raport}
"""

from django.core.management.base    import CommandError
from ajango.generator.views.list import View as List

class View(List):
    """ Klasa widoku wyswietlajacego raport. """
    def __init__(self, xmldoc, importRenderer, app):
        self.add_permited(["TEMPLATE", "LIST"])
        self.template_src = ""
        self.list_mode = False
        List.__init__(self, xmldoc, importRenderer, app)
    def init(self):
        """ Metoda inicjalizujaca. """
        List.init(self)
        self.type = "raport"
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if List.check(self, name, xmldoc_elem):
            return True
        if name.upper() == "TEMPLATE":
            self.template_src = xmldoc_elem.getAttribute("src")
            return True
        if name.upper() == "LIST":
            value = xmldoc_elem.getAttribute("value")
            if value.upper() == "FALSE":
                self.list_mode = False
            elif value.upper() == "TRUE":
                self.list_mode = True
            else:
                raise CommandError("List node cannot have %r value" % value)
            return True
        return False
    def execute(self, view, view_name="view"):
        """ Wykonanie zadan obiektu. """
        self.add_line("%s.set_template(%r)" % (view_name, self.template_src))
        value = "False"
        if self.list_mode:
            value = "True"
        self.add_line("%s.set_list_mode(%s)" % (view_name, value))
        List.execute(self, view, view_name)
    def is_display_in_menu(self):
        """ Informacja na temat widocznosci w menu glownym aplikacji. """
        return self.list_mode
