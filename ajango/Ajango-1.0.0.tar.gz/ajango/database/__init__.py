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
""" Funkcje pomocnicze do zarzadzania baza danych. """

from __future__                  import print_function
from django.core.management.base import CommandError
from xml.dom                     import minidom
import inspect

#pylint: disable=W0212
def get_table_name_in_db(table):
    """ Pobranie nazwy tabeli na podstawie obiektu modelu. """
    return table._meta.db_table

#pylint: disable=W0612
def get_table_by_name(table_name, models):
    """ Pobranie modelu na podstawie nazwy tabeli w bazie danych. """
    for name, temp_table in inspect.getmembers(models):
        if inspect.isclass(temp_table):
            try:
                if get_table_name_in_db(temp_table) == table_name:
                    return temp_table
            except AttributeError:
                pass
    raise CommandError("There are no table name called: %r" % table_name)
