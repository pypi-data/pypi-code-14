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


from __future__ import division
import os,  codecs

from sqlalchemy.schema import Column
import sqlalchemy.types

from camelot.admin.entity_admin import EntityAdmin
from camelot.core.orm import Entity
from camelot.view.controls import delegates
from camelot.view import forms
#from camelot.view.utils import text_from_richtext
from camelot.core.orm import ManyToOne,  OneToMany
import camelot.types
from camelot.core.utils import ugettext_lazy as _
from camelot.core.utils import ugettext as __

from chips.actions import *
from chips.processors import *
from chips.validators import *
from chips import calculations

#TODO: fix transparency for icons or make gb white
#TODO: thik if it would be a ggod idea to have an action to create a new material definition (modified copy) from TestCut

#Machine
class Machine(Entity):
    __tablename__='machines'


    #load default precode from flat file
    try:
        f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "chips/default_gcodes/machine_pre.nc"), "r",  "utf-8")
        lines = f.readlines()
        default_precode = u""
        for line in lines:
            default_precode = default_precode + unicode(line).strip() + u"<br/>"
        f.close()
    except:
        default_precode = None

    #load default postcode from flat file
    try:
        f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "chips/default_gcodes/machine_post.nc"), "r", "utf-8")
        lines = f.readlines()
        default_postcode = u""
        for line in lines:
            default_postcode = default_postcode + unicode(line).strip() + u"<br/>"
        f.close()
    except:
        default_postcode = None

    name = Column(sqlalchemy.types.Unicode(100),  nullable=False)
    comment = Column(camelot.types.RichText())
    F_XY_max = Column(sqlalchemy.types.Float(), nullable = False,  default=9000)
    F_Z_max = Column(sqlalchemy.types.Float(), nullable = False,  default=500)
    Smin = Column(sqlalchemy.types.Float(), nullable = False,  default=5000)
    Smax = Column(sqlalchemy.types.Float(), nullable = False,  default=26000)
    safe_z = Column(sqlalchemy.types.Float(), nullable = False,  default=20)
    precode = Column(camelot.types.RichText(),  nullable=True,  default = default_precode)
    postcode =  Column(camelot.types.RichText(),  nullable=True,  default = default_postcode)

    def __unicode__(self):
        return unicode(self.name) or 'unknown machine'

    class Admin(EntityAdmin):
        verbose_name = _('Machine')
        verbose_name_plural =_('Machines')
        delete_mode = 'on_request'

        #list
        list_display = ['name',  'comment']
        list_filter = []

        #form
        form_display = ['name',
                        forms.TabForm([
                        (_('Machine properties'), ['F_XY_max','F_Z_max', 'Smin', 'Smax','safe_z', 'comment']),
                        (_('G-Code'), ['precode', 'postcode'])
                        ])
                        ]
        form_size = (800, 600)
        field_attributes = dict(
            #type = dict(delegate = delegates.ComboBoxDelegate)
            F_XY_max = dict(name = _(u'Maximum feedrate XY axes'), suffix='mm/min', tooltip=_(u'Maximum feedrate of the machine in horizontal directions (X and Y axis).')),
            F_Z_max = dict(name = _(u'Maximum feedrate Z axis'),suffix='mm/min', tooltip=_(u'Maximum feedrate of the machine in vertical directions (Z axis).')),
            Smin = dict(name = _(u'Minimum spindle speed [S]'), suffix='rpm', tooltip=_(u'Minimum spindle speed of the machine.')),
            Smax = dict(name = _(u'Maximum spindle speed [S]'),suffix='rpm', tooltip=_(u'Maximum spindle speed of the machine.')),
            safe_z = dict(name = _(u'Safe Z height'),suffix='mm', tooltip=_(u'Safe Z height at which rapid moves can be performed.')),
            precode =dict(name = _(u'G-Code, program start'),tooltip=_(u'G-Code that is performed at the beginning of a CNC program. \n You can use variables documented in the help pages here.')),
            postcode = dict(name = _(u'G-Code program end'),tooltip=_(u'G-Code that is performed at the end of a CNC program.\n You can use variables documented in the help pages here.')),

        )
        form_actions=[]  #[ActionOne(),ActionTwo(),..


#Tools
class Tool(Entity):
    __tablename__='tools'
    recipes = OneToMany('Recipe')
    tests= OneToMany('Test')

    name = Column(sqlalchemy.types.Unicode(100),  nullable=False)
    tool_number = Column(sqlalchemy.types.Integer(), nullable = False,  default=0)
    type = Column(camelot.types.Enumeration(choices=[(0, None), (1, __(u"Square End")), (2, __(u"Ball end")), (3, __(u"Radiused")), (4, __(u"V-cutting")), (5, __(u"Fishtail")), (6, __(u"Engraving")), (7, __(u"Other"))], index=True,  default=__(u"Square End")))
    image = Column(camelot.types.Image( upload_to=u'tool_images'))
    flutes = Column(sqlalchemy.types.Integer(), nullable = False,  default=1)
    cutting_angle =Column(sqlalchemy.types.Float(), nullable = False,  default=180.0)
    diameter = Column(sqlalchemy.types.Float(), nullable = False,  default=1)
    cutting_length = Column(sqlalchemy.types.Float(), nullable = False,  default = 20)
    full_length = Column(sqlalchemy.types.Float(), nullable = False,  default=40)
    tool_material=Column(camelot.types.Enumeration(choices=[(0, None), (1, __(u"Carbide-Tipped")), (2, __(u"Cobalt")), (3, __(u"High Speed Steel (HSS)")), (4, __(u"Powdered Metal (PM) Cobalt")), (5, __(u"Solid Carbide")), (6, __(u"Titane")), (7, __(u"Other"))], index=True, default=u"Solid Carbide"))
    coating = Column(camelot.types.Enumeration(choices=[(0, None), (1, __(u"AlCrTiN")), (2, __(u"AlTiCrN")), (3, __(u"PCD")), (4, __(u"TiAlCrN")), (6, __(u"TiAlN Titanium aluminium nitride (black)")), (7, __(u"TiCN (bluish)")), (8, __(u"TiCN (bluish)")), (9, __(u"TiN Titanium Nitride (yellowish)")), (10, __(u"Other"))],  index=True,  default="None"))
    Smax= Column(sqlalchemy.types.Integer(), nullable = False,  default=25000)
    comment = Column(camelot.types.RichText())
    manufacturer = Column(sqlalchemy.types.Unicode(100))

    def __unicode__(self):
        return unicode(self.name) or 'unknown tool'

    class Admin(EntityAdmin):
        verbose_name = _('Tool')
        verbose_name_plural = _('Tools')
        delete_mode = 'on_request'

        #list
        list_display = ['name','tool_number','type','diameter','flutes','cutting_angle','manufacturer','cutting_length']
        list_filter = []

        #form
        form_display = list_display + ['full_length','tool_material', 'coating', 'Smax', 'image', 'comment', 'recipes', 'tests' ]
        form_display = ['name',
            forms.TabForm([
                (_('Tool'), [
                    forms.HBoxForm([['type', 'tool_material', 'coating', 'diameter', 'flutes', 'cutting_length', 'full_length', 'cutting_angle', 'Smax'], ['tool_number', 'manufacturer','image', 'comment']])
                ]),
                (_('Recipes'), ['recipes']),
                (_('Tests'), ['tests']),
                ])
        ]
        form_size = (800, 600)
        field_attributes = dict(
            diameter = dict(suffix='mm'),
            cutting_length = dict(name = _(u'Flute length'),suffix='mm'),
            full_length = dict(suffix='mm'),
            flutes= dict(name = _(u'Number of flutes')),
            cutting_angle = dict(suffix=u'\N{DEGREE SIGN}',  tooltip=_(u'Angle of the flutes at the tip. A flat end bit would be 180\N{DEGREE SIGN}')),
            Smax = dict(name = _(u'Maximum spindle speed [S]'),suffix='rpm'),
            tool_number = dict(tooltip=_(u'Tool number in the toolchanger. This can be used to issue toolchange commands.'))
            #type = dict(delegate = delegates.ComboBoxDelegate)
        )
        form_actions=[]  #[ActionOne(),ActionTwo(),..


#Material
class Material(Entity):
    __tablename__='materials'

    name = Column(sqlalchemy.types.Unicode(100),  nullable=False)
    type = Column(camelot.types.Enumeration(choices=[(0, None), (1, __(u"Metal")), (2, __(u"Plastic")), (3, __(u"Wood")), (4, __(u"Foam")), (5, __(u"Ceramics")), (6, __(u"Composites")), (7, __(u"Other"))]), index=True,  nullable=False)
    image = Column(camelot.types.Image( upload_to=u'material_images'))
    recommended_VCC = Column(sqlalchemy.types.Integer())
    recommended_CPT = Column(sqlalchemy.types.Float()) #percent!
    recommended_Ap = Column(sqlalchemy.types.Float()) #percent!
    hardness =Column(sqlalchemy.types.Float())
    machinability = Column(camelot.types.Rating())
    comment = Column(camelot.types.RichText())
    tests= OneToMany('Test')
    recipes = OneToMany('Recipe')



    def __unicode__(self):
        return unicode(self.type +" - "+ self.name) or 'unknown material'

    class Admin(EntityAdmin):
        verbose_name = _('Material')
        verbose_name_plural = _('Materials')
        delete_mode = 'on_request'

        #list
        list_display = ['name','type','comment','hardness','recommended_VCC','recommended_CPT', 'machinability']
        list_filter = []

        #form
        form_display = [
            forms.HBoxForm([['name'], []]),

            forms.TabForm([
                (_('Material'), [forms.HBoxForm([['type', 'recommended_VCC', 'recommended_CPT','recommended_Ap','machinability', 'hardness',  forms.Stretch()], ['image']]), 'comment',]),
                (_('Recipes'), ['recipes']),
                (_('Tests'), ['tests']),
                ])
        ]
        form_size = (800, 600)
        field_attributes = dict(
            recommended_VCC = dict(name = _(u'Recommended surface speed (VCC)'), suffix='m/min', tooltip='Recommended surface speed.\nThis should be a conservative starting point and can usually be obtained from material tables or bit manufacturer recommendations.'),
            recommended_CPT  = dict(name = _(u'Recommended chipload (CPT)'), suffix='%', precision=2,  tooltip=u'Recommended chipload in % of tool diameter. \nThis should be a conservative starting point and can usually be obtained from material tables or bit manufacturer recommendations.'),
            recommended_Ap = dict(name = _(u'Recommended depth of cut (Ap)'), suffix='%', precision=2,  tooltip=u'Recommended depth of cut in % of tool diameter. \nThis should be a conservative starting point and can usually be obtained from material tables or bit manufacturer recommendations.'),

            #type = dict(delegate = delegates.ComboBoxDelegate)
        )
        form_actions=[]  #[ActionOne(),ActionTwo(),..

        list_search = ['name','type', 'machinability', 'recommended_VCC', 'recommended_CPT']
        expanded_list_search = list_search


#Recipe
class Recipe(Entity):
    __tablename__='recipes'

    machine = ManyToOne('Machine',  required=True)
    tool = ManyToOne('Tool', required=True)
    material = ManyToOne('Material', required=True)
    test = ManyToOne('Test')

    name = Column(sqlalchemy.types.Unicode(100),  nullable=False)
    S =Column(sqlalchemy.types.Float(), default=0.0)
    F =Column(sqlalchemy.types.Float(), default=0.0)
    Fp =Column(sqlalchemy.types.Float(), default=0.0)
    Ap =Column(sqlalchemy.types.Float(precision=4), default=0.0)
    Ae =Column(sqlalchemy.types.Float(precision=4), default=0.0)

    coolant = Column(sqlalchemy.types.Unicode(100))
    rating = Column(camelot.types.Rating())
    comment = Column(camelot.types.RichText())



    def __unicode__(self):

        if self.material and self.tool and self.machine:
            return unicode("%s, %s-flute %smm X %smm, %s - %s on %s" %(self.material.name,  self.tool.flutes,  self.tool.diameter, self.tool.cutting_length, self.tool.type,  self.tool.name,  self.machine.name))
        else:
            return u'unknown recipe'

    @property
    def MRR(self):
        if self.Ae > 0  and self.F > 0 and self.Ap > 0:
            if self.Ae < self.tool.diameter:
                return (self.Ae * self.Ap * self.F) /1000
            else:
                return (self.tool.diameter * self.Ap * self.F) / 1000
        else:
            return 0

    @property
    def CPT(self):
        #(% CPT /100 = F / (RPM x D x No. Flutes))
        if self.S > 0 and self. F > 0 and self.tool:
            return self.F / (self.S * self.tool.flutes)
            #return self.F / (self.S * self.tool.diameter * self.tool.flutes) #this would calculate CPT in %
        else:
            return 0

    @property
    def VCC(self):
        if self.S > 0 and self.tool:
            return calculations.VCC(self.S, self.tool.diameter)



    class Admin(EntityAdmin):
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
        delete_mode = 'on_request'

        #list
        list_display = ['name','material','tool','rating', 'machine','comment', 'S', 'F', 'Fp', 'Ap', 'Ae', 'coolant', 'VCC', 'CPT']
        list_filter = []

        #form
        form_display = ['name','rating','machine','material','tool',
            forms.TabForm([
                (_('Recipe'), ['S','F','Fp','Ap','Ae','coolant','MRR','CPT', 'VCC']),
                (_('Info'), ['comment','test']),
                ])
            ]

        form_size = (800, 600)
        field_attributes = dict(

            test=dict(editable=False),
            S=dict(name = _(u'Spindle speed [S]'), suffix="rpm", tooltip = _(u'Spindle speed')),
            F=dict(name = _(u'Feedrate [F]'), suffix="mm/min", tooltip = _(u'Feedrate')),
            Fp=dict(name = _(u'Plunge feed [Fp]'), suffix="mm/min", tooltip = _(u'Plunge feedrate')),
            Ap=dict(name = _(u'Depth of cut [Ap]'), suffix="mm",  tooltip = _(u'Depth of cut')),
            Ae=dict(name = _(u'Width of cut [Ae]'), suffix="mm", tooltip = _(u'Width of cut')),
            CPT = dict(name = _(u'Chipload [CPT]'), delegate= delegates.FloatDelegate, precision=4,   suffix=u"mm", tooltip = _(u'Chipload')),
            MRR = dict(name = _(u'Material remove rate [MRR]'), delegate= delegates.FloatDelegate, precision=2,  suffix=u"cm\xb3/min", tooltip = _(u'Material removal rate. \nResults are only accurate for square end tools!')),
            VCC = dict(name = _(u'Surface speed [VCC]'), delegate= delegates.FloatDelegate, precision=0,   suffix=u"m/min", tooltip = _(u'Surface speed')),
            #type = dict(delegate = delegates.ComboBoxDelegate)
        )
        form_actions=[]  #[ActionOne(),ActionTwo(),..

        list_search = ['name','rating','S', 'F', 'Ap', 'Ae']
        expanded_list_search = list_search

#Test
class Test(Entity):
    __tablename__='tests'

    #relations
    machine = ManyToOne('Machine',  required = False) #TODO: is only set through _machine property, requirement is specified by field_attributes, seems not to work :-(
    tool = ManyToOne('Tool', required = False)
    material = ManyToOne('Material', required = False)
    testcuts = OneToMany('TestCut', cascade='all, delete, delete-orphan',  single_parent=True)

    #load default pre_cut_gcode from flat file
    try:
        f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "chips/default_gcodes/pre_cut.nc"), "r",  "utf-8")
        lines = f.readlines()
        default_pre_cut_gcode = u""
        for line in lines:
            default_pre_cut_gcode = default_pre_cut_gcode + unicode(line).strip() + u"<br/>"
        f.close()
    except:
        default_pre_cut_gcode = None

    #load default cut_gcode from flat file
    try:
        f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "chips/default_gcodes/cut.nc"), "r",  "utf-8")
        lines = f.readlines()
        default_cut_gcode = u""
        for line in lines:
            default_cut_gcode = default_cut_gcode + unicode(line).strip() + u"<br/>"
        f.close()
    except:
        default_cut_gcode = None

    #load default post_cut_gcode from flat file
    try:
        f = codecs.open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "chips/default_gcodes/post_cut.nc"), "r",  "utf-8")
        lines = f.readlines()
        default_post_cut_gcode = u""
        for line in lines:
            default_post_cut_gcode = default_post_cut_gcode + unicode(line).strip() + u"<br/>"
        f.close()
    except:
        default_post_cut_gcode = None


    name =  Column(sqlalchemy.types.Unicode(100), nullable = False)
    comment = Column(camelot.types.RichText())
    number_of_testcuts = Column(sqlalchemy.types.Integer(), nullable = False,  default=6)
    start_S =Column(sqlalchemy.types.Float(), nullable = False, default=0)
    S_increment=Column(sqlalchemy.types.Float(), nullable = False, default=0)
    start_CPT=Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    CPT_increment=Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    Ap =Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    Ap_increment =Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    Ae =Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    Ae_increment =Column(sqlalchemy.types.Float(precision=4), nullable = False, default=0)
    Fp_percent =Column(sqlalchemy.types.Float(), nullable = False, default=100)
    coolant = Column(sqlalchemy.types.Unicode(100))

    pre_cut_gcode = Column(camelot.types.RichText(),  default= default_pre_cut_gcode)
    cut_gcode = Column(camelot.types.RichText(), default= default_cut_gcode)
    post_cut_gcode = Column(camelot.types.RichText(), default= default_post_cut_gcode)


    def __unicode__(self):
        if self.tool and self.material:
            return unicode("%s, Tool: %s, Material: %s" %(self.name, self.tool.name,  self.material.name)) or 'unknown test'
        else:
            return unicode(self.name) or 'unknown test'


    #hooks to catch chages for related entities – used for calculations based on selected relations for Tool, Machine and Material
    #Machine property
    def _set_machine(self, machine):
        self.machine = machine
        self.update_default_parameters()

    def _get_machine(self):
        return self.machine

    _machine = property( _get_machine,  _set_machine )

    #Tool propery
    def _set_tool(self, tool):
        self.tool = tool
        self.update_default_parameters()

    def _get_tool(self):
        return self.tool

    _tool = property( _get_tool,  _set_tool )

    #Material property
    def _set_material(self, material):
        self.material = material
        self.update_default_parameters()

    def _get_material(self):
        return self.material

    _material = property( _get_material,  _set_material )


    def update_default_parameters(self):
        """is triggered by any of machine, tool or material properties and provides some calculations for good default parameters"""
        #update default values for S, CPT, WOC, Ap, Ae is set to tool diameter
        #only update if fields are 0
        #use functions from chips.calculations.S(mat_vcc,  tool_diameter)

        #update start_S
        if self.tool and self.machine and self.material:
            if self.start_S == 0 or self.start_S == None:
                S = calculations.S(self.material.recommended_VCC, self.tool.diameter)
                #check for speed limits of spindle and tool
                if S <= self.machine.Smax and S <= self.tool.Smax:
                    self.start_S = S
                elif S >= self.tool.Smax <= self.machine.Smax:
                    self.start_S = self.tool.Smax
                    self.S_increment = 0
                elif S <= self.tool.Smax >= self.machine.Smax:
                    self.start_S = self.machine.Smax
                    self.S_increment = 0

        #update start_CPT
        if self.tool and self.material:
            if self.start_CPT == 0 or self.start_CPT == None:
                self.start_CPT = round(self.tool.diameter / 100 * self.material.recommended_CPT , 4)

        #update Ap
        if self.tool and self.material:
            if self.Ap == 0 or self.Ap == None:
                self.Ap = round(self.tool.diameter / 100 * self.material.recommended_Ap , 4)

        #update Ae
        if self.tool:
            if self.Ae == 0 or self.Ae == None:
                self.Ae = self.tool.diameter


    class Admin(EntityAdmin):
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')
        delete_mode = 'on_request'

        #list
        list_display = ['name','_machine','_tool','_material','comment']
        list_filter = []

        #form
        form_display = [
                'name',
                forms.TabForm([
                (_('1. Machine / Tool / Material'), ['_machine', '_tool',  '_material', 'comment']),
                (_('2. Test Parameters'), [
                    forms.HBoxForm([
                        ['number_of_testcuts', 'start_S', 'S_increment', 'start_CPT', 'CPT_increment', 'Fp_percent'],
                        ['Ap', 'Ap_increment','Ae' , 'Ae_increment', 'coolant']
                        ])
                    ]),
                (_('3. G-Code'), ['pre_cut_gcode', 'cut_gcode',  'post_cut_gcode']) ],
                ),
                'testcuts'
        ]

        form_size = (1050, 768)
        field_attributes = dict(
            _machine = dict(name= _(u'Machine'),  delegate=delegates.Many2OneDelegate, target=Machine, editable=True, required=True),
            _tool = dict(name= _(u'Tool'), delegate=delegates.Many2OneDelegate, target=Tool, editable=True, required=True),
            _material = dict(name= _(u'Material'), delegate=delegates.Many2OneDelegate, target=Material, editable=True, required=True),
            number_of_testcuts=dict(name= _(u'Number of testcuts'), tooltip=_(u'The number of thestcuts that should be generated. \n(If feedrates or spindle speed exceeds the limits of the machine or the tool, steps may be skipped.)')),
            start_S = dict(name=_(u'Spindle speed [S]'), suffix='rpm',  tooltip=_(u'Spindle speed for the first testcut. Use a conservative value here. \nYou can calculate this based on the materials surface speed recommendation and the tools diameter with the spindle speed calculator.')),
            S_increment = dict(name=_(u'Speed increment [S+]'), suffix='rpm', tooltip=_(u'Increase amount for spindle speed')),
            start_CPT = dict(name=_(u'Chipload [CPT]'),suffix='mm', tooltip=_(u'Chipload for the first testcut. Use a conservative value here. \nYou can calculate this based on the materials chipload recommendation in % and the tools diameter with the chipload calculator.')),
            CPT_increment = dict(name=_(u'Chipload increment [CPT+]'),suffix='mm', tooltip=_(u'Increase amount for chipload')),
            Ap = dict(name=_(u'Depth of cut [Ap]'),suffix='mm',  precision=3,  tooltip=_(u'Ap (depth of cut). Use a very conservative value for S_CPT_increment tests.\n Optimum Ap should be optained in separate Ap_Ae_increment_tests, once optimal S and CPT values are evaluated.')),
            Ap_increment = dict(name=_(u'Depth of cut increment [Ap+]'),suffix='mm', precision=3, tooltip=_(u'Increase amount for Ap (depth of cut). \nUsually you want to set this to zero for S_CPT_increment')),
            Ae = dict(name=_(u'Width of cut [Ae]'),suffix='mm', precision=3, tooltip=_(u'Ae (width of cut). Use tool diameter for S_CPT_increment tests since we need slot cuts. \nOptimum Ae can be optained once optimal S and CPT values are evaluated.')),
            Ae_increment = dict(name=_(u'Width of cut increment [Ae+]'),suffix='mm', precision=3, tooltip=_(u'Increase amount for Ae (width of cut).\n Usually you want to set this to zero for S_CPT_increment')),
            Fp_percent = dict(name=_(u'Plunge feed [Fp]'), suffix='%', tooltip=_(u'Plunge feed - feedrate for Z axis in percent of Feedrate for XY axes. (Set 100% if both should be the same.)')),
            pre_cut_gcode = dict(name = _(u'G-Code before cut'), tooltip = _(u"G-Code that is executed before every testcut. \nYou can use variables like in {{cut_F}}, {{cut_S}}, {{export_cut_number}}, etc. here. \nYou can also do basic calculations like {{export_cut_number*15.0}} (multiplies the current cut number by 15mm i.e. to calculate an offset.). \nSee full list of variables on help pages.")),
            cut_gcode = dict(name = _(u'Cutting G-Code'), tooltip = _(u"G-Code that is executed to perform testcuts.\nYou can use variables like in {{cut_F}}, {{cut_S}}, {{export_cut_number}}, etc. here. \nYou can also do basic calculations like {{export_cut_number*15.0}} (multiplies the current cut number by 15mm i.e. to calculate an offset.). \nSee full list of variables on help pages.")),
            post_cut_gcode = dict(name = _(u'G-Code after cut'), tooltip = _(u"G-Code that is executed after every testcut.\nYou can use variables like in {{cut_F}}, {{cut_S}}, {{export_cut_number}}, etc. here. \nYou can also do basic calculations like {{export_cut_number*15.0}} (multiplies the current cut number by 15mm i.e. to calculate an offset.). \nSee full list of variables on help pages.")),
        )
        form_actions=[ExportGCode(), ClearTestCuts()] #add actions for calculating start_S and start_CPT, based on tool and Material recoomendations
        for processor in registered_processors:
            form_actions.insert(len(form_actions) -2, (processor())) #ad test processor actions here

        list_search = ['name','number_of_testcuts', 'start_S', 'start_CPT','Ap', 'Ae', 'coolant']
        expanded_list_search = list_search
        #save_mode="on_change"


#TestCut
class TestCut(Entity):
    __tablename__='testcuts'

    test = ManyToOne('Test')

    cut_number = Column(sqlalchemy.types.Integer(), nullable=False,  default=1)
    enabled=Column(sqlalchemy.types.Boolean(),  default=True)
    S =Column(sqlalchemy.types.Float(),  default=0.0)
    F =Column(sqlalchemy.types.Float(), default=0.0)
    Fp =Column(sqlalchemy.types.Float(), default=0.0)
    Ap =Column(sqlalchemy.types.Float(precision=4), default=0.0)
    Ae =Column(sqlalchemy.types.Float(precision=4), default=0.0)

    image = Column(camelot.types.Image( upload_to=u'testcut_images'))
    comment = Column(camelot.types.RichText())
    rating = Column(camelot.types.Rating())


    def __unicode__(self):
        if self.test.tool and self.test.material:
            return unicode("%s - Tool:%s - S%s, F%s, Fp%s, Ap: %s Ae:%s") %(self.test.name, self.test.tool.name,  round(self.S), round(self.F), round(self.Fp),  round(self.Ap, 2),  round(self.Ae, 2))+unicode(self.id) or 'unknown testcut'
        else:
            return unicode("%s - S%s, F%s, Fp%s, Ap: %s Ae:%s") %(self.test.name, round(self.S), round(self.F), round(self.Fp),  round(self.Ap, 2),  round(self.Ae, 2))+unicode(self.id) or 'unknown testcut'


    @property
    def MRR(self):
        if self.Ae > 0  and self.F > 0 and self.Ap > 0 and self.test.tool:
            if self.Ae < self.test.tool.diameter:
                return (self.Ae * self.Ap * self.F) /1000
            else:
                return (self.test.tool.diameter * self.Ap * self.F) / 1000
        else:
            return 0

    @property
    def CPT(self):
        #(% CPT /100 = F / (RPM x D x No. Flutes))
        if self.S > 0 and self. F > 0 and self.test.tool:
            return self.F / (self.S * self.test.tool.flutes)
        else:
            return 0

    @property
    def VCC(self):
        if self.S > 0 and self.test.tool:
            return calculations.VCC(self.S, self.test.tool.diameter)


    class Admin(EntityAdmin):
        validator = TestcutValidator
        verbose_name = _('TestCut')
        verbose_name_plural = _('TestCuts')
        delete_mode = 'on_request'

        #list
        list_display = ['cut_number','enabled','S','F','Fp','Ap','Ae','CPT','MRR','VCC','rating','comment', 'image']
        list_filter = []

        #form
        form_display = [
            forms.HBoxForm([
                ['cut_number','enabled','S', 'F','Fp','Ap','Ae'],
                ['rating','image', 'CPT','MRR','VCC', forms.Stretch()]
            ]),
            'comment'
            ]
        form_size = (800, 600)
        field_attributes = dict(
            cut_number =dict(name=_(u'order'),  editable=False),
            S = dict(name=_(u'S'),suffix='rpm'),
            CPT = dict(name=_(u'CPT'),suffix='mm',  delegate= delegates.FloatDelegate,  precision=4, tooltip = _(u'Chipload per tooth')),
            MRR = dict(name=_(u'MRR'),suffix=u'cm\xb3/min', delegate= delegates.FloatDelegate,  precision=2,  tooltip = _(u'Material remove rate. \nResults are only accurate for square end tools!')),
            VCC = dict(name = _(u'[VCC]'), delegate= delegates.FloatDelegate, precision=0,   suffix=u"m/min", tooltip = _(u'Surface speed')),
            Ap = dict(nsuffix='mm',  tooltip = _(u'Depth of cut')),
            Ae = dict(suffix='mm',  tooltip = _(u'Width of cut')),
            F = dict(suffix='mm/min', tooltip = _(u'Feedrate')),
            Fp = dict(suffix='mm/min', tooltip = _(u'Plunge feedrate')),
            #type = dict(delegate = delegates.ComboBoxDelegate)
        )
        form_actions=[SaveAsRecipe()]  #[ActionOne(),ActionTwo(),..


