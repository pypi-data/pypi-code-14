# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/23
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import logging
import cgi

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

  DEFAULT_CONFIG        = 'default'
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

  CHANNEL_INLINE        = 'inline'
  CHANNEL_DEFERRED      = 'deferred'
  CHANNEL_PROTECTED     = 'protected'

  SETTINGS_CONFIG_TOKEN = '@'
  SETTINGS_SUBKEYS      = ('defaults', 'overrides')

  scriptfmt             = u'<div id="{id}" style="{style}">{content}</div>'

  #----------------------------------------------------------------------------
  def __init__(self, settings, *args, **kw):
    super(Engine, self).__init__(*args, **kw)
    self.configs = {self.DEFAULT_CONFIG: {}}
    for key, val in settings.items():
      try:
        val = yaml.load(val)
      except Exception:
        pass
      cfg = self.DEFAULT_CONFIG
      if key.startswith(self.SETTINGS_CONFIG_TOKEN):
        key = key[len(self.SETTINGS_CONFIG_TOKEN):]
        if '.' not in key:
          continue
        cfg, key = key.split('.', 1)
      if cfg not in self.configs:
        self.configs[cfg] = {}
      if '.' in key and key.split('.', 1)[0] in self.SETTINGS_SUBKEYS:
        key, sub = key.split('.', 1)
        if key not in self.configs[cfg]:
          self.configs[cfg][key] = {}
        self.configs[cfg][key][sub] = val
        continue
      self.configs[cfg][key] = val
    defs = self.configs[self.DEFAULT_CONFIG]
    for cfg, vals in self.configs.items():
      if cfg == self.DEFAULT_CONFIG:
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
    log.debug('loaded configurations: %s', ', '.join(self.configs.keys()))

  #----------------------------------------------------------------------------
  def render(self, config=DEFAULT_CONFIG, channel=DEFAULT_CHANNEL):
    if channel != self.CHANNEL_INLINE:
      raise ValueError(
        'pyramid_jitt currently only supports rendering inline templates')
    conf = self.configs.get(config) or self.configs[self.DEFAULT_CONFIG]
    creg = conf.get('cache-region', self.DEFAULT_CACHEREGION)
    if not creg or cache_region is None:
      return self._render(config, channel)
    @cache_region(creg)
    def _cachedrender(config, channel):
      return self._render(config, channel)
    return _cachedrender(config, channel)

  #----------------------------------------------------------------------------
  def _render(self, config, channel):
    if config not in self.configs:
      log.warning(
        'request for undeclared pyramid-jitt config %r: using %r config',
        config, self.DEFAULT_CONFIG)
      conf = self.configs[self.DEFAULT_CONFIG]
    else:
      conf = self.configs[config]
    log.debug('rendering templates for config %r, channel %r', config, channel)
    compiler = asset.symbol(conf.get('compiler', self.DEFAULT_COMPILER))(
      defaults  = conf.get('defaults', None),
      overrides = conf.get('overrides', None),
    )

    def loadsym(spec):
      if spec is None:
        return spec
      return asset.symbol(spec)

    # TODO: implement deferred loading of non-inline templates!...
    template_transform = loadsym(conf.get('template_transform'))
    def force_inline_template_transform(text, attrs):
      if template_transform:
        text, attrs = template_transform(text, attrs)
      if not morph.tobool(attrs.get('inline')):
        import warnings
        warnings.warn(
          'pyramid_jitt does not yet support deferred loading of non-inline'
          ' templates -- forcing inline rendering')
        attrs = aadict(attrs, inline=True)
      return (text, attrs)
    # /TODO

    ret = compiler.render_assets(
      conf.get('assets'), roots=conf.get('roots'),
      asset_filter       = loadsym(conf.get('asset_filter')),
      name_transform     = loadsym(conf.get('name_transform')),
      # # TODO: revert to this:
      # #   template_transform = loadsym(conf.get('template_transform')),
      template_transform = force_inline_template_transform,
      # # /TODO
      template_filter    = loadsym(conf.get('template_filter')),
    )

    if channel == self.CHANNEL_INLINE:
      style = conf.get('style', self.DEFAULT_NODESTYLE)
      if morph.isstr(style):
        style = yaml.load(style)
      style = ';'.join(':'.join([k, style[k]]) for k in sorted(style.keys()))
      ret = self.scriptfmt.format(
        id      = cgi.escape(conf.get('id', self.DEFAULT_NODEID), quote=True),
        style   = cgi.escape(style, quote=True),
        content = ret,
      )
    return ret


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
