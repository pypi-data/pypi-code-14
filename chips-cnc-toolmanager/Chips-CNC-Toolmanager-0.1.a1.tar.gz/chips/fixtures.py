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


#from unicodeCSV import UnicodeReader
from camelot.model.fixture import Fixture
from model import *

def update_machines():
    """update machines"""
    machines = [
                dict(fkey = u'generic',  values = dict(name = u"Generic Table Router", F_XY_max = 9000 , F_Z_max = 500 , Smin =6000, Smax=24000, safe_z=20 ))
                ]
    for m in machines:
        Fixture.insert_or_update_fixture(Machine, fixture_key=m['fkey'], values=m['values'])

#TODO: TOOL, Material

#def update_accounts_list(filename):
#    if FixtureVersion.get_current_version( u'Einfacher Kontenplan DE' ) == 0:
#        reader = UnicodeReader( open( filename ) )
#        print reader.next()
#        for line in reader:
#            acc = Account()
#            acc.number = int(line[0])
#            acc.name = unicode(line[1])
#            acc.type = unicode(line[2])
#            acc.tax_account = line[3] == u"True"
#            acc.in_use =line[4] == u"True"
#
#        FixtureVersion.set_current_version( u'Einfacher Kontenplan', 1 )
#        #session.flush()

def update_fixtures():
    """update a static db data"""
    update_machines()
    #update_accounts_list("./fixture_data/Einfacher_Kontenplan.csv")
