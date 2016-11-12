# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup_requires = (
    'pytest-runner',
    )
install_requires = (
    'cnxml',
    'lxml',
    'pathlib;python_version<="2.7"',
    )
tests_require = [
    'pytest',
    ]
extras_require = {
    'test': tests_require,
    }
description = "Connexions LiteZip Library"
with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='cnx-litezip',
    version='1.1.0',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/cnx-litezip",
    license='LGPL, See also LICENSE.txt',
    description=description,
    long_description=long_description,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    test_suite='litezip.tests',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'litezip.tests': ['data/**/*.*'],
        },
    entry_points="""\
    [console_scripts]
    completezip2litezip = litezip.cli.completezip2litezip:main
    validate-litezip = litezip.cli.validate:main
    """,
    )
