# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/23
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import morph

from .engine import Engine
from .controller import JittController

#------------------------------------------------------------------------------

CONFIG_PREFIX           = 'jitt.'
DEFAULT_MOUNT_NAME      = 'JittController'
DEFAULT_MOUNT_PATH      = Engine.DEFAULT_MOUNT_PATH

#------------------------------------------------------------------------------
def includeme(config):
  '''
  Adds a "Just-In-Time" template compilation and packaging service to
  the specified `config` regisry. See
  `https://github.com/canaryhealth/pyramid_jitt`_ for details.
  '''
  settings = morph.pick(config.get_settings(), prefix=CONFIG_PREFIX)
  engine   = Engine(settings=settings)
  # todo: determine what the "correct" way of providing a Pyramid
  #       service is...
  config.registry.jitt = engine
  # /todo
  path = settings.get('mount-path', DEFAULT_MOUNT_PATH).strip()
  if path:
    name = settings.get('mount-name', DEFAULT_MOUNT_NAME).strip()
    config.include('pyramid_controllers')
    config.add_controller(name, path, JittController(engine))

#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
