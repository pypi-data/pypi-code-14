import os

from pathlib2 import Path
from jinja2 import Environment, PackageLoader
import click

from xcute.xcode import *
from prettytable import PrettyTable


def find_projects(xcode, path, ignore = None):
    # type: (Path, (Path) -> bool) -> XcodeProject
    for project_path in path.glob('**/*.xcodeproj'):
        if ignore and ignore(project_path):
            continue
        yield XcodeProject(xcode, project_path)

def all_build_arguments_for_project(project):
    for scheme in project.schemes:
        for target in scheme.targets:
            for platform in target.supported_platform_names:
                for configuration in ['Debug', 'Release']:
                    argument = XcodeBuildArguments(scheme = scheme.name, target = target.name, configuration=configuration, sdk=platform)
                    yield argument

def commands_for_project(project):
    options = all_build_arguments_for_project(project)

    def compare(option):
        return [project.path, option.sdk, option.scheme, option.configuration]

    options = sorted(options, key=compare)

    for option in options:
        command = 'xcodebuild -project \'{project.path}\' -scheme \'{option.scheme}\' -sdk {option.sdk} -configuration {option.configuration} build'.format(project = project, option = option)
        yield command
