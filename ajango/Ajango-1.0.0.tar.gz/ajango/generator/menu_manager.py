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
Modul zarzadzajacy menu.

Pozwala na automatyczne stworzenie menu z uzytych w aplikacji widokach.
Poszczegolne pozycje dostepne sa w menu pod warunkiem ze typ widoku nalezy
do jednego z wybranych typow.

    - L{empty<ajango.generator.views.empty>}.
    - L{list<ajango.generator.views.list>}.
    - L{editable<ajango.generator.views.editable>}.
    - L{input<ajango.generator.views.input>}.
    - L{container<ajango.generator.views.container>}.
"""

from ajango.generator.renderer import DefRenderer

def is_display_in_menu(view):
    """ Sprawdza czy widok ma byc pokazywany w menu. """
    display_type = ['empty', 'list', 'input', 'container']
    for elem in display_type:
        if view.type == elem:
            return True
    return view.is_display_in_menu()

class MenuManager(object):
    """ Manager budujacy menu. """
    def __init__(self, view_manager, importRenderer):
        self.view_manager = view_manager
        self.renderer = {'renderer' : DefRenderer('default_menu'),
                         'import' : importRenderer}
        self.views = []
        self.app_name = ""
    def set_app_name(self, app_name):
        """ Ustawienie nazwy menu. """
        self.app_name = app_name
    def add_view(self, view):
        """ Dodanie widoku do menu. """
        self.views.append(view)
    def execute(self, app_name):
        """ Wykonanie zadan obiektu. """
        rend = self.renderer['renderer']
        self.renderer['import'].add_import("SiteMenu", "ajango.site.site_menu")
        rend.add_line("menu = SiteMenu(%r)" % app_name)
        for elem in self.views:
            if is_display_in_menu(elem):
                rend.add_line("menu.add_view(%r, %r)" %
                              (elem.get_name(), elem.get_title()))
        rend.add_line("return menu.get_tab()")
    def get_renderer(self, ob_type):
        """ Pobierz obiekt renderera. """
        return self.renderer[ob_type]
