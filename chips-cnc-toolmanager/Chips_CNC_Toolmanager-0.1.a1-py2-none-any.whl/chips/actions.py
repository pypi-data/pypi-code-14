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


from camelot.admin.action import Action
from camelot.core.utils import ugettext_lazy as _
from camelot.view.art import Icon
from chips.utils import plaintext_from_richtext as text_from_richtext
from camelot.core.orm import Session
from camelot.view.action_steps import OpenFormView,  Refresh,  MessageBox,  UpdateObject, UpdateProgress,  SelectFile
from camelot.admin.action.form_action import  CloseForm
from PyQt4.QtGui import QMessageBox
from jinja2 import Environment,  DictLoader
import codecs
import chips

class ClearTestCuts(Action):
    verbose_name=_('Clear testcuts list')
    #icon = Icon('tango/32x32/actions/mail-message-new.png')
    tooltip = _('Delete all TestCuts from this test')


    def model_run(self,  model_context):
        test = model_context.get_object()
        test_admin  = model_context.admin
        session = Session()
        testcuts = test.testcuts
        for t in testcuts:
            t.delete()
            session.flush()

        test_admin.refresh(test)
        yield UpdateObject(test)
        yield Refresh()


class ExportGCode(Action):
    verbose_name=_('Export G-Code')
    icon = Icon('chips_iconset/128x128/gcode-gcode-export.png',  module=chips)
    tooltip = _('Create g-code for this series of testcuts. Only enabled testcuts are included in the export.')


    def model_run(self,  model_context):

        test = model_context.get_object()
        #only get enabled testcuts
        testcuts = [tc for tc in test.testcuts if tc.enabled]
        if len(testcuts)==0:
            yield MessageBox( _('Nothing to export. Please create some testcuts first.'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)

        else:

            select_output_file = SelectFile('G-Code files (*.nc *.ngc *.txt *.gcode);; All files (*.*)')
            select_output_file.existing=False
            filenames = yield select_output_file

            #check if we got a filename
            if len(filenames) > 0:
                filename = filenames[0]
                yield UpdateProgress( text = _('Exporting GCode') )

                #define variables that can be used in gcode here
                context = dict(
                    #Machine
                    machine_name = test.machine.name,
                    machine_safe_z = test.machine.safe_z,

                    #Tool
                    tool_name = test.tool.name,
                    tool_type = test.tool.type,
                    tool_material = test.tool.tool_material,
                    tool_coating = test.tool.coating,
                    tool_diameter = test.tool.diameter,
                    tool_flutes = test.tool.flutes,
                    tool_cutting_length = test.tool.cutting_length,
                    tool_full_lenght = test.tool.full_length,
                    tool_cutting_angle = test.tool.cutting_angle,
                    tool_Smax = test.tool.Smax,
                    tool_number = test.tool.tool_number,
                    tool_manufacturer = test.tool.manufacturer,

                    #Material
                    material_name = test.material.name,
                    material_type = test.material.type,
                    material_recommended_VCC = test.material.recommended_VCC,
                    material_recommended_CPT = test.material.recommended_CPT,
                    material_machinability = test.material.machinability,
                    material_hardness = test.material.hardness,

                    #Test
                    test_name = test.name,
                    test_number_of_cuts = len(testcuts), #use the actual value, not the set value from the test dialog
                    test_start_S = test.start_S,
                    test_S_increment = test.S_increment,
                    test_start_CPT = test.start_CPT,
                    test_CPT_increment = test.CPT_increment,
                    test_Fp_percent = test.Fp_percent,
                    test_Ap = test.Ap,
                    test_Ap_increment = test.Ap_increment,
                    test_Ae = test.Ae,
                    test_Ae_increment = test.Ae_increment,
                    test_coolant = test.coolant,
                    test_comment = text_from_richtext(test.comment))


                output_gcode = u''

                templates = dict(
                    header = u'(G-Code created by Chips - tool test and management suite)\n\n',
                    machine_precode = text_from_richtext(test.machine.precode)+u"\n",
                    machine_postcode = text_from_richtext(test.machine.postcode)+u"\n",
                    pre_cut_code = text_from_richtext(test.pre_cut_gcode)+u"\n",
                    cut_code = text_from_richtext(test.cut_gcode)+u"\n",
                    post_cut_code = text_from_richtext(test.post_cut_gcode)+u"\n",
                )

                e = Environment(loader=DictLoader(templates), autoescape=True,trim_blocks=True)

                #Processing Gcode

                #process header
                t = e.get_template('header')
                output_gcode += unicode(t.render(context))+u'\n'

                #process machine_precode
                t = e.get_template('machine_precode')
                output_gcode += t.render(context)+u'\n'

                for cut in testcuts:
                    #create new context dict to represent variables of a sigle cut
                    cut_context=dict(
                        export_cut_number=testcuts.index(cut), #the cut number of the exported cut (useful to reposition cuts)
                        cut_reference = cut.cut_number,#cut number from testcut object
                        cut_S = cut.S,
                        cut_F = cut.F,
                        cut_Fp = cut.Fp,
                        cut_Ap = cut.Ap,
                        cut_Ae = cut.Ae,
                        cut_CPT = cut.CPT,
                        cut_MRR = cut.MRR
                    )
                    #join cut_context with context dictionary to get access to all variables
                    cut_context = dict(cut_context.items() + context.items())

                    t = e.get_template('pre_cut_code')
                    output_gcode += t.render(cut_context) +u'\n'
                    t = e.get_template('cut_code')
                    output_gcode += t.render(cut_context) +u'\n'
                    t = e.get_template('post_cut_code')
                    output_gcode += t.render(cut_context) +u'\n'

                #process machine_postcode
                t = e.get_template('machine_postcode')
                output_gcode += t.render(context)

                #write the whole thing to a textfile
                try:
                    f = codecs.open(filename,"w", "utf-8")
                    f.write(output_gcode)
                    f.close()
                except Exception,  e:
                    yield MessageBox( _('Could not write file: %s' %e),  icon=QMessageBox.Warning,  standard_buttons=QMessageBox.Ok)


class SaveAsRecipe(Action):
    """This action is used in the TestCut form"""
    verbose_name=_('Save as Recipe')
    icon = Icon('chips_iconset/128x128/recipes-recipe-new.png',  module=chips)
    tooltip = _('Save the parameters from this Testcut as a new Recipe')


    def model_run(self,  model_context):
        from chips.model import Recipe
        testcut = model_context.get_object()
        session = Session()

        recipe = Recipe()
        recipe.name = u'<new recipe from test "%s" - cut number: %i>'%(testcut.test.name, testcut.cut_number)
        recipe.test = testcut.test
        recipe.machine = testcut.test.machine
        recipe.tool = testcut.test.tool
        recipe.material = testcut.test.material
        recipe.S = testcut.S
        recipe.F = testcut.F
        recipe.Fp = testcut.Fp
        recipe.Ap = testcut.Ap
        recipe.Ae = testcut.Ae
        recipe.coolant = testcut.test.coolant
        recipe.comment = testcut.comment
        recipe.rating = testcut.rating
        session.flush()

        recipe_admin=model_context.admin.get_related_admin(Recipe)
        yield OpenFormView([recipe],  recipe_admin)


###form validation
class CloseFormAction(Action):
    """this action provides a hook that is called on the model_context's object when it's form is closed (after validation)"""
    verbose_name=_('Close')
    icon = Icon('tango/32x32/actions/system-log-out.png')

    def model_run(self, model_context):
        obj = model_context.get_object()
        #see if we can call on_close() on this object
        if hasattr(obj, "on_close") and callable(getattr(obj,"on_close")):
            obj.on_close()
        yield CloseForm()

#######
class ValidateFormBeforeCloseFormAction( Action ):
    """Validate the form can be closed before calling our CloseFormAction.
    This way we can make sure the Form can be closed before we execute our on_close() functions.
    The Form will be validated again by CloseForm, though.
    This way we will be shure we do not mess up things in on_close()"""

    #shortcut = QtGui.QKeySequence.Close
    icon = Icon('tango/16x16/actions/system-log-out.png')
    verbose_name = _('Close')
    tooltip = _('Close')

    def gui_run( self, gui_context ):
        gui_context.widget_mapper.submit()
        super( ValidateFormBeforeCloseFormAction, self ).gui_run( gui_context )

    def model_run( self, model_context ):
        from PyQt4 import QtGui
        from camelot.view import action_steps
        yield action_steps.UpdateProgress( text = _('Validating Form') )
        validator = model_context.admin.get_validator()
        obj = model_context.get_object()
        admin  = model_context.admin
        if obj == None:
            yield action_steps.CloseView()
        #
        # validate the object, and if the object is valid, simply close
        # the view
        #
        messages = validator.objectValidity( obj )
        valid = ( len( messages ) == 0 )
        if valid:
            ###Form is valid what do we do now?
            yield CloseFormAction()
        else:
            #
            # if the object is not valid, request the user what to do
            #
            message = action_steps.MessageBox( '\n'.join( messages ),
                                               QtGui.QMessageBox.Warning,
                                               #_('Invalid form'),
                                               _('Invalid form on_close'),
                                               QtGui.QMessageBox.Ok | QtGui.QMessageBox.Discard )
            reply = yield message
            if reply == QtGui.QMessageBox.Discard:
                yield action_steps.CloseView()
                if admin.is_persistent( obj ):
                    admin.refresh( obj )
                    yield action_steps.UpdateObject( obj )
                else:
                    yield action_steps.DeleteObject( obj )
                    admin.expunge( obj )
