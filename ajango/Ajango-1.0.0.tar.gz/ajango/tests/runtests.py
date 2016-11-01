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
""" Implementacja testow jednostowych. """

import unittest
import importlib

from xml.dom.minidom              import parseString
from django.core.management.base  import CommandError
from ajango.database.validate     import validate_factory
from ajango.generator.application import Application
from ajango.core.factory          import FactoryBase


TEST_MODULES = [
    'ajango',
    'ajango.conf',
    'ajango.contrib',
    'ajango.contrib.automatic',
    'ajango.contrib.automatic.management',
    'ajango.contrib.automatic.management.commands',
    'ajango.contrib.automatic.management.commands.generateapps',
    'ajango.contrib.automatic.management.commands.makeskeleton',
    'ajango.contrib.automatic.apps',
    'ajango.core',
    'ajango.core.factory',
    'ajango.core.XMLReader',
    'ajango.core.generable',
    'ajango.database',
    'ajango.database.query',
    'ajango.database.columns',
    'ajango.database.columns.default',
    'ajango.database.columns.button',
    'ajango.database.data_base_manager',
    'ajango.database.inputs',
    'ajango.database.inputs.default',
    'ajango.database.inputs.number',
    'ajango.database.validate',
    'ajango.database.validate.isempty',
    'ajango.database.validate.regex',
    'ajango.database.validate.gt',
    'ajango.database.validate.lt',
    'ajango.generator',
    'ajango.generator.views',
    'ajango.generator.views.editable',
    'ajango.generator.views.empty',
    'ajango.generator.views.input',
    'ajango.generator.views.list',
    'ajango.generator.views.raport',
    'ajango.generator.views.container',
    'ajango.generator.views.display',
    'ajango.generator.application',
    'ajango.generator.config_global',
    'ajango.generator.project_manager',
    'ajango.generator.renderer',
    'ajango.generator.view_manager',
    'ajango.generator.menu_manager',
    'ajango.gui',
    'ajango.gui.window',
    'ajango.gui.controller',
    'ajango.gui.model',
    'ajango.site',
    'ajango.site.site_menu',
    'ajango.site.presentations',
    'ajango.site.presentations.upper',
    'ajango.site.sites',
    'ajango.site.sites.display',
    'ajango.site.sites.editable',
    'ajango.site.sites.empty',
    'ajango.site.sites.input',
    'ajango.site.sites.list',
    'ajango.site.sites.raport',
    'ajango.site.sites.container',
]

TEST_FACTORY = [
    ('ajango.database.columns', 'Column',
        {'type' : 'default', 'label' : 'Wiek', 'tag' : 'age' }),
    ('ajango.database.inputs', 'Input', \
        {'type': 'number', 'label': 'Wiek', 'tag': 'age', 'default': '18'}),
    ('ajango.database.validate', 'Validate', {'type': 'isempty', 'param': '' }),
    ('ajango.generator.views', 'View', \
        { 'xmldoc' : parseString("<view type=\"empty\" id=\"one\">"
           "</view>").documentElement}),
    ('ajango.site.presentations', 'Presentation', 'upper'),
    ('ajango.site.sites', 'Site', 'empty'),
]

class TestAjango(unittest.TestCase):
    """ Klasa testowa dla pakietu Ajango. """
    def __str__(self):
        return "Testy jednostkowe pakietu Ajango."
    def testVerifyAll(self):
        """
        Sprawdzenie czy wszystkie dostepne modele moga byc poprawnie wczytane.
        """
        module_tested = ""
        for mod in TEST_MODULES:
            try:
                module_tested = mod
                importlib.import_module(mod)
            except SyntaxError:
                assert False, "Modules %r not validate" % module_tested
            except ImportError:
                assert False, "No module named %r" % module_tested
            else:
                assert True, "Module is read %s" % module_tested
    def testValidators(self):
        """
        Sprawdzenie poprawnosci walidacji.
        """
        data = [{ 'type' : "isempty",
                  'test' : "" ,
                  'param' : None,
                  'is_valid' : False },
                { 'type' : "isempty",
                  'test' : " ",
                  'param' : None,
                  'is_valid' : True },
                { 'type' : "isempty",
                  'test' : "not empty string",
                  'param' : None,
                  'is_valid' : True },
                { 'type' : "regex",
                  'test' : "AAjfds",
                  'param' : "^[A]{2}",
                  'is_valid' : True },
                { 'type' : "regex",
                  'test' : "AAjfds",
                  'param' : "^[A-Z]{1}[a-z]+",
                  'is_valid' : False },
                { 'type' : "gt",
                  'test' : "5",
                  'param' : "1",
                  'is_valid' : True },
                { 'type' : "gt",
                  'test' : "5",
                  'param' : "5",
                  'is_valid' : False },
                { 'type' : "gt",
                  'test' : "5",
                  'param' : "10",
                  'is_valid' : False },
                { 'type' : "gt",
                  'test' : "one",
                  'param' : "5",
                  'is_valid' : False },
                { 'type' : "lt",
                  'test' : "5",
                  'param' : "10",
                  'is_valid' : True },
                { 'type' : "lt",
                  'test' : "5",
                  'param' : "5",
                  'is_valid' : False },
                { 'type' : "lt",
                  'test' : "5",
                  'param' : "1",
                  'is_valid' : False },
                { 'type' : "lt",
                  'test' : "ten",
                  'param' : "5",
                  'is_valid' : False }
               ]
        for test_case in data:
            validator = validate_factory(test_case)
            is_valid = test_case['is_valid']
            test_result = is_valid == validator.is_valid(test_case['test'])
            assert test_result, "Validator %r not work" % test_case['type']
    def testApplicationMainView(self):
        """ Sprawdzenie poprawnosci generowania aplikacji. """
        ob = Application(parseString("<application name=\"test\">"
                                     "</application>").documentElement)
        assert ob.get_main_view() == None, "Empty Application has view"
        ob = Application(parseString("<application name=\"test\">"
                                     "<view type=\"empty\" id=\"one\"></view>"
                                     "</application>").documentElement)
        assert ob.get_main_view().get_name() == "one", "Invalid Application id"
        ob = Application(parseString("<application name=\"test\">"
                                     "<view type=\"empty\" id=\"one\"></view>"
                                     "<view type=\"empty\" id=\"two\"></view>"
                                     "</application>").documentElement)
        assert ob.get_main_view().get_name() == "one", "Invalid Application id"
        ob = Application(parseString("<application name=\"test\">"
                                     "<view type=\"empty\" id=\"one\"></view>"
                                     "<view type=\"empty\" id=\"two\""
                                     " main=\"main\"></view>"
                                     "</application>").documentElement)
        assert ob.get_main_view().get_name() == "two", "Invalid Application id"
    def testApplicationMainViewRaise(self):
        """ Testowanie wystepowania wyjatku dla generatora aplikacji. """
        def test_case():
            Application(parseString("<application name=\"test\">"
                                    "<view type=\"empty\" id=\"one\""
                                    " main=\"main\"></view>"
                                    "<view type=\"empty\" id=\"two\""
                                    " main=\"main\"></view>"
                                    "</application>").documentElement)
        self.assertRaises(CommandError, test_case)
    def testFactory(self):
        """ Sprawdzenie poprawnosci implementacji fabryk. """
        def get_dictionary_from_param(param):
            return {'lib'     : param[0],
                    'factory' : '%sFactoryObject' % param[1],
                    'base'    : '%sBase' % param[1],
                    'arg'     : param[2]}
        for elem in TEST_FACTORY:
            # Testowanie fabryk.
            test_data = get_dictionary_from_param(elem)
            # Pobranie modulu dla konkretnej fabryki wraz z jej obiektem 
            try:
                module = importlib.import_module(test_data['lib'])
                factory = getattr(module, test_data['factory'])
                base = getattr(module, test_data['base'])
            except SyntaxError:
                assert False, "No module named %r" % test_data['lib']
            except ImportError:
                assert False, "No module named %r" % test_data['lib']
            assert issubclass(factory, FactoryBase), \
                   "Factory %s must be child of FactoryBase" % \
                    test_data['factory']
            factory_ob = factory(test_data['arg'])
            objects = factory_ob._get_base_address()
            for ob in objects.values():
                # Iteracja po klasach ktore powstaja z fabryki
                assert ob in TEST_MODULES, \
                       "Factory element doesn't exist: %r" % ob
                try:
                    ob_module = importlib.import_module(ob)
                    ob_object = getattr(ob_module, factory_ob.class_name)
                except SyntaxError:
                    assert False, "No module named %r" % ob
                except ImportError:
                    assert False, "No module named %r" % ob
                assert issubclass(ob_object, base), \
                       "Object %s must be child of %s" % (ob, test_data['base'])

if __name__ == "__main__":
    unittest.main()
