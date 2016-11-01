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
Modul generujacy kod tworzonej aplikacji.

Opis pliku szkieletowego
========================

Modul analizuje skrypt szkieletu i generuje na jego podstawie aplikacje zgodne
z frameworkiem Django. Przykladowy plik XML moze wygladac nastepujaco::

    <ajango>
        <application name="myfirstapp">
            <view type="empty" id="nowa">
                <echo> Ta strona nie jest jeszcze gotowa</echo>
            </view>
        </application>
    </ajango>

Poprawnie sformatowany plik sklada sie noda glownego o nazwie B{AJANGO}.
Wewnatrz niego nalezy zdefinowac odpowiednie aplikacje (node B{APPLICATION}),
ktore skladaja sie z widokow (node B{VIEW}). Poszczegolne widoki definiowane
sa niezaleznie a ich struktura zalezna jest od typu.

Dostepne widoki
===============

System pozwala na wygenerowanie nastepujacych
L{widokow<ajango.generator.views>}.

    - L{widok pusty <ajango.generator.views.empty>}
    - L{widok wprowadzania danych <ajango.generator.views.input>}
    - L{widok wyswietlania danych <ajango.generator.views.display>}
    - L{widok listy <ajango.generator.views.list>}
    - L{widok edycji danych <ajango.generator.views.editable>} (niedostepne)
    - L{widok raportu <ajango.generator.views.raport>}
    - L{agregacja widoku <ajango.generator.views.container>}
"""

from __future__                       import print_function
from django.core.management.base      import CommandError
from ajango.generator.project_manager import ProjectManager
from ajango.generator.application     import Application
from ajango.generator.config_global   import ConfigGlobal
from xml.dom                          import minidom
import os.path

class AjangoGenerator(object):
    """ Obiekt generujacy aplikacje na podstawie pliku szkieletowego. """
    def __init__(self, project_name, skeleton_file):
        self.project = ProjectManager(project_name)
        ConfigGlobal().set('project_manager', self.project)
        self.options = None
        self.apps = []
        self.main_app = None
        self.render(skeleton_file)
    def set_options(self, options):
        """ Ustawienie opcji dla obiektu. """
        self.options = options
    def render(self, skeleton_file):
        """ Budowanie zestawu obiektow dla pliku XML. """
        if not os.path.isfile(skeleton_file):
            raise CommandError(
                "%r: File doesn't exist" % skeleton_file
            )
        print("Render: "+ skeleton_file)
        xmldoc_main = minidom.parse(skeleton_file)
        xmldoc = xmldoc_main.childNodes[0]
        if xmldoc.tagName.upper() != 'AJANGO':
            raise CommandError("This Ajango skeleton is not Valid")
        for elem in xmldoc.childNodes:
            if isinstance(elem, minidom.Element):
                # Renderowanie aplikacji
                if elem.tagName.upper() == 'APPLICATION':
                    app = Application(elem)
                    for once in self.apps:
                        # Sprawdzanie czy aplikacje sie nie powtarzaja
                        if app.get_name() == once.get_name():
                            raise CommandError("There are two or more "
                                               "application named: %r" %
                                               app.get_name())
                    if app.getAttribute("main").lower() == "main":
                        # Sprawdzanie czy aplikacja nie jest glowna
                        if self.main_app != None:
                            raise CommandError("There are two or more "
                                               "application signed as 'main'")
                        self.main_app = app
                    self.apps.append(app)
                    self.project.add_main_view_url(app)
                else:
                    raise CommandError("Unknown tag name: %r " % elem.tagName)
        if self.main_app == None:
            # Jesli brak glownej aplikacji to pierwsza jest glowna.
            self.main_app = self.apps[0]
        self.project.add_main_url(self.main_app)
    def make_apps(self):
        """ Stworzenie wszystkich aplikacji. """
        for app in self.apps:
            if self.options != None:
                app.set_options(self.options)
            app.make_new()
            print("Building app: " + app.get_name())
            app.execution()
        project = ConfigGlobal().get('project_manager')
        project.execute()
