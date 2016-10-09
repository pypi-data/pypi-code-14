# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/23
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import logging
import os.path
import cgi
import json

from six.moves.urllib.parse import quote as urlquote
import yaml
import asset
import morph
from aadict import aadict

try:
  from beaker.cache import cache_region
except ImportError:
  cache_region = None

#------------------------------------------------------------------------------

log = logging.getLogger(__name__)

#------------------------------------------------------------------------------
class Engine(object):

  DEFAULT_REALM         = 'default'
  DEFAULT_CHANNEL       = 'inline'
  DEFAULT_NODEID        = 'Templates'
  DEFAULT_NODESTYLE     = {
    'display'             : 'none',
    'visibility'          : 'hidden',
    'opacity'             : '0',
    'width'               : '0',
    'height'              : '0',
  }
  DEFAULT_COMPILER      = 'jstc:Compiler'
  DEFAULT_CACHEREGION   = 'pyramid_jitt'
  DEFAULT_DEFERREDHTML  = 'pyramid_jitt:res/jittloader.html'
  DEFAULT_DEFERREDJS    = 'pyramid_jitt:res/jittloader-jquery.js'
  DEFAULT_MOUNT_PATH    = '/jitt'
  DEFAULT_MOUNT_HOST    = ''
  DEFAULT_LOADERALWAYS  = 'true'

  CHANNEL_INLINE        = 'inline'
  CHANNEL_DEFERRED      = 'deferred'
  CHANNEL_PROTECTED     = 'protected'
  CHANNEL_JIT           = 'jit'
  CHANNELS              = [locals()[k] for k in locals().keys() if k.startswith('CHANNEL_')]

  SETTINGS_REALM_TOKEN  = '@'
  SETTINGS_SUBKEYS      = ('defaults', 'overrides')

  wrapper_fmt           = u'<div id="{id}" style="{style}"{attributes}>{content}</div>'

  #----------------------------------------------------------------------------
  def __init__(self, settings, *args, **kw):
    super(Engine, self).__init__(*args, **kw)
    self.realms   = {self.DEFAULT_REALM: {}}
    self.channels = self.CHANNELS[:]
    for key, val in settings.items():
      try:
        val = yaml.load(val)
      except Exception:
        pass
      cfg = self.DEFAULT_REALM
      if key.startswith(self.SETTINGS_REALM_TOKEN):
        key = key[len(self.SETTINGS_REALM_TOKEN):]
        if '.' not in key:
          continue
        cfg, key = key.split('.', 1)
      if cfg not in self.realms:
        self.realms[cfg] = {}
      if '.' in key and key.split('.', 1)[0] in self.SETTINGS_SUBKEYS:
        key, sub = key.split('.', 1)
        if key not in self.realms[cfg]:
          self.realms[cfg][key] = {}
        self.realms[cfg][key][sub] = val
        continue
      self.realms[cfg][key] = val
    defs = self.realms[self.DEFAULT_REALM]
    for cfg, vals in self.realms.items():
      if cfg == self.DEFAULT_REALM:
        continue
      for key, defval in defs.items():
        if key in self.SETTINGS_SUBKEYS:
          if key not in vals:
            vals[key] = {}
          for subkey, defsubval in defval.items():
            if subkey not in vals[key]:
              vals[key][subkey] = defsubval
        else:
          if key not in vals:
            vals[key] = defval
    log.debug('loaded realms: %s', ', '.join(self.realms.keys()))

  #----------------------------------------------------------------------------
  def render(self, realm=DEFAULT_REALM, channel=DEFAULT_CHANNEL):
    if realm not in self.realms:
      log.warning(
        'request for undeclared pyramid-jitt realm %r: using %r realm',
        realm, self.DEFAULT_REALM)
      realm = self.DEFAULT_REALM
    conf = self.realms[realm]
    creg = conf.get('cache-region', self.DEFAULT_CACHEREGION)
    if not creg or cache_region is None:
      return self._render(realm, channel)
    @cache_region(creg)
    def _cachedrender(realm, channel):
      return self._render(realm, channel)
    return _cachedrender(realm, channel)

  #----------------------------------------------------------------------------
  def _render(self, realm, channel):
    if channel not in (self.CHANNEL_INLINE, self.CHANNEL_DEFERRED) \
        and not channel.startswith(self.CHANNEL_JIT + ':'):
      raise ValueError(
        'pyramid_jitt currently does not support rendering channel "%s"'
        % (channel,))
    conf = self.realms[realm]
    log.debug('rendering templates for realm %r, channel %r', realm, channel)
    compiler = asset.symbol(conf.get('compiler', self.DEFAULT_COMPILER))(
      defaults  = conf.get('defaults', None),
      overrides = conf.get('overrides', None),
    )
    def loadcb(spec):
      if spec is None:
        return spec
      cb = asset.symbol(spec)
      def _wrapper(*args, **kw):
        return cb(realm, channel, *args, **kw)
      return _wrapper
    context = aadict(
      callback  = loadcb(conf.get('template_filter')),
      realm     = realm,
      channel   = channel,
      deferred  = False,
      protected = False,
    )
    tfiltfp = getattr(self, '_template_filter_' + channel.split(':', 1)[0])
    tfilt   = lambda *args, **kw: tfiltfp(context, *args, **kw)
    ret = compiler.render_assets(
      conf.get('assets'), roots=conf.get('roots'),
      asset_filter       = loadcb(conf.get('asset_filter')),
      name_transform     = loadcb(conf.get('name_transform')),
      template_transform = loadcb(conf.get('template_transform')),
      template_filter    = tfilt,
    )
    if channel == self.CHANNEL_INLINE:
      style = conf.get('style', self.DEFAULT_NODESTYLE)
      if morph.isstr(style):
        style = yaml.load(style)
      style = ';'.join(':'.join([k, style[k]]) for k in sorted(style.keys()))
      nodeid = conf.get('id', self.DEFAULT_NODEID)
      channels = []
      if context.deferred:
        channels += [self.CHANNEL_DEFERRED]
      if context.protected:
        channels += [self.CHANNEL_PROTECTED]
      attrs = ''
      loader = channels or morph.tobool(conf.get('loader.always', self.DEFAULT_LOADERALWAYS))
      if loader:
        attrs = ' data-jitt-loaded="inline" data-jitt-deferred="'
        attrs += ','.join(cgi.escape(ch, quote=True) for ch in channels)
        attrs += '"'
      ret = self.wrapper_fmt.format(
        id         = cgi.escape(nodeid, quote=True),
        style      = cgi.escape(style, quote=True),
        attributes = attrs,
        content    = ret,
      )
      if loader:
        baseurl = conf.get('mount-path', self.DEFAULT_MOUNT_PATH)
        baseurl = os.path.join(baseurl, urlquote(realm, safe=''))
        # todo: the host *could* come from the current request...
        baseurl = conf.get('mount-host', self.DEFAULT_MOUNT_HOST) + baseurl
        ret += asset.load(
          conf.get('deferred-html', self.DEFAULT_DEFERREDHTML)
        ).read().format(
          id       = cgi.escape(nodeid + '_JittLoader', quote=True),
          nodeid   = json.dumps(nodeid),
          baseurl  = json.dumps(baseurl),
          channels = json.dumps(channels),
          loader   = asset.load(conf.get('deferred-js', self.DEFAULT_DEFERREDJS)).read(),
        )
    return ret

  #----------------------------------------------------------------------------
  def _template_filter_inline(self, context, text, attrs, *args, **kw):
    if context.callback and not context.callback(text, attrs, *args, **kw):
      return False
    if not morph.tobool(attrs.get('inline')):
      context.deferred = True
      if morph.tobool(attrs.get('protected')):
        context.protected = True
    return morph.tobool(attrs.get('inline'))

  #----------------------------------------------------------------------------
  def _template_filter_deferred(self, context, text, attrs, *args, **kw):
    if context.callback and not context.callback(text, attrs, *args, **kw):
      return False
    if morph.tobool(attrs.get('protected')):
      return False
    return not morph.tobool(attrs.get('inline'))

  #----------------------------------------------------------------------------
  def _template_filter_jit(self, context, text, attrs, *args, **kw):
    if context.callback and not context.callback(text, attrs, *args, **kw):
      return False
    return ( self.CHANNEL_JIT + ':' + attrs.get('name', '') ) == context.channel


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
