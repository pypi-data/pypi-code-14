# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <phil@canary.md>
# date: 2016/09/15
# copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest

from .. import api

#------------------------------------------------------------------------------
class TestHandlebarsEngine(unittest.TestCase):

  #----------------------------------------------------------------------------
  def test_partial(self):
    try:
      from .handlebars import HandlebarsEngine
      # todo: make the compiler version details regex'ed...
      self.assertEqual(
        HandlebarsEngine().precompile('hello, world!', {'name': 'foo', 'partial': True}),
        ('application/javascript-fragment',
         '''\
{"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "hello, world!";
},"useData":true}'''))
    except api.PrecompilerUnavailable:
      raise unittest.SkipTest(
        'handlebars executable not available (use "npm install handlebars")')

  #----------------------------------------------------------------------------
  def test_assemble(self):
    try:
      from .handlebars import HandlebarsEngine
      comp = HandlebarsEngine()
      parts = []
      for name, text in [
          ('hello',      'hello, world!'),
          ('hello/name', 'hello, {{name}}!'),
        ]:
        attrs = dict(name=name, partial=True)
        parts.append(comp.precompile(text, attrs) + (attrs,))
      # todo: make the compiler version details regex'ed...
      self.assertEqual(
        comp.assemble(parts),
        ('application/javascript',
         '''\
(function(){var t=Handlebars.template,ts=Handlebars.templates=Handlebars.templates||{};ts["hello"]=t({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "hello, world!";
},"useData":true});ts["hello/name"]=t({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper;

  return "hello, "
    + container.escapeExpression(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : {},{"name":"name","hash":{},"data":data}) : helper)))
    + "!";
},"useData":true});})();'''))
    except api.PrecompilerUnavailable:
      raise unittest.SkipTest(
        'handlebars executable not available (use "npm install handlebars")')

  #----------------------------------------------------------------------------
  def test_standalone(self):
    try:
      from .handlebars import HandlebarsEngine
      # todo: make the compiler version details regex'ed...
      self.assertEqual(
        HandlebarsEngine().precompile('this is {{name}}', {'name': 'foo'}),
        ('application/javascript',
         '''\
(function(){var t=Handlebars.template,ts=Handlebars.templates=Handlebars.templates||{};ts["foo"]=t({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var helper;

  return "this is "
    + container.escapeExpression(((helper = (helper = helpers.name || (depth0 != null ? depth0.name : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(depth0 != null ? depth0 : {},{"name":"name","hash":{},"data":data}) : helper)));
},"useData":true});})();'''))
    except api.PrecompilerUnavailable:
      raise unittest.SkipTest(
        'handlebars executable not available (use "npm install handlebars")')


#------------------------------------------------------------------------------
# end of $Id$
# $ChangeLog$
#------------------------------------------------------------------------------
