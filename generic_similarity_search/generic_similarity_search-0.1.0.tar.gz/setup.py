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
        name = 'generic_similarity_search',
        version = '0.1.0',
        description = '''''',
        long_description = '''''',
        author = "",
        author_email = "",
        license = '',
        url = '',
        scripts = [],
        packages = [
            'generic_similarity_search',
            'generic_similarity_search.api',
            'generic_similarity_search.index',
            'generic_similarity_search.parser',
            'generic_similarity_search.parser.provider',
            'generic_similarity_search.parser.provider.implementations'
        ],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'boto3',
            'checksumdir',
            'dyject',
            'numpy',
            'pyflann3',
            'pyproj',
            'tornado'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
