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
""" Zestaw funkcji pomocniczych pakietu Ajango. """

def add_to_python_array(buffor, pattern, value):
    """ Dodaje do zdefiniowanej tabeli wybrane wartosci. """
    pattern = pattern + " = ["
    buffor = buffor.replace(pattern, pattern + value)
    return buffor

def file_to_buffor(address):
    """ Odczytuje dane z pliku i zwraca do buffora. """
    buffor = ''
    try:
        fsettings = open(address, "r")
        buffor = fsettings.read()
    finally:
        fsettings.close()
    return buffor

def buffor_to_file(address, buffor):
    """ Zapisuje wartosc buffora do pliku. """
    try:
        fsettings = open(address, "w")
        fsettings.write(buffor)
    finally:
        fsettings.close()
