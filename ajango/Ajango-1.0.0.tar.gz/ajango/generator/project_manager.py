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
""" Pakiet zarzadzajacy projektem Django. """

import os.path
from django.core.management.base import CommandError
from ajango.core                 import add_to_python_array
from ajango.core                 import file_to_buffor, buffor_to_file

class ProjectManager(object):
    """ Klasa zarzadzajaca projektem Django. """
    def __init__(self, project_name):
        if not os.path.isdir(project_name):
            raise CommandError("%r: Cannot find project" % project_name)
        self.project_name = project_name
        self._verify_file('settings.py')
        self._verify_file('urls.py')
        self._verify_file('wsgi.py')
        self.apps = []
        self.urls = []
        self.is_global_url = False
    def _verify_file(self, file_skeleton):
        """ Sprawdzenie czy istnieje plik. """
        search_file = self.project_name + '/' + file_skeleton
        if not os.path.isfile(search_file):
            raise CommandError("Cannot find file: %r" % search_file)
    def add_application(self, app):
        """ Dodanie aplikacji do pliku settingsow projektu. """
        self.apps.append(app)
    def add_url(self, viewname, appname):
        """ Add view url. """
        self.urls.append("url(r'^%s/%s/', %s.views.%s, name=%r)," %
                         (appname, viewname, appname, viewname, viewname))
    def add_main_view_url(self, app):
        """ Zarejestrowanie widoku jako glowny widok aplikacji. """
        appname = app.get_name()
        viewname = app.get_main_view().get_name()
        self.urls.append("url(r'^%s$', %s.views.%s, name='%s_main')," %
                         (appname, appname, viewname, appname))
    def add_main_url(self, app):
        """ Zarejestrowanie glownego ekranu dla aplikacji. """
        if app == None:
            raise CommandError("Cannot set 'None' value as application")
        if self.is_global_url:
            raise CommandError("Cannot set two or more main application to url")
        self.is_global_url = True
        viewname = app.get_main_view().get_name()
        self.urls.append("url(r'^$', %s.views.%s, name='main')," %
                         (app.get_name(), viewname))
    def execute_url(self):
        """ Dodanie odpowiednich adresow url do pliku. """
        address = self.project_name + "/urls.py"
        buffor = file_to_buffor(address)
        import_str = ""
        for app in self.apps:
            import_str += "import %s.views\n" % app
        buffor = import_str + buffor
        url_str = ""
        for url in self.urls:
            url_str += "\n    %s" % url
        buffor = add_to_python_array(buffor, "urlpatterns", url_str)
        buffor_to_file(address, buffor)
    def execute_settings(self):
        """ dodanie aplikacji do pliku z ustawieniami settings.py"""
        address = self.project_name + "/settings.py"
        buffor = file_to_buffor(address)
        app_str = ""
        for app in self.apps:
            app_str += "\n    '%s'," % app
        buffor = add_to_python_array(buffor, "INSTALLED_APPS", app_str)
        buffor_to_file(address, buffor)
    def execute(self):
        """ Wykonanie zadan obiektu. """
        self.execute_url()
        self.execute_settings()
