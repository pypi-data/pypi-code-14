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
        name = 'karellen-testing',
        version = '0.0.1.dev20161012185112',
        description = '''Karellen Testing Frameworks and Utilities''',
        long_description = '''Karellen Testing Frameworks and Utilities
=========================================

`Karellen <https://www.karellen.co/karellen/>`__ Testing Frameworks and
Utilities

This project aggregates testing frameworks and utilities for all of the
projects under `Karellen <https://www.karellen.co/>`__ umbrella.

Mock
----

A collection of Mock utilities helping with common tasks

Spy
~~~

.. code:: python

    from unittest import TestCase
    from karellen.testing.mock import MagicSpy


    class Class_A(object):
        def method_X(self):
            self.method_Y()

        def method_Y(self):
            pass


    class TestSpy(TestCase):
        def test_class_a_api(self):
            mock = MagicSpy(Class_A())

            mock.method_X()
            mock.method_Y.assert_called_once_with()
''',
        author = "Karellen, Inc",
        author_email = "supervisor@karellen.co",
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/karellen/karellen-testing',
        scripts = [],
        packages = ['karellen.testing.mock'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Testing'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
