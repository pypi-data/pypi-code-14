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
""" Modul generujacy kontener stron.

Obiekt pozwala na wyswietlenie kilku widokow jednoczenie na jednej stronie.

Obiekt Generujacy
=================

L{ajango.generator.views.container}
"""


from ajango.site.sites           import SiteBase
from ajango.generator.views      import ViewBase

class Site(SiteBase):
    """ Klasa agregujaca strony. """
    def __init__(self, obj):
        self.views = []
        self.container_layout = ""
        SiteBase.__init__(self, obj)
    def init(self):
        """ Inicjalizacja obiektu. """
        self.type = "container"
    def set_container_layout(self, layout):
        """
        Ustawienie layoutu kontenera.

        @param self: Instancja obiektu strony.
        @param layout: Sposob wyswietlania strony I{horizontal} lub I{vertical}
        """
        if layout != 'horizontal' and layout != 'vertical':
            raise ValueError("there are unknown layout %r" % layout)
        self.container_layout = layout
    def add_view(self, view):
        """ Dodanie widoku do wyswietlenia w kontenerze. """
        if isinstance(view, ViewBase):
            raise ValueError("view argument must be ViewBase type.")
        self.views.append(view)
    def content(self):
        """ Wykonanie zadan obiektu. """
        self.data['layout'] = self.container_layout
        views_tab_data = []
        for view in self.views:
            views_tab_data.append(view.make_content_and_get_data())
        self.data['views'] = views_tab_data
