#!/usr/bin/python
# -*- coding: utf-8 -*-

##This file is part of Chips - CNC tool test and management suite
##Copyright (C) 2016  Sebastian Stetter
##https://bitbucket.org/sebste/chips

##This program is free software; you can redistribute it and/or
##modify it under the terms of the GNU General Public License
##as published by the Free Software Foundation; either version 2
##of the License, or (at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section
from camelot.admin.action import application_action, form_action, list_action
from camelot.core.utils import ugettext_lazy as _

from PyQt4.QtGui import QIcon,  QPixmap
from PyQt4.QtCore import Qt
from chips.model import Tool,  Machine,  Material,  Recipe, Test #, TestCut
from chips.actions import  ValidateFormBeforeCloseFormAction #MachiningCalculator
import os

class MyApplicationAdmin(ApplicationAdmin):
    import chips

    name = 'Chips - CNC tool test and management suite'
    application_url = 'https://bitbucket.org/sebste/chips'
    help_url = 'https://bitbucket.org/sebste/chips/wiki/browse/'
    author = 'Sebastian Stetter'
    domain = 'sebastianstetter.de'
    version = chips.__version__

    def get_splashscreen(self):
        """:return: a :class:`PyQt4.QtGui.QPixmap` to be used as splash screen"""
        qpm = QPixmap(os.path.join(os.path.dirname(__file__),'splash.png'))
        img = qpm.toImage()
        # support transparency
        if not qpm.mask():
            if img.hasAlphaBuffer(): bm = img.createAlphaMask()
            else: bm = img.createHeuristicMask()
            qpm.setMask(bm)
        return qpm

    def get_stylesheet(self):
        from camelot.view import art
        styles=['navpane_office2007_black.qss', 'black.qss', 'office2007_blue.qss', 'navpane_office2007_silver.qss', 'navpane3_office2007_silver.qss', 'navpane3_office2007_black.qss', 'office2007_black.qss', 'navpane_office2007_blue.qss', 'office2007_silver.qss', 'navpane3_office2007_blue.qss']
        return art.read('stylesheet/%s' %styles[2])

    def get_icon(self):
        """:return: the :class:`camelot.view.art.Icon` that should be used for the application"""
        return QIcon(os.path.join(os.path.dirname(__file__),'icon.png'))

    def get_sections(self):
        #from camelot.model.memento import Memento
        from camelot.model.i18n import Translation

        import chips

        return [ Section( _('Shop'),
                          self,
                          Icon('chips_iconset/128x128/app-machineshop.png',  module=chips),
                          items = [Recipe, Test, Material, Tool, Machine] ),
#                 Section( _('All Classes (development)'),
#                          self,
#                          Icon('tango/22x22/categories/applications-system.png'),
#                          items = [Machine,  Tool, Material, Recipe, Test, TestCut] ),
                 Section( _('Configuration'),
                          self,
                          Icon('tango/22x22/categories/applications-system.png'),
                          items = [#Memento,
                            Translation] )
                ]


    def get_about(self):
        """:return: the content of the About dialog, a string with html
                syntax"""
        from camelot.core import license
        return """<b>Chips v%s</b><br/>
                   CNC tool test and management suite.
                  <p>
                  Author: Sebastian Stetter
                  </p>
                  <p>
                  %s
                  </p>
                  <p>
                  <a href ="https://bitbucket.org/sebste/chips">https://bitbucket.org/sebste/chips</a><br/>
                  </p>
                  """%(self.version, license.license_type)

#Actions

    def get_actions(self):
        from camelot.admin.action import OpenNewView
        import chips

        new_recipe_action = OpenNewView( self.get_related_admin(Recipe) )
        new_recipe_action.icon = Icon('chips_iconset/128x128/recipes-recipe-new.png',  module=chips)

        new_material_action = OpenNewView( self.get_related_admin(Material) )
        new_material_action.icon = Icon('chips_iconset/128x128/materials-material-new.png',  module=chips)

        new_tool_action = OpenNewView( self.get_related_admin(Tool) )
        new_tool_action.icon = Icon('chips_iconset/128x128/tools-tool-new.png',  module=chips)

        new_machine_action = OpenNewView( self.get_related_admin(Machine) )
        new_machine_action.icon = Icon('chips_iconset/128x128/machines-machine-new.png',  module=chips)

        new_test_action = OpenNewView( self.get_related_admin(Test) )
        new_test_action.icon = Icon('chips_iconset/128x128/tests-test-new.png',  module=chips)



        return [new_recipe_action,new_test_action, new_tool_action, new_material_action, new_machine_action]

    def get_form_toolbar_actions(self, toolbar_area):
        #reimplelemt toolbar actions of form
        form_toolbar_actions = [ ValidateFormBeforeCloseFormAction(),  #replace form_action.CloseForm()
                        #form_action.CloseForm(),
                        form_action.ToFirstForm(),
                         form_action.ToPreviousForm(),
                         form_action.ToNextForm(),
                         form_action.ToLastForm(),
                         application_action.Refresh(),
                         #form_action.ShowHistory() #insert any other desired form_toolbar_action here
                         ]

        return form_toolbar_actions


    def get_related_toolbar_actions( self, toolbar_area, direction ):
        #reimplementation of related toolbar actions
        if toolbar_area == Qt.RightToolBarArea and direction == 'onetomany':
            return [ #list_action.AddNewObject(),
                     #list_action.DeleteSelection(),
                     #list_action.DuplicateSelection(),
                     list_action.PrintPreview(),
                     list_action.ExportSpreadsheet(),
                     ]
        if toolbar_area == Qt.RightToolBarArea and direction == 'manytomany':
            return [ list_action.AddExistingObject(),
                     list_action.RemoveSelection(),
                     list_action.ExportSpreadsheet(),
                     ]



#    def get_toolbar_actions( self, toolbar_area ):
#        #reimplement toolbar actions
#        if toolbar_area == Qt.TopToolBarArea:
#            toolbar_actions = self.edit_actions + self.change_row_actions + \
#                   self.export_actions + self.help_actions
#            return toolbar_actions


#    def get_main_menu( self ):
#        #reimplement main menu
#        from camelot.admin.menu import Menu
#
#        return [ Menu( _('&File'),
#                       [ application_action.Backup(),
#                         application_action.Restore(),
#                         None,
#                         Menu( _('Export To'),
#                               self.export_actions ),
#                         Menu( _('Import From'),
#                               [list_action.ImportFromFile()] ),
#                         None,
#                         application_action.Exit(),
#                         ] ),
#                 Menu( _('&Edit'),
#                       self.edit_actions + [
#                        None,
#                        list_action.SelectAll(),
#                        None,
#                        list_action.ReplaceFieldContents(),
#                        ]),
#                 Menu( _('View'),
#                       [ application_action.Refresh(),
#                         Menu( _('Go To'), self.change_row_actions) ] ),
#                 Menu( _('&Help'),
#                       self.help_actions + [
#                         application_action.ShowAbout() ] ),
#                 Menu( _('&My Cool Little Action'),
#                       self.help_actions + [
#                         SaveAsRecipe() ] )
#                 ]
