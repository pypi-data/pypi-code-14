# -*- coding: utf-8 -*-

"""Recipe mongodb"""

import os
from mako.template import Template
import logging

import zc.buildout
import zc.recipe.deployment
from zc.recipe.deployment import Configuration
import birdhousebuilder.recipe.supervisor
import birdhousebuilder.recipe.conda

templ_config = Template(filename=os.path.join(os.path.dirname(__file__), "mongod.conf"))
templ_cmd = Template('${conda_prefix}/bin/mongod --config ${etc_directory}/mongod.conf')


class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs mongodb as conda package and inits mongodb database."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name

        self.logger = logging.getLogger(self.name)

        # deployment layout
        def add_section(section_name, options):
            if section_name in buildout._raw:
                raise KeyError("already in buildout", section_name)
            buildout._raw[section_name] = options
            buildout[section_name]  # cause it to be added to the working parts

        self.deployment_name = self.name + "-mongodb-deployment"
        self.deployment = zc.recipe.deployment.Install(buildout, self.deployment_name, {
            'name': "mongodb",
            'prefix': self.options.get('prefix'),
            'user': self.options.get('user'),
            'etc-user': self.options.get('etc-user')})
        add_section(self.deployment_name, self.deployment.options)

        self.options['user'] = self.deployment.options['user']
        self.options['etc-user'] = self.deployment.options['etc-user']
        self.options['etc-prefix'] = self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = self.deployment.options['etc-directory']
        self.options['lib-directory'] = self.options['lib_directory'] = self.deployment.options['lib-directory']
        self.options['log-directory'] = self.options['log_directory'] = self.deployment.options['log-directory']
        self.options['run-directory'] = self.options['run_directory'] = self.deployment.options['run-directory']
        self.options['cache-directory'] = self.options['cache_directory'] = self.deployment.options['cache-directory']
        self.options['bin-directory'] = b_options['bin-directory']
        self.prefix = self.options['prefix']

        # conda environment path
        self.options['env'] = self.options.get('env', '')
        self.options['pkgs'] = self.options.get('pkgs', 'mongodb')
        self.options['channels'] = self.options.get('channels', 'defaults')

        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {
            #'prefix': self.options.get('conda-prefix', ''),
            'env': self.options['env'],
            'pkgs': self.options['pkgs'],
            'channels': self.options['channels']})
        self.options['conda-prefix'] = self.options['conda_prefix'] = self.conda.options['prefix']

        # mongodb options
        self.options['bind-ip'] = self.options['bind_ip'] = self.options.get('bind-ip', '127.0.0.1')
        self.options['port'] = self.options.get('port', '27017')

    def install(self, update=False):
        installed = []
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_config())
        installed += list(self.install_program())
        return installed

    def install_config(self):
        """
        install mongodb config file
        """
        text = templ_config.render(**self.options)
        config = Configuration(self.buildout, 'mongod.conf', {
            'deployment': self.deployment_name,
            'text': text})
        return [config.install()]

    def install_program(self):
        script = birdhousebuilder.recipe.supervisor.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'etc-user': self.options.get('etc-user'),
             'program': 'mongodb',
             'command': templ_cmd.render(**self.options),
             'priority': '10',
             'autostart': 'true',
             'autorestart': 'false',
             })
        return script.install()

    def update(self):
        return self.install(update=True)


def uninstall(name, options):
    pass
