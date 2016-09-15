# -*- coding: utf-8 -*-
from __future__ import print_function

"""
    odoodoc
    -------

    :copyright: Copyright 2016 by Minorisa, S.L.
    :license: BSD, see LICENSE for details.
"""

import re
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.transforms import Transform
from sphinx.util.compat import Directive

import erppeek

_client = None


def get_field_data(model_name, field_name, show_help, odoo_lang):
    global _client
    if show_help:
        type = 'help'
    else:
        type = 'field'
    otrans = _client.model('ir.translation').browse([
        ('name', '=', (model_name + ',' + field_name)),
        ('type', '=', type),
        ('lang', '=', odoo_lang)
    ], limit=1)
    xname = None
    if otrans and otrans[0]:
        xname = otrans[0].value
    else:
        xdict = _client.model(model_name).field(field_name)
        if show_help:
            xname = xdict.get('help', None)
        else:
            xname = xdict.get('string', None)
    return xname


class FieldDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'help': directives.flag,
        'class': directives.class_option,
    }

    def run(self):
        config = self.state.document.settings.env.config
        content = self.arguments[0]
        if 'help' in self.options:
            show_help = True
        else:
            show_help = False

        classes = [config.odoodoc_fieldclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        model_name, field_name = content.split('/')

        text = get_field_data(model_name, field_name, show_help, config.odoo_lang)
        if text is None:
            return [self.state_machine.reporter.warning(
                'Model/Field "%s" not found.' % content, line=self.lineno)]
        return [nodes.literal(text=text, classes=classes)]


def get_menu_data(module_name, menu_name, show_name_only, odoo_lang):
    xres_id = _client.model('ir.model.data').read([
        ('module', '=', module_name),
        ('name', '=', menu_name)
    ], limit=1, fields=['res_id'])
    xid = xres_id and xres_id[0] or False
    if not xid:
        return None
    xmenu = _client.model('ir.ui.menu').browse(xid['res_id'], context={'lang': odoo_lang})
    if show_name_only:
        text = xmenu.name or None
    else:
        text = xmenu.complete_name or None
    return text


class MenuDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        # Prints only the name of the menu entry instead of its full path
        'nameonly': directives.flag,
        'class': directives.class_option,
    }

    def run(self):
        config = self.state.document.settings.env.config
        content = self.arguments[0]
        if 'nameonly' in self.options:
            show_name_only = True
        else:
            show_name_only = False

        classes = [config.odoodoc_menuclass]
        if 'class' in self.options:
            classes.extend(self.options['class'])

        module_name, menu_name = content.split('/')

        text = get_menu_data(module_name, menu_name, show_name_only, config.odoo_lang)
        if text is None:
            return [self.state_machine.reporter.warning(
                'Menu entry "%s" not found.' % content, line=self.lineno)]

        return [nodes.literal(text=text, classes=classes)]


class References(Transform):
    """
    Parse and transform menu and field references in a document.
    """

    default_priority = 999

    def apply(self):
        config = self.document.settings.env.config
        pattern = config.odoodoc_pattern
        if isinstance(pattern, basestring):
            pattern = re.compile(pattern)
        for node in self.document.traverse(nodes.Text):
            parent = node.parent
            if isinstance(parent, (nodes.literal, nodes.FixedTextElement)):
                # ignore inline and block literal text
                continue
            text = unicode(node)
            modified = False

            match = pattern.search(text)
            while match:
                if len(match.groups()) != 1:
                    raise ValueError(
                        'odoodoc_issue_pattern must have '
                        'exactly one group: {0!r}'.format(match.groups()))
                # extract the reference data (excluding the leading dash)
                refdata = match.group(1)
                start = match.start(0)
                end = match.end(0)

                data = refdata.split(':')
                kind = data[0]
                content = data[1]
                if len(data) > 2:
                    options = data[2]
                else:
                    options = None

                if kind == 'field':
                    model_name, field_name = content.split('/')
                    if options == 'help':
                        show_help = True
                    else:
                        show_help = False
                    replacement = get_field_data(model_name, field_name, show_help,
                                                 config.odoo_lang)
                elif kind == 'menu':
                    module_name, menu_name = content.split('/')
                    replacement = get_menu_data(module_name, menu_name, False,
                                                config.odoo_lang)
                else:
                    replacement = refdata

                text = text[:start] + (replacement or u'') + text[end:]
                modified = True

                match = pattern.search(text)

            if modified:
                parent.replace(node, [nodes.Text(text)])


def init_transformer(app):
    global _client
    if app.config.odoodoc_plaintext:
        app.add_transform(References)
    _client = erppeek.Client(app.config.odoo_server,
                             db=app.config.odoo_db,
                             user=app.config.odoo_user,
                             password=app.config.odoo_pwd)


def icon_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Font Awesome icon.
    """
    s = u'<i class="fa fa-{}" aria-hidden="true"></i>'.format(text)
    node = nodes.raw('', s, format='html')
    return [node], []


def setup(app):
    app.add_config_value('odoo_server', None, 'env')
    app.add_config_value('odoo_db', None, 'env')
    app.add_config_value('odoo_user', None, 'env')
    app.add_config_value('odoo_pwd', None, 'env')
    app.add_config_value('odoo_lang', 'es_ES', 'env')
    app.add_config_value('odoodoc_plaintext', True, 'env')
    app.add_config_value('odoodoc_pattern', re.compile(r'@(.|[^@]+)@'), 'env')
    app.add_config_value('odoodoc_menuclass', 'odoodocmenu', 'env')
    app.add_config_value('odoodoc_fieldclass', 'odoodocfield', 'env')

    app.add_directive('field', FieldDirective)
    app.add_directive('menu', MenuDirective)

    app.add_role('icon', icon_role)

    app.connect(b'builder-inited', init_transformer)
