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
Obiekt generujacy kontener stron.

Obiekt generuje kod obsugujacy strone agregujaca widoki.

Dostepne znaczniki
==================

    1. B{LAYOUT} - Opcja okreslajaca sposob agregacji stron.
        - I{name} - Przyjmuje wartosc I{horizontal} lub I{vertical} (domyslnie).
    2. B{VIEW} - widok agregujacy L{wiecej <ajango.generator.views>}.

Generowany obiekt
=================

L{ajango.site.sites.container}
"""

from ajango.generator.views        import ViewBase
from ajango.generator.views        import view_factory
from ajango.generator.config_global import ConfigGlobal

class View(ViewBase):
    """ Klasa widoku kontenerowego. """
    def __init__(self, xmldoc, importRenderer, app):
        self.views = []
        self.layout = "vertical"
        ViewBase.__init__(self, xmldoc, importRenderer, app)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.type = "container"
        self.add_permited(["VIEW", "LAYOUT"])
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if ViewBase.check(self, name, xmldoc_elem):
            return True
        if name.upper() == "LAYOUT":
            self.layout = xmldoc_elem.getAttribute('name')
            if self.layout != 'horizontal' and self.layout != 'vertical':
                raise ValueError("there are unknown layout %r" %
                                 self.layout)
            return True
        if name.upper() == "VIEW":
            view = view_factory({'xmldoc' : xmldoc_elem,
                                 'imp_renderer' : self.renderer,
                                 'app' : self.app})
            self.views.append(view)
            return True
        return False
    def execute(self, view, view_name="view"):
        """ Budowanie kodu i wypelnianie renderera."""
        for elem in self.views:
            id_elem = ConfigGlobal().get('view_id_counter')
            ConfigGlobal().set('view_id_counter', id_elem + 1)
            elem.make_view_execute("view_%d" % id_elem)
            self.add_line("%s.add_view(view_%d)" % (view_name, id_elem))
        self.add_line("%s.set_container_layout(%r)" % (view_name, self.layout))
