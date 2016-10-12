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
#    CHJ.CSS.Media
#
# Purpose
#    Model CSS media type and queries
#
#    See: http://www.w3.org/TR/css3-mediaqueries/
#
# Revision Dates
#    30-Dec-2010 (CT) Creation
#    21-Jan-2014 (CT) Support `exprs` of type `dict` in `Query._setup_exprs`
#    17-Oct-2014 (CT) Put uppercased names into `Type.Table` because `print`
#    15-Aug-2015 (CT) Use `@eval_function_body` for scoped setup code
#    11-Oct-2016 (CT) Move from `GTW` to `CHJ`
#    ««revision-date»»···
#--

from   __future__                 import print_function, unicode_literals

from   _CHJ                       import CHJ
from   _TFL                       import TFL

import _CHJ._CSS

from   _TFL.Decorator             import eval_function_body
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.pyk                   import pyk

import _TFL._Meta.Object

class M_Media (TFL.Meta.Object.__class__) :
    """Meta class for media types and queries."""

    Nick = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.nick :
            cls.Nick [cls.nick] = cls
    # end def __init__

# end class M_Media

class _Media_ (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_Media)) :
    """Base class for media types and queries."""

    nick            = None

# end class _Media_

class Expression (_Media_) :
    """Media query expression.

    >>> print (MX ("color"))
    (color)
    >>> print (MX ("min_width", "1000px"))
    (min-width: 1000px)
    """

    nick = "MX"

    def __init__ (self, feature, expr = None) :
        self.feature = feature.replace ("_", "-")
        self.expr    = expr
    # end def __init__

    def __str__ (self) :
        if self.expr is not None :
            return "(%s: %s)" % (self.feature, self.expr)
        else :
            return "(%s)" % (self.feature, )
    # end def __str__

# end class Expression

class Query (_Media_) :
    """Media query.

    >>> print (Query ())
    <BLANKLINE>
    >>> print (Query ("screen"))
    screen
    >>> print (MQ ("screen", "color", min_width = "1000px"))
    screen and (color) and (min-width: 1000px)
    >>> print (MQ ("all", "color", min_width = "1000px"))
    (color) and (min-width: 1000px)
    >>> print (MQ (MX ("color"), min_width = "1000px"))
    (color) and (min-width: 1000px)

    Beware: skipping `type` and using strings for `* exprs` fails::

    >>> print (MQ ("color", min_width = "1000px"))
    color and (min-width: 1000px)
    """

    nick = "MQ"

    def __init__ (self, type = None, * exprs, ** kw) :
        if isinstance (type, Expression) :
            exprs = (type, ) + exprs
            type  = None
        self.type = type
        self.flag = kw.pop ("flag", None)
        self._setup_exprs  (exprs, kw)
    # end def __init__

    @property
    def type (self) :
        result = self._type
        if result and result.name == "all" :
            result = None
        return result
    # end def type

    @type.setter
    def type (self, value) :
        if value is not None :
            if not isinstance (value, Type) :
                value = Type (value)
        self._type = value
    # end def type

    def _setup_exprs (self, exprs, kw) :
        self.exprs = []
        add        = self.exprs.append
        for x in exprs :
            if isinstance (x, dict) :
                for f, e in sorted (pyk.iteritems (x)) :
                    add (Expression (f, e))
            else :
                if isinstance (x, pyk.string_types) :
                    x = (x, )
                if not isinstance (x, Expression) :
                    x = Expression (* x)
                add (x)
        for f, e in sorted (pyk.iteritems (kw)) :
            add (Expression (f, e))
    # end def _setup_exprs

    def __str__ (self) :
        type  = self.type
        parts = [str (type)] if type else []
        parts.extend (str (x) for x in self.exprs)
        result = " and ".join (parts)
        if result and self.flag :
            result = self.flag + " " + result
        return result
    # end def __str__

# end class Query

class Rule (_Media_) :
    """Media rule: block of CSS rules specific for a list of media queries.

    >>> from _CHJ._CSS.Rule import Rule as R
    >>> r1 = R ("tr.row1", "div.row1", color = "grey", clear = "both")
    >>> r2 = R ("tr.row2", "div.row2", color = "blue", clear = "both")
    >>> print (r1)
    tr.row1, div.row1
      { clear : both
      ; color : grey
      }
    >>> print (r2)
    tr.row2, div.row2
      { clear : both
      ; color : blue
      }
    >>> qr = Rule (MQ ("screen", "color", min_width = "1000px"), rules = (r1, r2))
    >>> print (qr)
    @media screen and (color) and (min-width: 1000px)
      {
        tr.row1, div.row1
          { clear : both
          ; color : grey
          }
    <BLANKLINE>
        tr.row2, div.row2
          { clear : both
          ; color : blue
          }
      }
    """

    nick = "MR"

    def __init__ (self, * queries, ** kw) :
        assert queries
        self.queries = list (queries)
        self.rules   = list (self._pop_rules (kw))
        assert not kw
    # end def __init__

    def block (self) :
        return "\n\n".join (str (r) for r in self.rules_iter ())
    # end def block

    def rules_iter (self) :
        for r in self.rules :
            for x in r :
                yield x
    # end def rules_iter

    def _pop_rules (self, kw) :
        for r in kw.pop ("rules") :
            if r.media_rule is not None :
                r = r.copy ()
            r.media_rule = self
            r.base_level = 2
            yield r
    # end def _pop_rules

    def __iter__ (self) :
        yield self
    # end def __iter__

    def __str__ (self) :
        queries = tuple (str (s) for s in self.queries)
        ls      = sum   (len (s) for s in queries) + 2 * (len (queries) - 1)
        q_sep   = (",\n%s" % indent0) if (ls >= 80) else ", "
        return "@media %s\n  {\n%s\n  }" % (q_sep.join (queries), self.block ())
    # end def __str__

# end class Rule

class Type (_Media_) :
    """Media type.

    >>> print (Type ("all"))
    all

    >>> print (Type ("print"))
    print

    >>> print (Type ("screen"))
    screen

    >>> print (Type ("Screen"))
    screen

    >>> Type ("screen") is Type ("screen")
    True

    >>> Type ("screen") is Type ("all")
    False

    """

    nick  = "MT"
    Table = {}

    def __new__ (cls, name) :
        name = name.upper ()
        if name in cls.Table :
            result = cls.Table [name]
        else :
            result = cls.Table [name] = cls.__c_super.__new__ (cls)
            result.name = name.lower ()
        return result
    # end def __new__

    def __init__ (self, name) :
        self.name = name.lower ()
    # end def __init__

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Type

@eval_function_body
def _instantiate_standard_types () :
    for _t in ("all", "screen", "print") :
        Type (_t)

@eval_function_body
def _setup_all () :
    global __all__
    _g = globals ()
    _g.update (Type.Table)
    _g.update (M_Media.Nick)
    __all__ = tuple \
        (k for (k, v) in pyk.iteritems (_g) if isinstance (v, (M_Media, Type)))

__doc__ = """
This in the docstring, so that it will be tested before the docstrings of the
various classes in here. The sequence of those tests is not determistic and
sometimes the following test would fail.

    >>> print (", ".join (sorted (Type.Table)))
    ALL, PRINT, SCREEN

"""

if __name__ != "__main__" :
    CHJ.CSS._Export_Module ()
### __END__ CHJ.CSS.Media
