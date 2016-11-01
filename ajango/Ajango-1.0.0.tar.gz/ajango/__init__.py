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
Modul jezyka Python umozliwiajacy automatyzacje tworzenia aplikacji
typu I{'light of buissnes'}.

Wymagania
=========

    1. Jezyk U{Python<https://www.python.org/>}.
    2. Pakiet U{Django<https://www.djangoproject.com/>}.

Instalacja pakietu
==================

Pakiet mozna pobrac ze strony U{https://bitbucket.org/rafyco/ajango} lub
z udostepnionego przez autora repozytorium::

    git clone https://bitbucket.org/rafyco/ajango.git

    python setup.py install

Pierwsze uruchomienie
=====================

Tworzymy projekt frameworka Django::

    python django-admin.py startproject <project> .

W pliku setting.py dodajemy do zmiennej C{INSTALLED_APPS} opcje
C{'ajango.contrib.automatic'}.

Uruchamiamy opcje tworzaca plik szkieletowy lub kopiujemy wczesniej
przygotowany plik do folderu z projektem::

    python manage.py makeskeleton

Edytujemy plik szkieletu opisujacego aplikacje. Operacje te wykonywane sa wedlug
uznania i potrzeb programisty.

Generujemy aplikacje poleceniem::

    python manage.py generateapps

Aplikacje zostana wygenerowane w pliku roboczym w postaci folderow
o odpowiednich nazwach. Oprocz tego zostana uzupelnione rowniez pliki z kodem
potrzebne do jej uruchomienia. W celu przetestowania powstalego produktu nalezy
wykonac polecenie uruchamiajace serwer testowy pakietu Django.

Plik szkieletu
==============

Wiecej informacji na temat pliku szkieletu mozna przeczytac w dokumentacji
pakietu L{ajango.generator}.

Polecenia terminala
===================

Ajango integruje sie z systemem zarzadzania I{Django}, dzieki czemu mozliwe jest
wykonywanie polecen z poziomu skryptu zarzadzajacego C{manage.py}

Dostepne polecenia:

    - L{generateapps<ajango.contrib.automatic.management.commands.generateapps>}
    - L{makeskeleton<ajango.contrib.automatic.management.commands.makeskeleton>}

Wiecej o poleceniach mozna przeczytac w dokumentacji pakietu:
L{ajango.contrib.automatic.management.commands}

Testy jednostkowe
=================

Modul zostal wzbogacony o serie testow jednostowych. Mozna je uruchomic
poleceniem::

    python -m ajango.tests

Implementacja testow dostepna w pakiecie L{ajango.tests.runtests}.
"""

def get_version():
    """ Pobierz wersje oprogramowania. """
    return "1.0.0"

__version__ = get_version()
