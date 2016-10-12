# -*- coding: utf-8 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TFL.Units.M_Kind
#
# Purpose
#    Meta class for TFL.Units.Kind
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    29-Aug-2008 (CT) s/super(...)/__m_super/
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.M_Class
import _TFL._Units.Unit

class M_Kind (TFL.Meta.M_Class) :
    """Meta class for TFL.Units.Kind"""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        cls.abbrs = abbrs = {}
        cls.units = units = {}
        for u in (cls.base_unit, ) + tuple (cls._units) :
            if u :
                units [u.name] = abbrs [u.abbr] = u
                setattr (cls, u.name, u)
    # end def __init__

# end class M_Kind

if __name__ != "__main__" :
    TFL.Units._Export ("M_Kind")
### __END__ TFL.Units.M_Kind
