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
""" Modul zarzadzania aplikacjami. """

import os
import os.path
from django.core.management.base       import CommandError
from django.core.management.templates  import TemplateCommand
from ajango.generator.config_global    import ConfigGlobal
from ajango.generator.views            import view_factory
from ajango.core.XMLReader             import XMLReader
from ajango.database.data_base_manager import DataBaseManager
from ajango.generator.view_manager     import ViewManager
from ajango.generator.menu_manager     import MenuManager
from ajango.generator.renderer         import ImportRenderer

class Application(XMLReader):
    """ Klasa zarzadzajaca aplikacjami. """
    def __init__(self, xmldoc, param=None):
        self.views = []
        self.managers = {}
        self.main_view = None
        self.imp_renderer = ImportRenderer()
        self.options = None
        self.managers['view'] = ViewManager()
        self.managers['menu'] = MenuManager(self.managers['view'],
                                            self.imp_renderer)
        self.managers['database'] = DataBaseManager(self)
        self.options = None
        self.name = ""
        XMLReader.__init__(self, xmldoc, param)
    def init(self):
        """ Metoda inicjalizujaca. """
        self.xml_name = "APPLICATION"
        self.add_permited(["VIEW"])
        self.managers['view'].set_menu(self.managers['menu'])
    def set_options(self, options):
        """ Ustawienie opcji. """
        self.options = options
    def is_exist(self):
        """ Sprawdzenie czy aplikacja juz istanieje. """
        return os.path.isdir(self.get_name())
    # pylint: disable=W0142
    def make_new(self):
        """ Wykonanie nowej aplikacji. """
        template_command = TemplateCommand()
        options = self.options
        template_command.validate_name(self.get_name(), 'app')
        try:
            os.mkdir(self.get_name())
        except OSError:
            raise CommandError("Cannot create new application named %r." %
                               self.get_name())
        template_command.handle('app',
                                self.get_name(),
                                self.get_name(),
                                **options)
        project_manager = ConfigGlobal().get('project_manager')
        project_manager.add_application(self)
        self.managers['database'].build_data_base(options)
    def get_name(self):
        """ Pobranie nazwy. """
        return self.name
    def pre_render(self):
        """ Czynnosci przed inicjalizacja. """
        self.name = self.getAttribute('name').lower()
        if self.name == '':
            raise CommandError("Missing parametr name in application")
    def check(self, name, xmldoc_elem):
        """ Oczytanie nodow wewnetrznych. """
        if name == 'VIEW':
            new_view = view_factory({'xmldoc' : xmldoc_elem,
                                     'imp_renderer': self.imp_renderer,
                                     'app': self})
            for once in self.views:
                if once.get_name() == new_view.get_name():
                    raise CommandError("Id %r is use by two or "
                                       "more views in %r" %
                                       (str(once), str(self)))
            if new_view.getAttribute("main").lower() == "main":
                if self.main_view != None:
                    raise CommandError("There are two or more views"
                                       "sign as 'main' -> %r %r " %
                                       (new_view.get_name(),
                                        self.main_view.get_name()))
                self.main_view = new_view
            self.views.append(new_view)
    def post_renderer(self):
        """ Czynnosci po inicjalizacji. """
        if self.main_view == None:
            self.main_view = self.views[0]
        project = ConfigGlobal().get('project_manager')
        project.add_main_view_url(self)
    def execution(self):
        """
        Wygenerowanie kodu wszystkich widokow i dodanie ich do Managera
        widokow, ktory je wypisze.
        """
        for elem in self.views:
            self.managers['view'].add(elem)
        self.managers['view'].save_all(self)
    def get_url(self):
        """ Zwraca link do plikow z aplikacja. """
        url = "./" + self.get_name()
        return url
    def __str__(self):
        return self.get_name()
    def get_main_view(self):
        """ Pobranie glownego widoku. """
        if self.main_view == None:
            try:
                return self.views[0]
            except IndexError:
                return None
        else:
            return self.main_view
