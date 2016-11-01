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
Polecenie pozwala na edycje pliku szkieletowego w formie graficznej.
Aplikacja wymaga do poprawnego dzialania zainstalowanej biblioteki I{Ajango}
oraz I{PyQt4}.

Skladnia polecenia
==================

Przykladowe wywolanie polecenia::

    $ python manager.py ajangogui

Generator skorzysta domyslnie z pliku U{skeleton.xml}. Mozna to ustawienie
zmienic wywolujac polecenie z flaga C{-f} po ktorej podana powinna byc nazwa
pliku z szablonem.

Nalezy zwrocic uwage na to iz Ajagno nie jest w stanie wygenerowac aplikacji
w katalogu w ktorym sie znajduje. W przypadku testowania dzialania generatora
zaleca sie wykonanie kopi zapasowej katalogu projektowego oraz podmienianie go
przed kolejnym generowaniem aplikacji.
"""

from django.core.management.base import BaseCommand
from ajango.gui                  import Application

class Command(BaseCommand):
    """
    Edycja aplikacji w trybie graficznym.

    Polecenie generuje aplikacje na postawie szkieletu. Jest on domyslnie
    przechowywany w pliku I{skeleton.xml} i moze byc ustawiony flaga C{-f} lub
    C{--file}.
    """
    help = ("Edit XML sceleton file in graphical mode.")
    def add_arguments(self, parser):
        """ Definiowanie argumentow. """
        parser.add_argument(
            '-f', '--file',
            action='store', dest='skeleton_file', default='skeleton.xml',
            help='Path to file with skeleton',
        )
    def handle(self, **options):
        """ Obsluga polecenia. """
        skeleton_file = options['skeleton_file']
        Application.main(skeleton_file)
