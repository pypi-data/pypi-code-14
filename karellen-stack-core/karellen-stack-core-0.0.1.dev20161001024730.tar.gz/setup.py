#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'karellen-stack-core',
        version = '0.0.1.dev20161001024730',
        description = '''karellen-stack-core''',
        long_description = '''karellen-stack-core
===================

Karellen Stack Core
''',
        author = "Karellen, Inc",
        author_email = "supervisor@karellen.co",
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/karellen/karellen-stack-core',
        scripts = [],
        packages = [
            'karellen.stack.core',
            'karellen.stack.providers',
            'karellen.stack.utils',
            'karellen.stack.core.extensions',
            'karellen.stack.core.schema'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Build Tools'
        ],
        entry_points = {
            'console_scripts': ['kstack = karellen.stack.core.cli:kstack_cli_main'],
            'karellen.stack.core.extension': ['installer = karellen.stack.core.extensions.installer:Installer'],
            'karellen.stack.dependency': ['python = karellen.stack.core.dependency'],
            'karellen.stack.manager.installer': [
                'xcode = karellen.stack.providers.darwin:DarwinXcodeProvider',
                'yum = karellen.stack.providers.yum:YumProvider'
            ],
            'karellen.stack.schema.loader': [
                'file = karellen.stack.providers.loaders:FileUrlLoader',
                'git+git = karellen.stack.providers.loaders:GitUrlLoader',
                'git+http = karellen.stack.providers.loaders:GitUrlLoader',
                'git+https = karellen.stack.providers.loaders:GitUrlLoader',
                'git+ssh = karellen.stack.providers.loaders:GitUrlLoader'
            ]
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'jsonmerge~=1.2.0',
            'jsonschema~=2.5.0',
            'psutil~=4.0',
            'pyyaml~=3.0',
            'setuptools~=27.0',
            'voluptuous~=0.9.0'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
