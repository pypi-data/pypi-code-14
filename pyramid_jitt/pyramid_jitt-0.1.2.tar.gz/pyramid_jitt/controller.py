# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/10/05
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from pyramid_controllers import Controller, RestController, expose, index, default, lookup
from pyramid.httpexceptions import HTTPNotFound, HTTPMethodNotAllowed

from .engine import Engine

#------------------------------------------------------------------------------
class JitChannelController(Controller):

  #----------------------------------------------------------------------------
  def __init__(self, engine, *args, **kw):
    super(JitChannelController, self).__init__(*args, **kw)
    self.engine = engine

  #----------------------------------------------------------------------------
  @default
  def default(self, request, *rem):
    name = '/'.join(rem if rem and rem != (None,) else [])
    html = self.engine.render(request._realm, request._channel + ':' + name)
    return html


#------------------------------------------------------------------------------
class ChannelController(Controller):

  #----------------------------------------------------------------------------
  def __init__(self, engine, *args, **kw):
    super(ChannelController, self).__init__(*args, **kw)
    self.engine = engine
    self.jitpath = JitChannelController(engine)

  #----------------------------------------------------------------------------
  @index(forceSlash=False)
  def index(self, request):
    html = self.engine.render(request._realm, request._channel)
    return html


#------------------------------------------------------------------------------
class RealmController(Controller):

  #----------------------------------------------------------------------------
  def __init__(self, engine, *args, **kw):
    super(RealmController, self).__init__(*args, **kw)
    self.engine   = engine
    self.CHANNEL  = ChannelController(engine, expose=False)
    self._jitpath = JitChannelController(engine)

  #----------------------------------------------------------------------------
  @lookup
  def lookup(self, request, channel, *rem):
    if channel not in self.engine.channels:
      raise HTTPNotFound()
    # TODO: apply access control here!...
    request._channel = channel
    if request._channel == Engine.CHANNEL_JIT:
      return (self._jitpath, rem)
    return (self.CHANNEL, rem)


#------------------------------------------------------------------------------
class JittController(Controller):

  #----------------------------------------------------------------------------
  def __init__(self, engine, *args, **kw):
    super(JittController, self).__init__(*args, **kw)
    self.engine = engine
    self.REALM  = RealmController(engine, expose=False)

  #----------------------------------------------------------------------------
  @lookup
  def lookup(self, request, realm, *rem):
    if request.method != 'GET':
      raise HTTPMethodNotAllowed()
    if realm not in self.engine.realms:
      raise HTTPNotFound()
    request._realm = realm
    return (self.REALM, rem)


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
