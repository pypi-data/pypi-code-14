# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/12
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import logging
import os.path
import shlex
import re
import textwrap
import cgi

import six
import asset
import morph
from aadict import aadict

from . import api

#------------------------------------------------------------------------------

log = logging.getLogger(__name__)

#------------------------------------------------------------------------------
class TemplateAttributeParser(shlex.shlex):
  # todo: this currently supports ``name; !flag`` but not ``name; ! flag``...
  #       make that work too.
  TOKEN_KEYEND  = ':'
  TOKEN_VALEND  = ';'
  TOKENS        = (TOKEN_KEYEND, TOKEN_VALEND)
  def __init__(self, instream, *args, **kw):
    kw['posix'] = kw.get('posix', True)
    self.src = None
    if morph.isstr(instream):
      self.src = instream
    shlex.shlex.__init__(self, instream, *args, **kw)
    self.commenters = ''
    self.wordchars += '%&()+-./=@[]^`{}~!'
  def dict(self):
    ret = dict()
    expect = 'name'
    curkey = None
    while True:
      token = self.get_token()
      if token == self.eof:
        if expect == self.TOKEN_KEYEND:
          token = True
          if curkey.startswith('!'):
            curkey = curkey[1:].strip()
            token = False
          ret[curkey] = token
          curkey = None
          expect = self.TOKEN_VALEND
        break
      if token == self.TOKEN_VALEND and expect == self.TOKEN_KEYEND:
        token = True
        if curkey.startswith('!'):
          curkey = curkey[1:].strip()
          token = False
        ret[curkey] = token
        curkey = None
        expect = 'key'
        continue
      if ( expect in self.TOKENS or token in self.TOKENS ) and token != expect:
        raise SyntaxError('invalid template attributes %r: expected %r, received %r'
                          % (self.src, expect, token))
      if expect == 'name':
        ret['name'] = token
        expect = self.TOKEN_VALEND
        continue
      if expect == 'key':
        curkey = token
        expect  = self.TOKEN_KEYEND
        continue
      if expect == self.TOKEN_KEYEND:
        expect = 'value'
        continue
      if expect == 'value':
        ret[curkey] = token
        curkey = None
        expect = self.TOKEN_VALEND
        continue
      if expect == self.TOKEN_VALEND:
        expect = 'key'
        continue
    if expect != self.TOKEN_VALEND:
      raise SyntaxError('invalid template attributes %r: dangling specification, expected %s'
                        % (self.src, expect))
    return ret

#------------------------------------------------------------------------------
class Compiler(object):
  '''
  A `Compiler` is the main template processor and renderer for the
  `jstc` package.
  '''

  DEFAULT_COMMENTS      = '##'
  DEFAULT_FRAGMENTS     = '##!'
  DEFAULT_HERESTRING    = '__here__'

  COLLISION_ERROR       = 'error'
  COLLISION_IGNORE      = 'ignore'
  COLLISION_OVERRIDE    = 'override'

  ROOT_AUTO             = 'auto'

  TYPE_HTMLFRAG         = 'text/html-fragment'
  TYPE_SCRIPT           = 'text/javascript'
  TYPE_JS               = 'application/javascript'
  TYPE_JSFRAG           = 'application/javascript-fragment'

  attrprefix            = 'data-template-'
  scriptattrs           = ('name', 'locale')
  scriptfmt             = six.u('<script type="{type}" {attributes}>{script}</script>')

  default_defaults      = {
                            'trim'            : True,
                            'inline'          : False,
                            'precompile'      : True,
                            'collision'       : COLLISION_ERROR,
                            'pass-through'    : 'id',
                            'prefix-through'  : 'name,locale',
                          }
  default_overrides     = {}

  #----------------------------------------------------------------------------
  def __init__(self,
               attrprefix       = None,
               mimetypes        = None,
               default_type     = None,
               comments         = DEFAULT_COMMENTS,
               fragments        = DEFAULT_FRAGMENTS,
               herestring       = DEFAULT_HERESTRING,
               defaults         = None,
               overrides        = None,
               scriptattrs      = None,
               *args, **kw):
    '''
    Creates a `jstc` Compiler object.

    :Parameters:

    attrprefix : str, default: 'data-'

      The string prefixed onto attributes specified non-precompiled
      templates. This is applies to all attributes except the "type"
      attribute and any listed in the "pass-through" meta-attribute.

    mimetypes : dict, default: (loaded from plugins)

      Maps template mime-types to extensions. The keys should be
      the mime-type, and the values should be a list of extensions
      (including the "."), e.g.:

      .. code:: json

        {
          "text/x-handlebars" : [ ".handlebars", ".hbs" ],
          "text/x-mustache"   : [ ".mustache" ]
        }

    default_type : str, default: (none)

      Specifies the default mimetype for a template if it cannot
      otherwise be determined. If this is not specified, an error is
      raised if any template cannot be mapped to a mimetype.

    comments : str | null, default: '##'

      Specifies a template-agnostic line-oriented comment string.
      To disable this "global" pre-template decommenting, set this
      value to null.

    fragments : str | null, default: '##!'

      Specifies a template-agnostic token that splits a template file
      into a multi-template container. To disable this "global"
      pre-template fragmenting, set this value to null.

    herestring : str | null, default: '__here__'

      Specifies a template name component that is "self-effacing", i.e.
      a template residing in the file named::

        path/to/template/__here__.hbs

      will have the name of the template name::

        path/to/template

      To disable this self-effacing template name component feature,
      set this value to null.

    scriptattrs : list(str), default: ['name', 'locale']

      Specifies the list of template attributes, if available, that
      will be prefixed with `attrprefix` and inserted into
      non-precompiled script template nodes. Note that this can be
      overridden on a per-template basis.

    defaults : dict, default: null

      Sets the default value of template attributes, i.e. if the
      template does not specify these attributes, then it will behave
      as if they had been. See :meth:`compile` for details on known
      attributes.

    overrides : dict, default: null

      Overrides template attributes. See :meth:`compile` for details
      on known attributes.
    '''
    super(Compiler, self).__init__(*args, **kw)
    self.deftype      = default_type
    self.precompilers = dict()
    for plugin in asset.plugins('jstc.engines.plugins'):
      self.precompilers[plugin.name] = plugin.handle()
    if attrprefix is not None:
      self.attrprefix = attrprefix
    if mimetypes is not None:
      self.mimetypes = mimetypes
    if scriptattrs is not None:
      self.scriptattrs = scriptattrs
    else:
      self.mimetypes = dict()
      for name, prec in self.precompilers.items():
        for ext in prec.extensions:
          self.mimetypes[name] = prec.extensions
    self.extensions = dict()
    for mimetype, exts in self.mimetypes.items():
      for ext in exts:
        if ext in self.extensions:
          log.warning('multiple jstc pre-compilers registered for extension %r' % (ext,))
        self.extensions[ext] = mimetype
    self.commenttoken  = comments
    self.fragmenttoken = fragments
    self.heretoken     = herestring
    self.decomment_cre = None
    if self.commenttoken:
      # todo: what about lines that have data before a '##'?...  the
      #       problem is that then i really need parsing of the template
      #       to determine if the '##' is part of the template or just a
      #       comment...
      self.decomment_cre = re.compile(
        '^\\s*' + re.escape(self.commenttoken) + '.*(\r\n|\r|\n|$)', re.MULTILINE)
    self.defaults = aadict(self.default_defaults).update(defaults or {})
    self.overrides = aadict(self.default_overrides).update(overrides or {})

  #----------------------------------------------------------------------------
  def render_assets(self, assets, roots=None,
                    force_inline       = None,
                    force_precompile   = None,
                    asset_filter       = None,
                    name_transform     = None,
                    template_transform = None,
                    template_filter    = None,
                    script_wrapper     = None,
    ):
    '''
    Compiles and prepares the templates in `assets` for delivery to
    remote JavaScript template processing routines.

    :Parameters:

    assets : list

      List of asset-specifications (see `asset` python package) to
      extract templates from.

    roots : list, default: null

      Specifies the "root" portion of each corresponding asset in
      `assets`. If not specified or set to ``"auto"``, then the root
      value will be "auto-magically-guestimated"... basically, it will
      assume the root begins at the wildcard for glob-patterns, for
      example with assets in ``package:path/to/dir/**.hbs``, the root
      will be ``path/to/dir``.

      The "root" is used only by the default `asset_filter`
      implementation and performs two functions: first, it filters out
      assets that do not start with the specified root, and second,
      the root prefix is removed from the asset name to create the
      template name.

    force_inline : bool, default: null

      If specified and not null, overrides all templates' ``inline``
      attribute.

    force_precompile : bool, default: null

      If specified and not null, overrides all templates' ``precompile``
      attribute.

    asset_filter : regex | callback, default: null

      If not null, `asset_filter` is used to filter which assets are
      selected for inclusion in the rendered output. If it is a
      string, it is interpreted as a regex pattern and matched against
      the asset name. Otherwise, it is used as a callback and called
      with a single argument, the asset name, and is expected to
      return a boolean result, where truthy indicates inclusion.

      The default implementation checks that the asset name does not
      end with a tilde (``~``) and no component of the asset path
      starts with a dot (``.``).

      Note that this is NOT the same as `template_filter` since there
      may be multiple templates per asset.

    name_transform : callback, default: null

      If not null, overrides the default asset filename to template
      name evaluation with a callback that is provided two arguments,
      the asset filename and the corresponding root from `roots`, and
      is expected to return a two-element tuple of (template-name,
      mimetype). The mimetype can either be the registered mime-type
      of the template engine to use, or a file extension that can be
      used to resolve to such a mime-type. For multi-template assets,
      the template-name is used as the basename for all contained
      templates, and the mimetype is used as the default for the
      contained templates, overrides the global default, and can be
      individually overridden by each contained template. The default
      implementation uses the return value from a call to
      `os.path.splitext` and stripped of the applicable root.

    template_transform : callback, default: null

      Specifies a callback that can adjust a template's content and/or
      attributes before being filtered and processed. It is called
      with two arguments, the content and the attributes, and is
      expected to return a two-elemente tuple of (content,
      attributes).

      Note that this callback is called after `name_transform`.

    template_filter : regex | callback, default: null

      Specifies a callback that is used to filter which templates are
      selected for inclusion in the rendered output. If it is a
      string, it is interpreted as a regex pattern and matched against
      the template name. Otherwise, it is used as a callback and
      called with two arguments, the content and the attributes, and
      is expected to return a boolean result, where truthy indicates
      inclusion.

      Note that this is NOT the same as `asset_filter` since there may
      be multiple templates per asset.

      Note that this callback is called after `template_transform`.

    script_wrapper : callback, default: null

      Specifies a callback that is used to wrap a pre-compiled
      template, expressed as a JavaScript code fragment, into an HTML
      fragment. The callback is called with one argument, the raw
      JavaScript code fragment. The default simply generates a
      JavaScript "script" element, e.g.:

      .. code:: html

        <script type="text/javascript">
          {JAVASCRIPT_CODE_FRAGMENT}
        </script>
    '''
    assets = morph.tolist(assets)
    roots  = morph.tolist(roots or self.ROOT_AUTO)
    roots  = roots + ( [roots[-1]] * ( len(assets) - len(roots) ) )
    overrides = aadict(self.overrides)
    if force_inline is not None:
      overrides.inline = force_inline
    if force_precompile is not None:
      overrides.precompile = force_precompile

    # asset_filter = regex | callback | null
    if asset_filter is None:
      asset_filter = lambda name, *args, **kw: not('/.' in name or name.endswith('~'))
    elif morph.isstr(asset_filter):
      asset_filter = re.compile(asset_filter)
      asset_filter = lambda name, *args, **kw: bool(asset_filter.match(name))

    # name_transform = callback | null
    if name_transform is None:
      name_transform = self._name_transform

    # template_transform = callback | null
    if template_transform is None:
      template_transform = lambda *args, **kw: args

    # template_filter = regex | callback | null
    if template_filter is None:
      template_filter = lambda *args, **kw: True
    elif morph.isstr(template_filter):
      template_filter = re.compile(template_filter)
      template_filter = lambda text, attrs, *args, **kw: bool(template_filter.match(attrs.get('name')))

    # script_wrapper = callback | null
    if script_wrapper is None:
      script_wrapper = self.script_wrap

    hooks = aadict(
      asset_filter       = asset_filter,
      name_transform     = name_transform,
      template_transform = template_transform,
      template_filter    = template_filter,
      script_wrapper     = script_wrapper,
    )

    res = dict()
    for idx, spec in enumerate(assets):
      for text, attrs in self._asset2templates(spec, roots[idx], hooks):
        attrs = aadict(self.defaults).update(attrs).update(overrides)
        text, attrs = hooks.template_transform(text, attrs)
        if not hooks.template_filter(text, attrs):
          continue
        if not attrs.type:
          attrs.type = self.deftype
        if not attrs.type:
          raise SyntaxError(
            'could not determine template type for %r (in %r)'
            % (attrs.name, spec))
        contentType, content = self._compile(text, aadict(attrs, partial=True))
        if attrs.type not in res:
          res[attrs.type] = dict()
        if attrs.name in res[attrs.type]:
          # todo: perhaps `collision` attributes should be checked in
          #       both old and new templates... eg: imagine template A
          #       and B collide, and A specifies a `collision`
          #       attribute of "override"... i.e. A is really provided
          #       as a "default" template, then many assets can
          #       override the default without each one needing to
          #       specify the `collision` attribute.
          #       ==> also to be considered then, is should the current
          #           "collision" attribute by carried over from A to B
          #           so that if there is a "C" it will inherit that???
          col = attrs.collision
          if col == Compiler.COLLISION_ERROR:
            # todo: give more context details (eg. which asset spec, which
            #       asset item filename, etc)
            raise api.TemplateCollision(
              '%r template %r is already defined' % (attrs.type, attrs.name))
          elif col == Compiler.COLLISION_IGNORE:
            log.debug(
              '%r template %r collision: ignored' % (attrs.type, attrs.name))
            continue
          elif col != Compiler.COLLISION_OVERRIDE:
            raise TypeError(
              'unknown/unimplement collision policy %r on %r template %r'
              % (col, attrs.type, attrs.name))
          log.debug(
            '%r template %r collision: override' % (attrs.type, attrs.name))
        res[attrs.type][attrs.name] = (contentType, content, attrs)

    ret = ''
    for mimetype in sorted(res.keys()):
      templates = res[mimetype]
      types = dict()
      for name in sorted(templates.keys()):
        contentType, content, attrs = templates[name]
        if contentType not in types:
          types[contentType] = []
        types[contentType].append([contentType, content, attrs])
      for contentType in sorted(types.keys()):
        parts = types[contentType]
        if contentType == self.TYPE_HTMLFRAG:
          ret += ''.join(el[1] for el in parts)
          continue
        if contentType == self.TYPE_JS:
          content = ''.join(part[1] for part in parts)
        elif contentType == self.TYPE_JSFRAG:
          contentType, content = self._assemble(mimetype, parts)
        else:
          raise TypeError(
            'unexpected compiled template content-type %r' % (contentType,))
        ret += hooks.script_wrapper(content)
    return ret

  #----------------------------------------------------------------------------
  def _name_transform(self, name, root):
    if not name.startswith(root):
      return (None, None)
    name = name[len(root):]
    return os.path.splitext(name)

  #----------------------------------------------------------------------------
  def _asset2templates(self, spec, root, hooks):
    if root == self.ROOT_AUTO:
      # todo: this feels "primitive"... it should really extract this
      #       from globre's parse result in some way...
      if '/**' in spec:
        root = spec.split('/**', 1)[0]
        # todo: this is heavily assuming "PKG:RESOURCE" format... ugh.
        if ':' in root:
          root = root.split(':', 1)[1]
      else:
        root = ''
    if root and not root.endswith('/'):
      root += '/'
    for item in asset.load(spec):
      if not hooks.asset_filter(item.name):
        continue
      ## TODO: handle file encodings!...
      for fragment in self.fragments(item.name, root, item.read(), hooks):
        if fragment is not None:
          yield fragment

  #----------------------------------------------------------------------------
  def fragments(self, filename, root, text, hooks):
    basename, mimetype = hooks.name_transform(filename, root)
    if basename is None:
      yield None
      return
    if self.heretoken:
      basename = '/'.join(x for x in basename.split('/') if x != self.heretoken)
    attrs = aadict(name=basename, type=self.extensions.get(mimetype, mimetype))
    if not self.fragmenttoken:
      yield text, attrs
      return
    # todo: how to escape "##!" at the beginning of a line?...
    tok = self.fragmenttoken
    if not text.startswith(tok) and ( '\n' + tok ) in text:
      text = text[text.index('\n' + tok) + 1:]
    if not text.startswith(tok):
      yield text, attrs
      return
    while text:
      idx = text.index('\n')
      options = aadict(TemplateAttributeParser(text[len(tok):idx]).dict())
      if not options.name:
        raise SyntaxError('missing or invalid template name')
      options.name = os.path.join(basename, options.name)
      if 'type' in options or 'type' in attrs:
        options.type = options.get('type', attrs.type)
      text = text[idx + 1:]
      if self.heretoken:
        options.name = '/'.join(x for x in options.name.split('/') if x != self.heretoken)
      idx = text.find('\n' + tok)
      if idx < 0:
        curtext = text
        text = None
      else:
        idx += 1
        curtext = text[:idx]
        text = text[idx:]
      yield curtext, options

  #----------------------------------------------------------------------------
  def compile(self, text, attrs=None):
    '''
    Compiles and prepares the template `text` for delivery to remote
    JavaScript template processing routines.

    :Parameters:

    text : str

      The template content.

    attrs : dict

      Specifies the compilation control parameters. Note that these
      will be adjusted based on this compiler's `defaults` and
      `overrides` constructor parameter. Note also that some of these
      attributes are used by the `render*` methods, not here.

      name : str

        The name of this template.

      type : str

        The mime-type of the template engine intended to parse this
        template.

      collision : { 'error' | 'ignore' | 'override' }, default: 'error'

        Specifies the compiler's behavior when multiple templates have
        the same computed name. The following values are supported:

        * ``error``: throws an error and aborts compilation
        * ``ignore``: only the first template is used
        * ``override``: only the last template is used

      precompile : bool, default: true

        Sets the pre-compilation setting, i.e. whether or not a
        template should be compiled to "bytecode" (or whatever
        template-specific equivalent exists, if any) instead of being
        delivered as-is (i.e. "raw").

        NOTE: precompiled isn't *always* better and/or faster... for
        some templating languages (such as Handlebars), the
        pre-compiled template can actually be a *much* larger payload
        (in some cases 4x!) -- your mileage may vary!

      trim : bool, default: true

        Specifies whether or not the template content should be
        dedented and trimmed of whitespace.

      inline : bool, default: false

        Specifies whether or not this template should be rendered as
        an inlined template. Typically, inlined templates are inserted
        directly into the base HTML page, and non-inlined templates
        are loaded asynchronously.

        NOTE: this attribute is NOT used by the `jstc` package...
        this is an attribute that is intended to be used by callers to
        filter templates in `template_filter` and/or specially process
        the resulting templates.

      partial : bool, default: false

        Specifies whether or not the return value can be in
        ``application/javascript-fragment`` format (see Returns for
        details).

      pass-through : str, default: "id"

        A comma-separated list of attributes that should be
        passed-through as-is from the `attrs` object into the
        "<script>" tag as HTML attributes. For example, if `attrs`
        contains the key/value pairs ``{'id': 'foo', 'pass-through':
        'id'}``, then the resulting "<script>" tag will be::

          <script ... id="foo">...</script>

        Note that this only applies to non-pre-compiled templates.

      prefix-through : str, default: "name,locale"

        Similar to the `pass-through` attribute, except these
        attribute names have the compiler's `attrprefix` setting
        prefixed to the HTML attribute name. For example, if `attrs`
        contains the key/value pairs ``{'media': 'print',
        'prefix-through': 'id'}`` and `attrprefix` is the default,
        then the resulting "<script>" tag will be::

          <script ... data-media="print">...</script>

        Note that this only applies to non-pre-compiled templates.

    :Returns:

    list

      The return value is a two-element tuple: (contentType, content).
      The `content` is the result of the compiled `text`, and contentType
      is one of the following values:

      * ``text/html-fragment``:

        For template types that do not support pre-compilation or the
        compiler failed for some other reason, the raw template is
        returned wrapped in an appropriate HTML element.

      * ``application/javascript``:

        The `content` is a pre-compiled version of `text`, suitably
        wrapped in an appropriate HTML "script" element.

      * ``application/javascript-fragment``:

        The `content` is a partially pre-compiled version of
        `text`. This means that an additional "assemble" step that
        completes the pre-compilation process is required before the
        template becomes usable. This contentType will only be
        returned if the `partial` attribute was truthy.

    '''
    attrs = aadict(self.defaults).update(attrs).update(self.overrides)
    return self._compile(text, attrs)

  #----------------------------------------------------------------------------
  def _compile(self, text, attrs):
    if morph.tobool(attrs.trim):
      text = textwrap.dedent(text).strip()
    # todo: should `attrs` be able to specify an alternate commenting scheme?...
    text = self.decomment(text)
    if not morph.tobool(attrs.precompile):
      # return (text, False, attrs)
      return self._htmlwrap(text, attrs)
    precomp = self.precompilers.get(attrs.type)
    if not precomp or precomp.precompile is api.PrecompilerUnavailable:
      return self._htmlwrap(text, attrs)
    try:
      return precomp.precompile(text, attrs=attrs)
    except api.PrecompilerUnavailable:
      return self._htmlwrap(text, attrs)

  #----------------------------------------------------------------------------
  def _assemble(self, mimetype, parts):
    precomp = self.precompilers.get(mimetype)
    if not precomp or precomp.assemble is api.PrecompilerUnavailable:
      raise ValueError(
        '%r template engine not registered or does not support `assemble`',
        mimetype)
    return precomp.assemble(parts)

  #----------------------------------------------------------------------------
  def _htmlwrap(self, text, attrs):
    pfx = self.attrprefix or ''
    curattrs = dict()
    for key in [k.strip() for k in attrs.get('prefix-through', '').split(',')]:
      if key and key in attrs:
        curattrs[pfx + key] = attrs.get(key)
    for key in [k.strip() for k in attrs.get('pass-through', '').split(',')]:
      if key and key in attrs:
        curattrs[key] = attrs.get(key)
    return (
      self.TYPE_HTMLFRAG,
      self.script_wrap(text, type=attrs.type, attrs=curattrs),
    )

  #----------------------------------------------------------------------------
  def script_wrap(self, script, type=None, attrs=None):
    attrtext = ' '.join(
      '{key}="{value}"'.format(
        key=key, value=cgi.escape(attrs[key], quote=True))
      for key in sorted((attrs or {}).keys())
    )
    return self.scriptfmt.format(
      type       = type or self.TYPE_SCRIPT,
      attributes = attrtext,
      script     = self.script_escape(script),
    )

  #----------------------------------------------------------------------------
  def script_escape(self, text):
    # todo: do i also need to escape '<', '>', and '&'?...
    text = text.replace('<![CDATA', '<![CDATA[<]]>![CDATA')
    return text.replace('</script', '<![CDATA[<]]>/script')

  #----------------------------------------------------------------------------
  def decomment(self, text):
    '''
    Removes template-agnostic global comment lines from `text`.
    '''
    if self.decomment_cre is None:
      return text
    return self.decomment_cre.sub('', text)


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
