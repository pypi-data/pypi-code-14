# -*- coding: utf-8 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TFL.Units.Unit
#
# Purpose
#    Model a unit
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TFL.pyk import pyk

from   _TFL._Meta.totally_ordered import totally_ordered

import _TFL._Meta.Object
import _TFL._Units

@totally_ordered
@pyk.adapt__div__
class Unit (TFL.Meta.Object) :
    """Model a unit kind"""

    def __init__ (self, name, factor = 1.0, abbr = None) :
        self.name   = name
        self.factor = float (factor)
        self.abbr   = abbr
    # end def __init__

    def __eq__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor == rhs
    # end def __eq__

    def __float__ (self) :
        return self.factor
    # end def __float__

    def __lt__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor > rhs
    # end def __lt__

    def __mul__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor * rhs
    # end def __mul__

    def __pow__ (self, rhs) :
        return self.factor ** rhs
    # end def __pow__

    def __repr__ (self) :
        return "%s = %s" % (self.name, self.factor)
    # end def __repr__

    def __truediv__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor / rhs
    # end def __truediv__

# end class Unit

if __name__ != "__main__" :
    TFL.Units._Export ("Unit")
### __END__ TFL.Units.Unit
