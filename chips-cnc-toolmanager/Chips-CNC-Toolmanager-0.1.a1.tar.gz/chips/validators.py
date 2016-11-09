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

from camelot.admin.validator.entity_validator import EntityValidator

class TestcutValidator(EntityValidator):

    def objectValidity(self, entity_instance):
        messages = super(TestcutValidator,self).objectValidity(entity_instance)
        if entity_instance.test.machine:
            if (entity_instance.S > entity_instance.test.machine.Smax):
                messages.append("Spindle Speed is too high for selected machine.")
            if (entity_instance.S < entity_instance.test.machine.Smin):
                messages.append("Spindle Speed is too low for selected machine.")
            if (entity_instance.F > entity_instance.test.machine.F_XY_max):
                messages.append("XY feedrate is too high for selected machine.")
            if (entity_instance.Fp > entity_instance.test.machine.F_Z_max):
                messages.append("Plunge feedrate is too high for selected machine.")
        if entity_instance.test.tool:
            if (entity_instance.S > entity_instance.test.tool.Smax):
                messages.append("Spindle Speed is too high for selected Tool.")

        return messages





#class VoucherValidator(EntityValidator):
#
#    def objectValidity(self, entity_instance):
#        messages = super(VoucherValidator,self).objectValidity(entity_instance)
#        if (not entity_instance.customer):
#            messages.append("Customer needed")
#
#        if (not entity_instance.voucher_type):
#            messages.append("VoucherType needed")
#
#        if (not entity_instance.currency):
#            messages.append("Currency needed")
#
#        if (not entity_instance.voucher_number) or (entity_instance.voucher_number == 0):
#            messages.append("No voucher number")
#
#        if (not entity_instance.customer_number) or (entity_instance.customer_number == 0):
#            messages.append("No customer number, does customer have one?")
#
#        return messages
