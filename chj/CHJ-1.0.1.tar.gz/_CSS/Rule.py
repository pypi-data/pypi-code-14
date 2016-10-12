# -*- coding: utf-8 -*-
# Copyright (C) 2010-2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package CHJ.CSS.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CHJ.CSS.Rule
#
# Purpose
#    Model CSS rules
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#    30-Dec-2010 (CT) `base_level` and `media_rule` added
#    31-Dec-2010 (CT) `Kits` added and used
#    21-Feb-2011 (CT) `Rule.__init__` changed to allow `kits` passed
#                     positionally
#     3-Apr-2013 (CT) Add `__call__`, add argument `proto` to `__init__`
#     8-Apr-2013 (CT) Remove `R` and other abbreviations
#    13-Apr-2014 (CT) Allow list-values in `Rule._formatted_decl`; factor `_gen`
#     9-Jul-2014 (CT) `Rule.__init__` changed to allow `Rule` arguments
#                     passed positionally
#    11-Oct-2016 (CT) Move from `GTW` to `CHJ`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _CHJ                       import CHJ
from   _TFL                       import TFL

import _CHJ._CSS

import _TFL._Meta.Object

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.predicate             import cartesian
from   _TFL.pyk                   import pyk

### Add support for CSS3 elements that need browser-prefixes (e.g.,
### border-radius, ...)
### http://www.usabilitypost.com/2011/02/05/simplify-css-with-less-elements/

def Kits (* ds, ** kw) :
    result = {}
    for d in ds :
        result.update (d)
    result.update (kw)
    return result
# end def Kits

class M_Rule (TFL.Meta.Object.__class__) :
    """Meta class for `Rule`."""

# end class M_Rule

class Rule (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_Rule)) :
    """Model a CSS rule.

    >>> import itertools
    >>> tr = Rule_Pseudo ("target", background_color = "yellow", color = "red")
    >>> r1 = Rule ("tr.row1", "div.row1", color = "grey", clear = "both", children = [tr])
    >>> r2 = Rule ("tr.row2", "div.row2", color = "blue", clear = "both", children = [tr])
    >>> for x in itertools.chain (r1, r2) :
    ...   print (x)
    ...
    tr.row1, div.row1
      { clear : both
      ; color : grey
      }
      tr.row1:target, div.row1:target
        { background-color : yellow
        ; color            : red
        }
    tr.row2, div.row2
      { clear : both
      ; color : blue
      }
      tr.row2:target, div.row2:target
        { background-color : yellow
        ; color            : red
        }

    """

    base_level   = 0
    media_rule   = None
    parent       = None
    parent_sep    = " "

    def __init__ (self, * selectors, ** declarations) :
        proto = declarations.pop ("proto", None)
        if proto :
            self.parent_sep = proto.parent_sep
        self.pop_to_self (declarations, "base_level", "parent", "parent_sep")
        self.children = list (self._pop_children (declarations))
        sels          = []
        kits          = []
        if proto :
            sels.extend (proto._selectors)
            kits.append (proto.declarations)
            self.children = proto.children + self.children
        for s in selectors :
            if isinstance (s, Rule) :
                declarations = dict (s.declarations, ** declarations)
            else :
                (kits if isinstance (s, dict) else sels).append (s)
        self._selectors   = tuple (sels)
        self.declarations = Kits \
            ( * (tuple (kits) + tuple (declarations.pop ("kits", ())))
            , ** declarations
            )
        if self.parent is not None :
            self.parent.children.append (self)
    # end def __init__

    def __call__ (self, * selectors, ** declarations) :
        declarations ["proto"] = self
        return self.__class__ (* selectors, ** declarations)
    # end def __call__

    def copy (self) :
        d = dict \
            ( self.declarations
            , children   = self.children
            , parent_sep = self.parent_sep
            )
        return self.__class__ (* self._selectors, ** d)
    # end def copy

    @property
    def level (self) :
        parent = self.parent
        if parent is not None :
            return parent.level - (not parent.declarations) + 1
        return self.base_level
    # end def level

    @Once_Property
    def selectors (self) :
        parent = self.parent
        parent_sep = self.parent_sep
        if parent is not None :
            return \
                [   parent_sep.join (s)
                for s in cartesian (parent.selectors, self._selectors)
                ]
        ps = parent_sep.strip ()
        return [(ps + s) for s in self._selectors]
    # end def selectors

    def _formatted_decl (self, declarations, sep) :
        def _gen (declarations) :
            for (p, v) in pyk.iteritems (declarations) :
                k = p.replace ("_", "-")
                if not isinstance (v, (tuple, list)) :
                    v = (v, )
                for w in v :
                    yield (k, w)
        pvs    = sorted (_gen (declarations))
        format = "%%s %%-%ds : %%s" % max (len (p) for p in declarations)
        yield format % (("{", ) + pvs [0])
        for p, v in pvs [1:] :
            yield format % (";", p, v)
        yield "}"
    # end def _formatted_decl

    def _pop_children (self, declarations) :
        for c in declarations.pop ("children", []) :
            if c.parent is not None :
                c = c.copy ()
            c.parent = self
            yield c
    # end def _pop_children

    def __iter__ (self) :
        if self.declarations :
            yield self
        for c in self.children :
            for r in c :
                yield r
    # end def __iter__

    def __str__ (self) :
        selectors    = self.selectors
        declarations = self.declarations
        level        = self.level
        indent0      = "  " * level
        indent1      = "  " * (level + 1)
        result       = ""
        if declarations :
            ls     = sum (len (s) for s in selectors) + 2 * (len(selectors) - 1)
            s_sep  = (",\n%s" % indent0) if (ls >= 80)               else ", "
            d_sep  = ("\n%s"  % indent1) if (len (declarations) > 1) else " "
            result = "%s%s%s%s" % \
                ( indent0
                , s_sep.join (selectors)
                , d_sep
                , d_sep.join (self._formatted_decl (declarations, d_sep))
                )
        return result
    # end def __str__

# end class Rule

class Rule_Attr (Rule) :
    """Rule for attribute selection"""

    parent_sep = ""

# end class Rule_Attr

class Rule_Child (Rule) :
    """Rule for a child of another element."""

    parent_sep = " > "

# end class Rule_Child

class Rule_Class (Rule) :
    """Rule for a class."""

    parent_sep = "."

# end class Rule_Class

class Rule_Pseudo (Rule) :
    """Rule for pseudo-classes"""

    parent_sep = ":"

# end class Rule_Pseudo

class Rule_Sibling (Rule) :
    """Rule for adjacent sibling element."""

    parent_sep = " + "

# end class Rule_Sibling

__all__ = tuple \
    ( k for (k, v) in pyk.iteritems (globals ()) if isinstance (v, M_Rule)
    ) + ("Kits", )

if __name__ != "__main__" :
    CHJ.CSS._Export (* __all__)
### __END__ CHJ.CSS.Rule
