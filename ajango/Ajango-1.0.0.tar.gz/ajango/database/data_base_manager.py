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
""" Modul zarzadzania i tworzenia modelu dla wygenerowanego programu. """

from django.core.management.commands.inspectdb import Command
from django.db                                 import DEFAULT_DB_ALIAS
from django.core.management.base               import CommandError
from ajango.core                               import buffor_to_file

class DataBaseManager(object):
    """ Obiekt zarzadzajacy i tworzacy model dla wygenerowanego programu. """
    def __init__(self, application):
        self.application_manager = application
    def get_application_manager(self):
        """ Zwraca uchwyt do menagera aplikacji. """
        return self.application_manager
    def build_data_base(self, options):
        """ Zbuduj pliki modelu w wybranej aplikacji. """
        inspectdb = Command()
        address = self.application_manager.get_name() + "/models.py"
        buffor = ""
        options['database'] = DEFAULT_DB_ALIAS
        try:
            for line in inspectdb.handle_inspection(options):
                buffor += "%s\n" % line
        except NotImplementedError:
            raise CommandError("Database inspection isn't supported"
                               "for the currently selected database backend.")
        buffor_to_file(address, buffor)
