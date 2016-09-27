# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/16
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest
import fso
import os
import textwrap

from .. import api

#------------------------------------------------------------------------------
class TestMustacheEngine(unittest.TestCase):

  #----------------------------------------------------------------------------
  def writecontent(self, files, dedent=True):
    for name, content in files.items():
      path = os.path.join(os.path.dirname(__file__), name)
      pdir = os.path.dirname(path)
      if not os.path.isdir(pdir):
        os.makedirs(pdir)
      with open(path, 'wb') as fp:
        fp.write(textwrap.dedent(content))

  #----------------------------------------------------------------------------
  def test_direct(self):
    from .mustache import MustacheEngine
    engine = MustacheEngine()
    self.assertIs(engine.precompile, api.PrecompilerUnavailable)

  #----------------------------------------------------------------------------
  def test_compiler(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(defaults=dict(inline=True, precompile=True))
    with fso.push() as overlay:
      self.writecontent({
        'test/template.mustache': 'A mustache template.',
      })
      self.assertEqual(
        compiler.render_assets(
          'jstc:engines/test/template.mustache', 'engines/test'),
        '<script type="text/x-mustache" data-template-name="template">A mustache template.</script>'
      )


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
