# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/23
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import morph

from .engine import Engine

#------------------------------------------------------------------------------

CONFIG_PREFIX           = 'jitt.'

#------------------------------------------------------------------------------
def includeme(config):
  '''
  Adds a "Just-In-Time" template compilation and packaging service to
  the specified `config` regisry. See
  `https://github.com/canaryhealth/pyramid_jitt`_ for details.
  '''
  # todo: determine what the "correct" way of providing a Pyramid
  #       service is...
  config.registry.jitt = Engine(
    settings = morph.pick(config.get_settings(), prefix=CONFIG_PREFIX),
  )

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
