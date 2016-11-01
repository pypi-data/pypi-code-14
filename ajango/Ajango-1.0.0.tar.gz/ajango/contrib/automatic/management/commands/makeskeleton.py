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
Polecenie generujace szkielet aplikacji.

Polecenie pozwala na wygenerowanie szkieletu projektu w formie pliku XML.
Niezbedne do jego dzialania jest wygenerowanie pliku projektowego systemu
I{Django} z ustawiona aplikacja I{Ajango}. Wiecej informacji na ten temat
w L{ajango}.

Gotowy plik mozna edytowac zgodnie z opisem w L{ajango.generator} a nastepnie
wygenerowac aplikacje poleceniem
L{generateapps <ajango.contrib.automatic.management.commands.generateapps>}

Skladnia polecenia
==================

Przykladowe wywolanie polecenia::

    $ python manager.py makeskeleton .

Znak kropki oznacza adres docelowym w ktorym zostanie wygenerowany plik.
"""

from django.core.management.templates import TemplateCommand
import ajango

class Command(TemplateCommand):
    """
    Generowanie szablonu szkieletu.

    Polecenie generuje szkielet aplikacji z ktorego potem nastapi automatyczne
    generowanie pliku. Aplikacje opisane sa w formacie XML a ich generowanie
    nastepuje po wykonianu polecenia C{generateapps} dostepnego w skrypcie
    frameworka Django.
    """
    help = ("Creates a Ajango skeleton file.")
    missing_args_message = "You must provide an application name."
    def add_arguments(self, parser):
        """ Definiowanie argumentow. """
        parser.add_argument('directory', nargs='?',
                            help='Optional destination directory')
        parser.add_argument('--template',
                            help='The path or URL to load the template from.')
        parser.add_argument(
            '--extension', '-e', dest='extensions',
            action='append', default=['py'],
            help='The file extension(s) to render (default: "py"). '
                 'Separate multiple extensions with commas, or use '
                 '-e multiple times.'
        )
        parser.add_argument(
            '--name', '-n', dest='files',
            action='append', default=[],
            help='The file name(s) to render. Separate multiple extensions '
                 'with commas, or use -n multiple times.'
        )
    def handle(self, **options):
        """ Obsluga polecenia. """
        skeleton_name = "name"
        target = options.pop('directory')
        # Check that the skeleton_name cannot be imported.
        options['template'] = ajango.__path__[0] + '/conf/skeleton_template'
        super(Command, self).handle('skeleton', skeleton_name,
                                    target, **options)
