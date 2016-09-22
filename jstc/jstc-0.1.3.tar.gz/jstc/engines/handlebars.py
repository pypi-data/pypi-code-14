# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/12
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import subprocess
import errno
import json

import asset

from . import base
from .. import api
from .. import compiler

#------------------------------------------------------------------------------
@asset.plugin('jstc.engines.plugins', 'text/x-handlebars')
class HandlebarsEngine(base.Engine):

  mimetype              = 'text/x-handlebars'
  extensions            = ('.hbs', '.handlebars')
  executable            = 'handlebars'
  parameters            = ()
  softfail              = ('ENOENT',)

  #----------------------------------------------------------------------------
  def __init__(self, executable=None, parameters=None, softfail=None, *args, **kw):
    super(HandlebarsEngine, self).__init__(*args, **kw)
    if executable is not None:
      self.executable = executable
    if parameters is not None:
      self.parameters = tuple(parameters)
    if softfail is not None:
      self.softfail = tuple(softfail)

    # todo: verify `handlebars --version >= 4.0.5`, or if `handlebars`
    #       is not available, cache that information...? prolly not,
    #       that way a server does not need to be restarted if it is
    #       installed (it'll "just start working") -- let pyramid_jitt
    #       or webassets deal with that.

  #----------------------------------------------------------------------------
  def precompile(self, text, attrs):
    args = [self.executable] + list(self.parameters) + ['--string', text, '--simple']
    if attrs.get('name'):
      args += ['--name', attrs.get('name')]
    res = (compiler.Compiler.TYPE_JSFRAG, self.execute(args).strip())
    if attrs.get('partial'):
      return res
    return self.assemble([res + (attrs,)])

  #----------------------------------------------------------------------------
  def execute(self, args, input=None):
    try:
      if input:
        # todo: implement
        raise NotImplementedError()
      return subprocess.check_output(args)
    except OSError as err:
      if err.errno == errno.ENOENT and 'ENOENT' in self.softfail:
        raise api.PrecompilerUnavailable()
      raise

  #----------------------------------------------------------------------------
  def assemble(self, parts):
    ret = '(function(){var t=Handlebars.template,ts=Handlebars.templates=Handlebars.templates||{};'
    for part in parts:
      contentType, content, attrs = part[:3]
      # todo: confirm correct contentType & content?...
      # todo: confirm attrs.name exists?...
      ret += 'ts[{name}]=t({content});'.format(
        name    = json.dumps(attrs.get('name')),
        content = content,
      )
    ret += '})();'
    return (compiler.Compiler.TYPE_JS, ret)

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
