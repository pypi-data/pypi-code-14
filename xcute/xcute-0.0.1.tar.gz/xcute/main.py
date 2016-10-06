import os

from pathlib2 import Path
from jinja2 import Environment, PackageLoader
import click

from xcute.xcode import *
from xcute.utilities import *
from prettytable import PrettyTable

@click.group()
def xcute_cli():
    #os.chdir("/Users/schwa/Projects/SwiftIO")
    #travis()
    pass

@xcute_cli.command()
@click.option('--setting', '-s', multiple=True)
def list(setting):

    setting = [f for f in setting]

    default_xcode = Xcode.default()

    def ignore(path):
        return 'Carthage/Checkouts' in str(path)

    projects = find_projects(default_xcode, Path('.'), ignore)

    columns = ['Project', 'Scheme', 'SDK', 'Configuration'] + setting
    x = PrettyTable(columns)

    for project in projects:
        for arg in all_build_arguments_for_project(project):
            arg.target = None
            settings = project.build_settings(arg)
            settings = settings[arg.scheme]

            row = [project.path, arg.scheme, arg.sdk, arg.configuration]

            for s in setting:
                row.append(settings.get(s, ''))

            x.add_row(row)
    print(x)


@xcute_cli.command()
@click.option('--template')
def export(template):
    default_xcode = Xcode.default()

    def ignore(path):
        return 'Carthage/Checkouts' in str(path)

    projects = find_projects(default_xcode, Path('.'), ignore)
    commands = (command for project in projects for command in commands_for_project(project))

    env = Environment(loader=PackageLoader('xcute', 'templates'))
    template = env.get_template('{}.jinja2'.format(template))
    print(template.render(commands=commands, travis_xcode_version='xcode8'))

if __name__ == '__main__':
    import shlex
    import sys

    #sys.argv = shlex.split('xcute list -s SWIFT_VERSION -s ENABLE_BITCODE -s arch -s XYZ')
    sys.argv = shlex.split('xcute travis')

    xcute_cli()