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
        name = 'netkraken-minion',
        version = '0.2',
        description = '''records network connections: source host, protocol, target host''',
        long_description = '''records network connections: source host, protocol, target host''',
        author = "Arne Hilmann",
        author_email = "arne.hilmann@gmail.com",
        license = '',
        url = 'https://github.com/netkraken/minion',
        scripts = [
            'scripts/collect-netconns',
            'scripts/netconns'
        ],
        packages = ['netkraken'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [
            ('/etc/init.d/', ['docroot/etc/init.d/netconns'])
        ],
        package_data = {},
        install_requires = [
            'countdb',
            'psutil>=2.1.0'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
