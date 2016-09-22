# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/15
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest
import os
import textwrap

from aadict import aadict
import fso

#------------------------------------------------------------------------------
class TestCompiler(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_fragments(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler()
    hooks = aadict(name_transform=compiler._name_transform)
    self.assertEqual(
      list(compiler.fragments('foo/bar.jst', '', 'i am a template.', hooks)),
      [('i am a template.', aadict(name='foo/bar', type='.jst'))])
    self.assertEqual(
      list(compiler.fragments('foo/bar.jst', '', '''\
##! zig
  i am the zig template.
##! __here__
  i am the root template.
''', hooks)),
      [
        ('  i am the zig template.\n',  aadict(name='foo/bar/zig', type='.jst')),
        ('  i am the root template.\n', aadict(name='foo/bar', type='.jst')),
      ])

  #----------------------------------------------------------------------------
  def test_attributes(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler()
    hooks = aadict(name_transform=compiler._name_transform)
    self.assertEqual(
      list(compiler.fragments('foo/bar.jst', '', '''\
##! zig; channels: "public,protected"
  i am the zig template.
##! __here__; public; protected
  i am the root template.
##! zag; type: text/jst; !public; !protected
  i am the zag template.
''', hooks)),
      [
        ('  i am the zig template.\n',  aadict(name='foo/bar/zig', type='.jst', channels='public,protected')),
        ('  i am the root template.\n', aadict(name='foo/bar', type='.jst', public=True, protected=True)),
        ('  i am the zag template.\n',  aadict(name='foo/bar/zag', type='text/jst', public=False, protected=False)),
      ])

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
  def test_render_simple(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      overrides=dict(inline=True, precompile=False))
    with fso.push() as overlay:
      self.writecontent({
        'test/common/hello.hbs':
          '''\
            ##! __here__
              Hello, world!
            ##! name
              Hello, {{name}}!
          '''
      })
      self.assertEqual(
        compiler.render_assets('jstc:test/common/hello.hbs', 'test'),
        '''\
<script type="text/x-handlebars" data-template-name="common/hello">Hello, world!</script>\
<script type="text/x-handlebars" data-template-name="common/hello/name">Hello, {{name}}!</script>\
''')

  #----------------------------------------------------------------------------
  def test_comments(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      overrides=dict(inline=True, precompile=False))
    with fso.push() as overlay:
      self.writecontent({
        'test/application.hbs':
          '''\
            <div>
              ## TODO: super-secret comment!
              Nothing to see here.
            </div>
          '''
      })
      self.assertEqual(
        compiler.render_assets('jstc:test/application.hbs', 'test'),
        '''\
<script type="text/x-handlebars" data-template-name="application"><div>
  Nothing to see here.
</div>\
</script>\
''')

  #----------------------------------------------------------------------------
  def test_root(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      overrides=dict(inline=True, precompile=False))
    with fso.push() as overlay:
      self.writecontent({
        'test/one/template.hbs': 'template "one".',
        'test/two/template.hbs': 'template "two".',
      })
      self.assertEqual(
        compiler.render_assets('jstc:test/one/template.hbs', 'test/one'),
        '''\
<script type="text/x-handlebars" data-template-name="template">template "one".</script>\
''')
      self.assertEqual(
        compiler.render_assets('jstc:test/two/template.hbs', 'test/two'),
        '''\
<script type="text/x-handlebars" data-template-name="template">template "two".</script>\
''')
      self.assertEqual(
        compiler.render_assets(
          ['jstc:test/one/template.hbs', 'jstc:test/two/template.hbs'], 'test'),
        '''\
<script type="text/x-handlebars" data-template-name="one/template">template "one".</script>\
<script type="text/x-handlebars" data-template-name="two/template">template "two".</script>\
''')

  #----------------------------------------------------------------------------
  def test_collision_error(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      overrides=dict(inline=True, precompile=False))
    with fso.push() as overlay:
      self.writecontent({
        'test/one/template.hbs': 'template "one".',
        'test/two/template.hbs': 'template "two".',
      })
      with self.assertRaises(jstc.TemplateCollision) as cm:
        compiler.render_assets(
          ['jstc:test/one/template.hbs', 'jstc:test/two/template.hbs'],
          ['test/one', 'test/two'])
      self.assertEqual(
        str(cm.exception),
        ''''text/x-handlebars' template 'template' is already defined''')

  #----------------------------------------------------------------------------
  def test_collision_ignore(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      defaults=dict(collision='ignore'),
      overrides=dict(inline=True, precompile=False),
    )
    with fso.push() as overlay:
      self.writecontent({
        'test/one/template.hbs': 'template "one".',
        'test/two/template.hbs': 'template "two".',
      })
      self.assertEqual(
        compiler.render_assets(
          ['jstc:test/one/template.hbs', 'jstc:test/two/template.hbs'],
          ['test/one', 'test/two']),
        '''\
<script type="text/x-handlebars" data-template-name="template">template "one".</script>\
''')

  #----------------------------------------------------------------------------
  def test_collision_override(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      defaults=dict(collision='override'),
      overrides=dict(inline=True, precompile=False),
    )
    with fso.push() as overlay:
      self.writecontent({
        'test/one/template.hbs': 'template "one".',
        'test/two/template.hbs': 'template "two".',
      })
      self.assertEqual(
        compiler.render_assets(
          ['jstc:test/one/template.hbs', 'jstc:test/two/template.hbs'],
          ['test/one', 'test/two']),
        '''\
<script type="text/x-handlebars" data-template-name="template">template "two".</script>\
''')

  #----------------------------------------------------------------------------
  def test_collision_pertemplate(self):
    import jstc.compiler
    compiler = jstc.compiler.Compiler(
      defaults=dict(collision='ignore'),
      overrides=dict(inline=True, precompile=False),
    )
    with fso.push() as overlay:
      self.writecontent({
        'test/one/template.hbs':
          '''\
            ##! a
              template "one/a".
            ##! b
              template "one/b".
          ''',
        'test/two/template.hbs':
          '''\
            ##! a; collision: ignore
              template "two/a".
            ##! b; collision: override
              template "two/b".
          ''',
      })
      self.assertEqual(
        compiler.render_assets(
          ['jstc:test/one/template.hbs', 'jstc:test/two/template.hbs'],
          ['test/one', 'test/two']),
        '''\
<script type="text/x-handlebars" data-template-name="template/a">template "one/a".</script>\
<script type="text/x-handlebars" data-template-name="template/b">template "two/b".</script>\
''')

  #----------------------------------------------------------------------------
  def test_asset_filter(self):
    import jstc
    with fso.push() as overlay:
      self.writecontent({
        'test/hello.hbs': 'hello!',
        'test/goodbye.hbs': 'so long!',
      })
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False),
        '''\
<script type="text/x-handlebars" data-template-name="goodbye">so long!</script>\
<script type="text/x-handlebars" data-template-name="hello">hello!</script>\
''')
      self.assertEqual(
        jstc.render_assets(
          'jstc:test/**.hbs', inline=True, precompile=False,
          asset_filter=lambda name: name == 'test/hello.hbs'),
        '''\
<script type="text/x-handlebars" data-template-name="hello">hello!</script>\
''')
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False,
          asset_filter=lambda name: name != 'test/hello.hbs'),
        '''\
<script type="text/x-handlebars" data-template-name="goodbye">so long!</script>\
''')

  #----------------------------------------------------------------------------
  def test_name_transform(self):
    import jstc
    with fso.push() as overlay:
      self.writecontent({
        'test/hello.hbs': 'hello!',
        'test/goodbye.hbs': 'so long!',
      })
      def mynt(name, root):
        return (name[2:].replace('d', 'd-').split('.')[0], 'text/x-mustache')
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False,
          name_transform=mynt),
        '''\
<script type="text/x-mustache" data-template-name="st/good-bye">so long!</script>\
<script type="text/x-mustache" data-template-name="st/hello">hello!</script>\
''')

  #----------------------------------------------------------------------------
  def test_template_transform(self):
    import jstc
    with fso.push() as overlay:
      self.writecontent({
        'test/hello.hbs': 'hello!',
        'test/goodbye.hbs': 'so long!',
      })
      def mytt(text, attrs):
        if attrs.name == 'hello':
          text = 'hello, world!'
          attrs.id = 'HW'
        else:
          attrs.type = 'template/jst'
        return (text, attrs)
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False,
          template_transform=mytt),
        '''\
<script type="template/jst" data-template-name="goodbye">so long!</script>\
<script type="text/x-handlebars" data-template-name="hello" id="HW">hello, world!</script>\
''')

  #----------------------------------------------------------------------------
  def test_template_filter(self):
    import jstc
    with fso.push() as overlay:
      self.writecontent({
        'test/hello.hbs': 'hello!',
        'test/goodbye.hbs': '''\
##! __here__
  so long!
##! friend
  ciao!
'''
      })
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False),
        '''\
<script type="text/x-handlebars" data-template-name="goodbye">so long!</script>\
<script type="text/x-handlebars" data-template-name="goodbye/friend">ciao!</script>\
<script type="text/x-handlebars" data-template-name="hello">hello!</script>\
''')
      self.assertEqual(
        jstc.render_assets('jstc:test/**.hbs', inline=True, precompile=False,
          template_filter=lambda text, attrs: 'ciao' not in text),
        '''\
<script type="text/x-handlebars" data-template-name="goodbye">so long!</script>\
<script type="text/x-handlebars" data-template-name="hello">hello!</script>\
''')


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
