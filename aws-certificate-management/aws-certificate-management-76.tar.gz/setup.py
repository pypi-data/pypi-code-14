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
        name = 'aws-certificate-management',
        version = '76',
        description = '''''',
        long_description = '''Tool to automate certificate creation in AWS''',
        author = "",
        author_email = "",
        license = '',
        url = 'https://github.com/ImmobilienScout24/aws-certificate-management',
        scripts = ['scripts/aws-certificate-management'],
        packages = ['aws_certificate_management'],
        py_modules = [],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'awscli',
            'boto3',
            'cfn-sphere'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
