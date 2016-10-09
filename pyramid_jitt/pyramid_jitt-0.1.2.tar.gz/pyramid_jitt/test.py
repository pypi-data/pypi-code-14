# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/10/05
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest
import os.path
import textwrap

import pyramid.paster
import fso
from webtest import TestApp, TestRequest
import asset

#------------------------------------------------------------------------------
def emptyapp(global_conf, **settings):
  from pyramid.config import Configurator
  return Configurator(settings=settings).make_wsgi_app()

#------------------------------------------------------------------------------
# todo: move this to pyramid-test?...
def makeUnicodeTestRequest(testcase):
  class UnicodeTestRequest(TestRequest):
    @staticmethod
    def blank(*args, **kw):
      ret = TestRequest.blank(*args, **kw)
      def send(*args, **kw):
        # monkeypatch to force PATH_INFO into a non-unicode...
        try:
          if ret.environ.get('PATH_INFO') == str(ret.environ.get('PATH_INFO')):
            ret.environ['PATH_INFO'] = str(ret.environ.get('PATH_INFO'))
        except:
          pass
        return ret._real_send(*args, **kw)
      ret._real_send = ret.send
      ret.send = send
      ret.get_response = send
      return ret
  return UnicodeTestRequest

#------------------------------------------------------------------------------
class JittTest(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def initapp(self, path):
    self.router = pyramid.paster.get_app(os.path.join(os.path.dirname(__file__), path))
    self.testapp = TestApp(self.router)
    self.testapp.RequestClass = makeUnicodeTestRequest(self)

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
  def defaultsetup(self, ini=None, files=None):
    self.writecontent({
      'test/test.ini':
        '''
          [app:main]
          use                                 = call:pyramid_jitt.test:emptyapp
          pyramid.includes                    = pyramid_jitt
          jitt.deferred-js                    = pyramid_jitt:test/deferred.js
          jitt.overrides.precompile           = false
          jitt.@inline-std.assets             = pyramid_jitt:test/common/**.hbs
          jitt.@inline-std.overrides.inline   = true
          jitt.@inline-noloader.assets             = pyramid_jitt:test/common/**.hbs
          jitt.@inline-noloader.overrides.inline   = true
          jitt.@inline-noloader.loader.always      = false
          jitt.@mixed.assets                  = pyramid_jitt:test/common/**.hbs
          jitt.@mixed.deferred-js             = pyramid_jitt:test/deferred.js
        ''',
      'test/deferred.js': 'function(){alert("loader loaded!");}',
      'test/common/hello.hbs':
        '''\
          ##! __here__
            Hello, world!
          ##! name
            Hello, {{name}}!
          ##! salutation; inline
            Dear {{name}},
          ##! familiar; protected
            Yo {{name}}!
        '''
    })
    self.initapp('test/test.ini')

  #----------------------------------------------------------------------------
  def test_inline_standard(self):
    with fso.push() as overlay:
      self.defaultsetup()
      chk = '''\
<div id="Templates" style="display:none;height:0;opacity:0;visibility:hidden;width:0" data-jitt-loaded="inline" data-jitt-deferred="">\
<script type="text/x-handlebars" data-template-name="hello">Hello, world!</script>\
<script type="text/x-handlebars" data-template-name="hello/familiar">Yo {{name}}!</script>\
<script type="text/x-handlebars" data-template-name="hello/name">Hello, {{name}}!</script>\
<script type="text/x-handlebars" data-template-name="hello/salutation">Dear {{name}},</script>\
</div>\
<script id="Templates_JittLoader" type="text/javascript">\
<!--//--><![CDATA[//><!--
  (function(){alert("loader loaded!");})("Templates", "/jitt/inline-std", []);\n//--><!]]></script>
'''
      self.assertMultiLineEqual(self.testapp.app.registry.jitt.render('inline-std'), chk)
      self.assertMultiLineEqual(self.testapp.get('/jitt/inline-std/inline').text, chk)

  #----------------------------------------------------------------------------
  def test_inline_noloader(self):
    with fso.push() as overlay:
      self.defaultsetup()
      chk = '''\
<div id="Templates" style="display:none;height:0;opacity:0;visibility:hidden;width:0">\
<script type="text/x-handlebars" data-template-name="hello">Hello, world!</script>\
<script type="text/x-handlebars" data-template-name="hello/familiar">Yo {{name}}!</script>\
<script type="text/x-handlebars" data-template-name="hello/name">Hello, {{name}}!</script>\
<script type="text/x-handlebars" data-template-name="hello/salutation">Dear {{name}},</script>\
</div>'''
      self.assertMultiLineEqual(self.testapp.app.registry.jitt.render('inline-noloader'), chk)
      self.assertMultiLineEqual(self.testapp.get('/jitt/inline-noloader/inline').text, chk)

  #----------------------------------------------------------------------------
  def test_mixed(self):
    with fso.push() as overlay:
      self.defaultsetup()
      inline_chk = '''\
<div id="Templates" style="display:none;height:0;opacity:0;visibility:hidden;width:0" data-jitt-loaded="inline" data-jitt-deferred="deferred,protected">\
<script type="text/x-handlebars" data-template-name="hello/salutation">Dear {{name}},</script>\
</div>\
<script id="Templates_JittLoader" type="text/javascript">\
<!--//--><![CDATA[//><!--
  (function(){alert("loader loaded!");})("Templates", "/jitt/mixed", ["deferred", "protected"]);\n//--><!]]></script>
'''
      self.assertMultiLineEqual(self.testapp.app.registry.jitt.render('mixed'), inline_chk)
      self.assertMultiLineEqual(self.testapp.get('/jitt/mixed/inline').text, inline_chk)


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
