from __future__ import print_function

import os

from changes_content import CHANGES
from contributing_content import CONTRIBUTING
from license_content import APACHE
from manifest_content import MANIFEST
from readme_content import README
from script_content import SCRIPT
from setup_content import SETUP
from test_content import TEST_BASIC


class Config(object):
    def __init__(
            self,
            project_name,
            project_description,
            keywords,
            url,
            author,
            author_email,
            license,
            scripts,
            requires,
            tests_requires,
            extras_requires,
            packages,
            version='0.0.1',
            include_license=False,
            include_tests=True,
            include_bin=True,
            include_readme=True,
            include_contributing=True,
            include_changes=True,
            include_manifest=True,
            include_requirements=True,
            overwrite=False
    ):
        """ Defines a project configuration """
        self.project_name = project_name
        self.project_description = project_description
        self.keywords = keywords
        self.url = url
        self.author = author
        self.author_email = author_email
        self.license = license
        self.scripts = scripts
        self.requires = requires
        self.tests_requires = tests_requires
        self.extras_requires = extras_requires
        self.packages = packages
        self.version = version
        self.include_license = include_license
        self.include_tests = include_tests
        self.include_bin = include_bin
        self.include_readme = include_readme
        self.include_contributing = include_contributing
        self.include_changes = include_changes
        self.include_manifest = include_manifest
        self.include_requirements = include_requirements
        self.overwrite = overwrite


class ProjectError(Exception):
    pass


def create_dir(path, overwrite, verbose):
    """ Creates a dir """
    if not os.path.exists(path):
        try:
            if verbose:
                print('Creating dir %s' % path)
            os.makedirs(path)
            return
        except OSError:
            raise ProjectError('Failed to create %s' % path)

    if not overwrite:
        raise ProjectError('Path %s already exists (not overwriting)' % path)


def create_file(path, content, overwrite, verbose):
    """ Creates a file """
    if not os.path.exists(path):
        try:
            if verbose:
                print('Creating file %s' % path)
            with open(path, 'w') as fh:
                fh.write(content)
            return
        except IOError:
            raise ProjectError('Failed to create %s' % path)

    if not overwrite:
        raise ProjectError('Path %s already exists (not overwriting)' % path)


def render_content(template, varz):
    content = template
    for var, value in varz.iteritems():
        target = '{{%s}}' % var
        content = content.replace(target, value)
    return content


class Project(object):
    """ A Python project """
    def __init__(self, config, base_path='.'):
        self.config = config
        self.base_path = base_path

    def create(self, verbose=False):
        """ Create a new project from the given config """
        config = self.config
        base_path = self.base_path
        overwrite = config.overwrite
        join = os.path.join

        # create project dir
        project_path = join(base_path, config.project_name)
        create_dir(project_path, overwrite, verbose)

        # setup.py
        path = join(project_path, 'setup.py')
        varz = {
            'PROJECT_NAME': config.project_name,
            'PROJECT_DESCRIPTION': config.project_description,
            'PROJECT_KEYWORDS': config.keywords,
            'PROJECT_URL': config.url,
            'PROJECT_AUTHOR': config.author,
            'PROJECT_AUTHOR_EMAIL': config.author_email,
            'PROJECT_LICENSE': config.license,
            # FIXME: is this the right way?
            'PROJECT_MAIN_PACKAGE': config.packages[0],
            'PROJECT_SCRIPTS': str([join('bin/', script) for script in config.scripts]),
            'PROJECT_REQUIRES': str(config.requires),
            'PROJECT_TESTS_REQUIRES': str(config.tests_requires),
            'PROJECT_EXTRAS_REQUIRES': str(config.extras_requires),
        }
        content = render_content(
            SETUP,
            varz
        )
        create_file(path, content, overwrite, verbose)

        # create packages
        for package in config.packages:
            package_path = join(project_path, package)
            create_dir(package_path, overwrite, verbose)

            # add __init__.py with the version
            path = join(package_path, '__init__.py')
            version = '__version__ = \'%s\'\n' % config.version
            create_file(path, version, overwrite, verbose)

            # tests
            if config.include_tests:
                # base dir
                tests_path = join(package_path, 'tests')
                create_dir(tests_path, overwrite, verbose)

                # make it a module
                path = join(tests_path, '__init__.py')
                create_file(path, '# tests\n', overwrite, verbose)

                # basic test file
                path = join(tests_path, 'test_basic.py')
                create_file(path, TEST_BASIC, overwrite, verbose)

        if config.include_bin:
            bin_path = join(project_path, 'bin')
            create_dir(bin_path, config.overwrite, verbose)

            # populate scripts
            for script in config.scripts:
                path = join(bin_path, script)
                create_file(path, SCRIPT, config.overwrite, verbose)
                os.chmod(path, 0755)

        if config.include_license:
            path = join(project_path, 'LICENSE')
            create_file(path, APACHE, config.overwrite, verbose)

        if config.include_readme:
            # TODO: project usage & tldr
            varz = {
                'PROJECT_NAME': config.project_name,
            }
            content = render_content(README, varz)
            path = join(project_path, 'README.rst')
            create_file(path, content, config.overwrite, verbose)

        if config.include_contributing:
            # FIXME: which one is the main pkg?
            varz = {
                'PACKAGE_NAME': config.packages[0],
            }
            content = render_content(CONTRIBUTING, varz)
            path = join(project_path, 'CONTRIBUTING')
            create_file(path, content, config.overwrite, verbose)

        if config.include_changes:
            path = join(project_path, 'CHANGES')
            create_file(path, CHANGES, config.overwrite, verbose)

        if config.include_manifest:
            path = join(project_path, 'MANIFEST.in')
            create_file(path, MANIFEST, config.overwrite, verbose)

        if config.include_requirements:
            path = join(project_path, 'requirements.txt')
            create_file(path, '', config.overwrite, verbose)
