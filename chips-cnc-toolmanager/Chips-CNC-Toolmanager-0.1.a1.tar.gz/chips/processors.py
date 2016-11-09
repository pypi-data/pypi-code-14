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
import chips
from camelot.core.orm import Session
from camelot.view.action_steps import Refresh, UpdateProgress, MessageBox
from PyQt4.QtGui import QMessageBox

from chips.utils import calculate_F,  calculate_Fp

class SpindleChiploadAlternatingIncrement(Action):
    verbose_name=_('Spindle speed / chipload test')
    icon = Icon('chips_iconset/128x128/processors-spindelspeedchipload-increment.png',  module=chips)
    tooltip = _(u'Alternating Spindle speed / chipload increment test:\n 1) Find conservative starting point - e.g. a baseline cut that is making a good chip and machine is happy.\n If you have no idea where to start, try 2,000 RPM and a 0.00075 chipload per tooth\n 2) Increase RPM, keep chipload constant (so higher feedrate!)\n 3) If #2 is OK, then try higher chipload (same RPM).  So again, this means a higher feedrate!\n 4) If #3 is OK, then back to #2 - e.g. increase RPM and continue process of zig/zag between increasing RPM and Chipload\n')



    def model_run(self,  model_context):
        from chips.model import TestCut
        test = model_context.get_object()
        admin  = model_context.admin
        session = Session()

        if admin.is_persistent( test ):
            step_count=0
            Ap = test.Ap
            Ae = test.Ae
            S = test.start_S
            CPT = test.start_CPT
            #calculate F based on S, CPT and number of flutes
            #S * CPT * flutes
            F = calculate_F(S, CPT, test.tool.flutes)
            Fp = calculate_Fp(F, test.Fp_percent, test.machine.F_Z_max)

            yield UpdateProgress( text = _('Creating Cuts for Spindle speed / chipload test (ZigZag test)') )

            while step_count <= test.number_of_testcuts:
                if S <= test.machine.Smax and S <= test.tool.Smax and F <= test.machine.F_XY_max:
                    #create a TestCut
                    testcut = TestCut()
                    testcut.cut_number=step_count
                    testcut.test=test
                    testcut.S = S
                    testcut.F = F
                    testcut.Fp = Fp
                    testcut.Ap = Ap
                    testcut.Ae = Ae
                    session.flush()

                    #increment values
                    step_count+=1
                    #Ap = Ap + test.Ap_increment
                    #Ae = Ae + test.Ae_increment
                    #Increase S and CPT alternatingly, S first
                    if step_count %2 == 0:
                        S = S + test.S_increment
                    else:
                        CPT = CPT + test.CPT_increment

                    #recalculate feedrates
                    F = calculate_F(S, CPT, test.tool.flutes)
                    Fp = calculate_Fp(F, test.Fp_percent, test.machine.F_Z_max)
                else:
                    yield MessageBox( _('Not all testcuts created because S or F exceeded limits of machine or tool.'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)
                    break

            yield Refresh()
        else:
            yield MessageBox( _('This test has not been saved to the database, yet. To create testcuts, a test name, machine, tool and material need to be specified!'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)



class Increment(Action):
    verbose_name=_('S, CPT, Ae, Ap increment test')
    icon = Icon('chips_iconset/128x128/processors-doc-increment.png',  module=chips)
    tooltip = _(u'S (spindle rpm), CPT (chipload), Ap (depth of cut) and Ae (width of cut) are incremented with every testcut by the given increment values')



    def model_run(self,  model_context):
        from chips.model import TestCut
        test = model_context.get_object()
        admin  = model_context.admin
        session = Session()

        if admin.is_persistent( test ):
            step_count=0
            Ap = test.Ap
            Ae = test.Ae
            S = test.start_S
            CPT = test.start_CPT
            #calculate F based on S, CPT and number of flutes
            #S * CPT * flutes
            F = calculate_F(S, CPT, test.tool.flutes)
            Fp = calculate_Fp(F, test.Fp_percent, test.machine.F_Z_max)

            yield UpdateProgress( text = _('Creating Cuts for increment test') )

            while step_count <= test.number_of_testcuts:
                if S <= test.machine.Smax and S <= test.tool.Smax and F <= test.machine.F_XY_max:
                    #create a TestCut
                    testcut = TestCut()
                    testcut.cut_number=step_count
                    testcut.test=test
                    testcut.S = S
                    testcut.F = F
                    testcut.Fp = Fp
                    testcut.Ap = Ap
                    testcut.Ae = Ae
                    session.flush()

                    #increment values
                    step_count+=1
                    Ap = Ap + test.Ap_increment
                    Ae = Ae + test.Ae_increment
                    S = S + test.S_increment
                    CPT = CPT + test.CPT_increment

                    #recalculate feedrates
                    F = calculate_F(S, CPT, test.tool.flutes)
                    Fp = calculate_Fp(F, test.Fp_percent, test.machine.F_Z_max)
                else:
                    yield MessageBox( _('Not all testcuts created because S or F exceeded limits of machine or tool.'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)
                    break

            yield Refresh()
        else:
            yield MessageBox( _('This test has not been saved to the database, yet. To create testcuts, a test name, machine, tool and material need to be specified!'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)


class SingleTestCut(Action):
    verbose_name=_('Single Testcut')
    icon = Icon('chips_iconset/128x128/gcode-gcode.png',  module=chips)
    tooltip = _(u'Creates a single testcut with the parameters specified in the test.')



    def model_run(self,  model_context):
        from chips.model import TestCut
        test = model_context.get_object()
        admin  = model_context.admin
        session = Session()

        if admin.is_persistent( test ):
            Ap = test.Ap
            Ae = test.Ae
            S = test.start_S
            CPT = test.start_CPT
            #calculate F based on S, CPT and number of flutes
            #S * CPT * flutes
            F = calculate_F(S, CPT, test.tool.flutes)
            Fp = calculate_Fp(F, test.Fp_percent, test.machine.F_Z_max)

            yield UpdateProgress( text = _('Creating single cut test') )


            if S <= test.machine.Smax and S <= test.tool.Smax and F <= test.machine.F_XY_max:
                #create a TestCut
                testcut = TestCut()
                testcut.cut_number=0
                testcut.test=test
                testcut.S = S
                testcut.F = F
                testcut.Fp = Fp
                testcut.Ap = Ap
                testcut.Ae = Ae
                session.flush()

            else:
                yield MessageBox( _('Not all testcuts created because S or F exceeded limits of machine or tool.\n'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)

            yield Refresh()
        else:
            yield MessageBox( _('This test has not been saved to the database, yet. To create testcuts, a test name, machine, tool and material need to be specified!\n'),  icon=QMessageBox.Information,  standard_buttons=QMessageBox.Ok)



registered_processors = [SingleTestCut, SpindleChiploadAlternatingIncrement, Increment]
