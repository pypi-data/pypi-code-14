#   Copyright 2016, SpockerDotNet LLC

import logging
import os

import umodules.helper as helper
from umodules.command import ICommand


def _install(project):
    #   check if any specific modules were specified
    logging.debug("- there are {0} modules specified".format(len(project.args.modules)))
    if len(project.args.modules) == 0:
        logging.debug("- installing main module and supporting modules")
        _install_main(project)
        _install_modules(project)
    else:
        logging.debug("- installing supporting modules only")
        _install_modules(project)

def _copy_module(project, module):
    pass


def _install_main(project):
    logging.log(99, 'Installing Project [{0}]'.format(project.name))
    #   do NOT install if the project path already exists
    if os.path.exists(project.project_path):
        if project.args.force:
            helper.clean_folder(project.project_path)
        else:
            raise Exception('Project Path Already Exists at [{0}] -- Try Using the --force'.format(project.project_path))
    #   create repository
    logging.debug('- check to see if the repository exists at [{0}]'.format(project.repository_path))
    if not os.path.exists(project.repository_path):
        os.makedirs(project.repository_path)
        logging.debug('- new repositor created at [{0}]'.format(project.repository_path))
    #   create project
    logging.debug('- check to see if the project exists at [{0}]'.format(project.project_path))
    if not os.path.exists(project.project_path):
        os.makedirs(project.project_path)
    _install_module(project, project.main)


def _install_modules(project):
    for module in project.modules:
        if module.active:
            if (len(project.args.modules)) > 0:
                for name in project.args.modules:
                    if name.lower() == module.name.lower():
                        logging.debug(
                            "- found matching module [{0}]".format(name))
                        _install_module(project, module)
                        _copy_module(project, module)
            else:
                _install_module(project, module)
                _copy_module(project, module)


def _install_module(project, module):
    logging.log(99, 'Installing Module [{1}]'.format(project.name, module.name))
    plugin = _get_plugin(project, module)
    if plugin is not None:
        plugin.pull(project, module)
        if not module.is_main:
            helper.copy_module(project, module)
    if plugin is None:
        raise Exception('Module Type [{0}] is Not Supported'.format(module.type))


def _get_plugin(project, module):
    logging.debug('- module type is [{0}]'.format(module.type))
    plugin = None
    for module_type in project.module_types:
        if module.type == module_type.plugin_object.name:
            logging.debug('- found module type of [{0}]'.format(module.type))
            plugin = module_type.plugin_object
    return plugin


class Install(ICommand):

    def run(self, project):
        logging.debug("- running [install] for Project {0}".format(project.name))
        try:
            _install(project)
        except Exception as e:
            raise Exception(e)

    def build(self, subparser):
        super().build(subparser)
        cmd = subparser.add_parser("install", help="...")
        cmd.set_defaults(func=self.run)
        cmd.add_argument("modules", action="store", nargs="*")
        logging.debug("- command [install] has been added to argparse")

    def activate(self):
        super().activate()

