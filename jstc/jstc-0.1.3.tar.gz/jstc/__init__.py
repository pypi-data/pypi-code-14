# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/15
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

'''
The `jstc` Python package compiles and packages JavaScript templates
for delivery to browsers for client-side evaluation.

See `LICENSE.txt` for licensing details.
'''

from .compiler import Compiler
from .api import *

#------------------------------------------------------------------------------
_default_compiler = None

#------------------------------------------------------------------------------
def get_default_compiler():
  '''
  Returns the global default `jstc.compiler.Compiler` singleton used
  by the `jstc.compile` and `jstc.render*` functions.
  '''
  global _default_compiler
  if _default_compiler is None:
    _default_compiler = Compiler()
  return _default_compiler

#------------------------------------------------------------------------------
def set_default_compiler(compiler):
  '''
  Sets the global default `jstc.compiler.Compiler` singleton used by
  the `jstc.compile` and `jstc.render*` functions.
  '''
  global _default_compiler
  _default_compiler = compiler
  return _default_compiler

#------------------------------------------------------------------------------
for method in ('compile', 'render_assets'):
  # todo: copy over method args/params signature so that ``help(jstc)``
  #       reports that correctly...
  meth = getattr(Compiler, method)
  def _makefunc(method):
    def _func(*args, **kw):
      return getattr(get_default_compiler(), method)(*args, **kw)
    return _func
  _func = _makefunc(method)
  for attr in ('__doc__', '__name__'):
    setattr(_func, attr, getattr(meth, attr))
  locals()[method] = _func
del method, attr

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
