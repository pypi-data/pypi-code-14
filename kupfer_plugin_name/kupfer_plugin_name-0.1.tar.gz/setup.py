#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from subprocess import call
from setuptools import setup
from setuptools.command.install import install

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

class CopyPlugin(install):
    """Customized setuptools install command - prints a friendly greeting."""
    
    def run(self):
        dirs = ["~", ".local", "share", "kupfer", "plugins"]
        install_path = path.expanduser(path.join(*dirs))
        print("mkdir {}".format(install_path))
        call("mkdir -p {}".format(install_path), shell=True)

        plugin_path = path.dirname(path.abspath(__file__))
        plugin_file = path.join(plugin_path, 'plugin_template.py')
        print("Copy {} to {}".format(plugin_file, install_path))
        call("cp -p {} {}".format(plugin_file, install_path), shell=True)

    
setup(
    cmdclass={
        'install': CopyPlugin,
    },
    py_modules=["plugin_template"],
    name='kupfer_plugin_name',
    version='0.1',
    description="kupfer_plugin_description",
    long_description=readme + '\n\n' + history,
    author="autor name",
    author_email='autor.email@company.com',
    url='https://github.com/hugosenari/Kupfer-Plugins/',
    license="ISC license",
    zip_safe=False,
    keywords='kupfer',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
