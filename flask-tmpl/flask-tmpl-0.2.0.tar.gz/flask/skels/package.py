#!/usr/bin/env python
# encoding: utf-8

from paste.script.templates import var
from paste.script.templates import Template

class Package(Template):
    """Package Template"""
    _template_dir = 'tmpl/package'
    summary = "A namespaced package with a test environment"
    use_cheetah = True
    vars = [
        var('namespave_package', 'Namespace package', default='flaskr'),
        var('package', 'The package contained ', default='example'),
        var('version', 'Version', default='0.1.0'),
        var('description', 'One-line decription of the package'),
        var('author', 'Author name', default='Tyrael Lau'),
        var('author_email', 'Author email', default='liqianglau@outlook.com'),
        var('keywords', 'Space-spearated keywords/tags'),
        var('url', 'URL of homepage'),
        var('license_name', 'License name', default='MIT'),
    ]

    def check_vars(self, vars, command):
        if not command.options.no_interactive and \
                not hasattr(command, '_deleted_once'):
            del vars['package']
            command._deleted_once = True
        return Template.check_vars(self, vars, command)
