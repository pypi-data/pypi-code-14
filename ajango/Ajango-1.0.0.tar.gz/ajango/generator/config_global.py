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
""" Modul konfiguracji globalnej pakietu Ajango. """

#pylint: disable=R0903
#pylint: disable=C0103
class ConfigGlobal(object):
    """ Klasa konfiguracyjna (singleton). """
    class __ConfigGlobal(object):
        """ Prywana klasa konfiguracyjna. """
        def __init__(self):
            self.config = {'view_id_counter' : 1}
        def get(self, name, default=None):
            """ Pobieranie wartosci ustawien. """
            try:
                return self.config[name]
            except KeyError:
                return default
        def set(self, name, value):
            """ Ustawienie wartosci konfiguracyjnej. """
            self.config[name] = value
    instance = None
    def __init__(self):
        if not ConfigGlobal.instance:
            ConfigGlobal.instance = ConfigGlobal.__ConfigGlobal()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def get_instance(self):
        """ Zwraca obiekt singletonu. """
        return self
