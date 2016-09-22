# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/12
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import asset

from . import base
from .. import api

#------------------------------------------------------------------------------
@asset.plugin('jstc.engines.plugins', 'text/x-mustache')
class MustacheEngine(base.Engine):

  mimetype              = 'text/x-mustache'
  extensions            = ('.mustache',)
  precompile            = api.PrecompilerUnavailable


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
